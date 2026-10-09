"""Optimise Roof Centre's original project photos for the static site.

Reads originals from the WordPress backup (read-only) and writes resized,
metadata-free WebP files to website/assets/img/. Re-run after adding photos:

    python tools/images.py
"""
from pathlib import Path
import json
from PIL import Image, ImageOps, ImageStat

ROOT = Path(__file__).resolve().parent.parent
_BACKUPS = sorted((ROOT / "reference" / "extracted").glob("backup-*"))
if not _BACKUPS:
    raise SystemExit("Original photos not found: reference/extracted/backup-*/ is not in Git.\n"
                     "The optimised images in website/assets/img/ are committed, so build.py works without this step.\n"
                     "To reprocess photos, extract the cPanel backup into reference/extracted/ first.")
UPLOADS = _BACKUPS[-1] / "homedir/public_html/wp-content/uploads"
OUT = ROOT / "website" / "assets" / "img"
MANIFEST = ROOT / "tools" / "image-manifest.json"

WIDTHS = [480, 800, 1200]
HERO_WIDTHS = [800, 1200, 1800, 2400]

# key: (source path, alt text, category, hero?)
# Categories drive the project gallery filter.
PHOTOS = {
    # Hero / feature images
    "colorbond-reroof-progress": ("2024/03/IMG_7771.jpg", "New white Colorbond roof sheets being installed over fresh battens", "replacement", True),
    "colorbond-ridge-solar": ("2024/02/IMG_7746.jpg", "Finished Colorbond roof with ridge capping and solar panels", "colorbond", True),
    "metal-roof-escarpment": ("2021/05/26.png", "Completed metal roof with the escarpment in the background", "colorbond", False),
    "chimney-tile-roof": ("2021/05/roof-2.jpg", "Terracotta tile roof and chimney flashing after repairs", "repair", True),
    "tarp-make-safe": ("2021/05/roof.jpg", "Temporary protection installed inside a roof cavity", "emergency", True),
    "cottage-reroof-complete": ("2024/03/IMG_7902.jpg", "Weatherboard cottage with its new white metal roof", "replacement", True),
    "cottage-reroof-gutter": ("2024/03/IMG_7901.jpg", "Roofer fitting guttering on a weatherboard cottage re-roof", "replacement", True),
    "cottage-battens": ("2024/03/IMG_7704.jpg", "Metal roof sheet laid over new battens on a cottage re-roof", "replacement", True),
    "cottage-valley": ("2024/03/IMG_7709.jpg", "New metal roof valley being formed on a cottage re-roof", "replacement", True),
    "cottage-strip": ("2024/03/IMG_7769.jpg", "Old tiles stripped back to the timber frame before re-roofing", "replacement", True),
    "cottage-before": ("2024/03/IMG_7675.jpg", "Weatherboard cottage before the old roof was replaced", "replacement", True),
    "cottage-sheets": ("2024/03/IMG_7768.jpg", "New roof sheets going on beside the old tiled section", "replacement", True),
    "cottage-tarp": ("2024/03/IMG_7750.jpg", "Partly re-roofed house with tarps protecting the open section", "replacement", True),
    "cottage-rear": ("2024/03/IMG_7780.jpg", "Rear of a weatherboard cottage with its new metal roof", "replacement", True),
    "cottage-valley-2": ("2024/03/IMG_7770.jpg", "Roof frame opened up while new metal sheets are installed", "replacement", True),
    "cottage-ridge": ("2024/03/IMG_7778.jpg", "Ridge and hip capping on a new white metal roof", "replacement", False),
    "cottage-sheet-edge": ("2024/03/IMG_7692.jpg", "Edge of a new corrugated roof sheet over the old frame", "replacement", False),
    # Chipping Norton roof replacement (as captioned on the original site)
    "cn-1": ("2024/02/IMG_7739.jpg", "Chipping Norton roof replacement: new ridge capping", "replacement", False),
    "cn-2": ("2024/02/IMG_7740.jpg", "Chipping Norton roof replacement: finished Colorbond roof", "replacement", False),
    "cn-3": ("2024/02/IMG_7741.jpg", "Chipping Norton roof replacement: roof valley detail", "replacement", False),
    "cn-4": ("2024/02/IMG_7742.jpg", "Chipping Norton roof replacement: ridge line and vent", "replacement", False),
    "cn-5": ("2024/02/IMG_7743.jpg", "Chipping Norton roof replacement: hip and valley", "replacement", False),
    "cn-6": ("2024/02/IMG_7744.jpg", "Ridge capping on a newly re-roofed home", "replacement", False),
    "cn-7": ("2024/02/IMG_7745.jpg", "Corrugated metal roof with new ridge vent", "replacement", False),
    # Botany roof repair (as captioned on the original site)
    "botany-1": ("2024/02/IMG_7761.jpg", "Botany roof repair: red metal roof under scaffolding", "repair", False),
    "botany-2": ("2024/02/IMG_7762.jpg", "Botany roof repair: new red metal roof sheets", "repair", False),
    "botany-3": ("2024/02/IMG_7763.jpg", "Botany roof repair: valley and flashing detail", "repair", False),
    "botany-4": ("2024/02/IMG_7764.jpg", "Botany roof repair: completed roof section", "repair", False),
    "botany-5": ("2024/02/IMG_7765.jpg", "Botany roof repair: old roof stripped to the battens", "repair", False),
    "botany-6": ("2024/02/IMG_7766.jpg", "Botany roof repair: weathered tiles before work", "repair", False),
    "botany-7": ("2024/02/IMG_7767.jpg", "Botany roof repair: roof frame exposed during works", "repair", False),
    # Repairs and restoration
    "tile-patch": ("2021/05/3.png", "Cracked roof tile with a temporary patch", "repair", False),
    "broken-valley": ("2021/05/35.png", "Broken tiles and a deteriorated valley before repair", "repair", False),
    "repair-red-tile": ("2021/05/41.png", "Roofer working on a red tile roof", "repair", False),
    "repair-tile-crew": ("2021/05/58.png", "Roofer working on a two-storey tile roof", "repair", False),
    "repair-tile-street": ("2021/05/47.png", "Roofer on a terracotta tile roof", "repair", False),
    "tile-valley-repair": ("2021/06/p4.png", "Tile roof valley opened up for repair", "repair", False),
    "tile-roof-valley": ("2021/06/p3.png", "Concrete tile roof valley after repair", "repair", False),
    "skylight-flashing": ("2021/06/p5.png", "Skylight shaft and flashing in a tile roof", "flashing", False),
    "restored-terracotta": ("2021/06/roofing.png", "Restored terracotta tile roof", "restoration", False),
    "restored-dark-tile": ("2021/06/roofing1.png", "Home with a restored dark tile roof", "restoration", False),
    "tile-to-metal": ("2021/05/49.png", "Tile roof being converted to metal roofing", "replacement", False),
    "tile-to-metal-2": ("2021/05/51.png", "New metal roof sheets beside old roof tiles", "replacement", False),
    "tile-to-metal-3": ("2021/05/55.png", "Metal sheeting going on alongside a tile roof", "replacement", False),
    "tile-to-metal-4": ("2021/05/56.png", "Join between new metal roofing and old tiles", "replacement", False),
    "tile-strip": ("2021/05/50.png", "Roofer stripping old tiles from a roof", "replacement", False),
    "frame-exposed": ("2021/06/RR5-min.png", "Roof frame exposed after the old roof was removed", "replacement", False),
    "frame-exposed-2": ("2021/05/c6c1cacb-0398-4ff8-bb88-0d02fbe2ab32.jpg", "Roof stripped back to the rafters", "replacement", False),
    "frame-blue": ("2021/06/RR3-min.png", "Roof frame with new sarking ready for sheeting", "replacement", False),
    "storm-damage": ("2021/06/RR-min.png", "Storm-damaged corrugated roof before replacement", "replacement", False),
    "old-tile-damage": ("2021/06/RR2-min.png", "Damaged tile roof before replacement", "replacement", False),
    "crew-commercial": ("2021/06/RR7.png", "Roofing crew working on a commercial roof", "replacement", False),
    "metal-roof-white": ("2021/06/RR6.png", "New metal roof over a rear extension", "colorbond", False),
    "polycarbonate": ("2021/05/46.png", "Clear roof sheeting beside a tile roof", "repair", False),
    # Colorbond
    "cb-1": ("2021/06/cr.png", "Colorbond roof sheets on a residential re-roof", "colorbond", False),
    "cb-2": ("2021/06/cr1.png", "Colorbond roof sheets ready for fixing", "colorbond", False),
    "cb-3": ("2021/06/cr2.png", "New home with a dark Colorbond roof", "colorbond", False),
    "cb-4": ("2021/06/cr3.png", "Long run of new Colorbond roofing", "colorbond", False),
    "cb-5": ("2021/06/cr4.png", "Colorbond roofing on a new build", "colorbond", False),
    "cb-6": ("2021/06/cr5.png", "Chimney flashing on a Colorbond roof", "colorbond", False),
    "cb-7": ("2021/06/cr6-min.png", "Colorbond sheet being fixed into place", "colorbond", False),
    "cb-8": ("2021/06/cr7.png", "Colorbond roof edge and gutter", "colorbond", False),
    "cb-9": ("2021/06/cr9-min.png", "Colorbond roof overlooking a pool", "colorbond", False),
    "cb-10": ("2021/05/17.png", "Brick home with a new dark Colorbond roof", "colorbond", False),
    "cb-11": ("2021/05/23.png", "Finished Colorbond roof on a brick home", "colorbond", False),
    "cb-12": ("2021/05/21.png", "Corrugated Colorbond roof sheets", "colorbond", False),
    "cb-13": ("2021/05/25.png", "Colorbond roof surface", "colorbond", False),
    "cb-14": ("2021/05/27.png", "Colorbond roof on a modern home", "colorbond", False),
    "cb-15": ("2021/05/31.png", "Street view of a home with a Colorbond roof", "colorbond", False),
    "cb-16": ("2021/05/19.png", "Row of homes with new metal roofs", "colorbond", False),
    "cb-interior-red": ("2021/05/18.png", "Red Colorbond hip roof inside a commercial building", "colorbond", False),
    "cb-interior-green": ("2021/05/28.png", "Colorbond hip roof inside a commercial building", "colorbond", False),
    "cb-interior-dark": ("2021/05/29.png", "Dark Colorbond hip roof inside a commercial building", "colorbond", False),
    # Gutters
    "gutter-1": ("2021/06/gdr.png", "Tradesman installing new guttering", "gutters", False),
    "gutter-2": ("2021/06/gdr2.png", "New gutter and fascia on a home", "gutters", False),
    "gutter-3": ("2021/06/gdr3-min.png", "Replaced gutters and downpipe", "gutters", False),
    "gutter-4": ("2021/06/gdr4.png", "Home with new gutters and downpipes", "gutters", False),
    "gutter-5": ("2021/06/gdr5.png", "New downpipe and gutter on a brick home", "gutters", False),
    "gutter-ladder": ("2021/05/40.png", "Roofer on a ladder working on a gutter", "gutters", False),
    "downpipe": ("2021/05/44.png", "Old gutter and downpipe before replacement", "gutters", False),
    # Emergency make safe
    "make-safe-1": ("2021/05/6.png", "Tarp secured over a damaged tile roof", "emergency", False),
    "make-safe-2": ("2021/05/11.png", "Tarp weighed down with sandbags on a roof", "emergency", False),
    "make-safe-3": ("2021/05/4.png", "Plastic sheeting protecting a damaged roof section", "emergency", False),
    "make-safe-4": ("2021/05/2.png", "Protective sheeting secured over a tiled roof", "emergency", False),
    "make-safe-5": ("2021/05/9.png", "Tarp over a roof secured with sandbags", "emergency", False),
    "make-safe-6": ("2021/05/0b9b6efc-a915-4e79-97e7-72df0c9f1cc8.jpg", "Temporary roof cover held down with weights", "emergency", False),
    # Flashings
    "flashing-1": ("2021/06/cvf.png", "New valley flashing between two roof sections", "flashing", False),
    "flashing-2": ("2021/06/cvf1-min.png", "Custom valley flashing in a tile roof", "flashing", False),
    "flashing-3": ("2021/06/cvf2-min.png", "Chimney flashing on a terracotta tile roof", "flashing", False),
    "flashing-4": ("2021/05/38.png", "Custom folded metal flashing", "flashing", False),
    "flashing-5": ("2021/05/59.png", "Roofer installing flashing against a brick wall", "flashing", False),
    "flashing-6": ("2021/05/60.png", "Roofer sealing flashing at a chimney", "flashing", False),
    "flashing-7": ("2021/05/62.png", "New valley iron being installed in a tile roof", "flashing", False),
    "flashing-8": ("2021/05/39.png", "Chimney and tile roof with new flashing", "flashing", False),
}


def trim_bars(im):
    """Crop the dark letterbox bars from phone screenshots."""
    g = im.convert("L")
    w, h = g.size

    def dark(y):
        s = ImageStat.Stat(g.crop((0, y, w, y + 1)))
        return s.mean[0] < 48 and s.stddev[0] < 6

    top = 0
    while top < h // 3 and dark(top):
        top += 1
    bottom = h
    while bottom > h * 2 // 3 and dark(bottom - 1):
        bottom -= 1
    if top > 4 or h - bottom > 4:
        return im.crop((0, top + 2 if top else 0, w, bottom - 2 if bottom < h else h))
    return im


def flatten(im):
    im = ImageOps.exif_transpose(im)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert("RGB")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for key, (src, alt, cat, hero) in PHOTOS.items():
        im = trim_bars(flatten(Image.open(UPLOADS / src)))
        widths = [w for w in (HERO_WIDTHS if hero else WIDTHS) if w <= im.width] or [im.width]
        if im.width not in widths and im.width < max(HERO_WIDTHS if hero else WIDTHS):
            widths.append(im.width)
        files = []
        for w in sorted(set(widths)):
            h = round(im.height * w / im.width)
            name = f"{key}-{w}.webp"
            dest = OUT / name
            if not dest.exists():
                im.resize((w, h), Image.LANCZOS).save(dest, "WEBP", quality=74 if w > 1200 else 78, method=6)
            files.append({"w": w, "h": h, "file": name})
        manifest[key] = {"alt": alt, "category": cat, "ratio": im.height / im.width, "files": files, "source": src}
        print(f"{key:28} {im.width}x{im.height} -> {[f['w'] for f in files]}")

    # Social sharing image (JPEG for widest compatibility)
    og = trim_bars(flatten(Image.open(UPLOADS / PHOTOS["colorbond-reroof-progress"][0])))
    og = ImageOps.fit(og, (1200, 630), Image.LANCZOS)
    og.save(OUT / "og-roof-centre.jpg", "JPEG", quality=80, optimize=True, progressive=True)

    # Logos: trim transparent padding, keep transparency
    for name, src in (("logo", "2021/05/logo.png"), ("logo-white", "2021/05/logo_white_2.png")):
        lg = Image.open(UPLOADS / src).convert("RGBA")
        lg = lg.crop(lg.getbbox())
        lg.thumbnail((720, 400), Image.LANCZOS)
        lg.save(OUT / f"{name}.png", optimize=True)
        lg.save(OUT / f"{name}.webp", "WEBP", quality=90, method=6)
        manifest[f"_{name}"] = {"w": lg.width, "h": lg.height}

    # Favicons from the original site icon
    icon = Image.open(UPLOADS / "2021/05/favicon.png").convert("RGBA")
    icon = icon.crop(icon.getbbox())
    side = max(icon.size)
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.paste(icon, ((side - icon.width) // 2, (side - icon.height) // 2))
    sq.resize((32, 32), Image.LANCZOS).save(ROOT / "website" / "favicon-32.png", optimize=True)
    sq.save(ROOT / "website" / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    apple = Image.new("RGB", (180, 180), (255, 255, 255))
    a = sq.resize((140, 140), Image.LANCZOS)
    apple.paste(a, (20, 20), a)
    apple.save(ROOT / "website" / "apple-touch-icon.png", optimize=True)
    for s in (192, 512):
        p = Image.new("RGB", (s, s), (255, 255, 255))
        a = sq.resize((int(s * 0.78), int(s * 0.78)), Image.LANCZOS)
        p.paste(a, ((s - a.width) // 2, (s - a.height) // 2), a)
        p.save(OUT / f"icon-{s}.png", optimize=True)

    MANIFEST.write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    print("images:", len(PHOTOS))


if __name__ == "__main__":
    main()

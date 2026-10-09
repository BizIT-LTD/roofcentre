"""Site content for roofcentre.com.au (Australian English).

Business facts come from the original WordPress site (database roofcent_wp1).
Anything not stated there has been kept general on purpose: no reviews,
licence numbers, warranties or project claims have been added.
"""

SITE = {
    "name": "Roof Centre",
    "url": "https://www.roofcentre.com.au",
    "phone": "0431 848 619",
    "phone_href": "tel:+61431848619",
    "email": "info@roofcentre.com.au",
    "hours": "Monday to Friday, 9 am – 5 pm",
    "hours_short": "Mon–Fri 9 am – 5 pm",
    "area": "Sydney",
    "facebook": "https://www.facebook.com/amir.mehdi.712",
    "pergola": "https://pergolabuildingcentre.com.au/",
}

# Service areas named on the original site. Each keeps its original URL.
SERVICES = [
    {
        "slug": "roof-repair",
        "name": "Roof Repair",
        "hero": "chimney-tile-roof",
        "card": "repair-tile-crew",
        "summary": "Leaks, broken tiles, rusted sheets and storm damage found and fixed properly.",
        "seo_title": "Roof Repairs in Sydney | Tile & Metal Roofs | Roof Centre",
        "description": "Roof Centre repairs tile and metal roofs across Sydney: leaks, cracked tiles, rusted sheets, flashings and storm damage. Call 0431 848 619 for a free quote.",
        "lead": "Professional repairs for all types of roofs, from broken tiles to rusted sheets. Whether your leak was caused by weather, rust, debris or overflowing water, our roofers will find the source and fix it.",
        "sections": [
            ("Finding the real cause of a leak", [
                "Water rarely comes through the ceiling directly below the damage. It can travel along battens, sarking or rafters before it drips, so a good repair starts with tracing the leak back to where it enters the roof.",
                "We inspect the roof surface, flashings, valleys, penetrations and gutters, then explain what we found and what needs fixing before any work starts.",
            ]),
            ("What we repair", [
                ["Cracked, slipped or broken roof tiles", "Rusted, loose or lifted metal roof sheets and screws", "Worn ridge and hip capping, bedding and pointing", "Failed valley irons and leaking flashings", "Leaks around skylights, vents, chimneys and solar mounts", "Storm and debris damage", "Overflowing or damaged gutters that push water back into the roof"],
            ]),
            ("Repair or replace?", [
                "Most roofs can be repaired when the damage is limited to one area. If tiles are breaking all over the roof, or metal sheets are rusting through in several places, ongoing repairs can cost more than a new roof. We will tell you honestly which option makes sense for your roof.",
            ]),
        ],
        "signs": ["Water stains or bubbling paint on ceilings", "Damp or musty smells in upper rooms", "Cracked, slipped or missing tiles", "Rust spots or holes in metal sheets", "Daylight visible in the roof space", "Gutters overflowing in heavy rain"],
        "gallery": ["botany-2", "botany-3", "broken-valley", "tile-patch", "tile-valley-repair", "repair-red-tile", "repair-tile-street", "tile-roof-valley"],
        "faqs": [
            ("Can you repair just part of my roof?", "Yes. Most leaks are caused by a specific problem such as a cracked tile, a failed flashing or a rusted sheet, and can be repaired without replacing the whole roof."),
            ("Can you match my existing tiles?", "We try to match the profile and colour of your existing tiles. Older tiles are sometimes no longer made, so the closest available match may differ slightly. We will discuss the options with you before replacing any."),
        ],
    },
    {
        "slug": "roof-restoration",
        "name": "Roof Restoration",
        "hero": "restored-terracotta",
        "card": "restored-dark-tile",
        "summary": "Bring a tired but sound roof back to good condition and extend its life.",
        "seo_title": "Roof Restoration in Sydney | Tile Roof Restoration | Roof Centre",
        "description": "Roof restoration for tired or weather-damaged roofs across Sydney. Repairs, re-bedding, re-pointing and resealing to extend your roof's life. Free quotes.",
        "lead": "Whether your roof has been damaged or is simply showing its age, a restoration can return it to good, weathertight condition without the cost of a full replacement.",
        "sections": [
            ("What a restoration involves", [
                "A restoration fixes the wear that builds up on a roof over the years. The exact scope depends on the roof's material and condition, and is agreed with you before work begins. It typically includes:",
                ["A full inspection of the roof surface, flashings and gutters", "Cleaning to remove dirt, moss and lichen", "Replacing cracked or broken tiles", "Re-bedding and re-pointing ridge and hip capping on tile roofs", "Replacing loose or rusted fixings on metal roofs", "Repairing or replacing worn valleys and flashings", "Applying a roof coating where it suits the roof"],
            ]),
            ("Is restoration right for my roof?", [
                "Restoration works best when the roof structure and most of the roofing material are still sound. If tiles are failing across the whole roof, or metal sheets are rusted through, a replacement is usually the better long-term option. We will inspect your roof and recommend the approach that suits it.",
            ]),
        ],
        "signs": ["Faded or patchy roof colour", "Moss or lichen growth", "Cracked or crumbling ridge pointing", "A few broken or slipped tiles", "Surface rust on metal sheets", "Minor leaks in heavy rain"],
        "gallery": ["restored-terracotta", "restored-dark-tile", "repair-red-tile", "repair-tile-crew", "repair-tile-street", "chimney-tile-roof"],
        "faqs": [
            ("How is restoration different from a repair?", "A repair fixes a specific problem, such as one leak. A restoration addresses the general wear across the whole roof so it stays weathertight for longer."),
        ],
    },
    {
        "slug": "roof-replacment",
        "name": "Roof Replacement",
        "hero": "colorbond-reroof-progress",
        "card": "cottage-reroof-complete",
        "summary": "Tile to tile or tile to metal. Domestic roof replacement is what we do best.",
        "seo_title": "Roof Replacement Sydney | Tile to Metal Re-roofing | Roof Centre",
        "description": "Complete roof replacement across Sydney, from tile to tile or tile to Colorbond and Zincalume metal roofing. Residential, commercial and industrial. Free quotes.",
        "lead": "Need a new roof? Whether you are replacing tile with tile or tile with metal, Roof Centre provides a quality service at a competitive price. Changing existing homes of any roof type to new Colorbond or Zincalume roofing is our speciality.",
        "sections": [
            ("When to replace rather than repair", [
                "A roof usually needs replacing when the material itself is failing: tiles that are porous and cracking across the whole roof, metal sheets rusting through in many places, or leaks that keep coming back after repairs. Replacement also makes sense when you are renovating and want a lighter, lower-maintenance roof.",
            ]),
            ("How a roof replacement works", [
                ["Inspection and measure: we look at the roof, the frame and access, and confirm what you want.", "Written quote: you get a clear scope of work before anything is booked.", "Strip the old roof: tiles or sheets are removed and the frame is checked.", "Prepare the frame: battens are replaced or added as needed, and sarking or insulation blanket is fitted where specified.", "Install the new roof: new sheets or tiles, ridges, flashings and valleys.", "Gutters and downpipes: replaced at the same time if they are included in the quote.", "Clean-up and final check: the site is cleaned up and the finished roof is checked with you."],
            ]),
            ("Tile to metal", [
                "Replacing tiles with Colorbond or Zincalume steel makes the roof much lighter and removes the ongoing maintenance of ridge pointing and broken tiles. Metal roofing also suits low pitches that tiles cannot be used on. See our <a href=\"/colorbond-roofing/\">Colorbond roofing</a> page for more on colours and options.",
            ]),
            ("Older roofs and asbestos", [
                "Some older homes have roofing, flashings or eaves that contain asbestos. If we suspect asbestos is present, it must be assessed and removed by a licensed asbestos removalist before roofing work can go ahead. We will let you know if this applies to your job.",
            ]),
        ],
        "signs": ["Tiles cracking across many areas of the roof", "Metal sheets rusted through in several places", "Leaks that return after repairs", "Sagging roof lines", "Storm damage across a large area", "Planning a renovation or extension"],
        "gallery": ["cottage-before", "cottage-strip", "cottage-battens", "cottage-valley", "cottage-reroof-gutter", "cottage-reroof-complete", "cn-2", "cn-3", "storm-damage", "frame-exposed", "tile-to-metal", "crew-commercial"],
        "faqs": [
            ("Can you replace a tile roof with Colorbond?", "Yes. Converting tile roofs to Colorbond or Zincalume steel is our speciality. We also replace tile roofs with new tiles."),
            ("Do you work on commercial and industrial roofs?", "Yes. Domestic roof replacement is our main work, but we also repair, restore and replace commercial and industrial roofs."),
            ("Can you replace my gutters at the same time?", "Yes. Replacing gutters and downpipes along with the roof is often efficient because access is already set up. We can include them in your quote."),
        ],
    },
    {
        "slug": "colorbond-roofing",
        "name": "Colorbond Roofing",
        "hero": "colorbond-ridge-solar",
        "card": "cb-3",
        "summary": "New Colorbond and Zincalume steel roofs for homes, extensions and commercial buildings.",
        "seo_title": "Colorbond Roofing in Sydney | New Metal Roofs | Roof Centre",
        "description": "Colorbond and Zincalume steel roofing for new homes, re-roofs and extensions across Sydney. Licensed and insured roofers. Call 0431 848 619 for a free quote.",
        "lead": "Roof Centre is a leading choice for Colorbond roofing. We are fully licensed and insured, and we bring several years of hands-on experience to every Colorbond job.",
        "sections": [
            ("Why choose Colorbond steel?", [
                "COLORBOND® steel is pre-painted steel roofing made in Australia by BlueScope and designed for Australian conditions. It is popular for re-roofs and new homes because it is:",
                ["Lightweight, putting much less load on the roof frame than tiles", "Low maintenance, with no ridge pointing or broken tiles to repair", "Available in a wide range of colours to suit your home", "Suitable for low-pitch roofs where tiles cannot be used", "Easy to pair with matching gutters, fascia and flashings"],
            ]),
            ("Choosing a colour", [
                "Colour affects both how your home looks and how much heat the roof absorbs. Lighter colours reflect more of the sun's heat, while darker colours absorb more. It's worth checking with your council or estate rules too, as some areas have guidelines on roof colours.",
            ]),
            ("Coastal homes", [
                "Salt air speeds up corrosion on metal roofs. For homes close to the ocean or bays, there are steel grades and fasteners made for coastal exposure. Tell us where your property is and we will include suitable materials in your quote.",
            ]),
            ("Zincalume", [
                "ZINCALUME® steel is the unpainted, metallic-finish alternative. It suits sheds, commercial buildings and homes where a classic silver roof is wanted.",
            ]),
        ],
        "signs": ["Re-roofing from tiles to metal", "New homes and extensions", "Patios and carports joining the main roof", "Replacing old, rusted metal roofs", "Commercial and industrial buildings"],
        "gallery": ["cb-3", "cb-10", "cb-11", "cb-9", "cb-1", "cb-5", "cb-6", "cb-8", "colorbond-ridge-solar", "metal-roof-escarpment", "cb-interior-red", "cb-interior-dark"],
        "faqs": [
            ("Do you install Zincalume as well as Colorbond?", "Yes. We install both pre-painted Colorbond steel and unpainted Zincalume steel roofing."),
            ("Can you fit Colorbond to an existing tile roof frame?", "Usually, yes. The frame is checked once the tiles are removed, and battens are adjusted or replaced to suit metal roofing."),
        ],
    },
    {
        "slug": "gutter-8-downpipe-replacement",
        "name": "Gutter & Downpipe Replacement",
        "short": "Gutters & Downpipes",
        "hero": "cottage-reroof-gutter",
        "card": "gutter-1",
        "summary": "New gutters, downpipes and fascia, plus gutter cleaning to keep water flowing.",
        "seo_title": "Gutter & Downpipe Replacement in Sydney | Roof Centre",
        "description": "Gutter and downpipe replacement and gutter cleaning across Sydney. Licensed and insured roofers with several years' experience. Free quotes on 0431 848 619.",
        "lead": "Need your gutters cleaned, or new ones installed? Roof Centre does it all, backed by several years of experience, a builder's licence and full insurance.",
        "sections": [
            ("Why gutters matter", [
                "Gutters and downpipes carry rainwater away from your roof, walls and foundations. When they are blocked, rusted or undersized, water can overflow into the eaves and roof space, stain walls, and pool around the house.",
            ]),
            ("What we do", [
                ["Gutter cleaning to remove leaves and debris", "Replacing rusted, leaking or sagging gutters", "New downpipes and downpipe repairs", "Fascia replacement where the timber or metal has deteriorated", "Gutters and downpipes in a range of profiles and Colorbond colours", "Gutter replacement as part of a full roof replacement"],
            ]),
            ("Sizing and falls", [
                "New gutters need to be the right size for the roof area, with enough downpipes and the correct fall so water drains instead of sitting. We check these details when we quote, especially on older homes where the original gutters may have been undersized.",
            ]),
        ],
        "signs": ["Water spilling over the gutter edge in rain", "Rust holes or leaking joints", "Gutters sagging or pulling away from the fascia", "Water stains on walls or eaves", "Plants growing in the gutters", "Pooling water around the house"],
        "gallery": ["gutter-1", "gutter-2", "gutter-3", "gutter-4", "gutter-5", "gutter-ladder", "downpipe", "cottage-reroof-gutter"],
        "faqs": [
            ("How often should gutters be cleaned?", "It depends on how many trees are near your home. Homes surrounded by trees may need cleaning several times a year, while others need it less often. Checking before storm season is a good habit."),
        ],
    },
    {
        "slug": "gutter-protection",
        "name": "Gutter Protection",
        "hero": "gutter-ladder",
        "card": "gutter-ladder",
        "summary": "Gutter guard to keep leaves and debris out and reduce blockages.",
        "seo_title": "Gutter Protection & Gutter Guard in Sydney | Roof Centre",
        "description": "Gutter protection for Sydney homes. Gutter guard helps keep leaves and debris out of your gutters and reduces blockages. Call Roof Centre for a free quote.",
        "lead": "Gutter protection, often called gutter guard, is a mesh cover fitted over your gutters. It helps keep leaves and debris out while still letting rainwater through.",
        "sections": [
            ("Benefits of gutter protection", [
                ["Fewer blocked gutters and downpipes", "Less overflow into eaves and roof spaces during heavy rain", "Less frequent gutter cleaning", "Helps keep birds and pests from nesting in gutters", "Reduces the build-up of dry leaves in gutters"],
            ]),
            ("How it's installed", [
                "The gutters are cleaned and checked first, because guard should not be fitted over rusted or leaking gutters. Mesh is then fixed along the roof edge and over the gutter. The fixing method depends on whether the roof is tile or metal, so it can shed debris without trapping water.",
            ]),
            ("Is it maintenance-free?", [
                "No product makes gutters completely maintenance-free. Fine debris can still settle on top of the mesh, so an occasional check and clean is still worthwhile. Gutter protection reduces how often this needs doing.",
            ]),
        ],
        "signs": ["Trees close to or overhanging the roof", "Gutters that block every season", "Birds or pests nesting in gutters", "Hard-to-reach two-storey gutters"],
        "gallery": ["gutter-ladder", "gutter-2", "gutter-4", "gutter-5", "gutter-3", "gutter-1"],
        "faqs": [
            ("Can gutter guard go on any roof?", "Gutter guard can be fitted to most tile and metal roofs. We will check your gutters' condition first and recommend replacing them if they are rusted or leaking."),
        ],
    },
    {
        "slug": "emergency-roof-make-safe",
        "name": "Emergency Roof Make Safe",
        "short": "Emergency Make Safe",
        "hero": "cottage-tarp",
        "card": "make-safe-2",
        "summary": "Urgent temporary protection after storms, fallen branches or sudden leaks.",
        "seo_title": "Emergency Roof Make Safe in Sydney | Storm Damage | Roof Centre",
        "description": "Emergency roof make-safe after storms, fallen trees or sudden leaks in Sydney. Temporary protection to stop further damage, then lasting repairs. Call 0431 848 619.",
        "lead": "When a storm, fallen branch or sudden failure leaves your roof open to the weather, a make-safe stops further damage until permanent repairs can be done.",
        "sections": [
            ("What a make-safe involves", [
                "A make-safe is temporary work to protect your home. Depending on the damage, it can include:",
                ["Tarping damaged sections of the roof and securing the tarp", "Temporarily replacing or refixing displaced tiles and sheets", "Securing loose sheets, flashings or capping that could blow off", "Clearing debris that is blocking water from draining"],
                "Once the roof is secure, we can inspect the damage properly and quote for permanent repairs or replacement.",
            ]),
            ("What to do while you wait", [
                ["Stay off the roof, especially in wet or windy weather", "Keep clear of fallen power lines and call your electricity network if lines are down", "Move furniture and valuables away from leaks and put out buckets", "If a ceiling is sagging with water, keep everyone out of that room", "Take photos of the damage for your insurer"],
                "For storm or flood emergencies where life or property is at immediate risk, contact the NSW SES on <a href=\"tel:132500\">132 500</a>, or call 000 in a life-threatening emergency.",
            ]),
            ("Insurance", [
                "If you plan to make an insurance claim, contact your insurer as early as possible. Photos taken before and after the make-safe will help with your claim.",
            ]),
        ],
        "signs": ["Storm or hail damage", "Fallen trees or branches", "Lifted or missing roof sheets", "Water coming through the ceiling", "Tiles blown off or displaced"],
        "gallery": ["make-safe-1", "make-safe-2", "make-safe-3", "make-safe-4", "make-safe-5", "make-safe-6", "cottage-tarp", "tarp-make-safe"],
        "faqs": [
            ("Is a make-safe a permanent repair?", "No. A make-safe is temporary protection to stop further damage. Permanent repairs are quoted and carried out once the roof is secure and conditions are safe."),
        ],
    },
    {
        "slug": "custom-valley-flashings",
        "name": "Custom Valley Flashings",
        "short": "Valley Flashings",
        "hero": "cottage-valley",
        "card": "flashing-2",
        "summary": "Valley irons and flashings made to fit, replacing rusted or leaking ones.",
        "seo_title": "Custom Valley Flashings in Sydney | Roof Centre",
        "description": "Custom valley irons and roof flashings for tile and metal roofs in Sydney. Fix leaks at valleys, chimneys, walls and skylights. Call Roof Centre for a free quote.",
        "lead": "Need custom valley flashings? Roof Centre is fully licensed and insured, with several years of experience making and fitting flashings for tile and metal roofs.",
        "sections": [
            ("What valleys and flashings do", [
                "A roof valley is the channel where two roof slopes meet. The valley iron underneath carries a large share of the roof's rainwater, so when it rusts or the tiles beside it shift, leaks follow.",
                "Flashings seal the joins where the roof meets walls, chimneys, skylights, vents and other penetrations. They are one of the most common sources of roof leaks.",
            ]),
            ("Made to suit your roof", [
                "Older homes often have valleys and junctions that standard off-the-shelf flashings don't fit well. Custom-folded flashings are made to the right size and shape for each junction, which gives a neater, more reliable seal.",
            ]),
            ("Common flashing work", [
                ["Replacing rusted or holed valley irons", "Re-flashing chimneys and brick walls", "Flashings around skylights, vents and exhaust flues", "Apron and barge flashings on metal roofs", "Flashings where extensions join the existing roof"],
            ]),
        ],
        "signs": ["Leaks near a valley or chimney", "Rust visible along the valley", "Cracked mortar or sealant at flashings", "Water stains near skylights or vents"],
        "gallery": ["flashing-1", "flashing-2", "flashing-3", "flashing-5", "flashing-6", "flashing-7", "flashing-8", "flashing-4", "skylight-flashing", "cb-6"],
        "faqs": [
            ("Do valley irons need replacing when the roof is restored?", "Not always. We check them during an inspection. Rusted or holed valleys should be replaced, as they are a common cause of leaks."),
        ],
    },
]

AREAS = [
    {
        "slug": "roof-repair-botany",
        "suburb": "Botany",
        "name": "Roof Repair Botany",
        "hero": "botany-2",
        "seo_title": "Roof Repair Botany NSW | Local Roof Repairs | Roof Centre",
        "description": "Roof repairs in Botany NSW for tile and metal roofs: leaks, broken tiles, rusted sheets, flashings and gutters. Call Roof Centre on 0431 848 619 for a free quote.",
        "lead": "Roof repairs, replacements and gutter work for homes and businesses in Botany and the surrounding suburbs.",
        "about": "Botany sits on the northern shore of Botany Bay, about 11 kilometres south of the Sydney CBD, in the Bayside Council area. Its neighbours include Mascot, Banksmeadow, Pagewood and Port Botany.",
        "local": [
            ("Roofs near the bay", "Homes close to the water are exposed to salt air, which speeds up rust on metal roof sheets, fixings, gutters and flashings. Regular checks help catch corrosion before it turns into a leak, and coastal-grade materials are worth considering for new metal roofing."),
            ("Wind and storms", "Strong winds off the bay can lift loose tiles, capping and sheets. Ridge capping with cracked pointing and loosely fixed sheets are common weak points after a storm."),
        ],
        "project_title": "Botany roof repair",
        "project": ["botany-1", "botany-2", "botany-3", "botany-4", "botany-5", "botany-6"],
    },
    {
        "slug": "roof-repair-chipping-norton",
        "suburb": "Chipping Norton",
        "name": "Roof Repair Chipping Norton",
        "hero": "cn-2",
        "seo_title": "Roof Repair Chipping Norton NSW | Roof Centre",
        "description": "Roof repairs and roof replacement in Chipping Norton NSW. Tile and metal roofs, gutters and flashings. Call Roof Centre on 0431 848 619 for a free quote.",
        "lead": "Roof repairs, roof replacements and Colorbond roofing for homes in Chipping Norton and nearby suburbs.",
        "about": "Chipping Norton is about 27 kilometres south-west of the Sydney CBD, in the City of Liverpool and the South Western Sydney region.",
        "local": [
            ("Ageing tile roofs", "Many homes in the area have original concrete or terracotta tile roofs. Over time the tiles become porous, the ridge pointing cracks and valley irons rust. Depending on the overall condition, these roofs can be repaired, restored or replaced with metal."),
            ("Storm season", "Summer storms in Western Sydney can bring hail, strong winds and heavy rain. If your roof is damaged, see our <a href=\"/emergency-roof-make-safe/\">emergency make-safe</a> page for what to do."),
        ],
        "project_title": "Chipping Norton roof replacement",
        "project": ["cn-1", "cn-2", "cn-3", "cn-4", "cn-5", "cottage-ridge"],
    },
    {
        "slug": "roof-repair-near-me",
        "suburb": None,
        "name": "Roof Repair Near Me",
        "hero": "repair-tile-crew",
        "seo_title": "Roof Repair Near Me | Local Sydney Roofers | Roof Centre",
        "description": "Looking for roof repairs near you? Roof Centre is a local Sydney roofing contractor repairing tile and metal roofs. Call 0431 848 619 for a free quote.",
        "lead": "Looking for a local roofer? Roof Centre repairs, restores and replaces roofs for homes and businesses across Sydney.",
        "about": "We work across Sydney, including Botany and Chipping Norton. Call us to check whether we cover your suburb.",
        "local": [
            ("What to expect when you call", "Tell us what you have noticed: where the leak is, what type of roof you have and how long it has been happening. Photos are helpful. We will arrange a time to inspect the roof and give you a quote."),
            ("Choosing a roofer", "Ask for a written quote that lists the work to be done, check that the roofer is licensed and insured, and make sure you understand whether the job is a repair, a restoration or a replacement. Roof Centre is licensed and insured, and we can provide builder and client references on request."),
        ],
        "project_title": "Recent roof work",
        "project": ["botany-2", "cn-2", "cottage-reroof-complete", "repair-red-tile", "flashing-3", "gutter-1"],
    },
]

GENERAL_FAQS = [
    ("Do you offer free quotes?", "Yes. Contact our team for a free quote or more information. Call <a href=\"tel:+61431848619\">0431 848 619</a> or <a href=\"/contact/#quote\">send us an enquiry</a>."),
    ("Are you licensed and insured?", "Yes. Roof Centre is licensed and fully insured, and we can provide builder and client references on request."),
    ("What areas do you service?", "We work across Sydney, including Botany and Chipping Norton. Call us to check whether we cover your suburb."),
    ("What types of roofs do you work on?", "We repair, restore and replace tile and metal roofs on residential, commercial and industrial buildings. Converting existing homes to Colorbond or Zincalume roofing is our speciality."),
    ("What are your business hours?", "Monday to Friday, 9 am to 5 pm. You can send an enquiry through the website at any time, and we will reply as soon as we can."),
    ("How do I know if my roof needs repair or replacement?", "If the damage is limited to one area, such as a few broken tiles or a leaking flashing, a repair is usually enough. If the roof material is failing across the whole roof, or leaks keep coming back, replacement may be better value. We will inspect your roof and explain the options."),
    ("How long does a roof replacement take?", "It depends on the size and pitch of the roof, access, the materials and the weather. We will give you an expected timeframe with your quote."),
    ("My roof is leaking during a storm. What should I do?", "Stay off the roof. Move belongings away from the leak, put out buckets and keep people out of any room where the ceiling is sagging. Call us to arrange a make-safe. For storm emergencies where life or property is at immediate risk, call the NSW SES on <a href=\"tel:132500\">132 500</a>, or 000 in a life-threatening emergency."),
    ("Do you clean gutters?", "Yes. We clean gutters and also replace gutters, downpipes and fascia, and install gutter protection."),
    ("What should I include in my enquiry?", "Your suburb, the type of roof (tile or metal), what the problem is and how long it has been happening. Photos are very helpful."),
]

ABOUT = {
    "intro": [
        "Roof Centre is a local roofing contractor for homeowners and commercial clients who need to replace or renovate their roof. Our goal is always to make your new roof or roof repair last as long as possible, using high-grade materials while keeping to your budget.",
        "We are fully insured, hold the relevant licences, and can provide builder and client references on request.",
        "Our speciality is converting existing homes with any type of roof to new Colorbond or Zincalume steel roofs. Domestic roof replacement is what we do best, but we also repair and restore industrial, commercial and residential roofs.",
    ],
}

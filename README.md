# heli — Desert Strike Spiritual Successor

An open-world, isometric helicopter rescue, logistics, and combat sim set in a real-world-mapped 150km Himalayan border region (Sikkim / eastern Nepal / Darjeeling foothills) shattered by a massive earthquake. The Quad and China both arrive as disaster-relief partners — until China is discovered fortifying the towns it is rebuilding. Fuel scarcity, aid logistics, and collateral damage feed a regional political legitimacy system that determines whether the humanitarian mission holds or collapses into open war.

**Target feel:** indie-scoped — large map and layered systems, but stylized presentation and tight, readable individual systems. Scope discipline is a first-class design constraint.

## Project Documents

| Document | Purpose |
|---|---|
| [SPEC.md](SPEC.md) | Design spec v2.0 — the authoritative development/prompting reference: premise, geography and terrain pipeline, design pillars, camera/fuel/legitimacy systems, five-stage campaign, mission structure, command layer, factions, technical direction, and consolidated open questions. |
| [progress.md](progress.md) | Running progress log, updated with every change to allow tracking between chat/dev sessions. |

## Core Systems (see SPEC.md for detail)

- **Fixed isometric camera** with automatic cruise zoom-out (target-value + continuous lerp, asymmetric easing).
- **Fuel & logistics:** effort-based burn rate (altitude, load, hover, speed); player-built FARP/aid-hub network; relief cargo, ordnance, and auxiliary tanks compete for the same lift; running dry is recoverable ("stuck, not dead").
- **Legitimacy & collateral:** tracked regionally, not globally, and two-directional — relief work banks legitimacy, collateral and visible militarization spend it; China competes for the same trust; failed aid or high collateral spawns local armed groups that degrade logistics; command-delegated damage counts the same as direct action.
- **Five-stage escalation campaign:** Search & Rescue → Relief Logistics → The Turn (suspicion and first skirmishes) → Hostilities → Full-Blown War, each stage changing what is mechanically available. Relief tasking persists into the combat stages.
- **Command layer:** waypoint system that grows from tutorial relief-convoy escorts into finale district-level attack/defend/hold orders.

## Technical Direction

- **Engine:** Unity (stylized visual target; terrain via heightmap import, e.g. MapMagic 2 / Gaia on Unity terrain). Unity `.gitignore` is already in place.
- **Terrain data:** SRTM 30m / Copernicus GLO-30 DEM via OpenTopography or QGIS, stylized in World Machine/Gaea, exported as 16-bit heightmap with vertical compression.
- **Disaster state:** pre-authored world damage (destroyed bridges, landslide-blocked roads, flood scour) plus scripted aftershock events — level dressing and mission logic, not a simulation layer.
- **Flagged scope risks:** 150km terrain streaming/LOD; command-layer "attack" AI; rescue-interaction depth; aggregate system count. Fuel/logistics and the legitimacy loop are the must-ship systems; command sophistication, armed-groups-as-faction, and rescue depth are the first cut candidates.

## Repository Status

Pre-production. No Unity project has been created yet — the repository currently contains the design spec, this README, the progress log, and a Unity-ready `.gitignore`.

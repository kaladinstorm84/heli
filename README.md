# heli — Desert Strike Spiritual Successor

An open-world, isometric helicopter combat and logistics sim set in a real-world-mapped 150km Himalayan border region (Sikkim / eastern Nepal / Darjeeling foothills). Fuel scarcity, forward-base logistics, and collateral damage feed a regional political legitimacy system that determines whether the player's covert-but-invited Quad intervention holds or collapses into open war.

**Target feel:** indie-scoped — large map and layered systems, but stylized presentation and tight, readable individual systems. Scope discipline is a first-class design constraint.

## Project Documents

| Document | Purpose |
|---|---|
| [SPEC.md](SPEC.md) | Design spec v1.0 — the authoritative development/prompting reference: premise, geography and terrain pipeline, design pillars, camera/fuel/legitimacy systems, five-stage campaign, mission structure, command layer, factions, technical direction, and consolidated open questions. |
| [progress.md](progress.md) | Running progress log, updated with every change to allow tracking between chat/dev sessions. |

## Core Systems (see SPEC.md for detail)

- **Fixed isometric camera** with automatic cruise zoom-out (target-value + continuous lerp, asymmetric easing).
- **Fuel & logistics:** effort-based burn rate (altitude, load, hover, speed); player-built FARP network; auxiliary tanks as a loadout trade-off; running dry is recoverable ("stuck, not dead").
- **Legitimacy & collateral:** tracked regionally, not globally; high collateral spawns local insurgency that degrades logistics; command-delegated damage counts the same as direct action.
- **Five-stage escalation campaign:** Recon → Base Setup → Minor Skirmishes → Hostilities → Full-Blown War, each stage changing what is mechanically available.
- **Command layer:** waypoint system that grows from tutorial escorts into finale district-level attack/defend/hold orders.

## Technical Direction

- **Engine:** Unity (stylized visual target; terrain via heightmap import, e.g. MapMagic 2 / Gaia on Unity terrain). Unity `.gitignore` is already in place.
- **Terrain data:** SRTM 30m / Copernicus GLO-30 DEM via OpenTopography or QGIS, stylized in World Machine/Gaea, exported as 16-bit heightmap with vertical compression.
- **Flagged scope risks:** 150km terrain streaming/LOD; command-layer "attack" AI; aggregate system count. Fuel/logistics and the legitimacy loop are the must-ship systems; command sophistication and insurgency-as-faction are the first cut candidates.

## Repository Status

Pre-production. No Unity project has been created yet — the repository currently contains the design spec, this README, the progress log, and a Unity-ready `.gitignore`.

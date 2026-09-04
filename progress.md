# Progress Log

Running log of changes to allow progress tracking between chat/dev sessions. Newest entries first.

## 2026-09-04 — DEM download tool (first code in the repo)

- Added `tools/terrain/download_dem.py`: downloads Copernicus GLO-30 (30m) tiles from the public AWS Open Data mirror (no login/API key), caches them, merges/clips to a bounding box, and optionally exports a Unity-ready 16-bit little-endian RAW heightmap reprojected to UTM 45N with a JSON sidecar (extent, elevation range, import settings).
- Presets matching SPEC.md §2: `playable` (150km box, 9 tiles), `extended` (backdrop margin for the converging-ceiling boundary), `prototype` (~12km Teesta bend/Chungthang slice for the hex-grid/silhouette test).
- Added `tools/terrain/requirements.txt` (numpy, rasterio, requests) and `tools/terrain/README.md` (usage, Unity import notes incl. Flip Vertically and vertical compression, Copernicus data credit).
- `.gitignore`: added `/data/` for downloaded DEM data.
- **Tested end-to-end:** ran the `prototype` preset — 1 tile (42MB) downloaded, clipped GeoTIFF 432x396px, heightmap 1025x1025 verified (exact pixel count, full 16-bit range), elevation 1,298–4,589m over 12.0x12.3km (plausible for the Teesta gorge at Chungthang). Also verified 9-tile enumeration for `playable` via `--list-tiles`.
- Updated `README.md` with a Tools section. Discussion context (not yet specced): considering Catlike Coding-style hex-grid terrain — the GeoTIFF output is the sampling source for that route; the RAW export serves the Unity-terrain route.

## 2026-09-03 — Spec v2.3: repair race pacing decided (progress-clocked, not wall-clocked)

- Resolved the aid-race pacing question in `SPEC.md` §5/§12: China's repair queue must never advance on real time — an "X repairs per hour" model would punish exploration, careful flying, and side questing (pillar 1 violation).
- Model: progress-clocked, pace-matched to the player. Primary clock = player repair completions (~1:1); floor clock = main-mission completions and stage transitions at lower weight (guarantees plot-critical Chinese-rebuilt/fortified infrastructure exists even for rush-the-plot players); everything else ticks China zero.
- Presentation note added: pace-matching must not read as mirroring — hide the clock via queue ordering, spatial separation, and decoupled completion announcements.
- §12 updated: pacing question marked decided; remaining tuning open (tick weights, uncontested-node speed, rubber-banding); new question on whether non-repair relief progress also ticks the queue.
- Updated `README.md` (spec version, pacing note). Docs-only change; no build to run.

## 2026-09-03 — Spec v2.2: the repair race (China repairs and earns legitimacy too)

- Extended the repair mechanic in `SPEC.md` §5: repairable nodes are contested — China's relief mission works its own repair queue, and China-completed nodes bank Chinese regional legitimacy and reopen routes oriented to Chinese logistics.
- Tied the race to the premise: Chinese-rebuilt infrastructure is the delivery vector for the fortification twist — towns arrive garrisoned because China rebuilt the routes into them. Conceding a node in Stage 2 can mean facing it as enemy infrastructure in Stage 4.
- Ripple edits: §6 (China competes actively via rescues/aid/repairs; a region whose bridge China rebuilt doesn't read Chinese trucks as a threat), §7 Stage 2 (repair race as the stage's visible competition), §10 faction table, §12 (aid-race simulation question extended with a concrete cheap model; new question on interfering with in-progress Chinese repairs and its legitimacy cost).
- Data flag: added `repaired_by` (player/China/none) with per-owner systemic effects incl. late-game fortification eligibility.
- Updated `README.md` (spec version, repair-race bullet). Docs-only change; no build to run.

## 2026-09-03 — Spec v2.1: infrastructure repair ("assist") mechanic

- Added an Infrastructure Repair subsection to `SPEC.md` §5: SnowRunner-flavored haulage of heavy repair materials to damaged infrastructure nodes (bridges, blocked roads, helipads); Nepali crews do the repair once supplied — player is the lifeline, not the builder.
- Systemic payoffs: repaired routes enable/shorten ground convoy routes (existing convoy layer), reduce standing airlift demand, automate FARP resupply, and bank regional legitimacy. Late-game edge: repaired infrastructure is usable by the enemy and cuttable by armed groups.
- Ripple edits: §2 disaster layer (repairable nodes as the exception to static damage), §7 Stage 2 (repair unlocks as the stage's core investment decision), §8 side missions (repair jobs), §11 (repairable-node authoring: discrete prefab state swaps, no construction sim), §12 (new open questions: sling-load vs land-and-unload delivery, node-type scope/count, enemy exploitation of repaired routes).
- Data flag recommendation: `repair_state` (damaged/supplied/repaired) + material requirements + unlocked effects per node, reusing the `plot_critical` convention.
- Updated `README.md` (spec version, new core-systems bullet). Docs-only change; no build to run.

## 2026-09-03 — Premise rework: spec v2.0 (disaster-relief opening)

- Rewrote `SPEC.md` as v2.0 for the new premise: a massive earthquake devastates eastern Nepal (collapsed glacial lakes/reservoirs → flash floods and mudslides); the Quad and China both arrive as relief partners; cooperation holds until China is discovered fortifying the towns it is rebuilding.
- Mechanical spine retained from v1.0 (fuel/FARP logistics, regional legitimacy, isometric camera, command layer, five-stage escalation, terrain pipeline). Changes ripple through framing:
  - §1 Premise rewritten; real-world anchors extended with the 2015 Gorkha earthquake and the 2023 South Lhonak GLOF/Chungthang dam collapse (in-map Teesta valley flood precedent).
  - §2 adds a "disaster layer" mapping quake/flood damage onto the existing valley/ridge geography; southern map boundary now framed as the edge of the disaster zone.
  - §5 FARPs begin as aid hubs; relief cargo/casevac competes with ordnance and aux tanks for lift; hover-heavy rescue work makes hover burn a felt cost pre-combat.
  - §6 legitimacy is now two-directional (relief banks it, collateral spends it); China competes for regional trust ("aid race"); insurgency reframed as local armed groups born of failed aid/collateral.
  - §7 stages renamed/reworked: Search & Rescue → Relief Logistics → The Turn → Hostilities → War; relief tasking persists through combat stages; finale city is also still a disaster zone.
  - §8 tutorial re-set inside disaster response (search sweep, relief-convoy escort with landslide clearance, first aid hub).
  - §10 faction table updated (Chinese Relief Mission/PLA dual role; Local Armed Groups replace generic insurgency).
  - §11 adds disaster-state authoring approach (pre-authored damage + scripted events, no simulation) and flags rescue-interaction depth as a new scope risk.
  - §12 open questions updated (legitimacy accounting, aid race simulation, joint-ops content, rescue mechanic depth, disaster dynamism).
- Updated `README.md` pitch, systems summary, and technical notes to match v2.0.
- Docs-only change; still no Unity project or code, so no build to run.

## 2026-08-16 — Design spec captured in repo

- Added `SPEC.md` (Design spec v1.0) — authoritative development/prompting reference for the Desert Strike spiritual successor: premise (Quad intervention on Nepal's eastern border), real-world Sikkim/eastern-Nepal geography and DEM terrain pipeline, core design pillars, isometric camera system, fuel/logistics (FARP) system, regional legitimacy & collateral system, five-stage escalation campaign, mission structure, command layer, faction overview, technical direction (Unity), and consolidated open questions.
- Rewrote `README.md` from placeholder to a proper project overview linking the spec and summarizing core systems, technical direction, and repository status.
- Added this `progress.md` file.
- No Unity project or code exists yet; no build to run (docs-only change). Committed on branch `cursor/add-design-spec-docs-e8b9` after user approval to commit.

## Current State

- **Phase:** pre-production, spec at v2.3 (disaster-relief premise + contested repair race with progress-clocked pacing). First tooling in place (DEM download).
- **Repo contents:** `SPEC.md`, `README.md`, `progress.md`, `tools/terrain/` (DEM download tool), Unity `.gitignore`.
- **Next candidate steps (not started):**
  - Resolve open questions in SPEC.md §12 (legitimacy accounting, escalation pacing, rescue mechanic depth, fuel-burn formula, finale scope, camera/command interaction rules).
  - Create the Unity project skeleton.
  - Prototype the terrain pipeline: pull the 150km bounding-box DEM (Copernicus GLO-30 via OpenTopography), test vertical compression, import as 16-bit heightmap.
  - Prototype the camera cruise-zoom lerp model (cheap, isolated, validates a core feel decision early).

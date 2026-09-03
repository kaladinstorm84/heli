# SPEC.md — Desert Strike Spiritual Successor
### Open-World Helicopter Rescue / Logistics / Combat Sim
**Status:** Design spec v2.3 — intended as a development/prompting reference document

> **v2.3 decision:** the repair race is progress-clocked, not wall-clocked — China's repair queue advances with the player's own repair/mission progress (roughly pace-matched), never with real time, so exploration, careful flying, and side quests are never taxed. See Section 5.
>
> **v2.2 addition:** the repair race — China's relief mission also repairs infrastructure and earns regional legitimacy for it. Repairable nodes are contested: whoever supplies a repair claims its legitimacy and its systemic payoff, and Chinese-rebuilt infrastructure is the delivery vector for the fortification twist. See Sections 5–6.
>
> **v2.1 addition:** infrastructure repair ("assist") mechanic — SnowRunner-flavored haulage of repair materials to broken bridges/roads, which reopens ground convoy routes, reduces standing airlift demand, and banks regional legitimacy. See Section 5.
>
> **v2.0 premise change:** the campaign no longer opens as a covert military intervention. Nepal has been struck by a massive earthquake; the Quad and China both arrive as disaster-relief partners, and the campaign escalates from cooperative humanitarian operations into confrontation when China is discovered fortifying the towns it is "rebuilding." The mechanical spine of v1.0 (fuel/FARP logistics, regional legitimacy, isometric camera, command layer, five-stage escalation) is retained — the disaster framing strengthens rather than replaces it.

---

## 0. One-Line Pitch

A modern, open-world spiritual successor to *Desert Strike* — isometric helicopter rescue, logistics, and combat across a real-world-mapped 150km Himalayan border region shattered by a massive earthquake, where the Quad and China begin as rival relief partners and the player's conduct — aid delivered, restraint shown, collateral avoided — determines whether a humanitarian mission collapses into open war.

**Target feel: indie-scoped.** Large map and layered systems, but stylized/simplified presentation and tight, readable individual systems — not AAA simulation depth or photorealistic fidelity. Scope discipline is a first-class design constraint, not an afterthought.

---

## 1. Premise & Setting

A massive earthquake has devastated eastern Nepal and the surrounding Himalayan border region. Beyond the direct destruction, the quake has collapsed high-altitude glacial lakes, reservoirs, and dams, triggering flash floods and mudslides down the valley corridors — the roads are severed, the bridges are down, and for most of the region **helicopters are the only logistics that work.**

Nepal issues an international appeal. The Quad (US, India, Japan, Australia) responds with a joint humanitarian task force — the player's unit. **China responds too**, with its own substantial relief mission. In the early campaign this genuinely works: deconflicted airspace, divided sectors, even joint operations. The player flies rescue and aid missions alongside, and sometimes with, Chinese aircraft.

**The turn:** reports begin to surface — first rumor, then intel, then news — that China is *fortifying* the towns it has taken responsibility for rebuilding. Relief depots that look like ammunition points. "Reconstruction crews" laying hardened positions. A humanitarian footprint quietly becoming a garrison footprint in sovereign Nepali territory, while the disaster keeps every road closed and every eye on the rescue effort.

**Core strategic tension:** the Quad cannot simply strike — it arrived as a humanitarian mission, and the side that is *seen* to militarize the relief effort loses. Chinese information operations are primed to amplify any Quad aggression or collateral damage into proof that the Quad was the occupying force all along. Meanwhile every fortified town is a fact on the ground that gets harder to reverse. **Military effectiveness and political legitimacy actively pull against each other**, and the player's humanitarian performance — lives saved, aid delivered, restraint shown — is the currency that keeps Nepal's trust. Winning engagements carelessly can mean losing the country.

Real-world anchor points used for plausibility, not literal depiction: the 2015 Gorkha earthquake (Nepal's vulnerability and the international rotary-wing relief effort that followed), the 2023 South Lhonak glacial lake outburst flood in Sikkim (which destroyed the Chungthang dam and tore down the Teesta valley — the exact flood mechanism this premise scales up, inside the map's bounding box), the Doklam/Zuluk tri-junction area (genuine site of past China-India-Bhutan border tension), and the Siliguri Corridor ("Chicken's Neck" — the narrow strategic link between mainland India and its northeast) as the finale's implied stakes.

---

## 2. Setting Geography — Real-World Data

**Region:** Sikkim, eastern Nepal (Taplejung/Ilam districts), and the Darjeeling/Siliguri foothills of West Bengal. Chosen because this is one of the few places on Earth with a documented contiguity of biomes — subtropical forest to alpine/cold desert — within roughly 100km, driven by elevation rather than latitude.

**Approximate 150km x 150km bounding box, anchored by:**
- **North:** Yumthang (high alpine, approach to Tibetan plateau)
- **Northwest:** Kangchenjunga (8,586m, extreme high-altitude wall, sits on the India-Nepal border)
- **West:** Taplejung / Phungling and Ilam, Nepal (the epicenter region and the sovereign territory in question)
- **East:** Zuluk (near Nathu La / Chumbi Valley, closest point to real-world China border tension, and the Chinese relief mission's natural entry corridor)
- **South:** Darjeeling → Kurseong → Siliguri corridor approach (lowest elevation, most populated, highest political exposure)
- **Center:** Gangtok (temperate mid-elevation hub)

**Elevation gradient (north/high to south/low) drives biome placement:**
1. High-altitude cold desert / alpine (Yumthang, Kangchenjunga approaches)
2. Subalpine conifer / alpine meadow
3. Temperate broadleaf forest (Gangtok band)
4. Subtropical forest / foothill (Namchi, Darjeeling, Kurseong)

Biome bands should follow real elevation contours and valley/ridge structure (Teesta and Rangit river valleys as natural travel corridors and biome dividers) — not a grid quartering.

**Disaster layer (v2.0):** the earthquake damage maps onto the same geography rather than being scattered:
- **North/high:** collapsed glacial lakes and moraine dams (GLOF sources), avalanche-buried passes — the origin points of the floods.
- **Valley corridors (Teesta/Rangit):** flash-flood and mudslide damage concentrated along the rivers — destroyed bridges, washed-out roads, drowned low-lying settlements. The same valleys that were the natural travel corridors are now the damage corridors, which is exactly why ground logistics is dead and the player's helicopter matters.
- **South/populated:** highest casualty and displacement concentration, mass shelter needs, highest political visibility.
- Damage state should be **pre-authored and largely static**, not dynamically simulated — indie scope. Aftershocks/secondary floods, if used, are scripted mission events, not a simulation layer. The exception is the designated set of **repairable infrastructure nodes** (see Section 5, Infrastructure Repair), which step through pre-authored damaged/repaired states when the player supplies them — discrete state swaps, still not simulation.

**Terrain data pipeline:**
- Source: SRTM (30m global) or Copernicus DEM (GLO-30, generally cleaner in mountainous terrain); ASTER GDEM as a gap-filler for SRTM voids in steep Himalayan terrain.
- Extraction: OpenTopography (bounding-box export) or QGIS.
- Processing: World Machine or Gaea for erosion/stylization — raw SRTM at this scale will be too noisy/blocky and needs "video-game-truth" compression.
- **Vertical compression required.** Real elevation delta across this box is roughly 300m–8,586m. Used raw, this produces near-vertical, unplayable terrain. Scale elevation delta down while preserving relative silhouette and ridge/valley logic.
- Export as 16-bit heightmap, native import to engine.

**Map boundary technique — converging ceiling:**
- Define playable altitude ceiling as a function of distance-to-edge: full ceiling in the interior, tapering toward zero clearance near the boundary.
- Because real terrain naturally rises toward the north/northeast edges of this box, the ceiling curve intersects rising terrain and produces a natural, non-arbitrary "wall" — no invisible barriers.
- Render real terrain beyond the playable footprint (wider DEM sample, lower LOD, non-collidable) so distant peaks recede naturally instead of cutting off.
- **Known asymmetry:** this only works cleanly on the north/east (genuinely rising terrain). The southern edge (Terai/Siliguri approach) is low and flat and won't cap altitude naturally — use a narrative/systemic boundary device instead. The v2.0 premise offers a natural one: the southern edge is the intact world — functioning airfields, ground logistics, other agencies' area of operations — and the player's tasking simply ends where the disaster zone ends.

---

## 3. Core Design Pillars

1. **Scarcity is systemic, not punitive.** Fuel and ordnance are resources to plan around and invest in solving, not a countdown that punishes exploration.
2. **The map is the plot's geography.** Biomes are real operational theaters with real constraints — and in v2.0, the disaster damage follows the same real valley/ridge logic — not reskinned terrain.
3. **Restraint is a real cost, not a moral rail.** The "quiet" solution is harder, slower, or costlier than the "loud" one — never simply the correct choice with no trade-off.
4. **Early logistics pays off late.** Infrastructure built as "boring" early-game relief work becomes late-game military capability — the aid network *is* the war network.
5. **Consequences are local, not global.** Player actions affect the specific region they happened in, not an abstract global meter.
6. **Scope discipline over system count.** Fuel/logistics tension and the legitimacy consequence loop are the soul of the game. Other systems (multi-unit command, AI complexity, disaster simulation) should stay implementation-simple even where they're player-facing-rich, to protect the indie-scoped target feel.

---

## 4. Camera System

- **Fixed isometric perspective**, always — no camera mode switching between traversal and combat.
- **Automatic cruise zoom-out:** triggers when sustained straight-line flight (heading variance within a small tolerance) is held at ≥75% of max speed for over 2 seconds.
- **Implementation model:** target-value + continuous lerp, not discrete triggered animations. Every frame, compute a desired zoom level from current state (speed/heading/combat status); lerp the camera's actual zoom toward that target continuously, so interruption mid-transition simply changes the target and the lerp reverses smoothly from its current position — never resets/restarts.
- **Asymmetric easing:** zoom-out is slow/gentle (~1.5–2s, ease-out) since there's no urgency; zoom-in is fast (~0.4–0.6s, ease-in) since it typically reacts to a threat and shouldn't feel like it's lagging behind danger.
- **Two LOD tiers required for art direction:** "cruise silhouette" (must read as a landmark at far zoom — design biome art around recognizable silhouettes: a monastery on a ridge, a collapsed dam, a flood-scoured valley, a bridge over a gorge — intact or fallen) and "combat detail" (must support cover, sightlines, tactical positioning up close — and in v2.0, rescue detail: survivors on rooftops, landing zones in rubble).
- **Open question:** does a locked-on threat or active weapons fire force combat zoom regardless of speed/heading? (Recommend yes.)

---

## 5. Fuel & Logistics System

- **Burn rate is effort-based:** altitude, cargo/combat load, hover time, and speed all affect consumption — not pure distance. Altitude specifically reduces effective lift/payload in high-Himalaya missions, forcing loadout trade-offs unique to that biome. Rescue work is hover-heavy (winching, confined-area landings), making hover burn a felt cost from the first mission — before combat ever enters.
- **FARP (Forward Arming and Refueling Point) network is fixed and player-learnable**, not randomly scattered — players build a mental map of safe legs between biomes, mirroring a road network.
- **FARPs are player-built infrastructure**, established during the relief-logistics stage and side missions. In v2.0 they begin life as **aid hubs** — fuel, supplies, medical staging — and the same network later extends military operational range when the campaign turns. This is the direct payoff loop for logistics-focused play, and it is also a legitimacy anchor: a region served by a player aid hub remembers it.
- **Cargo is now more than ordnance:** relief supplies, casualty evacuation, reconstruction materiel, and (later) weapons all compete for the same lift capacity. Auxiliary tanks remain a loadout choice trading cargo/ordnance capacity for range — scarcity becomes a build decision, not just a constraint.
- **Running dry is recoverable, not a fail state:** forced auto-rotation landing → on-foot or awaiting rescue, rather than instant mission failure ("stuck, not dead," after SnowRunner).

### Infrastructure Repair — the "Assist" Mechanic (v2.1)

Deliberately SnowRunner-flavored: the world is full of broken infrastructure, and fixing it is a haulage problem the player opts into.

- **Repairable nodes:** specific damaged infrastructure — bridges, landslide-blocked road segments, damaged helipads/airstrips, possibly power/comms relays — are marked as repairable, distinct from ambient (permanent, cosmetic) disaster damage.
- **The player is the lifeline, not the builder.** Repair means airlifting the required materials (multiple heavy loads: girders, fuel for machinery, engineering stores) to the site; Nepali engineer crews or local workers do the actual repair once supplied. Keeps the fantasy helicopter-centric and the implementation thin — no construction minigame, the node flips through pre-authored damage states as deliveries land.
- **Multi-trip commitment with SnowRunner texture:** repair loads are heavy and awkward — they cut range and handling (see effort-based burn), and delivery sites are the hard kind (a gorge bridgehead, a half-collapsed road shelf), making the approach and set-down the skill expression. Sling-load vs. land-and-unload is an open question below.
- **The payoff is systemic, not cosmetic — repaired infrastructure reopens ground logistics:**
  - Repaired bridges/roads enable or shorten **convoy routes** (the same waypoint/convoy system from the tutorial and command layer), letting ground transport take over supply legs the player was flying by hand.
  - Settlements reconnected by ground become cheaper to serve — standing airlift demand drops, freeing the player's lift capacity for the next problem. This is the core loop: **fly the hard version until you've earned the easy version.**
  - FARP/aid-hub resupply can automate along repaired routes instead of depending on player trips.
  - Repairs bank **regional legitimacy** like other relief work — and a repaired bridge is a visible, persistent monument to it, on-theme with the cruise-silhouette LOD tier (a rebuilt bridge should read at far zoom).
- **The repair race (v2.2): China repairs too.** Repairable nodes are contested opportunities, not a player-exclusive to-do list. China's relief mission works its own repair queue, and a node China completes:
  - banks **Chinese** regional legitimacy in that region (see Section 6) — visibly, with Chinese crews, signage, and ribbon-cutting optics;
  - reopens the route for everyone, but oriented to Chinese logistics — and later stages reveal the sting: **Chinese-rebuilt infrastructure is the delivery vector for fortification.** The premise's "towns China rebuilt" arrive garrisoned because China rebuilt the roads and bridges into them. Every node the player concedes in Stage 2 is potential enemy infrastructure in Stage 4.
  - This converts repair from a side activity into the aid race's scoreboard: the player cannot fix everything (lift capacity is finite), so *which* nodes to win — and which to knowingly concede to China — becomes a strategic choice with a long fuse.
- **Race pacing is progress-clocked, not wall-clocked (v2.3).** China's repair queue must never advance on real time — an "X repairs per hour" model would punish exploration, careful flying, and side questing, violating pillar 1 (scarcity is systemic, not punitive). Instead, China's queue advances on **player-progress ticks**, pace-matched to the player's own repair rate:
  - Primary clock: the player completing a repair node advances China's current queue item by roughly one node — the race stays close by construction, and the choice space stays "*which* nodes do I win," never "can I out-grind the timer."
  - Floor clock: main-mission completions and stage transitions also tick China's queue (at a lower weight), so a rush-the-plot player who ignores repair entirely still arrives in Stage 3–4 with the plot-critical Chinese-rebuilt (and fortified) infrastructure in place — the premise cannot be starved out by not playing the repair game.
  - Time spent exploring, flying carefully, doing rescues, or running non-repair side missions advances China **zero**. The race only moves when the player moves it or the plot does.
  - Presentation note: pace-matching must not read as mirroring (China visibly finishing a bridge the moment the player finishes theirs feels rigged). Hide the clock with queue ordering, spatial separation (China works its own sectors), and completion announcements decoupled from the player's delivery moments.
- **Late-game edge:** infrastructure the player repaired is real terrain that everyone can use. Chinese forces can advance over a player-rebuilt bridge; armed groups can cut a repaired route the player's logistics now lean on. Defending — or in the worst case, re-dropping — a bridge the player personally restored is a deliberately available dramatic beat, and keeps repair from being a purely safe investment.
- **Data flag recommendation:** repairable nodes mirror the forward-base pattern — `repair_state` (damaged / supplied / repaired), `repaired_by` (player / China / none), material requirements, and the systemic effects unlocked per state and owner (convoy routes, demand reductions, legitimacy attribution, late-game fortification eligibility). Plot-critical repairs (if any) use the same `plot_critical: bool` convention as bases.

---

## 6. Legitimacy & Collateral System

- **Tracked regionally** (valley/settlement level), not globally. What happens in one area does not affect the player elsewhere, but does change that region's future patrol density, hostility, intel quality, and mission availability.
- **Legitimacy is now two-directional (v2.0):** relief performance — rescues completed, aid delivered, hubs established — *builds* regional legitimacy; collateral damage and visible militarization *spend* it. The early campaign is where the player banks the goodwill the late campaign will burn.
- **China competes for the same resource — actively.** The Chinese relief mission runs its own rescues, aid deliveries, and **infrastructure repairs** (see Section 5, the repair race), each banking Chinese legitimacy in the region where it happens. Regions can end up trusting the Chinese relief mission more than the Quad. The "aid race" of the cooperative stages is the legitimacy war's opening moves, before a shot is fired — and after the turn, a region that trusts China is harder to operate in: worse intel, more reporting of Quad movements, political cover for Chinese fortification. A region whose bridge China rebuilt does not read Chinese trucks on it as a threat — which is exactly the problem.
- **High regional collateral (or abandoned/failed relief) raises local armed-group activity** — a third faction, distinct from Chinese forces and the Nepali government, born of desperation and grievance in a disaster zone, that the player did not choose to fight.
- **Armed groups primarily degrade player logistics**, not just add combat volume: sabotage and looting of the FARP/aid-hub network, harassed supply routes, drying up local intel — ties consequences directly back into the fuel/logistics system rather than just spawning more enemies.
- **China benefits passively.** Chinese-aligned information operations can amplify a bad Quad engagement — or a failed relief promise — into a strategic loss without China needing to act directly.
- **Design intent:** the effective military solution (heavier ordnance, fast resolution) should sometimes be in genuine tension with collateral cost — restraint must be a real trade-off, not a hidden "correct" path with no downside. In a disaster zone this is sharpened: the "battlefield" is full of people who cannot leave.
- **Command delegation carries the same weight as direct action:** damage caused by player-directed allied forces (see Section 8, Command Layer) counts against the player's legitimacy standing exactly as if the player caused it directly. This requires enough player visibility into off-screen directed-unit behavior that consequences feel earned, not arbitrary.
- **Open question:** do local armed groups escalate into a full independent faction with their own AI and territory, or remain a passive modifier (patrol density, supply friction, mission availability)? Recommend prototyping as a passive modifier first.

---

## 7. Campaign Structure — Five-Stage Escalation Ladder

Each stage changes what's *mechanically available*, not just what's narratively happening. The v2.0 arc: cooperation → suspicion → confrontation → war.

### Stage 1 — Search & Rescue / Damage Assessment
- Light loadouts, no meaningful weapons; fuel/range and hover time are the primary constraints.
- Missions: damage-assessment overflights, survivor location and winch rescue, casualty evacuation. Establishes the map for the player while doubling as base-network scouting.
- Chinese aircraft are present, deconflicted, occasionally cooperative — the player *sees* the partner who will become the antagonist.
- Failure state is **lives lost or tasking missed**, not death.

### Stage 2 — Relief Logistics (Base Setup / Haulage)
- Logistics missions: cargo weight cuts into range; aid demand outstrips lift capacity, forcing triage.
- Player physically builds the FARP/aid-hub network relied on later — the "boring" relief infrastructure that becomes the war's operational backbone.
- **Infrastructure repair unlocks here** (see Section 5): airlifting materials to broken bridges and blocked roads reopens ground convoy routes, converting the player's hand-flown supply legs into automated ground logistics — the stage's core investment decision (serve demand now vs. repair the route that removes the demand).
- **The repair race is this stage's visible competition:** Chinese crews work their own repair queue, and nodes the player doesn't win get rebuilt — and credited — by China. Legitimacy banking is at its cheapest here, and so is quietly losing it: what reads as friendly rivalry in Stage 2 is retroactively revealed as positioning in Stage 3.

### Stage 3 — The Turn (Suspicion & Shadow Recon → First Skirmishes)
- Reports surface of Chinese fortification in towns under Chinese reconstruction. Tasking quietly shifts: recon of fortified sites flown under relief cover, intel gathering, shadowing Chinese convoys.
- First combat — still deniable on both sides (unmarked elements, "accidents," contested accounts). Neither side wants to be the one who visibly broke the humanitarian truce.
- Introduces loud-vs-quiet tension: a visibly decisive tactical win can still be a strategic cost.

### Stage 4 — Hostilities
- Cooperation collapses publicly. Legitimacy/neutrality framing becomes a live, tracked variable; Nepali domestic political support responds to player conduct in Stages 1–3 — the aid record is now the political record.
- Loadouts open up; every visible engagement runs a background legitimacy cost.
- **Relief tasking does not stop.** Rescue and aid missions continue alongside combat operations, competing for the same airframes, fuel, and hours — abandoning the humanitarian mission to fight the war is itself a legitimacy cost. This is the stage's signature tension.

### Stage 5 — Full-Blown War / Finale
- Deniability collapses entirely; the campaign's original framing — a humanitarian mission — has failed regardless of battlefield outcome.
- **Escalation is expressed through SCALE, not new mechanics.** Base defense (bounded perimeter, single threat vector, likely nearby resupply) becomes city-wide defense: multiple simultaneous fronts, constant civilian presence, no single "hold this line" objective — a resource-allocation/triage problem rather than a reactive one.
- **Finale objective:** repel an occupying force from a city and then defend the whole city — a city that is *also still a disaster zone*: the population cannot evacuate over severed roads, shelters concentrate civilians, and the aid network is the defense's supply line. Collateral damage stakes are at their highest point in the campaign, exactly when the player has the most firepower available.
- Thematic note available: this stage can represent the campaign's stated goal (keep the relief effort from becoming a war) *failing* even while battles are being won — a tragic-victory framing rather than a clean one, if desired.
- **Open question:** exact scope of the finale battlespace — city itself vs. the terrain immediately defending its approach (softer to build, still carries the stakes without turning a real populated area into a full warzone).

**Open question (campaign-wide):** is escalation pace player-driven (relief performance and restraint controlling how fast — or whether — the ladder climbs) or scripted? Player-driven is more implementation work but makes "your conduct determines whether this becomes a war" mechanically real rather than narrated. Recommended if feasible. Note: the discovery of Chinese fortification (the Stage 3 turn) likely needs to be scripted regardless — it is the premise, not a player outcome; what the player can influence is everything after it.

---

## 8. Mission Structure

### Tutorial Missions
Each step introduces exactly one new system before combining them. All three now sit naturally inside the disaster-response opening:
1. **Search sweep** — fly a damage-assessment/survivor-search pattern and scout an initial base location (navigation/recon only; hover and fuel costs introduced gently).
2. **Escort** a relief convoy to a cut-off settlement:
   - Set waypoints for ground forces to follow.
   - Mild "combat" clearing natural hazards (light weapons — debris, unstable slopes threatening the route).
   - Heavier weapons for **land clearance** — blasting a landslide-blocked pass open (quietly foreshadows the ordnance-vs-collateral tension before the legitimacy system is mechanically active — clearing rock should feel different from anything near a settlement, even here).
3. **Identify and establish the first forward aid hub (FARP):**
   - Carry initial cargo to the location.
   - Set up a convoy route to the new hub.

*Sequencing note:* the fuel-pressure moment should land just before the aid-hub tutorial step, so the base-building payoff is felt, not just explained.

### Main Missions
- Mostly plot-driven. Early game: rescue and relief set-pieces (dam-collapse response, mass evacuation). Late game: heavy focus on action/combat, with many defensive missions — primarily repelling/driving back enemy advances — while relief tasking continues in parallel.
- **Completable with minimal forward infrastructure** — specifically the FARPs/aid hubs that are plot-critical (i.e., ones the enemy needs to capture/contest later for narrative reasons). Optional player-built FARPs make main missions easier but are never required.
- Defensive missions should escalate in **mechanical shape**, not just stakes, across the campaign (e.g., early defense = hold one position with backup available; late defense = manage multiple simultaneous fronts with no reinforcement) so the finale reads as a structural shift, not a harder repeat of an earlier mission type.
- **Data flag recommendation:** forward bases should carry a `plot_critical: bool`. Losing a plot-critical base always triggers scripted narrative fallout; losing an optional one triggers only systemic fallout (reduced range, lost supply route, regional legitimacy hit).

### Side Missions
- Primarily relief work: establishing optional aid hubs/FARPs, supply runs to cut-off settlements, rescue tasking, and **infrastructure repair jobs** (hauling materials to a broken bridge or blocked pass so crews can fix it — see Section 5) — each easing main missions (extended range, faster resupply, reopened convoy routes, better intel) *and* banking regional legitimacy.
- Fully optional by design — supports both a "rush the plot" playstyle and a "prepare thoroughly" playstyle without gating either. The prepared player enters the war with both an operational network and a goodwill buffer; the rushing player enters it lean on both.

---

## 9. Command Layer (Finale-Focused Extension)

- Extends the existing waypoint/convoy system (introduced in the tutorial) rather than introducing a new mechanic — allied units gain **attack / defend / hold** stances in addition to movement waypoints.
- **Progression of the same system across the campaign:**
  - Tutorial: waypoints move an escorted relief convoy along a route (passive, single-purpose).
  - Side missions: waypoints define aid-hub/FARP convoy routes (player-authored infrastructure).
  - Main missions: introduces assigning allied units to hold a position while the player handles another front.
  - Finale: full command layer — assign units to districts with a stance, player becomes the mobile response asset reacting to whichever front is failing, directing from altitude.
- **Any damage caused by player-directed forces counts against the player's legitimacy standing**, identical to direct player action.
- **Open questions to resolve before implementation:**
  - Can orders be issued during the zoomed-out cruise camera state, or does combat-zoom lock out commanding? (The cruise-zoom tactical view is a natural candidate for doubling as the command interface.)
  - What does an "attack" order actually commit a unit to — push to a waypoint, clear a district, or counter a specific enemy group? (Hold/defend AI is comparatively simple; attack-and-advance AI through contested, dynamic terrain is a significantly larger implementation lift — scope accordingly.)
  - How is off-screen directed-unit behavior surfaced to the player so legitimacy consequences from their actions feel earned rather than arbitrary?

---

## 10. Faction Overview

| Faction | Role |
|---|---|
| Quad Joint Task Force | Player faction. Multinational asset/doctrine variety by member nation. Arrives with a humanitarian mandate; acquires quiet military teeth as the campaign turns. Its legitimacy is its permission to stay. |
| Nepali Government | Host nation, disaster-struck and dependent on both relief missions. Domestic support is a tracked variable responsive to player conduct — aid record first, restraint record later. |
| Chinese Relief Mission / PLA | Begins as a genuine, effective relief partner running its own rescues, aid deliveries, and infrastructure repairs — competing for the same regional legitimacy as the player. Revealed to be fortifying the towns and routes it rebuilt. Escalates in parallel with campaign stages from co-operator to primary antagonist. Information operations run throughout. |
| Local Armed Groups | Emergent third faction triggered by regional collateral damage and failed/abandoned relief. Not aligned with China — a consequence of player conduct and disaster desperation, not a scripted enemy. |

---

## 11. Technical Direction

**Target feel:** indie-scoped — stylized/simplified presentation, tight and readable individual systems, avoid AAA simulation depth or photorealistic fidelity even at large map scale. Scope discipline is treated as a design constraint on par with any gameplay system.

**Engine:** Unity, favored over Unreal specifically because the intended visual direction is stylized rather than photoreal — Unreal's core advantage (Nanite/Lumen-driven realistic terrain fidelity at range) matters less against an indie-esque target look, and Unity's lighter footprint and faster iteration fit better. Real-world heightmap import at this scale is achievable via terrain plugins (e.g., MapMagic 2, Gaia) layered on Unity's terrain system.

**Disaster-state authoring (v2.0):** earthquake/flood damage is pre-authored world state — destroyed bridge variants, landslide meshes over roads, flood-scour texturing along river corridors, damaged-settlement prefab sets — not runtime destruction or fluid simulation. Aftershock/secondary-flood moments, if used, are scripted mission events. This keeps the disaster premise inside indie scope: it is level dressing plus mission logic, not a simulation layer.

**Repairable-node authoring (v2.1):** repairable infrastructure is the same technique run in reverse — each node is a small set of discrete prefab states (damaged → under-repair → repaired) swapped as delivery thresholds are met, with engineer-crew dressing to sell the work happening between player visits. No construction animation systems, no incremental structural modeling. The systemic side (convoy-route availability, demand reduction) is data on the node, evaluated by the existing logistics/convoy layer rather than new machinery.

**Known large risks to flag going into production:**
- Real-terrain streaming/LOD at 150km scale is a nontrivial systems problem regardless of engine choice.
- The command-layer AI (particularly "attack" behavior) is likely the single largest scope risk in the mission-structure design — recommend prototyping hold/defend AI first and treating attack-and-advance AI as a stretch goal until proven feasible within the indie-scope constraint.
- Rescue interaction depth (winching, survivor AI, triage UI) is a new v2.0 surface — keep it mechanically thin (hover + hold + timer, stylized presentation) or it becomes a second game's worth of animation and edge cases.
- Stacking fuel/logistics + regional legitimacy + rescue interactions + multi-unit command + real-terrain streaming is, in aggregate, a lot of systems for an indie-scoped project. Recommend explicitly prioritizing fuel/logistics and the legitimacy consequence loop as the systems that must ship well; treat command-layer sophistication, armed-groups-as-independent-faction, and rescue-interaction depth as the first things to simplify if scope needs to be cut.

---

## 12. Open Questions (Consolidated)

- [ ] Local armed groups: passive modifier vs. full independent faction (recommend prototyping passive first)
- [ ] Escalation pacing: player-driven vs. scripted (the Stage 3 fortification reveal itself likely scripted; everything downstream player-influenced)
- [ ] Legitimacy accounting: how relief actions (rescues, aid delivered, hubs built) numerically bank legitimacy vs. how collateral spends it — one regional scalar or separate goodwill/hostility tracks?
- [x] ~~The aid race: wall-clock simulated vs. scripted~~ — **decided (v2.3): progress-clocked.** China's queue advances on player repair completions (primary) and mission/stage beats (floor), never real time. Remaining tuning open: exact tick weights, whether uncontested nodes tick faster, and any rubber-banding if the player is far ahead/behind
- [ ] The repair race: does non-repair *relief* progress (rescue arcs, aid-hub establishment) also tick China's queue at low weight, or strictly repairs + plot beats? (Strictly repairs is cleaner; broader ticks make China feel less player-reactive)
- [ ] The repair race: can the player interfere with in-progress Chinese repairs (or vice versa) in Stages 3–4, and at what legitimacy cost? (Striking disaster-relief works is close to the maximum possible legitimacy self-harm — that may be exactly the point, or a door better left closed)
- [ ] Joint-operations content in Stages 1–2: playable cooperative missions with Chinese aircraft, or ambient/narrative presence only? (Playable buys the betrayal more weight; ambient is far cheaper.)
- [ ] Rescue mechanics depth: winch/hover interaction model, survivor representation, and how thin it can stay while still feeling like rescue
- [ ] Infrastructure repair: delivery interaction (sling-load precision drop vs. land-and-unload vs. both by cargo type) — sling-load is the more SnowRunner-flavored skill expression but needs a physics rope; scope check required
- [ ] Infrastructure repair: which node types beyond bridges/roads (helipads, power/comms relays?) and how many repairable nodes the map can support before authoring cost bites
- [ ] Infrastructure repair: do enemy forces actively exploit player-repaired routes in Stages 4–5 (real AI pathing consequence) or is that reserved for scripted narrative beats?
- [ ] FARP/aid-hub density and placement logic across the four biomes, accounting for vertical/altitude difficulty and disaster damage distribution, not just even spread
- [ ] Fuel-burn formula (base rate + altitude modifier + load modifier + hover modifier + combat-state modifier)
- [ ] Domestic Nepali political factions (pro-Quad / neutral / pro-China-leaning) — active mechanic or narrative flavor only?
- [ ] Loadout system: numeric interaction between auxiliary tanks, relief cargo, ordnance, and altitude performance
- [ ] Full mission-type matrix per campaign stage (search/rescue, haulage, recon, skirmish, assault, defense — with relief tasking persisting into combat stages)
- [ ] Finale scope: the city itself vs. terrain immediately defending its approach
- [ ] Disaster dynamism: fully static damage state vs. scripted aftershock/secondary-GLOF mission events
- [ ] Combat-zoom override rule for the camera system (locked threat / active fire forces zoom-in regardless of speed/heading?)
- [ ] Command layer: order-issuing availability during combat-zoom vs. cruise-zoom
- [ ] Command layer: precise definition of "attack" order behavior and its AI implementation cost

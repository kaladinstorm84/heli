# SPEC.md — Desert Strike Spiritual Successor
### Open-World Helicopter Combat / Logistics Sim
**Status:** Design spec v1.0 — intended as a development/prompting reference document

---

## 0. One-Line Pitch

A modern, open-world spiritual successor to *Desert Strike* — isometric helicopter combat and logistics across a real-world-mapped 150km Himalayan border region, where fuel scarcity, forward-base logistics, and collateral damage all feed into a political legitimacy system that determines whether the player's covert-but-invited intervention holds or collapses into open war.

**Target feel: indie-scoped.** Large map and layered systems, but stylized/simplified presentation and tight, readable individual systems — not AAA simulation depth or photorealistic fidelity. Scope discipline is a first-class design constraint, not an afterthought.

---

## 1. Premise & Setting

China is applying pressure on Nepal's eastern border. Nepal has formally requested support from the Quad (US, India, Japan, Australia) to preserve its sovereignty and prevent alignment with China. The player operates as part of a Quad joint task force embedded in the region.

**Core strategic tension:** the goal is not conquest — it's keeping Nepal aligned and stable *without* Quad presence reading as an occupying force. Heavy-handed operations and high collateral damage risk feeding a narrative (amplified by Chinese information operations) that the Quad is itself the threat to Nepali sovereignty. **Military effectiveness and political legitimacy actively pull against each other.** Winning battles carelessly can mean losing the campaign.

Real-world anchor points used for plausibility, not literal depiction: the Doklam/Zuluk tri-junction area (genuine site of past China-India-Bhutan border tension) and the Siliguri Corridor ("Chicken's Neck" — the narrow strategic link between mainland India and its northeast) as the finale's implied stakes.

---

## 2. Setting Geography — Real-World Data

**Region:** Sikkim, eastern Nepal (Taplejung/Ilam districts), and the Darjeeling/Siliguri foothills of West Bengal. Chosen because this is one of the few places on Earth with a documented contiguity of biomes — subtropical forest to alpine/cold desert — within roughly 100km, driven by elevation rather than latitude.

**Approximate 150km x 150km bounding box, anchored by:**
- **North:** Yumthang (high alpine, approach to Tibetan plateau)
- **Northwest:** Kangchenjunga (8,586m, extreme high-altitude wall, sits on the India-Nepal border)
- **West:** Taplejung / Phungling and Ilam, Nepal (the sovereign territory being defended)
- **East:** Zuluk (near Nathu La / Chumbi Valley, closest point to real-world China border tension)
- **South:** Darjeeling → Kurseong → Siliguri corridor approach (lowest elevation, most populated, highest political exposure)
- **Center:** Gangtok (temperate mid-elevation hub)

**Elevation gradient (north/high to south/low) drives biome placement:**
1. High-altitude cold desert / alpine (Yumthang, Kangchenjunga approaches)
2. Subalpine conifer / alpine meadow
3. Temperate broadleaf forest (Gangtok band)
4. Subtropical forest / foothill (Namchi, Darjeeling, Kurseong)

Biome bands should follow real elevation contours and valley/ridge structure (Teesta and Rangit river valleys as natural travel corridors and biome dividers) — not a grid quartering.

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
- **Known asymmetry:** this only works cleanly on the north/east (genuinely rising terrain). The southern edge (Terai/Siliguri approach) is low and flat and won't cap altitude naturally — use a narrative/systemic boundary device instead (restricted/monitored airspace tied to the deniability theme, or simply scoping the mission area to end there).

---

## 3. Core Design Pillars

1. **Scarcity is systemic, not punitive.** Fuel and ordnance are resources to plan around and invest in solving, not a countdown that punishes exploration.
2. **The map is the plot's geography.** Biomes are real operational theaters with real constraints, not reskinned terrain.
3. **Restraint is a real cost, not a moral rail.** The "quiet" solution is harder, slower, or costlier than the "loud" one — never simply the correct choice with no trade-off.
4. **Early logistics pays off late.** Infrastructure built as "boring" early-game investment becomes late-game capability.
5. **Consequences are local, not global.** Player actions affect the specific region they happened in, not an abstract global meter.
6. **Scope discipline over system count.** Fuel/logistics tension and the legitimacy consequence loop are the soul of the game. Other systems (multi-unit command, AI complexity) should stay implementation-simple even where they're player-facing-rich, to protect the indie-scoped target feel.

---

## 4. Camera System

- **Fixed isometric perspective**, always — no camera mode switching between traversal and combat.
- **Automatic cruise zoom-out:** triggers when sustained straight-line flight (heading variance within a small tolerance) is held at ≥75% of max speed for over 2 seconds.
- **Implementation model:** target-value + continuous lerp, not discrete triggered animations. Every frame, compute a desired zoom level from current state (speed/heading/combat status); lerp the camera's actual zoom toward that target continuously, so interruption mid-transition simply changes the target and the lerp reverses smoothly from its current position — never resets/restarts.
- **Asymmetric easing:** zoom-out is slow/gentle (~1.5–2s, ease-out) since there's no urgency; zoom-in is fast (~0.4–0.6s, ease-in) since it typically reacts to a threat and shouldn't feel like it's lagging behind danger.
- **Two LOD tiers required for art direction:** "cruise silhouette" (must read as a landmark at far zoom — design biome art around recognizable silhouettes: a monastery on a ridge, a bridge over a gorge) and "combat detail" (must support cover, sightlines, tactical positioning up close).
- **Open question:** does a locked-on threat or active weapons fire force combat zoom regardless of speed/heading? (Recommend yes.)

---

## 5. Fuel & Logistics System

- **Burn rate is effort-based:** altitude, combat load, hover time, and speed all affect consumption — not pure distance. Altitude specifically reduces effective lift/payload in high-Himalaya missions, forcing loadout trade-offs unique to that biome.
- **FARP (Forward Arming and Refueling Point) network is fixed and player-learnable**, not randomly scattered — players build a mental map of safe legs between biomes, mirroring a road network.
- **FARPs are player-built infrastructure**, established during Base Setup / side missions, and extend operational range for Main Missions. This is the direct payoff loop for logistics-focused play.
- **Auxiliary tanks are a loadout choice** trading cargo/ordnance capacity for range — scarcity becomes a build decision, not just a constraint.
- **Running dry is recoverable, not a fail state:** forced auto-rotation landing → on-foot or awaiting rescue, rather than instant mission failure ("stuck, not dead," after SnowRunner).

---

## 6. Legitimacy & Collateral System

- **Tracked regionally** (valley/settlement level), not globally. Damage in one area does not punish the player elsewhere, but does change that region's future patrol density, hostility, and mission availability.
- **High regional collateral raises local insurgency activity** — a third faction, distinct from Chinese forces and the Nepali government, that the player did not choose to fight.
- **Insurgency primarily degrades player logistics**, not just adds combat volume: sabotage of the FARP network, harassed supply routes, drying up local intel — ties consequences directly back into the fuel/logistics system rather than just spawning more enemies.
- **China benefits passively.** Chinese-aligned information operations can amplify a bad Quad engagement into a strategic loss without China needing to act directly.
- **Design intent:** the effective military solution (heavier ordnance, fast resolution) should sometimes be in genuine tension with collateral cost — restraint must be a real trade-off, not a hidden "correct" path with no downside.
- **Command delegation carries the same weight as direct action:** damage caused by player-directed allied forces (see Section 8, Command Layer) counts against the player's legitimacy standing exactly as if the player caused it directly. This requires enough player visibility into off-screen directed-unit behavior that consequences feel earned, not arbitrary.
- **Open question:** does insurgency escalate into a full independent faction with its own AI and territory, or remain a passive modifier (patrol density, supply friction, mission availability)? Recommend prototyping as a passive modifier first.

---

## 7. Campaign Structure — Five-Stage Escalation Ladder

Each stage changes what's *mechanically available*, not just what's narratively happening.

### Stage 1 — Recon
- Light loadouts, minimal weapons; fuel/range is the primary constraint.
- Establishes the map for the player while doubling as base-network scouting.
- Failure state is **detection**, not death.

### Stage 2 — Base Setup (Transport / Haulage)
- Logistics missions: cargo weight cuts into range.
- Player physically builds the FARP network relied on later.
- Early "chore" missions become late-game infrastructure.

### Stage 3 — Minor Skirmishes
- First combat; still deniable (unmarked forces, plausible-accident framing).
- Introduces loud-vs-quiet tension: a visibly decisive tactical win can still be a strategic cost.

### Stage 4 — Hostilities
- Legitimacy/neutrality framing becomes a live, tracked variable.
- Nepali domestic political support responds to player conduct in Stages 1–3.
- Loadouts open up; every visible engagement runs a background legitimacy cost.

### Stage 5 — Full-Blown War / Finale
- Deniability collapses entirely; the campaign's original constraint has failed regardless of battlefield outcome.
- **Escalation is expressed through SCALE, not new mechanics.** Base defense (bounded perimeter, single threat vector, likely nearby resupply) becomes city-wide defense: multiple simultaneous fronts, constant civilian presence, no single "hold this line" objective — a resource-allocation/triage problem rather than a reactive one.
- **Finale objective:** repel an occupying force from a city and then defend the whole city, with collateral damage stakes at their highest point in the campaign, exactly when the player has the most firepower available.
- Thematic note available: this stage can represent the campaign's stated goal (avoid overt war) *failing* even while battles are being won — a tragic-victory framing rather than a clean one, if desired.
- **Open question:** exact scope of the finale battlespace — city itself vs. the terrain immediately defending its approach (softer to build, still carries the stakes without turning a real populated area into a full warzone).

**Open question (campaign-wide):** is escalation pace player-driven (restraint/stealth performance controls how fast the ladder climbs) or scripted? Player-driven is more implementation work but makes "your conduct determines whether this becomes a war" mechanically real rather than narrated. Recommended if feasible.

---

## 8. Mission Structure

### Tutorial Missions
Each step introduces exactly one new system before combining them:
1. **Scout** for an initial base location (navigation/recon only).
2. **Escort** allied forces to a location:
   - Set waypoints for forces to follow.
   - Mild combat clearing "natural threats" (light weapons).
   - Heavier weapons for "land clearance" (quietly foreshadows the ordnance-vs-collateral tension before the legitimacy system is mechanically active — clearing terrain should feel different from clearing a settlement, even here).
3. **Identify and establish the first forward base:**
   - Carry initial cargo to the location.
   - Set up a convoy route to the forward base.

*Sequencing note:* the fuel-pressure moment should land just before the forward-base tutorial step, so the base-building payoff is felt, not just explained.

### Main Missions
- Mostly plot-driven; heavy focus on action/combat.
- Includes many defensive missions — primarily repelling/driving back enemy advances.
- **Completable with minimal forward infrastructure** — specifically the FARPs that are plot-critical (i.e., ones the enemy needs to capture/contest later for narrative reasons). Optional player-built FARPs make main missions easier but are never required.
- Defensive missions should escalate in **mechanical shape**, not just stakes, across the campaign (e.g., early defense = hold one position with backup available; late defense = manage multiple simultaneous fronts with no reinforcement) so the finale reads as a structural shift, not a harder repeat of an earlier mission type.
- **Data flag recommendation:** forward bases should carry a `plot_critical: bool`. Losing a plot-critical base always triggers scripted narrative fallout; losing an optional one triggers only systemic fallout (reduced range, lost supply route).

### Side Missions
- Primarily about establishing optional forward locations that ease main missions (extended range, faster resupply, intel).
- Fully optional by design — supports both a "rush the plot" playstyle and a "prepare thoroughly" playstyle without gating either.

---

## 9. Command Layer (Finale-Focused Extension)

- Extends the existing waypoint/convoy system (introduced in the tutorial) rather than introducing a new mechanic — allied units gain **attack / defend / hold** stances in addition to movement waypoints.
- **Progression of the same system across the campaign:**
  - Tutorial: waypoints move escorted forces along a route (passive, single-purpose).
  - Side missions: waypoints define FARP convoy routes (player-authored infrastructure).
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
| Quad Joint Task Force | Player faction. Multinational asset/doctrine variety by member nation. Invited-but-deniable presence. |
| Nepali Government | Host nation and active stakeholder. Domestic support is a tracked variable responsive to player conduct. |
| Chinese Military / Paramilitary | Primary antagonist force; escalates in parallel with campaign stages. |
| Local Insurgency | Emergent third faction triggered by regional collateral damage. Not aligned with China — a consequence of player conduct, not a scripted enemy. |

---

## 11. Technical Direction

**Target feel:** indie-scoped — stylized/simplified presentation, tight and readable individual systems, avoid AAA simulation depth or photorealistic fidelity even at large map scale. Scope discipline is treated as a design constraint on par with any gameplay system.

**Engine:** Unity, favored over Unreal specifically because the intended visual direction is stylized rather than photoreal — Unreal's core advantage (Nanite/Lumen-driven realistic terrain fidelity at range) matters less against an indie-esque target look, and Unity's lighter footprint and faster iteration fit better. Real-world heightmap import at this scale is achievable via terrain plugins (e.g., MapMagic 2, Gaia) layered on Unity's terrain system.

**Known large risks to flag going into production:**
- Real-terrain streaming/LOD at 150km scale is a nontrivial systems problem regardless of engine choice.
- The command-layer AI (particularly "attack" behavior) is likely the single largest scope risk in the mission-structure design — recommend prototyping hold/defend AI first and treating attack-and-advance AI as a stretch goal until proven feasible within the indie-scope constraint.
- Stacking fuel/logistics + regional legitimacy/insurgency + multi-unit command + real-terrain streaming is, in aggregate, a lot of systems for an indie-scoped project. Recommend explicitly prioritizing fuel/logistics and the legitimacy consequence loop as the systems that must ship well; treat command-layer sophistication and insurgency-as-independent-faction as the first things to simplify if scope needs to be cut.

---

## 12. Open Questions (Consolidated)

- [ ] Insurgency: passive modifier vs. full independent faction (recommend prototyping passive first)
- [ ] Escalation pacing: player-driven vs. scripted
- [ ] FARP density and placement logic across the four biomes, accounting for vertical/altitude difficulty, not just even spread
- [ ] Fuel-burn formula (base rate + altitude modifier + load modifier + combat-state modifier)
- [ ] Domestic Nepali political factions (pro-Quad / neutral / pro-China-leaning) — active mechanic or narrative flavor only?
- [ ] Loadout system: numeric interaction between auxiliary tanks, ordnance, and altitude performance
- [ ] Full mission-type matrix per campaign stage (recon, haulage, skirmish, assault, defense)
- [ ] Finale scope: the city itself vs. terrain immediately defending its approach
- [ ] Combat-zoom override rule for the camera system (locked threat / active fire forces zoom-in regardless of speed/heading?)
- [ ] Command layer: order-issuing availability during combat-zoom vs. cruise-zoom
- [ ] Command layer: precise definition of "attack" order behavior and its AI implementation cost

# Progress Log

Running log of changes to allow progress tracking between chat/dev sessions. Newest entries first.

## 2026-08-16 — Design spec captured in repo

- Added `SPEC.md` (Design spec v1.0) — authoritative development/prompting reference for the Desert Strike spiritual successor: premise (Quad intervention on Nepal's eastern border), real-world Sikkim/eastern-Nepal geography and DEM terrain pipeline, core design pillars, isometric camera system, fuel/logistics (FARP) system, regional legitimacy & collateral system, five-stage escalation campaign, mission structure, command layer, faction overview, technical direction (Unity), and consolidated open questions.
- Rewrote `README.md` from placeholder to a proper project overview linking the spec and summarizing core systems, technical direction, and repository status.
- Added this `progress.md` file.
- No Unity project or code exists yet; no build to run (docs-only change). Committed on branch `cursor/add-design-spec-docs-e8b9` after user approval to commit.

## Current State

- **Phase:** pre-production (design docs only).
- **Repo contents:** `SPEC.md`, `README.md`, `progress.md`, Unity `.gitignore`.
- **Next candidate steps (not started):**
  - Resolve open questions in SPEC.md §12 (insurgency scope, escalation pacing, fuel-burn formula, finale scope, camera/command interaction rules).
  - Create the Unity project skeleton.
  - Prototype the terrain pipeline: pull the 150km bounding-box DEM (Copernicus GLO-30 via OpenTopography), test vertical compression, import as 16-bit heightmap.
  - Prototype the camera cruise-zoom lerp model (cheap, isolated, validates a core feel decision early).

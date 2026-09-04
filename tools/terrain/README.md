# Terrain Tools

## download_dem.py

Downloads Copernicus GLO-30 (30m) elevation data for the project area from the
public AWS Open Data mirror — no account or API key required. Merges/clips the
1° source tiles to a bounding box and can export a Unity-ready heightmap.

### Setup

```bash
pip install -r tools/terrain/requirements.txt
```

### Usage

```bash
# ~12km prototype slice (Teesta bend / Chungthang) + 1025x1025 Unity heightmap
python tools/terrain/download_dem.py --preset prototype --heightmap 1025

# Full 150km playable bounding box (9 tiles, ~500 MB of source data)
python tools/terrain/download_dem.py --preset playable --heightmap 4097

# Playable box + backdrop margin for non-collidable distant terrain
python tools/terrain/download_dem.py --preset extended

# Custom area / dry run
python tools/terrain/download_dem.py --bbox 88.5 27.5 88.8 27.7
python tools/terrain/download_dem.py --preset playable --list-tiles
```

Presets match SPEC.md §2: `playable` is the Siliguri–Yumthang / Taplejung–Zuluk
box, `extended` adds margin for the converging-ceiling backdrop, and
`prototype` is the hex-grid/silhouette test slice around the Teesta bend.

### Outputs (default `data/dem/`, gitignored)

- `tiles/` — cached 1° source tiles (reused across runs and presets)
- `dem_<preset>.tif` — merged/clipped GeoTIFF, WGS84, elevation in meters
- `heightmap_<preset>.raw` — 16-bit little-endian RAW, reprojected to UTM 45N
  (square meters), normalized to the area's min/max elevation
- `heightmap_<preset>.json` — sidecar with extent, elevation range, and Unity
  import settings

### Unity import notes

Terrain → Import Raw: 16-bit, little-endian, resolution as exported, enable
**Flip Vertically** (rows are written north-to-south). Set terrain width/length
from `extent_m` in the sidecar. The sidecar's `unity_terrain_height_uncompressed_m`
is the real elevation span — per SPEC.md §2, apply vertical compression by
setting terrain height to a fraction of it (prototype with ~0.4–0.6 first).

If the hex-grid terrain route (Catlike Coding-style) is adopted, use
`dem_<preset>.tif` as the sampling source for per-cell elevations instead of
the RAW export.

### Data credit (required in game credits)

Produced using Copernicus WorldDEM-30 © DLR e.V. 2010–2014 and © Airbus
Defence and Space GmbH 2014–2018, provided under COPERNICUS by the European
Union and ESA.

#!/usr/bin/env python3
"""Download Copernicus GLO-30 DEM data for the project area.

Pulls 1-degree tiles from the public AWS Open Data mirror (no login/API key),
caches them locally, merges and clips to a bounding box, and optionally
exports a Unity-ready 16-bit RAW heightmap reprojected to square meters.

Presets (see SPEC.md section 2):
  prototype  ~12km slice around the Teesta bend / Chungthang (hex-grid test area)
  playable   the full ~150km x 150km playable bounding box
  extended   playable box + margin for distant non-collidable backdrop terrain

Examples:
  python download_dem.py --preset prototype --heightmap 1025
  python download_dem.py --preset playable
  python download_dem.py --bbox 88.5 27.5 88.8 27.7 --heightmap 2049
  python download_dem.py --preset extended --list-tiles

Data credit (required in game credits): produced using Copernicus WorldDEM-30
(c) DLR e.V. 2010-2014 and (c) Airbus Defence and Space GmbH 2014-2018,
provided under COPERNICUS by the European Union and ESA.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

try:
    import numpy as np
    import rasterio
    import requests
    from rasterio.merge import merge as rio_merge
    from rasterio.transform import from_bounds
    from rasterio.warp import Resampling, reproject, transform_bounds
except ImportError as exc:
    sys.exit(
        f"Missing dependency: {exc.name}. Install with:\n"
        "  pip install -r tools/terrain/requirements.txt"
    )

TILE_URL = "https://copernicus-dem-30m.s3.amazonaws.com/{name}/{name}.tif"

# (min_lon, min_lat, max_lon, max_lat) in WGS84 degrees
PRESETS = {
    # Teesta bend / Chungthang slice: gorge + ridge in a small area, and the
    # site of the 2023 South Lhonak GLOF dam collapse referenced in the spec.
    "prototype": (88.58, 27.55, 88.70, 27.66),
    # Full playable box: Siliguri foothills (S) to Yumthang (N),
    # Taplejung/Ilam (W) to Zuluk (E).
    "playable": (87.60, 26.70, 89.10, 28.10),
    # Playable + ~0.4 deg margin so peaks beyond the converging-ceiling
    # boundary can render as non-collidable backdrop.
    "extended": (87.20, 26.30, 89.50, 28.50),
}

# UTM zone 45N covers the whole box; used for square-meter heightmap export.
UTM_EPSG = 32645


def tile_name(lat: int, lon: int) -> str:
    ns = "N" if lat >= 0 else "S"
    ew = "E" if lon >= 0 else "W"
    return f"Copernicus_DSM_COG_10_{ns}{abs(lat):02d}_00_{ew}{abs(lon):03d}_00_DEM"


def tiles_for_bbox(bbox: tuple[float, float, float, float]) -> list[str]:
    min_lon, min_lat, max_lon, max_lat = bbox
    names = []
    for lat in range(math.floor(min_lat), math.floor(max_lat) + 1):
        for lon in range(math.floor(min_lon), math.floor(max_lon) + 1):
            names.append(tile_name(lat, lon))
    return names


def download_tile(name: str, cache_dir: Path) -> Path | None:
    """Download one tile into the cache; returns None for missing tiles."""
    dest = cache_dir / f"{name}.tif"
    if dest.exists():
        print(f"  cached   {name}")
        return dest
    url = TILE_URL.format(name=name)
    tmp = dest.with_suffix(".tif.part")
    print(f"  fetching {name} ...", flush=True)
    with requests.get(url, stream=True, timeout=120) as resp:
        if resp.status_code == 404:
            # Tiles that are entirely ocean don't exist; not expected inland.
            print(f"  MISSING  {name} (404, skipping)")
            return None
        resp.raise_for_status()
        done = 0
        with open(tmp, "wb") as fh:
            for chunk in resp.iter_content(chunk_size=1 << 20):
                fh.write(chunk)
                done += len(chunk)
        print(f"           {done / 1e6:.1f} MB")
    tmp.rename(dest)
    return dest


def merge_and_clip(tile_paths: list[Path], bbox, out_tif: Path) -> None:
    sources = [rasterio.open(p) for p in tile_paths]
    try:
        mosaic, transform = rio_merge(sources, bounds=bbox)
        profile = sources[0].profile.copy()
        profile.update(
            driver="GTiff",
            height=mosaic.shape[1],
            width=mosaic.shape[2],
            transform=transform,
            compress="deflate",
            tiled=True,
        )
        out_tif.parent.mkdir(parents=True, exist_ok=True)
        with rasterio.open(out_tif, "w", **profile) as dst:
            dst.write(mosaic)
    finally:
        for src in sources:
            src.close()


def export_heightmap(src_tif: Path, out_base: Path, size: int) -> None:
    """Reproject to UTM (square meters), resample to size x size, and write a
    16-bit little-endian RAW heightmap plus a JSON sidecar for Unity import."""
    with rasterio.open(src_tif) as src:
        dst_bounds = transform_bounds(src.crs, f"EPSG:{UTM_EPSG}", *src.bounds)
        dst_transform = from_bounds(*dst_bounds, size, size)
        data = np.full((size, size), np.nan, dtype=np.float32)
        reproject(
            source=rasterio.band(src, 1),
            destination=data,
            dst_transform=dst_transform,
            dst_crs=f"EPSG:{UTM_EPSG}",
            dst_nodata=np.nan,
            resampling=Resampling.bilinear,
        )
        src_bounds = src.bounds

    valid = np.isfinite(data)
    if not valid.any():
        sys.exit("Heightmap export failed: no valid elevation data in window.")
    elev_min = float(np.nanmin(data))
    elev_max = float(np.nanmax(data))
    data = np.where(valid, data, elev_min)

    span = max(elev_max - elev_min, 1.0)
    norm = ((data - elev_min) / span * 65535.0).round().astype("<u2")

    raw_path = out_base.with_suffix(".raw")
    norm.tofile(raw_path)

    width_m = dst_bounds[2] - dst_bounds[0]
    height_m = dst_bounds[3] - dst_bounds[1]
    sidecar = {
        "source": src_tif.name,
        "bbox_wgs84": list(src_bounds),
        "crs": f"EPSG:{UTM_EPSG}",
        "extent_m": {"width": round(width_m, 1), "height": round(height_m, 1)},
        "elevation_m": {"min": round(elev_min, 1), "max": round(elev_max, 1)},
        "raw_format": {
            "resolution": size,
            "depth": "16-bit",
            "byte_order": "little-endian",
            "row_order": "north-to-south (enable 'Flip Vertically' in Unity)",
        },
        "unity_terrain_height_uncompressed_m": round(elev_max - elev_min, 1),
        "note": "Apply the spec's vertical compression by scaling terrain "
        "height below the uncompressed value while keeping X/Z extent.",
    }
    json_path = out_base.with_suffix(".json")
    json_path.write_text(json.dumps(sidecar, indent=2) + "\n")

    print(f"Heightmap : {raw_path} ({size}x{size}, 16-bit LE)")
    print(f"Sidecar   : {json_path}")
    print(f"Elevation : {elev_min:.0f} m to {elev_max:.0f} m over "
          f"{width_m / 1000:.1f} x {height_m / 1000:.1f} km")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    area = parser.add_mutually_exclusive_group(required=True)
    area.add_argument("--preset", choices=sorted(PRESETS))
    area.add_argument(
        "--bbox", nargs=4, type=float,
        metavar=("MIN_LON", "MIN_LAT", "MAX_LON", "MAX_LAT"),
        help="custom bounding box in WGS84 degrees",
    )
    parser.add_argument(
        "--out-dir", type=Path, default=Path("data/dem"),
        help="output directory (default: data/dem)",
    )
    parser.add_argument(
        "--heightmap", type=int, metavar="SIZE",
        help="also export a SIZE x SIZE 16-bit RAW heightmap for Unity "
        "(use 2^n+1, e.g. 1025, 2049, 4097)",
    )
    parser.add_argument(
        "--list-tiles", action="store_true",
        help="list required tiles and exit without downloading",
    )
    args = parser.parse_args()

    bbox = PRESETS[args.preset] if args.preset else tuple(args.bbox)
    label = args.preset or "custom"
    if not (bbox[0] < bbox[2] and bbox[1] < bbox[3]):
        sys.exit("Invalid bbox: expected MIN_LON MIN_LAT MAX_LON MAX_LAT.")
    if args.heightmap is not None:
        n = args.heightmap - 1
        if args.heightmap < 33 or (n & (n - 1)) != 0:
            sys.exit("--heightmap SIZE must be 2^n+1 (e.g. 1025, 2049, 4097).")

    tiles = tiles_for_bbox(bbox)
    print(f"Area '{label}': lon {bbox[0]}..{bbox[2]}, lat {bbox[1]}..{bbox[3]}")
    print(f"Requires {len(tiles)} tile(s):")
    for name in tiles:
        print(f"  {name}")
    if args.list_tiles:
        return

    cache_dir = args.out_dir / "tiles"
    cache_dir.mkdir(parents=True, exist_ok=True)
    print("Downloading (public AWS mirror, no login required):")
    tile_paths = [p for name in tiles if (p := download_tile(name, cache_dir))]
    if not tile_paths:
        sys.exit("No tiles could be downloaded for this area.")

    out_tif = args.out_dir / f"dem_{label}.tif"
    merge_and_clip(tile_paths, bbox, out_tif)
    with rasterio.open(out_tif) as ds:
        print(f"DEM       : {out_tif} ({ds.width}x{ds.height} px, "
              f"~{abs(ds.transform.a) * 111320:.0f} m/px at equator scale)")

    if args.heightmap:
        export_heightmap(out_tif, args.out_dir / f"heightmap_{label}", args.heightmap)


if __name__ == "__main__":
    main()

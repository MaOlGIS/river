# River Network Python Preprocessing Pipeline

This project prepares segmented vector river-network data for downstream
cartographic visualization in GIS software. The main workflow is a clean Python
preprocessing pipeline built around GeoPandas, Pandas, Shapely and PyProj.

The repository is inspired by the Japan MLIT W05 river dataset, but the core
code separates reusable network-processing logic from W05-specific field names
and regional assumptions.

## What This Project Does

- discovers vector river datasets grouped by folder,
- validates required stream-network attributes,
- checks and harmonizes CRS metadata,
- filters river segments with known flow direction,
- preserves original line geometry,
- assigns optional region metadata,
- computes length and source-distance metrics,
- exports a GeoPackage layer ready for GIS symbolization.

The prepared output can then be styled, laid out and exported in ArcGIS Pro,
QGIS or another GIS package. Software-specific cartographic automation is kept
outside the main preprocessing workflow.

## Repository Layout

```text
river_pipeline/
  config.py        # Dataset profiles and field mappings
  discovery.py     # Filesystem and vector dataset discovery helpers
  network.py       # Pure Python directed-network metrics

notebooks/
  river_network_processing_plan.ipynb

examples/
  # reserved for dataset-specific examples
```

## Data

Raw data is intentionally not tracked in Git. The local `data/` folder is close
to 1 GB and contains files over GitHub's normal 100 MB limit.

To run the notebook with the Japan W05 example, place the extracted W05 source
folders under:

```text
data/
  W05-xx_xx_GML/
    W05-xx_xx-g_Stream.shp
    W05-xx_xx-g_Stream.dbf
    W05-xx_xx-g_Stream.shx
    W05-xx_xx-g_RiverNode.shp
    ...
```

The W05 profile expects these execution-critical fields:

- `W05_006`: known-flow flag,
- `W05_009`: upstream/start node ID,
- `W05_010`: downstream/end node ID.

## Setup

Create an environment with the geospatial Python dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Then open and run:

```text
notebooks/river_network_processing_plan.ipynb
```

The notebook writes prepared GeoPackage outputs and a CSV QA report under
`outputs/python_preprocessing/`.

## Main Workflow

The main workflow is the notebook and `river_pipeline` package. It does not
depend on ArcPy or any other desktop-GIS automation API.

## Limitations

- The bundled W05 profile is dataset-specific and does not make all river data
  automatically compatible.
- CRS fallback values must be checked against source documentation and spatial
  extents before serious use.
- Length metrics depend on a suitable projected CRS.
- Source-distance metrics assume a directed acyclic network. Cyclic segments
  are intentionally flagged with undefined distances.

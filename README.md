# Python preprocessing pipeline pro říční síť

Tento projekt připravuje segmentovanou vektorovou říční síť pro následnou
kartografickou vizualizaci v GIS software. Hlavní workflow je čistý Python
preprocessing pipeline postavený na knihovnách GeoPandas, Pandas, Shapely a
PyProj.

Projekt je inspirovaný datasetem Japan MLIT W05, ale jádro kódu odděluje
znovupoužitelnou logiku síťového zpracování od W05-specific názvů polí a
regionálních předpokladů.

## Co Projekt Dělá

- vyhledá vektorové říční datasety seskupené ve složkách,
- zkontroluje povinné atributy říční sítě,
- ověří a harmonizuje CRS metadata,
- vyfiltruje segmenty se známým směrem toku,
- zachová původní liniovou geometrii,
- volitelně doplní regionální metadata,
- spočítá délkové a source-distance metriky,
- vyexportuje GeoPackage vrstvu připravenou pro GIS symbolizaci.

Připravený výstup lze následně stylovat, vložit do layoutu a exportovat v
ArcGIS Pro, QGIS nebo jiném GIS nástroji. Software-specific kartografická
automatizace není součástí hlavního preprocessing workflow.

## Struktura Repozitáře

```text
river_pipeline/
  config.py        # Dataset profily a field mapping
  discovery.py     # Vyhledávání složek a vektorových datasetů
  network.py       # Čistý Python výpočet directed-network metrik

notebooks/
  river_network_processing_plan.ipynb

examples/
  # místo pro dataset-specific příklady
```

## Data

Raw data nejsou verzovaná v Gitu. Lokální složka `data/` má téměř 1 GB a
obsahuje soubory přes běžný GitHub limit 100 MB.

Pro spuštění notebooku nad příkladem Japan W05 vlož rozbalené zdrojové W05
složky sem:

```text
data/
  W05-xx_xx_GML/
    W05-xx_xx-g_Stream.shp
    W05-xx_xx-g_Stream.dbf
    W05-xx_xx-g_Stream.shx
    W05-xx_xx-g_RiverNode.shp
    ...
```

W05 profil očekává tato execution-critical pole:

- `W05_006`: flag známého směru toku,
- `W05_009`: upstream/start node ID,
- `W05_010`: downstream/end node ID.

## Instalace

Vytvoř prostředí s geospatial Python závislostmi:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Potom otevři a spusť:

```text
notebooks/river_network_processing_plan.ipynb
```

Notebook zapisuje připravené GeoPackage výstupy a CSV QA report do:

```text
outputs/python_preprocessing/
```

## Hlavní Workflow

Hlavní workflow tvoří notebook a package `river_pipeline`. Nezávisí na ArcPy ani
na žádném jiném desktop-GIS automation API.

Výstupem preprocessing pipeline je dataset připravený pro:

- aplikaci symbologie,
- tvorbu layoutů,
- export map v libovolném GIS software.

## Limitace

- Přiložený W05 profil je dataset-specific a neznamená automatickou kompatibilitu
  se všemi říčními daty.
- Fallback CRS je kvalifikovaný předpoklad a musí se ověřit proti zdrojové
  dokumentaci a spatial extentu.
- Délkové metriky závisí na vhodném projektovaném CRS.
- Source-distance metrika předpokládá orientovanou acyklickou síť. Segmenty v
  cyklech jsou označené neurčitelnou vzdáleností.

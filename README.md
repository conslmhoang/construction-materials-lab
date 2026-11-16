# Construction Materials Lab — Mix Design & Strength Prediction

Live site: https://conslmhoang.github.io/construction-materials-lab/

A browser-only tool for fiber-reinforced cementitious and geopolymer composites (ECC/SHCC, UHPC, UHP-ECC):

1. **Mix design**: proportions → kg per m³ and per batch, with cost, embodied energy and CO₂ (21 materials, the same ones the model uses).
2. **Strength prediction**: compressive strength and tensile strain capacity from the mix,
   curing method/temperature/humidity/duration and test age. It includes an 80% range, a strength-vs-age table,
   a "what changes the prediction" table and optional calibration with your own lab results.
3. **Logs**: every mix design, batch and prediction is logged and can be downloaded as Excel/CSV.

| Page | What it shows |
|---|---|
| `index.html` | Calculator + prediction |
| `benchmark.html` | 10 ML models compared (10-fold cross-validation, random split) |
| `data.html` | The 285 source papers and how the data were cleaned |

## Training data: `04 Dataset_web.xlsx`

One sheet, one row per mix and test age, and only the columns the web has:

| Columns | Content |
|---|---|
| Paper, DOI | source paper |
| 21 materials | same names and units as the calculator (`materials21.json`): cement + fly ash + GGBS = the binder (shares add up to 1), the other 14 = mass ratio to that binder, 4 fibers = vol% |
| 4 conditions | curing method, curing temperature (°C), curing duration (days), test age (days) |
| 2 outputs | compressive strength (MPa), tensile strain capacity (%); blank when not used |

`ml_spike/web_data.py` turns each row into the model inputs with the same rules as the web page,
so training and the web compute identical numbers. `03 Dataset_ratio.xlsx` is the full extraction
(773 columns) that this file is built from.

## Models (10-fold CV, random split, mean of 3 seeds)

| Output | Rows / papers | Model | R² | MAE |
|---|---|---|---|---|
| Compressive strength | 610 / 124 | CatBoost | 0.95 | 7.3 MPa |
| Tensile strain capacity | 325 / 82 | CatBoost | 0.81 | 0.89 % |

## Rebuilding

```
cd ml_spike
python build_web_dataset.py              # 03 Dataset_ratio.xlsx -> 04 Dataset_web.xlsx
python benchmark10.py                    # compare 10 models (benchmark.html)
python train_export.py ../strength_model.js   # models for the web
python build_sources_json.py             # data/sources.json (data.html)
cd .. && python embed_materials.py "01 Datamix.xlsx" index.html   # material database
```

Python environment: `ml_spike/.venv` (pandas, scikit-learn, catboost, xgboost, matplotlib, openpyxl).

Le Minh Hoang — Construction Materials Lab, Chonnam National University (Prof. Bang Yeon Lee).

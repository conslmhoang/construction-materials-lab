# Construction Materials Lab — Mix Design & Strength Prediction

Live site: https://conslmhoang.github.io/construction-materials-lab/

A browser-only tool for fibre-reinforced cementitious and geopolymer composites (ECC/SHCC, UHPC, UHP-ECC):

1. **Mix design**: proportions → kg per m³ and per batch, with cost, embodied energy and CO₂ (69 materials).
2. **Strength prediction**: compressive strength, direct tensile strength and tensile strain capacity from the mix,
   curing method/temperature/humidity/duration and test age. It includes an 80% range, a strength-vs-age table,
   a "what changes the prediction" table and optional calibration with your own lab results.
3. **Logs**: every mix design and batch can be downloaded as Excel/CSV.

| Page | What it shows |
|---|---|
| `index.html` | Calculator + prediction |
| `benchmark.html` | 10 ML models compared (10-fold cross-validation, random split) |
| `data.html` | The 285 source papers and how the data were cleaned |

## Models (10-fold CV, random split, mean of 3 seeds)

| Output | Rows / papers | Model | R² | MAE |
|---|---|---|---|---|
| Compressive strength | 1460 / 191 | CatBoost | 0.95 | 6.9 MPa |
| Direct tensile strength | 638 / 128 | CatBoost | 0.83 | 0.86 MPa |
| Tensile strain capacity | 610 / 125 | Extra Trees | 0.77 | 0.84 % |

## Rebuilding

```
cd ml_spike
python benchmark10.py "../03 Dataset_ratio.xlsx" bench10              # compare 10 models
python add_random_oof.py "../03 Dataset_ratio.xlsx" bench10           # predictions for the parity plot
python train_export.py "../03 Dataset_ratio.xlsx" model ../strength_model.js   # models for the web
python build_sources_json.py                                          # data/sources.json for data.html
cd .. && python embed_materials.py "01 Datamix.xlsx" index.html        # material database
```

Python environment: `ml_spike/.venv` (pandas, scikit-learn, catboost, xgboost, matplotlib, openpyxl).

Le Minh Hoang — Construction Materials Lab, Chonnam National University (Prof. Bang Yeon Lee).

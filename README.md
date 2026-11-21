# Construction Materials Lab — Mix Design & Strength Prediction

Live site: https://conslmhoang.github.io/construction-materials-lab/

A browser-only tool for fiber-reinforced cementitious and geopolymer composites (ECC/SHCC, UHPC, UHP-ECC):

1. **Mix design**: proportions → kg per m³ and per batch, with cost, embodied energy and CO₂ (20 materials, the same ones the model uses).
2. **Strength prediction**: compressive strength and tensile strain capacity from the mix,
   curing method/temperature/duration, test age and the fiber length, diameter, strength and modulus. It includes an 80% range, a strength-vs-age table,
   and a Save button that adds a result to the prediction log.
3. **Logs**: every mix design and batch is logged, predictions when you press Save; each row can be deleted (×), and the logs download as Excel/CSV.

| Page | What it shows |
|---|---|
| `index.html` | Calculator + prediction |
| `benchmark.html` | 10 ML models compared (10-fold cross-validation, random split) |
| `data.html` | The 508 source papers |

## Excel files: `excel/`

| File | Content |
|---|---|
| `Materials_20.xlsx` | Density, energy (MJ/kg), CO2 (kg/kg) and cost ($/kg) of the 20 materials, plus the suggested fiber length, diameter, tensile strength and elastic modulus, each with its source. The web can load it (Load material database from Excel). Rebuild: `python ml_spike/build_materials_xlsx.py` |
| `04 Dataset_web.xlsx` | Training data of the ML models (below) |

## Training data: `excel/04 Dataset_web.xlsx`

One sheet, one row per mix and test age, and only the columns the web has:

| Columns | Content |
|---|---|
| Paper, DOI | source paper |
| 20 materials | same names and units as the calculator (`materials21.json`): cement + fly ash + GGBS = the binder (shares add up to 1), the other 14 = mass ratio to that binder, 3 fibers (PE, PVA, steel) = vol%. PBO fiber was removed |
| 12 fiber properties | length (mm), diameter (µm), tensile strength (MPa) and elastic modulus (GPa) of each fiber type as reported in the paper; blank = not reported. The strain model uses all four (volume-weighted); a value the paper does not report = the reference value in `materials21.json` (PE and PVA: the fiber of Prof. Bang Yeon Lee's lab; steel: 10.3390/ma15051668), the same value the web suggests |
| 4 conditions | curing method, curing temperature (°C), curing duration (days), test age (days) |
| 2 outputs | compressive strength (MPa), tensile strain capacity (%); blank when not used |

`ml_spike/web_data.py` turns each row into the model inputs with the same rules as the web page,
so training and the web compute identical numbers. `03 Dataset_ratio.xlsx` is the full extraction
(773 columns) that this file is built from.

## Models (10-fold CV, random split, mean of 3 seeds)

| Output | Rows / papers | Model | R² | MAE |
|---|---|---|---|---|
| Compressive strength | 2,144 / 395 | Extra Trees × Abrams W/P curve | 0.94 | 7.8 MPa |
| Tensile strain capacity | 1,094 / 302 | Extra Trees | 0.78 | 0.95 % |

The strain model also uses the fiber length, diameter, tensile strength and elastic modulus; the compressive-strength
model does not (they did not improve it).

NaOH given only as a molar solution is converted to NaOH solids + water with the OxyChem Caustic Soda Handbook,
Table 1 (density and NaOH content at 60 °F): `ml_spike/additions_v2/naoh_solution.py`, `ml_spike/reference/naoh_solution_table.csv`.

The compressive-strength model is one model: Extra Trees that learn the deviation from an Abrams curve
(log fc falls linearly with water / (cement + FA + GGBS + SF + MK + LP), fitted on the data). Trees alone hardly lowered the
strength when more water was added in regions with few data (e.g. high-fly-ash ECC at W/B 0.36: 64 MPa predicted,
47.4 MPa measured; with the curve 50 MPa). In the 10-model comparison every model gets the same Abrams curve for
compressive strength. Averaging with CatBoost or weighted stacking added only about 0.006 R², so the web keeps one model.

Strain audit (Nov 2026): the 30 papers with the largest strain errors were checked against the papers. Every strain
value matched; the errors were in the inputs. 63 rows were removed (marble powder entered as limestone, curing that is not
one web method or has no stated temperature, unstated admixture dosage, one paper that could not be checked), curing labels,
water (from the mix table) and hybrid PVA fiber properties were corrected, and compressive strengths read from figures were
removed. Edits: `ml_spike/audit/corrections.json` (applied by `build_web_dataset.py`), evidence: `ml_spike/audit/report_*.md`.
On the rows the audit did not touch, the strain MAE fell from 1.00 to 0.95 %.

## Rebuilding

```
cd ml_spike
python build_web_dataset.py              # 03 Dataset_ratio.xlsx -> excel/04 Dataset_web.xlsx
python benchmark10.py                    # compare 10 models (benchmark.html)
python train_export.py ../strength_model.js   # models for the web
python build_sources_json.py             # data/sources.json (data.html)
cd .. && python embed_materials.py "01 Datamix.xlsx" index.html   # material database
```

Python environment: `ml_spike/.venv` (pandas, scikit-learn, catboost, xgboost, matplotlib, openpyxl).

Le Minh Hoang — Construction Materials Lab, Chonnam National University (Prof. Bang Yeon Lee).

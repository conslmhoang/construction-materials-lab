"""Compare the 10 most-used ML models on "04 Dataset_web.xlsx".

Targets : compressive strength, tensile strain capacity
Inputs  : the 33 values the web computes (web_data.py) — same as train_export.py
Score   : 10-fold cross-validation, random split, mean of 3 seeds

Usage:  python benchmark10.py
Writes bench10/benchmark10.csv, bench10/benchmark10.json (read by benchmark.html), bench10/benchmark10.png
"""
import os, json, time
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
here = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(here, "bench10"); os.makedirs(OUT, exist_ok=True)
from web_data import load, FEATURES
from sklearn.model_selection import KFold
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import TransformedTargetRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor

X, Y, groups = load()

pre = lambda: [SimpleImputer(strategy="median", add_indicator=True), StandardScaler()]
fill = lambda: SimpleImputer(strategy="constant", fill_value=-1)
sy = lambda est: TransformedTargetRegressor(regressor=est, transformer=StandardScaler())
MODELS = {
    "Linear Regression": ("Linear",   lambda: make_pipeline(*pre(), LinearRegression())),
    "KNN":               ("Distance", lambda: make_pipeline(*pre(), KNeighborsRegressor(7, weights="distance"))),
    "SVR":               ("Kernel",   lambda: make_pipeline(*pre(), sy(SVR(C=3, epsilon=0.05)))),
    "ANN (MLP)":         ("Neural",   lambda: make_pipeline(*pre(), sy(MLPRegressor(hidden_layer_sizes=(64, 32), alpha=1e-2, max_iter=3000,
                                                                   early_stopping=True, random_state=0)))),
    "Decision Tree":     ("Tree",     lambda: make_pipeline(fill(), DecisionTreeRegressor(min_samples_leaf=5, random_state=0))),
    "Random Forest":     ("Bagging",  lambda: make_pipeline(fill(), RandomForestRegressor(300, min_samples_leaf=2, max_features=0.5,
                                                                                         n_jobs=-1, random_state=0))),
    "Extra Trees":       ("Bagging",  lambda: make_pipeline(fill(), ExtraTreesRegressor(300, min_samples_leaf=2, max_features=0.5,
                                                                                       n_jobs=-1, random_state=0))),
    "Gradient Boosting": ("Boosting", lambda: make_pipeline(fill(), GradientBoostingRegressor(n_estimators=400, max_depth=3,
                                                              learning_rate=0.05, subsample=0.8, random_state=0))),
    "XGBoost":           ("Boosting", lambda: XGBRegressor(n_estimators=500, max_depth=3, learning_rate=0.05, subsample=0.8,
                                                           colsample_bytree=0.8, min_child_weight=3, n_jobs=4, random_state=0)),
    "CatBoost":          ("Boosting", lambda: CatBoostRegressor(iterations=800, depth=4, learning_rate=0.05, l2_leaf_reg=3,
                                                                verbose=0, random_seed=0, thread_count=4, allow_writing_files=False)),
}
TARGETS = {"fc": ("Compressive strength fc", "MPa"),
           "eps": ("Tensile strain capacity εtu", "%")}

def run(Xa, y, splits, mk):
    pp = np.zeros(len(y))
    for tr, te in splits:
        keep = ~np.all(np.isnan(Xa[tr]), axis=0)
        pp[te] = mk().fit(Xa[tr][:, keep], y[tr]).predict(Xa[te][:, keep])
    return pp

rows, web = [], {"date": pd.Timestamp.now().strftime("%Y-%m-%d"), "features": FEATURES, "targets": {}}
for key, (label, unit) in TARGETS.items():
    m = Y[key].notna().values
    Xa = X[m].values.astype(float); ya = Y[key].values[m]; ga = groups[m].values
    T = {"label": label, "unit": unit, "n_rows": int(m.sum()), "n_papers": int(len(np.unique(ga))), "models": [], "oof_random": {}}
    for mname, (family, mk) in MODELS.items():
        t0 = time.time(); r = {"target": key, "model": mname, "family": family}; sc = []
        for s_ in range(3):
            pp = run(Xa, ya, KFold(10, shuffle=True, random_state=s_).split(Xa), mk)
            sc.append((r2_score(ya, pp), mean_absolute_error(ya, pp), mean_squared_error(ya, pp) ** 0.5))
            if s_ == 0: T["oof_random"][mname] = [round(float(v), 3) for v in pp]
        for j, k in enumerate(["R2", "MAE", "RMSE"]):
            r[f"{k} random-row"] = round(float(np.mean([v[j] for v in sc])), 3)
        r["fit_s"] = round(time.time() - t0, 1)
        print(f"{key:4s} {mname:18s} R2={r['R2 random-row']:.3f}  MAE={r['MAE random-row']:.2f}  ({r['fit_s']:.0f}s)", flush=True)
        rows.append(r); T["models"].append({k: v for k, v in r.items() if k != "target"})
    T["y"] = [round(float(v), 3) for v in ya]
    web["targets"][key] = T

df = pd.DataFrame(rows)
df.to_csv(os.path.join(OUT, "benchmark10.csv"), index=False, encoding="utf-8-sig")
json.dump(web, open(os.path.join(OUT, "benchmark10.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

fig, axs = plt.subplots(1, 2, figsize=(12, 5.5))
for ax, (key, g) in zip(axs, df.groupby("target", sort=False)):
    g = g.sort_values("R2 random-row"); yy = np.arange(len(g))
    ax.barh(yy, g["R2 random-row"].clip(lower=0), 0.6, color="#2a78d6")
    for yi, v in zip(yy, g["R2 random-row"]): ax.text(max(v, 0) + 0.01, yi, f"{v:.2f}", va="center", fontsize=9)
    ax.set_yticks(yy); ax.set_yticklabels(g["model"]); ax.set_xlim(0, 1.08); ax.set_xlabel("R² (10-fold CV, random split)")
    ax.set_title(f"{TARGETS[key][0]} (n={web['targets'][key]['n_rows']})"); ax.grid(axis="x", alpha=.3)
plt.tight_layout(); plt.savefig(os.path.join(OUT, "benchmark10.png"), dpi=110)
print("best:")
for key, g in df.groupby("target", sort=False):
    b = g.sort_values("R2 random-row").iloc[-1]; print(f"  {key}: {b['model']}  R2={b['R2 random-row']:.3f}  MAE={b['MAE random-row']:.2f}")

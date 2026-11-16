"""Compare the 10 most-used ML models in concrete-strength literature on the CLEANED dataset.

Targets : fc (compressive), ft (direct tensile), eps (tensile strain capacity)
Rows    : clean/dataset_clean.csv flags use_fc / use_ft / use_eps
Features: the 33 inputs the web calculator can supply (same list as train_export.py)
Validation (3 seeds each):
  random-row  – 10-fold, rows shuffled (what most papers report; optimistic)
  half-paper  – half of every paper's mixes in train, other half in test (= your lab already has data)
  paper-out   – 10-fold GroupKFold by paper (= a brand-new lab; the honest score)

Usage: python benchmark10.py "../03 Dataset_ratio.xlsx" bench10
Writes bench10/benchmark10.csv, bench10/benchmark10.json (for the web), bench10/benchmark10.png
"""
import sys, os, json, time
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, "spike.py"), encoding="utf-8").read()
exec(src.split("lines, curves = [], {}")[0])          # X, d, N, groups_all, OUT
os.makedirs(OUT, exist_ok=True)
from sklearn.model_selection import GroupKFold, KFold
from sklearn.metrics import mean_squared_error
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

FEATURES = ["OPC", "GGBS", "FA", "SF", "MK", "LP",
            "WG_B", "NaOH_B", "CaOH2_B", "Na2SO4_B", "SSM_B",
            "W_B", "Sand_B", "QP_B", "Light_B", "SP_B", "VMA_B",
            "V_PE", "V_PVA", "V_Steel", "V_PBO", "V_total",
            "Cure_T", "Cure_days", "Cure_RH", "Age_days", "Cure_water", "Cure_sealed", "Cure_heat",
            "W_C", "Activator_tot", "Paste_vol", "Binder_kgm3"]

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
TARGETS = {"fc": ("Compressive strength fc", "MPa", 389),
           "ft": ("Direct tensile strength ft", "MPa", 404),
           "eps": ("Tensile strain capacity εtu", "%", 418)}

F = pd.read_csv(os.path.join(here, "clean", "dataset_clean.csv"), encoding="utf-8-sig")
assert len(F) == len(X), (len(F), len(X))

def half_paper(g, seed):
    rng = np.random.default_rng(seed); tr, te = [], []
    for p in np.unique(g):
        idx = rng.permutation(np.where(g == p)[0])
        if len(idx) < 2: tr += list(idx); continue
        h = len(idx) // 2; tr += list(idx[:h]); te += list(idx[h:])
    return [(np.array(tr), np.array(te))]

def run(Xa, y, splits, mk):
    ii, pp = [], []
    for tr, te in splits:
        keep = ~np.all(np.isnan(Xa[tr]), axis=0)
        pp += list(mk().fit(Xa[tr][:, keep], y[tr]).predict(Xa[te][:, keep])); ii += list(te)
    ii, pp = np.array(ii), np.array(pp)
    return ii, pp

cols = [list(X.columns).index(f) for f in FEATURES]
rows, web = [], {"date": pd.Timestamp.now().strftime("%Y-%m-%d"), "features": FEATURES, "targets": {}}
for key, (label, unit, col) in TARGETS.items():
    m = F[f"use_{key}"].values.astype(bool) & np.isfinite(N(col).values)
    Xa = X.loc[m].values.astype(float)[:, cols]; ya = N(col).values[m]; ga = groups_all[m].values
    T = {"label": label, "unit": unit, "n_rows": int(m.sum()), "n_papers": int(len(np.unique(ga))), "models": [], "oof": {}}
    for mname, (family, mk) in MODELS.items():
        t0 = time.time(); r = {"target": key, "model": mname, "family": family}
        for mode in ["random-row", "half-paper", "paper-out"]:
            sc = []
            for s in range(3):
                if mode == "random-row": sp = list(KFold(10, shuffle=True, random_state=s).split(Xa))
                elif mode == "paper-out": sp = list(GroupKFold(10, shuffle=True, random_state=s).split(Xa, ya, ga))
                else: sp = half_paper(ga, s)
                ii, pp = run(Xa, ya, sp, mk)
                sc.append((r2_score(ya[ii], pp), mean_absolute_error(ya[ii], pp), mean_squared_error(ya[ii], pp) ** 0.5))
                if mode == "paper-out" and s == 0:
                    o = np.full(len(ya), np.nan); o[ii] = pp
                    T["oof"][mname] = [round(float(v), 3) for v in o]
            for j, k in enumerate(["R2", "MAE", "RMSE"]):
                r[f"{k} {mode}"] = round(float(np.mean([v[j] for v in sc])), 3)
        r["fit_s"] = round(time.time() - t0, 1)
        print(f"{key:4s} {mname:18s} random R2={r['R2 random-row']:.2f}  half-paper R2={r['R2 half-paper']:.2f}  "
              f"paper-out R2={r['R2 paper-out']:.2f} MAE={r['MAE paper-out']:.2f}  ({r['fit_s']:.0f}s)", flush=True)
        rows.append(r); T["models"].append({k: v for k, v in r.items() if k != "target"})
    T["y"] = [round(float(v), 3) for v in ya]
    web["targets"][key] = T

df = pd.DataFrame(rows)
df.to_csv(os.path.join(OUT, "benchmark10.csv"), index=False, encoding="utf-8-sig")
json.dump(web, open(os.path.join(OUT, "benchmark10.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

fig, axs = plt.subplots(1, 3, figsize=(17, 5.5))
for ax, (key, g) in zip(axs, df.groupby("target", sort=False)):
    g = g.sort_values("R2 random-row"); yy = np.arange(len(g))
    ax.barh(yy + 0.27, g["R2 random-row"].clip(lower=0), 0.27, color="#d5dde8", label="random rows (optimistic)")
    ax.barh(yy, g["R2 half-paper"].clip(lower=0), 0.27, color="#7fa6d3", label="50/50 per paper (lab already seen)")
    ax.barh(yy - 0.27, g["R2 paper-out"].clip(lower=0), 0.27, color="#2f5f98", label="paper held out (new lab)")
    ax.set_yticks(yy); ax.set_yticklabels(g["model"]); ax.set_xlim(0, 1); ax.set_xlabel("R²")
    ax.set_title(f"{TARGETS[key][0]} (n={web['targets'][key]['n_rows']})"); ax.grid(axis="x", alpha=.3)
axs[0].legend(loc="lower right", fontsize=8)
plt.tight_layout(); plt.savefig(os.path.join(OUT, "benchmark10.png"), dpi=110)
print("\nbest by random-split R2 (headline):")
for key, g in df.groupby("target", sort=False):
    b = g.sort_values("R2 random-row").iloc[-1]; print(f"  {key}: {b['model']}  R2={b['R2 random-row']:.3f}  MAE={b['MAE random-row']:.2f}")

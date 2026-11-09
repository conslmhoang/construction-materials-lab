"""Benchmark 12 regression models on the web-aligned features.
Two validation modes:
  random-row   – rows shuffled, mixes from one paper can sit in train AND test (what most papers report)
  paper-out    – whole papers held out (= a new lab), the honest score for the web app
Usage: python benchmark_models.py "../03 Dataset_ratio.xlsx" <outdir> additions
"""
import sys, os, json, time
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, "spike.py"), encoding="utf-8").read()
exec(src.split("lines, curves = [], {}")[0])
exec("WEB2 = " + open(os.path.join(here, "split_compare.py"), encoding="utf-8").read().split("WEB2 = ")[1].split("MODELS = ")[0]); WEB = WEB2  # web inputs: no specimen size, no fibre properties
from sklearn.model_selection import GroupKFold, KFold
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import RidgeCV, LassoCV
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, ConstantKernel
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor, HistGradientBoostingRegressor
from sklearn.compose import TransformedTargetRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor

pre = lambda: [SimpleImputer(strategy="median", add_indicator=True), StandardScaler()]
scaled_y = lambda est: TransformedTargetRegressor(regressor=est, transformer=StandardScaler())
MODELS = {
    "Ridge (linear)":   lambda: make_pipeline(*pre(), RidgeCV(alphas=np.logspace(-3, 3, 20))),
    "Lasso (linear)":   lambda: make_pipeline(*pre(), LassoCV(cv=5, max_iter=20000)),
    "KNN":              lambda: make_pipeline(*pre(), KNeighborsRegressor(7, weights="distance")),
    "SVR (RBF)":        lambda: make_pipeline(*pre(), scaled_y(SVR(C=3, epsilon=0.05))),
    "Gaussian Process": lambda: make_pipeline(*pre(), scaled_y(GaussianProcessRegressor(
                            ConstantKernel() * RBF(5.0) + WhiteKernel(0.3), normalize_y=False))),
    "MLP (neural net)": lambda: make_pipeline(*pre(), scaled_y(MLPRegressor(hidden_layer_sizes=(64, 32), alpha=1e-2, max_iter=3000,
                            early_stopping=True, random_state=0))),
    "Random Forest":    lambda: make_pipeline(SimpleImputer(strategy="constant", fill_value=-1),
                            RandomForestRegressor(500, min_samples_leaf=2, max_features=0.5, n_jobs=-1, random_state=0)),
    "Extra Trees":      lambda: make_pipeline(SimpleImputer(strategy="constant", fill_value=-1),
                            ExtraTreesRegressor(500, min_samples_leaf=2, max_features=0.5, n_jobs=-1, random_state=0)),
    "GBM (sklearn)":    lambda: make_pipeline(SimpleImputer(strategy="constant", fill_value=-1),
                            GradientBoostingRegressor(n_estimators=400, max_depth=3, learning_rate=0.05, subsample=0.8, random_state=0)),
    "HistGB (current)": lambda: HistGradientBoostingRegressor(max_iter=400, learning_rate=0.05, max_leaf_nodes=8, max_depth=3,
                            min_samples_leaf=10, l2_regularization=1.0, random_state=0),
    "XGBoost":          lambda: XGBRegressor(n_estimators=500, max_depth=3, learning_rate=0.05, subsample=0.8,
                            colsample_bytree=0.8, min_child_weight=3, reg_lambda=1.0, n_jobs=4, random_state=0),
    "LightGBM":         lambda: LGBMRegressor(n_estimators=500, num_leaves=8, max_depth=3, learning_rate=0.05,
                            subsample=0.8, subsample_freq=1, colsample_bytree=0.8, min_child_samples=10, verbose=-1, random_state=0),
    "CatBoost":         lambda: CatBoostRegressor(iterations=800, depth=4, learning_rate=0.05, l2_leaf_reg=3,
                            verbose=0, random_seed=0, thread_count=4),
}

def half_paper_splits(g, seed):
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
    return r2_score(y[ii], pp), mean_absolute_error(y[ii], pp)

names = list(X.columns)
cols = [names.index(f) for f in WEB]
results = []
for tname, (y, mask) in targets.items():
    m = mask & y.notna()
    Xa = X[m].values.astype(float)[:, cols]; ya = y[m].values; ga = groups_all[m].values
    for mname, mk in MODELS.items():
        t0 = time.time(); r = {"target": tname, "model": mname}
        for mode in ["random-row", "half-paper", "paper-out"]:
            sc = []
            for s in range(3):
                if mode == "random-row": sp = KFold(10, shuffle=True, random_state=s).split(Xa)
                elif mode == "paper-out": sp = GroupKFold(10, shuffle=True, random_state=s).split(Xa, ya, ga)
                else: sp = half_paper_splits(ga, s)
                sc.append(run(Xa, ya, list(sp), mk))
            r[f"R2 {mode}"] = round(float(np.mean([a for a, b in sc])), 3)
            r[f"MAE {mode}"] = round(float(np.mean([b for a, b in sc])), 2)
        print(f"{tname:18s} {mname:17s} random R2={r['R2 random-row']:.2f}  half-paper R2={r['R2 half-paper']:.2f}  paper-out R2={r['R2 paper-out']:.2f} "
              f"MAE={r['MAE paper-out']:.2f}  ({time.time()-t0:.0f}s)", flush=True)
        results.append(r)

df = pd.DataFrame(results)
df.to_csv(os.path.join(OUT, "benchmark_models.csv"), index=False, encoding="utf-8-sig")
fig, axs = plt.subplots(1, 3, figsize=(16, 5.5), sharey=False)
for ax, (tname, g) in zip(axs, df.groupby("target", sort=False)):
    g = g.sort_values("R2 paper-out")
    yy = np.arange(len(g))
    ax.barh(yy + 0.27, g["R2 random-row"].clip(lower=0), 0.27, color="#d5dde8", label="random rows")
    ax.barh(yy, g["R2 half-paper"].clip(lower=0), 0.27, color="#7fa6d3", label="50/50 per paper (lab already seen)")
    ax.barh(yy - 0.27, g["R2 paper-out"].clip(lower=0), 0.27, color="#2f5f98", label="paper held out (brand-new lab)")
    ax.set_yticks(yy); ax.set_yticklabels(g["model"]); ax.set_xlim(0, 1); ax.set_title(tname); ax.set_xlabel("R²")
    ax.grid(axis="x", alpha=.3)
axs[0].legend(loc="lower right", fontsize=8)
plt.tight_layout(); plt.savefig(os.path.join(OUT, "benchmark_models.png"), dpi=110)
print("\nsaved benchmark_models.csv / .png")

"""Compare 3 ways of testing, on the web input set (no specimen size, no fibre properties):
  paper-out   – whole papers hidden (a brand-new lab, model knows nothing about it)
  half-paper  – each paper: half of its mixes train, other half test (model has seen this lab before)
  random-row  – rows shuffled
Usage: python split_compare.py "../03 Dataset_ratio.xlsx" <outdir> <additions dir>
"""
import sys, os
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, "spike.py"), encoding="utf-8").read()
exec(src.split("lines, curves = [], {}")[0])
from sklearn.model_selection import GroupKFold, KFold
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from catboost import CatBoostRegressor

WEB2 = ["OPC", "GGBS", "FA", "SF", "MK", "LP",
        "WG_B", "NaOH_B", "CaOH2_B", "Na2SO4_B", "SSM_B",
        "W_B", "Sand_B", "QP_B", "Light_B", "SP_B", "VMA_B",
        "V_PE", "V_PVA", "V_Steel", "V_PBO", "V_total",
        "Cure_T", "Cure_days", "Cure_RH", "Age_days", "Cure_water", "Cure_sealed", "Cure_heat",
        "W_C", "Activator_tot", "Paste_vol", "Binder_kgm3"]
MODELS = {
    "CatBoost": lambda: CatBoostRegressor(iterations=800, depth=4, learning_rate=0.05, l2_leaf_reg=3, verbose=0, random_seed=0, thread_count=4),
    "_RF_off": lambda: make_pipeline(SimpleImputer(strategy="constant", fill_value=-1),
                        RandomForestRegressor(400, min_samples_leaf=2, max_features=0.5, n_jobs=-1, random_state=0)),
}

def half_paper_splits(g, seed):
    rng = np.random.default_rng(seed)
    tr, te = [], []
    for p in np.unique(g):
        idx = rng.permutation(np.where(g == p)[0])
        if len(idx) < 2: tr += list(idx); continue
        h = len(idx) // 2
        tr += list(idx[:h]); te += list(idx[h:])
    return [(np.array(tr), np.array(te))]

def score(Xa, y, splits, mk):
    idx_all, p_all = [], []
    for tr, te in splits:
        keep = ~np.all(np.isnan(Xa[tr]), axis=0)
        p_all += list(mk().fit(Xa[tr][:, keep], y[tr]).predict(Xa[te][:, keep])); idx_all += list(te)
    yy = y[idx_all]; pp = np.array(p_all)
    return r2_score(yy, pp), mean_absolute_error(yy, pp), np.median(np.abs(pp - yy) / yy) * 100

names = list(X.columns)
cols = [names.index(f) for f in WEB2]
rows = []
for tname, (y, mask) in targets.items():
    m = mask & y.notna()
    Xa = X[m].values.astype(float)[:, cols]; ya = y[m].values; ga = groups_all[m].values
    print(f"\n== {tname}: {m.sum()} rows, {len(np.unique(ga))} papers")
    for mname, mk in [(k, v) for k, v in MODELS.items() if not k.startswith("_")]:
        for mode in ["paper-out", "half-paper", "random-row"]:
            res = []
            for s in range(3):
                if mode == "paper-out": sp = list(GroupKFold(10, shuffle=True, random_state=s).split(Xa, ya, ga))
                elif mode == "random-row": sp = list(KFold(10, shuffle=True, random_state=s).split(Xa))
                else: sp = half_paper_splits(ga, s)
                res.append(score(Xa, ya, sp, mk))
            r2, mae, mape = np.mean(res, axis=0)
            print(f"   {mname:14s} {mode:11s} R2={r2:.2f}  MAE={mae:.2f}  median error={mape:.0f}%", flush=True)
            rows.append(dict(target=tname, model=mname, mode=mode, R2=round(r2, 3), MAE=round(mae, 2), median_err_pct=round(mape, 1)))
pd.DataFrame(rows).to_csv(os.path.join(OUT, "split_compare.csv"), index=False, encoding="utf-8-sig")

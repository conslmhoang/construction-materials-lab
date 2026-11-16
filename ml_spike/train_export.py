"""Train the final strength models and export them for the web calculator.

  fc  : CatBoost     (best by random-split 10-fold CV, R2 0.95 — see benchmark10.py)
  ft  : CatBoost     (best, R2 0.83)
  eps : Extra Trees  (R2 0.78; XGBoost 0.782 is a tie and has no browser exporter)

Headline score = random-split 10-fold CV x 3 seeds (the user's chosen metric);
paper-held-out and half-paper scores are kept as secondary information.

Rows: clean/dataset_clean.csv flags use_fc / use_ft / use_eps (same rows as benchmark10.py).

Usage:
  python train_export.py "../03 Dataset_ratio.xlsx" model [../index.html]

Writes model/strength_model.json, model/test_vectors.json and, if index.html is given,
replaces the block between "// >>> MODEL BEGIN" and "// <<< MODEL END" in it.
"""
import sys, os, json, re
here = os.path.dirname(os.path.abspath(__file__))
HTML = sys.argv[3] if len(sys.argv) > 3 else None
sys.argv = sys.argv[:3]                                # spike.py would read argv[3] as an additions dir
src = open(os.path.join(here, "spike.py"), encoding="utf-8").read()
exec(src.split("lines, curves = [], {}")[0])          # X, targets, groups_all, d
from sklearn.model_selection import GroupKFold, KFold
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor
from catboost import CatBoostRegressor

F = pd.read_csv(os.path.join(here, "clean", "dataset_clean.csv"), encoding="utf-8-sig")
assert len(F) == len(X), (len(F), len(X))
COL = {"fc": 389, "ft": 404, "eps": 418}
FEATURES = ["OPC", "GGBS", "FA", "SF", "MK", "LP",
            "WG_B", "NaOH_B", "CaOH2_B", "Na2SO4_B", "SSM_B",
            "W_B", "Sand_B", "QP_B", "Light_B", "SP_B", "VMA_B",
            "V_PE", "V_PVA", "V_Steel", "V_PBO", "V_total",
            "Cure_T", "Cure_days", "Cure_RH", "Age_days", "Cure_water", "Cure_sealed", "Cure_heat",
            "W_C", "Activator_tot", "Paste_vol", "Binder_kgm3"]
SPEC = {
    "fc":  dict(target="fc (MPa)",          kind="catboost", unit="MPa", label="Compressive strength"),
    "ft":  dict(target="ft direct (MPa)",   kind="catboost",    unit="MPa", label="Direct tensile strength"),
    "eps": dict(target="eps_tu direct (%)", kind="et",          unit="%",   label="Tensile strain capacity"),
}

NAME = {"catboost": "CatBoost", "et": "Extra Trees", "rf": "Random Forest"}

def make(kind):
    if kind == "catboost":
        return CatBoostRegressor(iterations=800, depth=4, learning_rate=0.05, l2_leaf_reg=3,
                                 verbose=0, random_seed=0, thread_count=4, allow_writing_files=False)
    if kind == "rf":
        return RandomForestRegressor(n_estimators=150, min_samples_leaf=3, max_features=0.5, n_jobs=-1, random_state=0)
    return ExtraTreesRegressor(n_estimators=150, min_samples_leaf=3, max_features=0.5, n_jobs=-1, random_state=0)

def prep(kind, Xa):
    return Xa if kind == "catboost" else np.where(np.isnan(Xa), -1.0, Xa)   # trees: NaN -> -1 (same in JS)

def half_paper(g, seed):
    rng = np.random.default_rng(seed); tr, te = [], []
    for p in np.unique(g):
        idx = rng.permutation(np.where(g == p)[0])
        if len(idx) < 2: tr += list(idx); continue
        h = len(idx) // 2; tr += list(idx[:h]); te += list(idx[h:])
    return np.array(tr), np.array(te)

names = list(X.columns)
cols = [names.index(f) for f in FEATURES]
r4 = lambda v: float(f"{v:.5g}")
out = {"version": pd.Timestamp.now().strftime("%Y-%m-%d"), "features": FEATURES, "targets": {}}
tests = {"features": FEATURES, "rows": []}

for key, s in SPEC.items():
    y = N(COL[key])
    m = F[f"use_{key}"].values.astype(bool) & y.notna().values
    Xa = X[m].values.astype(float)[:, cols]; ya = y[m].values; ga = groups_all[m].values
    kind = s["kind"]

    # ---- headline: random-split 10-fold CV, 3 seeds
    rr2, rmae = [], []
    for sd in range(3):
        pr = np.zeros(len(ya))
        for tr_, te_ in KFold(10, shuffle=True, random_state=sd).split(Xa):
            pr[te_] = make(kind).fit(prep(kind, Xa[tr_]), ya[tr_]).predict(prep(kind, Xa[te_]))
        rr2.append(r2_score(ya, pr)); rmae.append(mean_absolute_error(ya, pr))
        if sd == 0: pr0 = pr.copy()
    # ---- 80% prediction interval from random-split residuals, binned by predicted value (5 bins)
    edges = np.quantile(pr0, [.2, .4, .6, .8])
    bins = np.searchsorted(edges, pr0, side="left")          # same rule as JS: count of edges below p
    res = ya - pr0
    lo_ = [r4(np.quantile(res[bins == b_], .1)) for b_ in range(5)]
    hi_ = [r4(np.quantile(res[bins == b_], .9)) for b_ in range(5)]
    cover = float(np.mean([(lo_[b_] <= r <= hi_[b_]) for b_, r in zip(bins, res)]))

    # ---- stricter error estimates
    pred = np.zeros(len(ya))
    for tr, te in GroupKFold(10, shuffle=True, random_state=0).split(Xa, ya, ga):
        pred[te] = make(kind).fit(prep(kind, Xa[tr]), ya[tr]).predict(prep(kind, Xa[te]))
    tr, te = half_paper(ga, 0)
    ph = make(kind).fit(prep(kind, Xa[tr]), ya[tr]).predict(prep(kind, Xa[te]))

    # ---- lab correction: additive vs multiplicative, using k measured mixes of the same paper
    rng = np.random.default_rng(1); err = {"none": [], "add": [], "mul": []}
    for k in (1, 2, 3):
        for p in np.unique(ga):
            idx = np.where(ga == p)[0]
            if len(idx) < k + 2: continue
            for _ in range(10):
                q = rng.permutation(idx); cal, ev = q[:k], q[k:]
                add = (ya[cal] - pred[cal]).mean()
                mul = ya[cal].mean() / max(pred[cal].mean(), 1e-6)
                err["none"].append(np.mean(np.abs(ya[ev] - pred[ev])))
                err["add"].append(np.mean(np.abs(ya[ev] - (pred[ev] + add))))
                err["mul"].append(np.mean(np.abs(ya[ev] - pred[ev] * mul)))
    corr = "mul" if np.mean(err["mul"]) <= np.mean(err["add"]) else "add"

    # ---- final model on all rows
    mdl = make(kind).fit(prep(kind, Xa), ya)
    entry = dict(label=s["label"], unit=s["unit"], kind="catboost" if kind == "catboost" else "trees", model_name=NAME[kind], n_rows=int(m.sum()), n_papers=int(len(np.unique(ga))),
                 r2_random=round(float(np.mean(rr2)), 3), mae_random=round(float(np.mean(rmae)), 3),
                 mae_new_lab=round(float(mean_absolute_error(ya, pred)), 3),
                 r2_new_lab=round(float(r2_score(ya, pred)), 3),
                 mae_lab_known=round(float(mean_absolute_error(ya[te], ph)), 3),
                 r2_lab_known=round(float(r2_score(ya[te], ph)), 3),
                 correction=corr,
                 interval=dict(level=0.8, edges=[r4(v) for v in edges], lo=lo_, hi=hi_, coverage=round(cover, 3)),
                 correction_mae={k_: round(float(np.mean(v)), 3) for k_, v in err.items()},
                 y_min=r4(ya.min()), y_max=r4(ya.max()))
    if kind == "catboost":
        tmp = os.path.join(OUT, f"_{key}_catboost.json"); mdl.save_model(tmp, format="json")
        cb = json.load(open(tmp)); os.remove(tmp)
        ff = cb["features_info"]["float_features"]
        nan_mode = {f["flat_feature_index"]: f.get("nan_value_treatment", "AsIs") for f in ff}
        trees = []
        for t in cb["oblivious_trees"]:
            trees.append({"s": [[sp["float_feature_index"], r4(sp["border"])] for sp in t["splits"]],
                          "v": [r4(v) for v in t["leaf_values"]]})
        sb = cb.get("scale_and_bias", [1, [0]])
        entry.update(trees=trees, scale=sb[0], bias=float(np.ravel(sb[1])[0]),
                     nan=[nan_mode.get(i, "AsIs") for i in range(len(FEATURES))])
    else:
        trees = []
        for est in mdl.estimators_:
            t = est.tree_
            trees.append({"f": t.feature.tolist(), "t": [r4(v) for v in t.threshold],
                          "l": t.children_left.tolist(), "r": t.children_right.tolist(),
                          "v": [r4(v) for v in t.value[:, 0, 0]]})
        entry.update(trees=trees)
    out["targets"][key] = entry

    # ---- domain ranges (1st-99th percentile of rows that have a value)
    if key == "fc":
        rng_ = {}
        for j, f in enumerate(FEATURES):
            v = Xa[:, j][np.isfinite(Xa[:, j])]
            if len(v): rng_[f] = [r4(np.percentile(v, 1)), r4(np.percentile(v, 99))]
        out["ranges"] = rng_
    # ---- test vectors for the JS predictor
    pick = np.random.default_rng(7).choice(len(ya), 15, replace=False)
    pp = mdl.predict(prep(kind, Xa[pick]))
    for i, p in zip(pick, pp):
        tests["rows"].append({"target": key, "x": [None if not np.isfinite(v) else float(v) for v in Xa[i]], "pred": float(p)})

    print(f"{key:4s} {kind:8s} n={entry['n_rows']:4d} papers={entry['n_papers']:3d}  random R2={entry['r2_random']:.3f} MAE={entry['mae_random']:.2f}  new-lab R2={entry['r2_new_lab']:.2f} "
          f"MAE={entry['mae_new_lab']:.2f}  lab-known R2={entry['r2_lab_known']:.2f} MAE={entry['mae_lab_known']:.2f}  "
          f"correction MAE none/add/mul = {entry['correction_mae']}  -> {corr}", flush=True)

js = json.dumps(out, separators=(",", ":"))
open(os.path.join(OUT, "strength_model.json"), "w", encoding="utf-8").write(js)
json.dump(tests, open(os.path.join(OUT, "test_vectors.json"), "w"))
print(f"strength_model.json: {len(js)/1e6:.2f} MB")

if HTML:
    html = open(HTML, encoding="utf-8").read()
    pat = re.compile(r"(// >>> MODEL BEGIN\n).*?(\n// <<< MODEL END)", re.S)
    if not pat.search(html): sys.exit("MODEL markers not found in " + HTML)
    html = pat.sub(lambda mt: mt.group(1) + "const STRENGTH_MODEL = " + js + ";" + mt.group(2), html)
    open(HTML, "w", encoding="utf-8", newline="\n").write(html)
    print("embedded model into", HTML)

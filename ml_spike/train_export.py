"""Train the final strength models from "04 Dataset_web.xlsx" and export them for the web.

  fc  : CatBoost     eps : Extra Trees   (best in benchmark10.py)

Inputs = the 21 web materials + curing/test conditions + 5 values computed from them (web_data.py).
Headline score = random-split 10-fold CV x 3 seeds.

Usage:  python train_export.py [../strength_model.js]
Writes model/strength_model.json, model/test_vectors.json and, if given, the model block of strength_model.js.
"""
import sys, os, json, re
import numpy as np, pandas as pd
here = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(here, "model"); os.makedirs(OUT, exist_ok=True)
HTML = sys.argv[1] if len(sys.argv) > 1 else None
from web_data import load, FEATURES, M21
from sklearn.model_selection import GroupKFold, KFold
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor
from catboost import CatBoostRegressor

X, Y, groups = load()
SPEC = {
    "fc":  dict(kind="catboost", unit="MPa", label="Compressive strength"),
    "eps": dict(kind="et",       unit="%",   label="Tensile strain capacity"),
}

NAME = {"catboost": "CatBoost", "et": "Extra Trees", "rf": "Random Forest"}

def make(kind):
    if kind == "catboost":
        return CatBoostRegressor(iterations=800, depth=4, learning_rate=0.05, l2_leaf_reg=3,
                                 verbose=0, random_seed=0, thread_count=4, allow_writing_files=False)
    if kind == "rf":
        return RandomForestRegressor(n_estimators=150, min_samples_leaf=3, max_features=0.5, n_jobs=-1, random_state=0)
    return ExtraTreesRegressor(n_estimators=300, min_samples_leaf=2, max_features=0.5, n_jobs=-1, random_state=0)   # = benchmark10.py

def prep(kind, Xa):
    return Xa if kind == "catboost" else np.where(np.isnan(Xa), -1.0, Xa)   # trees: NaN -> -1 (same in JS)

def half_paper(g, seed):
    rng = np.random.default_rng(seed); tr, te = [], []
    for p in np.unique(g):
        idx = rng.permutation(np.where(g == p)[0])
        if len(idx) < 2: tr += list(idx); continue
        h = len(idx) // 2; tr += list(idx[:h]); te += list(idx[h:])
    return np.array(tr), np.array(te)

r4 = lambda v: float(f"{v:.5g}")
r7 = lambda v: float(f"{v:.8g}")              # split thresholds: keep enough digits to match Python exactly
out = {"version": pd.Timestamp.now().strftime("%Y-%m-%d"), "features": FEATURES,
       "materials": [{k: m[k] for k in ("name", "key", "group")} for m in M21], "targets": {}}
tests = {"features": FEATURES, "rows": []}

for key, s in SPEC.items():
    y = Y[key]
    m = y.notna().values
    Xa = X[m].values.astype(float); ya = y[m].values; ga = groups[m].values
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
            trees.append({"s": [[sp["float_feature_index"], r7(sp["border"])] for sp in t["splits"]],
                          "v": [r4(v) for v in t["leaf_values"]]})
        sb = cb.get("scale_and_bias", [1, [0]])
        entry.update(trees=trees, scale=sb[0], bias=float(np.ravel(sb[1])[0]),
                     nan=[nan_mode.get(i, "AsIs") for i in range(len(FEATURES))])
    else:
        trees = []
        for est in mdl.estimators_:
            t = est.tree_
            trees.append({"f": t.feature.tolist(), "t": [r7(v) for v in t.threshold],
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

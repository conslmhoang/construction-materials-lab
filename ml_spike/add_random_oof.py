"""Add random-split (10-fold, seed 0) out-of-fold predictions to bench10/benchmark10.json,
so the web parity plot shows the same validation as the headline R².
Usage: python add_random_oof.py "../03 Dataset_ratio.xlsx" bench10
"""
import os, json
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, "benchmark10.py"), encoding="utf-8").read()
exec(src.split("cols = [list(X.columns)")[0])        # data, MODELS, TARGETS, F, run()

cols = [list(X.columns).index(f) for f in FEATURES]
path = os.path.join(OUT, "benchmark10.json")
web = json.load(open(path, encoding="utf-8"))
for key, (label, unit, col) in TARGETS.items():
    m = F[f"use_{key}"].values.astype(bool) & np.isfinite(N(col).values)
    Xa = X.loc[m].values.astype(float)[:, cols]; ya = N(col).values[m]
    assert len(ya) == len(web["targets"][key]["y"])
    web["targets"][key]["oof_random"] = {}
    for mname, (family, mk) in MODELS.items():
        ii, pp = run(Xa, ya, list(KFold(10, shuffle=True, random_state=0).split(Xa)), mk)
        o = np.full(len(ya), np.nan); o[ii] = pp
        web["targets"][key]["oof_random"][mname] = [round(float(v), 3) for v in o]
        print(key, mname, round(r2_score(ya, o), 3), flush=True)
json.dump(web, open(path, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("updated", path)

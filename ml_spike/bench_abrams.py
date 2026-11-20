"""Fair comparison: every one of the 10 models with and without the Abrams curve (compressive strength).
Abrams version: log fc = a + k * W/P fitted on the training fold; the model learns log fc - (a + k * W/P);
prediction = exp(model + curve). W/P = water / (cement + FA + GGBS + SF + MK + LP) = Water / (1 + SF + MK + LP).
Scores: 10-fold random CV x 3 seeds (headline) and 10-fold by paper (new lab).
Writes bench10/bench_abrams.csv
"""
import os, time
import numpy as np, pandas as pd
from sklearn.model_selection import KFold, GroupKFold
from sklearn.metrics import r2_score, mean_absolute_error
from web_data import load, TARGET_FEATURES
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "benchmark10.py"), encoding="utf-8").read()
B = {"__file__": os.path.abspath(__file__)}; exec(_src[:_src.index("TARGETS =")], B)   # MODELS dict with exactly the settings of benchmark10.py
B = type("B", (), {"MODELS": B["MODELS"]})

X, Y, groups = load()
feats = TARGET_FEATURES["fc"]; m = Y["fc"].notna().values
A = X.loc[m, feats].values.astype(float); y = Y["fc"].values[m]; g = groups[m].values
wi = [feats.index(f) for f in ("Water", "SF", "MK", "LP")]
wp = lambda Z: Z[:, wi[0]] / (1 + np.nansum(Z[:, wi[1:]], axis=1))

def run(splits, mk, abrams):
    pp = np.zeros(len(y))
    for tr, te in splits:
        keep = ~np.all(np.isnan(A[tr]), axis=0)
        if abrams:
            k, a = np.polyfit(wp(A[tr]), np.log(y[tr]), 1)
            mdl = mk().fit(A[tr][:, keep], np.log(y[tr]) - a - k * wp(A[tr]))
            pp[te] = np.exp(mdl.predict(A[te][:, keep]) + a + k * wp(A[te]))
        else:
            pp[te] = mk().fit(A[tr][:, keep], y[tr]).predict(A[te][:, keep])
    return pp

rows = []
for name, (fam, mk) in B.MODELS.items():
    for ab in (False, True):
        t0 = time.time()
        r2s, maes = [], []
        for sd in range(3):
            pp = run(KFold(10, shuffle=True, random_state=sd).split(A), mk, ab)
            r2s.append(r2_score(y, pp)); maes.append(mean_absolute_error(y, pp))
        pg = run(GroupKFold(10, shuffle=True, random_state=0).split(A, y, g), mk, ab)
        rows.append(dict(model=name, abrams=ab, R2=np.mean(r2s), MAE=np.mean(maes), R2_newlab=r2_score(y, pg),
                         MAE_newlab=mean_absolute_error(y, pg)))
        print(f"{name:18s} abrams={ab!s:5s} R2={np.mean(r2s):.3f} MAE={np.mean(maes):.2f} newlab R2={rows[-1]['R2_newlab']:.3f} ({time.time()-t0:.0f}s)", flush=True)
pd.DataFrame(rows).round(4).to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bench10", "bench_abrams.csv"), index=False)

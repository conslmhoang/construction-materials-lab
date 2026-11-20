"""Physics check of each model, with and without the Abrams curve (fc):
 1) the user's ECC-PE lab mix at W/B 0.25 / 0.30 / 0.358 / 0.45 (measured 47.4 MPa at 0.358);
 2) on all data rows: share of rows whose prediction does NOT drop when water rises by +0.05 (10-fold, out-of-fold).
"""
import os, numpy as np, pandas as pd
from sklearn.model_selection import KFold
from web_data import load, features, densities, TARGET_FEATURES, M21
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "benchmark10.py"), encoding="utf-8").read()
B = {"__file__": os.path.abspath(__file__)}; exec(_src[:_src.index("TARGETS =")], B); MODELS = B["MODELS"]

X, Y, g = load(); F = TARGET_FEATURES["fc"]; m = Y["fc"].notna().values
A = X.loc[m, F].values.astype(float); y = Y["fc"].values[m]
wi = [F.index(f) for f in ("Water", "SF", "MK", "LP")]
wp = lambda Z: Z[:, wi[0]] / (1 + np.nansum(Z[:, wi[1:]], axis=1))
row = {mm["name"]: 0.0 for mm in M21}
row.update({"Cement (OPC)": .313, "GGBS (slag)": .113, "Fly ash (FA)": .574, "Silica fume (SF)": .19, "Sand": .53, "Water": .358,
            "Superplasticizer (SP)": .014, "PE fiber": 1.74, "Curing method": "Water curing", "Curing temperature (°C)": 20,
            "Curing duration (days)": 28, "Test age (days)": 28})
WB = (0.25, 0.30, 0.358, 0.45)
U = features(pd.DataFrame([{**row, "Water": w} for w in WB]), densities())[F].values.astype(float)

class Fit:
    def __init__(s, mk, ab): s.mk, s.ab = mk, ab
    def fit(s, Z, t):
        s.keep = ~np.all(np.isnan(Z), axis=0)
        if s.ab: s.k, s.a = np.polyfit(wp(Z), np.log(t), 1); t = np.log(t) - s.a - s.k * wp(Z)
        s.m = s.mk().fit(Z[:, s.keep], t); return s
    def predict(s, Z):
        p = s.m.predict(Z[:, s.keep]); return np.exp(p + s.a + s.k * wp(Z)) if s.ab else p

def up(Z):
    Z = Z.copy(); Z[:, wi[0]] += 0.05; return Z

rows = []
for name, (_, mk) in MODELS.items():
    for ab in (False, True):
        flat = np.zeros(len(y), bool)
        for tr, te in KFold(10, shuffle=True, random_state=0).split(A):
            f = Fit(mk, ab).fit(A[tr], y[tr]); flat[te] = f.predict(up(A[te])) >= f.predict(A[te]) - 1e-9
        pu = Fit(mk, ab).fit(A, y).predict(U)
        rows.append(dict(model=name, abrams=ab, **{f"WB {w}": round(float(v), 1) for w, v in zip(WB, pu)},
                         no_drop_pct=round(100 * flat.mean(), 1)))
        print(rows[-1], flush=True)
pd.DataFrame(rows).to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bench10", "abrams_check.csv"), index=False)

"""Fair check of the audit: 10-fold CV x 3 seeds on the old and on the corrected dataset, scored only on rows the
audit did NOT touch (same rows, same values in both). Usage: python audit/fair_compare.py <old 04 xlsx>"""
import os, sys, json, numpy as np, pandas as pd
from sklearn.model_selection import KFold
from sklearn.ensemble import ExtraTreesRegressor
from web_data import load, TARGET_FEATURES, DATA
here = os.path.dirname(os.path.abspath(__file__))
COR = json.load(open(os.path.join(here, "corrections.json"), encoding="utf-8")); touched = {c["excel_row"] for c in COR}
old = pd.read_excel(sys.argv[1], sheet_name="Data"); old["_row"] = old.index + 2
key = lambda D: D["DOI"].astype(str) + "|" + D["Tensile strain capacity (%)"].astype(str) + "|" + D["Compressive strength (MPa)"].astype(str) + "|" + D["Water"].round(4).astype(str) + "|" + D["Sand"].round(4).astype(str) + "|" + D["Test age (days)"].astype(str)
Xo, Yo, _ = load(sys.argv[1]); Xn, Yn, _ = load(DATA)
new = pd.read_excel(DATA, sheet_name="Data")
untouched_keys = set(key(old[~old._row.isin(touched)]))
def cv(X, Y, Dk, tgt, mk):
    F = TARGET_FEATURES[tgt]; m = Y[tgt].notna().values
    A = X.loc[m, F].values.astype(float); y = Y[tgt].values[m]; u = Dk[m].isin(untouched_keys).values
    if tgt == "fc":
        wi = [F.index(f) for f in ("Water", "SF", "MK", "LP")]; wp = A[:, wi[0]] / (1 + np.nansum(A[:, wi[1:]], axis=1))
    A = np.nan_to_num(A, nan=-1.0); maes = []
    for sd in range(3):
        p = np.zeros(len(y))
        for tr, te in KFold(10, shuffle=True, random_state=sd).split(A):
            if tgt == "fc":
                k, a = np.polyfit(wp[tr], np.log(y[tr]), 1)
                p[te] = np.exp(mk().fit(A[tr], np.log(y[tr]) - a - k * wp[tr]).predict(A[te]) + a + k * wp[te])
            else: p[te] = mk().fit(A[tr], y[tr]).predict(A[te])
        maes.append(np.abs(p - y)[u].mean())
    return np.mean(maes), u.sum()
mk = lambda: ExtraTreesRegressor(300, min_samples_leaf=2, max_features=0.5, n_jobs=-1, random_state=0)
for t in ("eps", "fc"):
    a, na = cv(Xo, Yo, key(old), t, mk); b, nb = cv(Xn, Yn, key(new), t, mk)
    print(f"{t}: MAE on untouched rows  old data {a:.3f} (n={na})  corrected data {b:.3f} (n={nb})")

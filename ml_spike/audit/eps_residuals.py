"""Out-of-fold strain residuals (Extra Trees 300, 10-fold random, same settings as the web model). Writes audit/eps_oof.csv and audit/eps_papers.csv"""
import os, numpy as np, pandas as pd
from sklearn.model_selection import KFold
from sklearn.ensemble import ExtraTreesRegressor
from web_data import load, TARGET_FEATURES, DATA
here = os.path.dirname(os.path.abspath(__file__))
X, Y, g = load(); F = TARGET_FEATURES["eps"]; m = Y["eps"].notna().values
A = np.nan_to_num(X.loc[m, F].values.astype(float), nan=-1.0); y = Y["eps"].values[m]
p = np.zeros(len(y))
for tr, te in KFold(10, shuffle=True, random_state=0).split(A):
    p[te] = ExtraTreesRegressor(300, min_samples_leaf=2, max_features=0.5, n_jobs=-1, random_state=0).fit(A[tr], y[tr]).predict(A[te])
D = pd.read_excel(DATA, sheet_name="Data")
R = D.loc[m].copy(); R["row"] = np.where(m)[0] + 2; R["pred"] = p.round(2); R["err"] = (p - y).round(2); R["abserr"] = np.abs(p - y).round(2)
R.to_csv(os.path.join(here, "eps_oof.csv"), index=False)
P = R.groupby("Paper").agg(n=("abserr", "size"), mae=("abserr", "mean"), bias=("err", "mean"), sum_abs=("abserr", "sum"),
                           eps_min=("Tensile strain capacity (%)", "min"), eps_max=("Tensile strain capacity (%)", "max"), doi=("DOI", "first"))
P = P.sort_values("sum_abs", ascending=False); P.to_csv(os.path.join(here, "eps_papers.csv"))
print("MAE", np.abs(p - y).mean().round(3), "rows", len(y), "papers", len(P))
print("share of total abs error from top 25 papers:", (P.sum_abs.head(25).sum() / P.sum_abs.sum()).round(3))
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 45)
print(P.head(30).round(2))

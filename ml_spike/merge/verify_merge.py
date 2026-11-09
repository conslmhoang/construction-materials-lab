import sys, os, numpy as np, pandas as pd
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(here, "spike.py"), encoding="utf-8").read().split("lines, curves = [], {}")[0]
def load(argv):
    sys.argv = argv; g = {}
    exec(src, g); return g
old = load(["x", sys.argv[1], ".", "additions"])          # backup workbook + CSV additions
new = load(["x", "../03 Dataset_ratio.xlsx", "."])        # merged workbook only
print("rows old/new:", len(old["X"]), len(new["X"]))
Xo, Xn = old["X"].astype(float).values, new["X"].astype(float).values
same = np.isclose(Xo, Xn, equal_nan=True, rtol=1e-9, atol=1e-12)
print("feature cells identical:", same.all(), " mismatching cells:", (~same).sum())
if not same.all():
    r, c = np.where(~same); print([(int(a), old["X"].columns[b], Xo[a, b], Xn[a, b]) for a, b in list(zip(r, c))[:10]])
for col in (389, 404, 418):
    a, b = old["N"](col).values, new["N"](col).values
    print("target col", col, "identical:", np.allclose(a, b, equal_nan=True))
print("papers old/new:", old["groups_all"].nunique(), new["groups_all"].nunique())
print("same paper grouping:", (old["groups_all"].values == new["groups_all"].values).all())

print("\n-- order-independent comparison --")
def table(g):
    t = g["X"].astype(float).copy()
    t["fc"], t["ft"], t["eps"] = g["N"](389).values, g["N"](404).values, g["N"](418).values
    t["paper"] = g["groups_all"].astype(str).str.strip().values
    t["ttype"] = g["T"](363).values
    return t.round(6).fillna(-999)
A, B = table(old), table(new)
key = list(A.columns)
A = A.sort_values(key).reset_index(drop=True); B = B.sort_values(key).reset_index(drop=True)
eq = (A.values == B.values)
print("all cells identical after sorting:", eq.all(), " mismatching cells:", (~eq).sum())
if not eq.all():
    r, c = np.where(~eq); print([(A.columns[b], A.iat[a, b], B.iat[a, b]) for a, b in list(zip(r, c))[:10]])

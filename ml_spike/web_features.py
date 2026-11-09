"""Compare feature sets under leave-paper-out CV:
   ALL      – every engineered feature
   PRUNED   – top-k by held-out importance (feature_selection.json)
   WEB      – only what the web calculator can supply: its mix components (ratios),
              fibre vol% + fibre properties, curing/test conditions, and values derived from them.
Usage: python web_features.py "../03 Dataset_ratio.xlsx" <outdir> additions
"""
import sys, os, json
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, "spike.py"), encoding="utf-8").read()
exec(src.split("lines, curves = [], {}")[0])
from sklearn.model_selection import GroupKFold

WEB = [
    # binder composition (mass fraction of binder) — materials in the web database
    "OPC", "GGBS", "FA", "SF", "MK", "LP",
    # activators / ratios to binder
    "WG_B", "NaOH_B", "CaOH2_B", "Na2SO4_B", "SSM_B",
    "W_B", "Sand_B", "QP_B", "Light_B", "SP_B", "VMA_B",
    # fibres
    "V_PE", "V_PVA", "V_Steel", "V_PBO", "V_total",
    "Fib_L_mm", "Fib_d_um", "Fib_ft_MPa", "Fib_E_GPa",
    # curing / test conditions
    "Cure_T", "Cure_days", "Cure_RH", "Age_days", "Cure_water", "Cure_sealed", "Cure_heat",
    "Comp_size_mm", "Comp_cyl",
    # derived from the above (web computes kg/m3 exactly)
    "W_C", "Activator_tot", "Fib_index", "Paste_vol", "Binder_kgm3",
]
sel = json.load(open(os.path.join(here, "feature_selection.json"), encoding="utf-8"))
names = list(X.columns)
assert all(f in names for f in WEB), [f for f in WEB if f not in names]

def cv(Xa, y, g, cols):
    r2, mae = [], []
    for s in range(5):
        pred = np.zeros(len(y))
        for tr, te in GroupKFold(10, shuffle=True, random_state=s).split(Xa, y, g):
            pred[te] = fp(Xa[tr][:, cols], y[tr], Xa[te][:, cols])
        r2.append(r2_score(y, pred)); mae.append(mean_absolute_error(y, pred))
    return np.mean(r2), np.std(r2), np.mean(mae)

for tname, (y, mask) in targets.items():
    m = mask & y.notna()
    Xa = X[m].values.astype(float); ya = y[m].values; ga = groups_all[m].values
    sets = {"ALL": list(range(len(names))),
            "PRUNED": [names.index(f) for f in sel[tname]["picked"]],
            "WEB": [names.index(f) for f in WEB]}
    # WEB minus features with <= 0 held-out importance in the ranking
    rank = dict(sel[tname]["ranking"])
    sets["WEB-lean"] = [names.index(f) for f in WEB if rank.get(f, 0) > 0]
    for k, cols in sets.items():
        r2, sd, mae = cv(Xa, ya, ga, cols)
        print(f"{tname:18s} {k:9s} ({len(cols):2d} feats): R2={r2:.3f}±{sd:.3f}  MAE={mae:.2f}", flush=True)
    print("   WEB-lean keeps:", ", ".join(names[c] for c in sets["WEB-lean"]))

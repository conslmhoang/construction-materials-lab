"""Before/after cleaning: CatBoost, web inputs, paper held out vs half of each paper known.
Usage: python clean/eval_clean.py "../03 Dataset_ratio.xlsx" clean additions
"""
import sys, os
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(here, "spike.py"), encoding="utf-8").read()
exec(src.split("lines, curves = [], {}")[0])
from sklearn.model_selection import GroupKFold
from catboost import CatBoostRegressor

F = pd.read_csv(os.path.join(OUT, "dataset_clean.csv"), encoding="utf-8-sig")
assert len(F) == len(X)
FEAT = ["OPC", "GGBS", "FA", "SF", "MK", "LP", "WG_B", "NaOH_B", "CaOH2_B", "Na2SO4_B", "SSM_B",
        "W_B", "Sand_B", "QP_B", "Light_B", "SP_B", "VMA_B", "V_PE", "V_PVA", "V_Steel", "V_PBO", "V_total",
        "Cure_T", "Cure_days", "Cure_RH", "Age_days", "Cure_water", "Cure_sealed", "Cure_heat",
        "W_C", "Activator_tot", "Paste_vol", "Binder_kgm3"]
cb = lambda: CatBoostRegressor(iterations=800, depth=4, learning_rate=0.05, l2_leaf_reg=3, verbose=0, random_seed=0, thread_count=4)
std = targets["fc (MPa)"][1].values
Y = {"fc": N(389).values, "ft": N(404).values, "eps": N(418).values}
OLD = {"fc": std & np.isfinite(Y["fc"]), "ft": targets["ft direct (MPa)"][1].values & np.isfinite(Y["ft"]),
       "eps": targets["eps_tu direct (%)"][1].values & np.isfinite(Y["eps"])}

def evaluate(m, y):
    Xa = X.loc[m, FEAT].values.astype(float); ya = y[m]; ga = groups_all[m].values
    po, hp = [], []
    for s in (0, 1, 2):
        pred = np.zeros(len(ya))
        for tr, te in GroupKFold(10, shuffle=True, random_state=s).split(Xa, ya, ga):
            pred[te] = cb().fit(Xa[tr], ya[tr]).predict(Xa[te])
        po.append((r2_score(ya, pred), mean_absolute_error(ya, pred), np.median(np.abs(pred - ya) / ya) * 100))
        rng = np.random.default_rng(s); tr, te = [], []
        for p in np.unique(ga):
            ii = rng.permutation(np.where(ga == p)[0])
            if len(ii) < 2: tr += list(ii); continue
            h = len(ii) // 2; tr += list(ii[:h]); te += list(ii[h:])
        p_ = cb().fit(Xa[tr], ya[tr]).predict(Xa[te])
        hp.append((r2_score(ya[te], p_), mean_absolute_error(ya[te], p_), np.median(np.abs(p_ - ya[te]) / ya[te]) * 100))
    return int(m.sum()), len(np.unique(ga)), np.mean(po, 0), np.mean(hp, 0)

rows = []
for t in ["fc", "ft", "eps"]:
    for lab, m in [("before", OLD[t]), ("after", F[f"use_{t}"].values)]:
        n, npap, po, hp = evaluate(m, Y[t])
        print(f"{t:4s} {lab:6s} rows={n:5d} papers={npap:3d} | new lab R2={po[0]:.2f} MAE={po[1]:.2f} err={po[2]:.0f}% "
              f"| lab known R2={hp[0]:.2f} MAE={hp[1]:.2f} err={hp[2]:.0f}%", flush=True)
        rows.append(dict(target=t, data=lab, rows=n, papers=npap, R2_new_lab=round(po[0], 3), MAE_new_lab=round(po[1], 2),
                         R2_lab_known=round(hp[0], 3), MAE_lab_known=round(hp[1], 2)))
pd.DataFrame(rows).to_csv(os.path.join(OUT, "before_after.csv"), index=False, encoding="utf-8-sig")

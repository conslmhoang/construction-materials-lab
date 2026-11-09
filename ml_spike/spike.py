"""THROWAWAY SPIKE: how well can we predict fc / ft / eu from 03 Dataset_ratio.xlsx today?"""
import sys, re, warnings
import numpy as np, pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import GroupKFold, KFold
from sklearn.metrics import r2_score, mean_absolute_error
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")

XLSX, OUT = sys.argv[1], sys.argv[2]
raw = pd.read_excel(XLSX, "Dataset", header=None)
d = raw.iloc[2:].reset_index(drop=True)
d.columns = range(raw.shape[1])
d[0] = d[0].ffill()
d = d[d.iloc[:, 4:].notna().any(axis=1)].reset_index(drop=True)
d["_new"] = 0; d["_file"] = "03 Dataset_ratio.xlsx"
d["_notes"] = d[771].fillna("").astype(str) + " " + d[772].fillna("").astype(str)   # AI-derived + verify flag
d["_src"] = d[770].fillna("").astype(str)
d.loc[d[769].astype(str).str.startswith("[Agent-extracted"), "_file"] = d[769].astype(str).str.extract(r", ([^;]+.csv);")[0]
import glob, os
hdr = raw.iloc[1].astype(str).tolist()
ADD = sys.argv[3] if len(sys.argv) > 3 else None
if ADD:
    for f in glob.glob(os.path.join(ADD, "*.csv")):
        if os.path.basename(f) == "TEMPLATE.csv": continue
        a = pd.read_csv(f, encoding="utf-8-sig")
        if a.empty: continue
        rows = pd.DataFrame(np.nan, index=range(len(a)), columns=d.columns, dtype=object)
        for c in a.columns:
            if c in hdr: rows[hdr.index(c)] = a[c].values
        rows["_new"] = 1; rows["_file"] = os.path.basename(f)
        rows["_notes"] = a["Conversions / notes"].astype(str).values if "Conversions / notes" in a else ""
        rows["_src"] = a["Source table/page"].astype(str).values if "Source table/page" in a else ""
        d = pd.concat([d, rows], ignore_index=True)
    print("rows after additions:", len(d), " new rows:", int(d["_new"].sum()))
N = lambda i: pd.to_numeric(d[i], errors="coerce")
Z = lambda idx: sum(N(i).fillna(0) for i in idx)
T = lambda i: d[i].astype(str).str.lower().where(d[i].notna(), "")

X = pd.DataFrame(index=d.index)
# binder fractions
for name, i in dict(OPC=4, SAC=5, CAC=6, GGBS=7, FA=8, SF=9, MK=10, LP=11, Diatomite=12, NanoSi=13,
                    RecycledPowder=14, Dolomite=15, PondAsh=16, OtherB=17, RHA=18, MgO=37, CKD=55).items():
    X[name] = N(i).fillna(0)
# activator
for name, i in dict(WG=67, NaOH=68, CaOH2=69, Na2SO4=70, SSM=71, Na2CO3=72, Na2O=73).items():
    X[name + "_B"] = N(i).fillna(0)
X["Ms"], X["NaOH_M"] = N(74), N(75)
# mix ratios
X["W_B"] = N(83).fillna(N(134)).fillna(N(85))
X["Sand_B"] = Z([86, 87, 90, 91, 92, 93, 94, 95, 97, 161, 174, 181])
X["QP_B"] = N(104).fillna(0)
X["Light_B"] = Z([102, 103, 105, 106, 107, 139])
X["Coarse_B"] = N(148).fillna(0)
X["SP_B"] = N(110).fillna(N(116)).fillna(N(172))
X["VMA_B"] = Z([117, 118])
X["SandMax_um"] = N(98)
X["Binder_kgm3"] = N(154)
# fibres (vol%)
fib = dict(PE=[182], PVA=[189], Steel=[199, 206, 207, 281, 282, 289], PP=[217], Glass=[227], PET=[235],
           Basalt=[242], Carbon=[295], PBO=[211], Other=[241, 271, 303, 313])
for k, idx in fib.items():
    X["V_" + k] = Z(idx)
X["V_total"] = X[[c for c in X if c.startswith("V_")]].sum(axis=1)
X.loc[X["V_total"] == 0, "V_total"] = N(302).fillna(0)
# dominant fibre geometry: PE/PVA/steel
L = N(184).fillna(N(191)).fillna(N(201)).fillna(N(218))
D = N(185).fillna(N(192)).fillna(N(202)).fillna(N(219))
X["Fib_L_mm"], X["Fib_d_um"] = L, D
X["Fib_ft_MPa"] = N(186).fillna(N(193)).fillna(N(203))
X["Fib_E_GPa"] = N(187).fillna(N(194)).fillna(N(204))
# processing
X["Cure_T"] = N(329)
X["Cure_days"] = N(328)
X["Cure_RH"] = N(330)
X["Heat_h"] = N(345)
X["Age_days"] = N(341).fillna(N(328))
cm = T(327)
X["Cure_water"] = cm.str.contains("water").astype(int)
X["Cure_sealed"] = cm.str.contains("seal|wrap|plastic").astype(int)
X["Cure_heat"] = cm.str.contains("heat|steam|oven|°c").astype(int) * (N(329).fillna(20) > 40)
# specimen size (first number)
X["Comp_size_mm"] = pd.to_numeric(T(358).str.extract(r"(\d+\.?\d*)")[0], errors="coerce")
X["Comp_cyl"] = T(357).str.contains("cyl").astype(int)

# physics-derived: estimated binder content (absolute volume), paste/water indices
dens = dict(OPC=3.15, SAC=2.9, CAC=3.0, GGBS=2.9, FA=2.3, SF=2.2, MK=2.5, LP=2.7, Diatomite=2.1, NanoSi=2.2,
            RecycledPowder=2.6, Dolomite=2.8, PondAsh=2.2, OtherB=2.6, RHA=2.1, MgO=3.5, CKD=2.7)
fr = X[list(dens)].sum(axis=1).replace(0, np.nan)
vb = sum(X[k] / v for k, v in dens.items()) / fr            # m3*1000 per tonne binder -> L/kg
vol_per_kg = (vb + X["W_B"].fillna(0.3) + X["Sand_B"] / 2.65 + X["QP_B"] / 2.65 + X["Coarse_B"] / 2.7
              + X["WG_B"] / 1.5 + X["NaOH_B"] / 2.1 + X["Light_B"] / 0.8) / 1000
X["B_est_kgm3"] = ((1 - X["V_total"] / 100 - 0.02) / vol_per_kg).where(fr.notna())
X["Binder_kgm3"] = X["Binder_kgm3"].fillna(X["B_est_kgm3"])
X["W_C"] = X["W_B"] / X["OPC"].replace(0, np.nan)
X["Paste_vol"] = (vb + X["W_B"].fillna(0.3)) / 1000 * X["B_est_kgm3"]
X["Fib_index"] = X["V_total"] * X["Fib_L_mm"] / (X["Fib_d_um"] / 1000)
X["logAge"] = np.log1p(X["Age_days"])
X["Activator_tot"] = X[["WG_B", "NaOH_B", "CaOH2_B", "Na2SO4_B", "SSM_B", "Na2CO3_B"]].sum(axis=1)

# --- filter to "standard" condition rows (no fire, freeze-thaw, dynamic, carbonation, wet-dry, pre-crack)
expT = N(331)
special = ((expT > 40) | N(342).notna() | N(351).notna() | N(353).notna() | N(352).notna() |
           T(369).str.contains("dyn|shpb") | N(370).notna() | N(333).notna() | N(347).notna() |
           N(334).notna())
std = ~special
tt = T(363)
direct = tt.str.contains("direct|uniaxial") & ~tt.str.contains("split|flex")
targets = {
    "fc (MPa)": (N(389), std),
    "ft direct (MPa)": (N(404), std & direct),
    "eps_tu direct (%)": (N(418), std & direct),
}
groups_all = d[0].astype(str)

def model():
    return HistGradientBoostingRegressor(max_iter=400, learning_rate=0.05, max_leaf_nodes=8, max_depth=3,
                                         min_samples_leaf=10, l2_regularization=1.0, random_state=0)

def fp(Xtr, ytr, Xte):
    keep = ~np.all(np.isnan(Xtr), axis=0)
    return model().fit(Xtr[:, keep], ytr).predict(Xte[:, keep])

lines, curves = [], {}
rng = np.random.default_rng(0)
for tname, (y, mask) in targets.items():
    m = mask & y.notna()
    Xm, ym, gm = X[m].values.astype(float), y[m].values, groups_all[m].values
    papers = np.unique(gm)
    # leave-paper-out CV (10 folds)
    pred = np.zeros_like(ym, dtype=float)
    for tr, te in GroupKFold(n_splits=10).split(Xm, ym, gm):
        pred[te] = fp(Xm[tr], ym[tr], Xm[te])
    # optimistic random CV (mixes from same paper in train & test)
    pr = np.zeros_like(pred)
    for tr, te in KFold(10, shuffle=True, random_state=0).split(Xm):
        pr[te] = fp(Xm[tr], ym[tr], Xm[te])
    base = np.full_like(pred, ym.mean())
    orig = (d.loc[m, "_new"].values == 0)
    lines.append(f"   [original-rows only] R2={r2_score(ym[orig], pred[orig]):.2f} MAE={mean_absolute_error(ym[orig], pred[orig]):.2f}")
    lines.append(f"{tname}: n={m.sum()} rows, {len(papers)} papers, mean={ym.mean():.2f}\n"
                 f"   leave-paper-out : R2={r2_score(ym, pred):.2f}  MAE={mean_absolute_error(ym, pred):.2f}"
                 f"  MAPE={np.median(np.abs(pred-ym)/ym)*100:.0f}% (median)\n"
                 f"   random-row CV   : R2={r2_score(ym, pr):.2f}  MAE={mean_absolute_error(ym, pr):.2f}   (optimistic)\n"
                 f"   predict-mean    : MAE={mean_absolute_error(ym, base):.2f}")
    # learning curve: train on k papers, test on held-out papers
    ks = sorted(set([int(x) for x in np.linspace(8, int(len(papers) * 0.8), 7)]))
    res = []
    for k in ks:
        sc = []
        for rep in range(25):
            perm = rng.permutation(papers)
            trp, tep = set(perm[:k]), set(perm[int(len(papers) * 0.8):])
            tr = np.array([g in trp for g in gm]); te = np.array([g in tep for g in gm])
            if te.sum() < 5: continue
            p = fp(Xm[tr], ym[tr], Xm[te])
            sc.append(mean_absolute_error(ym[te], p))
        res.append((k, np.mean(sc), np.std(sc)))
    curves[tname] = (res, ym.mean())
    # feature importance proxy: drop-column not cheap; use permutation on full fit
    from sklearn.inspection import permutation_importance
    full = model().fit(Xm, ym)
    pi = permutation_importance(full, Xm, ym, n_repeats=5, random_state=0)
    top = np.argsort(-pi.importances_mean)[:8]
    lines.append("   top features: " + ", ".join(X.columns[i] for i in top))
    # parity plot
    plt.figure(figsize=(4, 4)); plt.scatter(ym, pred, s=8, alpha=.6)
    lo, hi = ym.min(), ym.max(); plt.plot([lo, hi], [lo, hi], "k--", lw=1)
    plt.xlabel("measured"); plt.ylabel("predicted (paper held out)"); plt.title(tname)
    plt.tight_layout(); plt.savefig(f"{OUT}/parity_{tname.split()[0]}.png", dpi=110); plt.close()

fig, axs = plt.subplots(1, 3, figsize=(12, 3.6))
for ax, (tname, (res, mu)) in zip(axs, curves.items()):
    k, m_, s_ = zip(*res)
    rel = np.array(m_) / mu * 100
    ax.errorbar(k, rel, yerr=np.array(s_) / mu * 100, marker="o", capsize=3)
    ax.set_title(tname); ax.set_xlabel("# papers in training"); ax.set_ylabel("MAE on unseen papers (% of mean)")
    ax.grid(alpha=.3)
plt.tight_layout(); plt.savefig(f"{OUT}/learning_curves.png", dpi=110)
for tname, (res, mu) in curves.items():
    lines.append(f"curve {tname}: " + "  ".join(f"{k}p→{m/mu*100:.0f}%" for k, m, s in res))
print("\n".join(lines))

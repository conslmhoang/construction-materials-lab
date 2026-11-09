"""Data-cleaning audit: flags every row (never deletes) and writes clean/flags.csv.
Usage: python clean/audit.py "../03 Dataset_ratio.xlsx" clean additions
"""
import sys, os, re
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(here, "spike.py"), encoding="utf-8").read()
exec(src.split("lines, curves = [], {}")[0])          # d, X, targets, groups_all, N, T, model, fp
from sklearn.model_selection import GroupKFold
from catboost import CatBoostRegressor

notes = (d["_notes"].astype(str) + " " + d["_src"].astype(str)).str.lower()
title = d[0].astype(str)
fc, ft, eps = N(389), N(404), N(418)

# ---------------------------------------------------------- 1. tension test type
raw_tt = T(363)
def tension_type(s):
    if not s: return ""
    if re.search(r"split|brazil", s): return "splitting"
    if re.search(r"flex|bend|point|mor\b|modulus of rupture", s): return "flexural"
    if re.search(r"notch", s): return "direct-notched"
    if re.search(r"direct|uniaxial|dog|dumb|bone|briquet|centric|coupon|axial tens|figure-eight|plate", s): return "direct"
    return "other:" + s[:30]
ttype = raw_tt.map(tension_type)
F = pd.DataFrame({"file": d["_file"], "paper": title.str[:90], "doi": d[3].astype(str).str[:60],
                  "fc": fc, "ft": ft, "eps": eps, "tension_raw": raw_tt.str[:50], "tension_type": ttype})
# DOI is only on the first row of a paper in the original workbook
F["doi"] = F["doi"].replace("nan", np.nan)
F["doi"] = F.groupby("paper")["doi"].transform(lambda s: s.ffill().bfill())

# ---------------------------------------------------------- 2. flags
F["flag_verify"] = notes.str.contains("verify")
F["flag_no_wb"] = X["W_B"].isna()
F["flag_no_age"] = X["Age_days"].isna()
bsum = X[["OPC", "SAC", "CAC", "GGBS", "FA", "SF", "MK", "LP", "Diatomite", "NanoSi", "RecycledPowder",
          "Dolomite", "PondAsh", "OtherB", "RHA", "MgO", "CKD"]].sum(axis=1)
F["flag_no_binder"] = bsum < 0.5
F["flag_no_fibre"] = X["V_total"].fillna(0) <= 0
natural = r"banana|kenaf|sisal|jute|date.?palm|coir|hemp|bamboo|natural fib"
F["flag_natural_fibre"] = notes.str.contains(natural) | title.str.lower().str.contains(natural)
F["flag_coarse_agg"] = X["Coarse_B"].fillna(0) > 0.5
F["flag_exotic_binder"] = (X["OtherB"].fillna(0) > 0.5) | (X["CAC"].fillna(0) > 0.5) | title.str.lower().str.contains("magnesium phosphate")
F["flag_special_cond"] = ~targets["fc (MPa)"][1]          # fire / freeze-thaw / dynamic / carbonation etc.

# physics checks
ratio = ft / fc
F["flag_ft_fc_ratio"] = F["tension_type"].eq("direct") & ratio.notna() & ((ratio < 0.015) | (ratio > 0.25))
F["flag_strain_no_fibre"] = eps.gt(0.5) & F["flag_no_fibre"]

# republished data: identical inputs AND identical output in two different papers
key_cols = ["W_B", "Sand_B", "V_total", "OPC", "FA", "GGBS", "SF", "Age_days"]
k = X[key_cols].astype(float).round(3).fillna(-9).map(str).apply(lambda r: "|".join(r), axis=1)
for tgt, y in [("fc", fc), ("ft", ft)]:
    kk = k + "|" + y.round(1).astype(str)
    has = y.notna()
    npap = pd.Series(title.values, index=kk.index)[has].groupby(kk[has]).nunique()
    dup_keys = set(npap[npap > 1].index)
    first_paper = pd.Series(title.values, index=kk.index)[has].groupby(kk[has]).first()
    F[f"flag_dup_{tgt}"] = has & kk.isin(dup_keys) & (title != kk.map(first_paper))

# ---------------------------------------------------------- 3. model-based outliers (half-paper CV)
FEAT = ["OPC", "GGBS", "FA", "SF", "MK", "LP", "WG_B", "NaOH_B", "CaOH2_B", "Na2SO4_B", "SSM_B",
        "W_B", "Sand_B", "QP_B", "Light_B", "SP_B", "VMA_B", "V_PE", "V_PVA", "V_Steel", "V_PBO", "V_total",
        "Cure_T", "Cure_days", "Cure_RH", "Age_days", "Cure_water", "Cure_sealed", "Cure_heat",
        "W_C", "Activator_tot", "Paste_vol", "Binder_kgm3"]
cb = lambda: CatBoostRegressor(iterations=500, depth=4, learning_rate=0.06, verbose=0, random_seed=0, thread_count=4)
for tgt, (y, mask) in [("fc", targets["fc (MPa)"]), ("ft", (ft, targets["ft direct (MPa)"][1]))]:
    m = (mask & y.notna()).values
    Xa = X.loc[m, FEAT].values.astype(float); ya = y[m].values; ga = groups_all[m].values
    pred = np.full(len(ya), np.nan)
    for tr, te in GroupKFold(10, shuffle=True, random_state=0).split(Xa, ya, ga):
        # rows of the test papers: train on the other half of the same paper too (lab known)
        rng = np.random.default_rng(0)
        te = rng.permutation(te); half = len(te) // 2
        for a_, b_ in [(te[:half], te[half:]), (te[half:], te[:half])]:
            mdl = cb().fit(Xa[np.r_[tr, a_]], ya[np.r_[tr, a_]])
            pred[b_] = mdl.predict(Xa[b_])
    lr = np.log(ya / np.clip(pred, 1e-3, None))           # log-ratio residual
    mad = np.median(np.abs(lr - np.median(lr))) * 1.4826
    z = (lr - np.median(lr)) / mad
    F.loc[m, f"pred_{tgt}"] = pred
    F.loc[m, f"z_{tgt}"] = z
    F[f"flag_outlier_{tgt}"] = F[f"z_{tgt}"].abs() > 3.5

flag_cols = [c for c in F if c.startswith("flag_")]
os.makedirs(OUT, exist_ok=True)
F.to_csv(os.path.join(OUT, "flags.csv"), index=False, encoding="utf-8-sig")

print(f"rows: {len(F)}   papers: {F.paper.nunique()}")
print("\n-- tension test type (rows with ft) --")
print(F.loc[ft.notna(), "tension_type"].value_counts().to_string())
print("\n-- flags (rows flagged / rows with fc / with ft) --")
for c in flag_cols:
    print(f"  {c:22s} {int(F[c].sum()):5d}   fc:{int((F[c] & fc.notna()).sum()):4d}  ft:{int((F[c] & ft.notna()).sum()):4d}")
print("\n-- worst outliers --")
for tgt in ["fc", "ft"]:
    o = F[F[f"flag_outlier_{tgt}"]].sort_values(f"z_{tgt}", key=abs, ascending=False).head(12)
    print(f"[{tgt}]"); print(o[["file", "paper", tgt, f"pred_{tgt}", f"z_{tgt}"]].round(2).to_string(index=False))
print("\n-- republished duplicates --")
print(F[F.flag_dup_fc | F.flag_dup_ft][["file", "paper", "fc", "ft"]].to_string(index=False)[:3000])

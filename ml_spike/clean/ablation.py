"""Does each cleaning rule help?  Drop the flagged rows from TRAINING only, and always score on the
same 'core' test rows (rows no rule flags), so every rule is compared on identical test data.
Usage: python clean/ablation.py "../03 Dataset_ratio.xlsx" clean additions
"""
import sys, os
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(here, "spike.py"), encoding="utf-8").read()
exec(src.split("lines, curves = [], {}")[0])
from sklearn.model_selection import GroupKFold
from catboost import CatBoostRegressor

F = pd.read_csv(os.path.join(OUT, "flags.csv"), encoding="utf-8-sig")
assert len(F) == len(X), (len(F), len(X))
FEAT = ["OPC", "GGBS", "FA", "SF", "MK", "LP", "WG_B", "NaOH_B", "CaOH2_B", "Na2SO4_B", "SSM_B",
        "W_B", "Sand_B", "QP_B", "Light_B", "SP_B", "VMA_B", "V_PE", "V_PVA", "V_Steel", "V_PBO", "V_total",
        "Cure_T", "Cure_days", "Cure_RH", "Age_days", "Cure_water", "Cure_sealed", "Cure_heat",
        "W_C", "Activator_tot", "Paste_vol", "Binder_kgm3"]
cb = lambda: CatBoostRegressor(iterations=500, depth=4, learning_rate=0.06, verbose=0, random_seed=0, thread_count=4)

std = targets["fc (MPa)"][1].values
direct_new = F["tension_type"].eq("direct").values
TG = {"fc": (N(389).values, std),
      "ft": (N(404).values, std & direct_new),
      "eps": (N(418).values, std & direct_new)}

outl = F["flag_outlier_fc"].fillna(False).values | F["flag_outlier_ft"].fillna(False).values
RULES = {
    "baseline (all rows)":        np.zeros(len(F), bool),
    "drop VERIFY":                F.flag_verify.values,
    "drop natural fibre":         F.flag_natural_fibre.values,
    "drop coarse aggregate":      F.flag_coarse_agg.values,
    "drop exotic binder":         F.flag_exotic_binder.values,
    "drop no-fibre rows":         F.flag_no_fibre.values,
    "drop missing W/B or age":    (F.flag_no_wb | F.flag_no_age).values,
    "drop model outliers":        outl,
    "drop physics-check fails":   (F.flag_ft_fc_ratio | F.flag_strain_no_fibre).values,
}
if len(sys.argv) > 4 and sys.argv[4] == "combo":
    BASE = RULES
    RULES = {"baseline (all rows)": BASE["baseline (all rows)"],
             "combo fc": BASE["drop no-fibre rows"] | BASE["drop model outliers"] | BASE["drop exotic binder"] | BASE["drop missing W/B or age"],
             "combo ft": BASE["drop coarse aggregate"] | BASE["drop physics-check fails"] | BASE["drop model outliers"],
             "combo eps": BASE["drop model outliers"] | BASE["drop VERIFY"] | BASE["drop physics-check fails"],
             "combo safe (outliers+physics+coarse+exotic)": BASE["drop model outliers"] | BASE["drop physics-check fails"] | BASE["drop coarse aggregate"] | BASE["drop exotic binder"]}
    any_flag = np.zeros(len(F), bool)
    for v in BASE.values(): any_flag |= v
    OUTCSV = "ablation_combo.csv"
else:
    OUTCSV = "ablation.csv"
any_flag = any_flag if "any_flag" in dir() else np.zeros(len(F), bool)
if OUTCSV == "ablation.csv":
    for k, v in RULES.items(): any_flag |= v

res = []
for tname, (y, mask) in TG.items():
    m = mask & np.isfinite(y)
    idx = np.where(m)[0]
    Xa = X.loc[m, FEAT].values.astype(float); ya = y[m]; ga = groups_all[m].values
    core = ~any_flag[m]
    print(f"\n== {tname}: {m.sum()} rows, core test rows {core.sum()}, papers {len(np.unique(ga))}", flush=True)
    for rname, drop in RULES.items():
        keep = ~drop[m]
        sc_po, sc_hp = [], []
        for s in (0, 1):
            pp, yy = [], []
            for tr, te in GroupKFold(10, shuffle=True, random_state=s).split(Xa, ya, ga):
                tr = tr[keep[tr]]; te = te[core[te]]
                if len(te) == 0: continue
                pp += list(cb().fit(Xa[tr], ya[tr]).predict(Xa[te])); yy += list(ya[te])
            sc_po.append((r2_score(yy, pp), mean_absolute_error(yy, pp)))
            # half-paper: each paper split in two; train on half (filtered) + all other papers' halves
            rng = np.random.default_rng(s); tr_, te_ = [], []
            for p in np.unique(ga):
                ii = rng.permutation(np.where(ga == p)[0])
                h = len(ii) // 2; tr_ += list(ii[:h]); te_ += list(ii[h:])
            tr_ = np.array(tr_); te_ = np.array(te_)
            tr_ = tr_[keep[tr_]]; te_ = te_[core[te_]]
            p_ = cb().fit(Xa[tr_], ya[tr_]).predict(Xa[te_])
            sc_hp.append((r2_score(ya[te_], p_), mean_absolute_error(ya[te_], p_)))
        r = dict(target=tname, rule=rname, train_rows=int(keep.sum()),
                 R2_new_lab=round(np.mean([a for a, b in sc_po]), 3), MAE_new_lab=round(np.mean([b for a, b in sc_po]), 2),
                 R2_lab_known=round(np.mean([a for a, b in sc_hp]), 3), MAE_lab_known=round(np.mean([b for a, b in sc_hp]), 2))
        res.append(r)
        print(f"  {rname:44s} train={r['train_rows']:5d}  new-lab R2={r['R2_new_lab']:.3f} MAE={r['MAE_new_lab']:.2f}"
              f"   lab-known R2={r['R2_lab_known']:.3f} MAE={r['MAE_lab_known']:.2f}", flush=True)
pd.DataFrame(res).to_csv(os.path.join(OUT, OUTCSV), index=False, encoding="utf-8-sig")

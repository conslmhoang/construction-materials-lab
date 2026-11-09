"""SHAP analysis for fc / ft / eps_tu models.
Usage: python shap_analysis.py "../03 Dataset_ratio.xlsx" <outdir> additions
Outputs: shap_<target>_beeswarm.png, shap_<target>_dependence.png, shap_importance.csv
"""
import sys, os
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, "spike.py"), encoding="utf-8").read()
exec(src.split("lines, curves = [], {}")[0])      # builds X, targets, groups_all, model()
import shap

names = list(X.columns)
table = {}
for tname, (y, mask) in targets.items():
    tag = tname.split()[0]
    m = mask & y.notna()
    Xs = X[m]
    Xs = Xs.loc[:, (Xs.notna().sum() >= 15) & (Xs.std() > 0)].astype(float)
    mdl = model().fit(Xs.values, y[m].values)
    ex = shap.TreeExplainer(mdl)
    sv = ex(Xs)
    mean_abs = pd.Series(np.abs(sv.values).mean(0), index=Xs.columns).sort_values(ascending=False)
    table[tname] = mean_abs
    print(f"\n== {tname} (n={m.sum()}, base value={float(np.ravel(ex.expected_value)[0]):.2f})")
    for f, v in mean_abs.head(15).items():
        # sign of effect: correlation between feature value and its SHAP
        x = Xs[f].values; s = sv.values[:, list(Xs.columns).index(f)]
        ok = np.isfinite(x)
        rho = np.corrcoef(x[ok], s[ok])[0, 1] if ok.sum() > 3 and np.std(x[ok]) > 0 else np.nan
        print(f"   {f:15s} mean|SHAP|={v:7.3f}   direction: {'↑ value → ↑ prediction' if rho > 0.3 else '↑ value → ↓ prediction' if rho < -0.3 else 'non-monotonic / mixed'} (r={rho:+.2f})")
    plt.figure()
    shap.plots.beeswarm(sv, max_display=15, show=False)
    plt.title(f"SHAP — {tname}"); plt.tight_layout()
    plt.savefig(os.path.join(OUT, f"shap_{tag}_beeswarm.png"), dpi=120, bbox_inches="tight"); plt.close("all")
    top4 = list(mean_abs.index[:4])
    fig, axs = plt.subplots(1, 4, figsize=(16, 3.6))
    for ax, f in zip(axs, top4):
        shap.plots.scatter(sv[:, f], ax=ax, show=False)
        ax.set_title(f)
    plt.suptitle(f"SHAP dependence — {tname}"); plt.tight_layout()
    plt.savefig(os.path.join(OUT, f"shap_{tag}_dependence.png"), dpi=110, bbox_inches="tight"); plt.close("all")

pd.DataFrame(table).round(4).to_csv(os.path.join(OUT, "shap_importance.csv"), encoding="utf-8-sig")
print("\nsaved shap_importance.csv")

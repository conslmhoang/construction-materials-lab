"""Feature importance on held-out papers + backward selection (leave-paper-out CV).
Usage: python select_features.py "../03 Dataset_ratio.xlsx" <outdir> additions
"""
import sys, os, json
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, "spike.py"), encoding="utf-8").read()
exec(src.split("lines, curves = [], {}")[0])      # builds X, targets, groups_all, model(), fp()
from sklearn.model_selection import GroupKFold

SEEDS = [0, 1, 2, 3, 4]

def cv_score(Xa, y, g, cols):
    """mean R2 / MAE over 5 shuffled 10-fold leave-paper-out splits"""
    r2s, maes = [], []
    for s in SEEDS:
        pred = np.zeros(len(y))
        for tr, te in GroupKFold(10, shuffle=True, random_state=s).split(Xa, y, g):
            pred[te] = fp(Xa[tr][:, cols], y[tr], Xa[te][:, cols])
        r2s.append(r2_score(y, pred)); maes.append(mean_absolute_error(y, pred))
    return np.mean(r2s), np.std(r2s), np.mean(maes)

def heldout_importance(Xa, y, g, cols, rng):
    """permutation importance measured on held-out papers (MAE increase)"""
    imp = np.zeros(len(cols))
    for s in SEEDS[:3]:
        for tr, te in GroupKFold(10, shuffle=True, random_state=s).split(Xa, y, g):
            Xtr, Xte = Xa[tr][:, cols], Xa[te][:, cols].copy()
            keep = ~np.all(np.isnan(Xtr), axis=0)
            mdl = model().fit(Xtr[:, keep], y[tr])
            base = mean_absolute_error(y[te], mdl.predict(Xte[:, keep]))
            for j in range(len(cols)):
                if not keep[j]: continue
                Xp = Xte.copy(); Xp[:, j] = rng.choice(Xa[tr][:, cols[j]], len(te))  # break the link, keep distribution
                imp[j] += mean_absolute_error(y[te], mdl.predict(Xp[:, keep])) - base
    return imp / (3 * 10)

rng = np.random.default_rng(0)
names = list(X.columns)
summary = {}
fig, axs = plt.subplots(2, 3, figsize=(15, 9))
for col_i, (tname, (y, mask)) in enumerate(targets.items()):
    m = mask & y.notna()
    Xa = X[m].values.astype(float); ya = y[m].values; ga = groups_all[m].values
    # drop columns that are (almost) constant in this subset
    usable = [j for j in range(Xa.shape[1]) if np.nanstd(Xa[:, j]) > 0 and np.isfinite(Xa[:, j]).sum() >= 15]
    imp = heldout_importance(Xa, ya, ga, usable, rng)
    order = [usable[i] for i in np.argsort(-imp)]
    imp_sorted = np.sort(imp)[::-1]
    # backward selection along the importance ranking
    ks = [k for k in [3, 5, 8, 10, 12, 15, 20, 25, 30, 40] if k < len(order)] + [len(order)]
    res = []
    for k in ks:
        r2, sd, mae = cv_score(Xa, ya, ga, order[:k])
        res.append((k, r2, sd, mae)); print(f"{tname:18s} top-{k:3d}: R2={r2:.3f}±{sd:.3f} MAE={mae:.2f}", flush=True)
    best = max(res, key=lambda r: r[1])
    # smallest k within 1 SD of the best
    k_pick = min(r[0] for r in res if r[1] >= best[1] - best[2])
    summary[tname] = dict(n_rows=int(m.sum()), n_papers=int(len(np.unique(ga))),
                          all_features=dict(k=res[-1][0], R2=round(res[-1][1], 3), MAE=round(res[-1][3], 2)),
                          best=dict(k=best[0], R2=round(best[1], 3), MAE=round(best[3], 2)),
                          picked_k=k_pick, picked=[names[j] for j in order[:k_pick]],
                          ranking=[(names[j], round(float(v), 4)) for j, v in zip(order, imp_sorted)])
    ax = axs[0, col_i]; top = 20
    ax.barh([names[j] for j in order[:top]][::-1], imp_sorted[:top][::-1], color="#3b6ea5")
    ax.set_title(f"{tname}: held-out importance (ΔMAE)"); ax.tick_params(labelsize=8)
    ax = axs[1, col_i]
    k_, r2_, sd_, _ = zip(*res)
    ax.errorbar(k_, r2_, yerr=sd_, marker="o", capsize=3); ax.axvline(k_pick, ls="--", c="gray")
    ax.set_xlabel("# features kept (by importance)"); ax.set_ylabel("R² on unseen papers"); ax.grid(alpha=.3)
    ax.set_title(f"picked k={k_pick}")
plt.tight_layout(); plt.savefig(os.path.join(OUT, "feature_selection.png"), dpi=110)
json.dump(summary, open(os.path.join(OUT, "feature_selection.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for t, s in summary.items():
    print(f"\n== {t}: all {s['all_features']}  best {s['best']}  picked k={s['picked_k']}")
    print("   keep:", ", ".join(s["picked"]))
    print("   bottom (≤0 importance):", ", ".join(n for n, v in s["ranking"] if v <= 0))

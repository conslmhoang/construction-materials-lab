"""Turn clean/flags.csv into the cleaning decision per row and a review workbook.
Rules chosen from clean/ablation*.csv (each rule kept only if it improved held-out accuracy):
  fc, ft : drop no-fibre rows, model outliers, exotic binders, rows missing W/B or test age
  eps    : drop model outliers, physics-check fails, coarse-aggregate rows, exotic binders
Rows are never deleted: dataset_clean.csv keeps every row with use_fc / use_ft / use_eps and a reason.
Usage: python clean/make_clean.py clean
"""
import sys, os
import numpy as np, pandas as pd

OUT = sys.argv[1]
F = pd.read_csv(os.path.join(OUT, "flags.csv"), encoding="utf-8-sig")
b = lambda c: F[c].fillna(False).astype(bool)
outl = b("flag_outlier_fc") | b("flag_outlier_ft")

REASONS = {
    "no fibre":            b("flag_no_fibre"),
    "model outlier":       outl,
    "exotic binder":       b("flag_exotic_binder"),
    "missing W/B":         b("flag_no_wb"),
    "missing test age":    b("flag_no_age"),
    "physics check":       b("flag_ft_fc_ratio") | b("flag_strain_no_fibre"),
    "coarse aggregate":    b("flag_coarse_agg"),
    "fire/freeze/dynamic/other special test": b("flag_special_cond"),
}
SP = "fire/freeze/dynamic/other special test"
RULE = {"fc":  [SP, "no fibre", "model outlier", "exotic binder", "missing W/B", "missing test age"],
        "ft":  [SP, "no fibre", "model outlier", "exotic binder", "missing W/B", "missing test age"],
        "eps": [SP, "model outlier", "physics check", "coarse aggregate", "exotic binder"]}

for t, rs in RULE.items():
    drop = np.zeros(len(F), bool)
    why = pd.Series([[] for _ in range(len(F))], index=F.index)
    for r in rs:
        drop |= REASONS[r].values
        for i in np.where(REASONS[r].values)[0]: why.iat[i].append(r)
    why = why.map("; ".join)
    has = F[t].notna() & (F["tension_type"].eq("direct") if t != "fc" else True)
    F[f"has_{t}"] = has
    F[f"use_{t}"] = has & ~drop
    F[f"why_not_{t}"] = np.where(has & drop, why, "")

F.to_csv(os.path.join(OUT, "dataset_clean.csv"), index=False, encoding="utf-8-sig")

summary = []
for t in RULE:
    has = F[f"has_{t}"]
    summary.append(dict(output=t, rows_with_value=int(has.sum()), kept=int(F[f"use_{t}"].sum()),
                        excluded=int((has & ~F[f"use_{t}"]).sum()),
                        papers_kept=int(F.loc[F[f"use_{t}"], "paper"].nunique())))
S = pd.DataFrame(summary)
print(S.to_string(index=False))

cols = ["file", "paper", "doi", "fc", "ft", "eps", "tension_type", "pred_fc", "z_fc", "pred_ft", "z_ft"]
excl = F[(F.why_not_fc != "") | (F.why_not_ft != "") | (F.why_not_eps != "")][cols + ["why_not_fc", "why_not_ft", "why_not_eps"]]
verify = F[b("flag_verify")][cols]
outliers = F[outl][cols].sort_values("z_fc", key=lambda s: s.abs(), ascending=False)

with pd.ExcelWriter(os.path.join(OUT, "cleaning_review.xlsx")) as xw:
    S.to_excel(xw, sheet_name="Summary", index=False)
    excl.to_excel(xw, sheet_name="Excluded rows", index=False)
    outliers.to_excel(xw, sheet_name="Model outliers", index=False)
    verify.to_excel(xw, sheet_name="VERIFY rows (kept)", index=False)
    for ws in xw.sheets.values():
        for col in ws.columns:
            ws.column_dimensions[col[0].column_letter].width = min(max(len(str(col[0].value)) + 2, 10), 60)
print("wrote dataset_clean.csv and cleaning_review.xlsx")
for r, v in REASONS.items():
    print(f"  {r:18s} {int(v.sum()):4d} rows")

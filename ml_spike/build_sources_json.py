"""Write data/sources.json for data.html: every source paper with its DOI and how many of its
mixes are used for each model (rows of "excel/04 Dataset_web.xlsx", the training file).
Usage: python build_sources_json.py      (run from ml_spike/)
"""
import os, json, re
import pandas as pd
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
S = pd.read_csv(os.path.join(root, "03 Dataset_sources.csv"), encoding="utf-8-sig")
F = pd.read_csv(os.path.join(here, "clean", "dataset_clean.csv"), encoding="utf-8-sig")

W = pd.read_excel(os.path.join(root, "excel", "04 Dataset_web.xlsx"), sheet_name="Data")
OUTS = {"fc": "Compressive strength (MPa)", "eps": "Tensile strain capacity (%)"}
for k, c in OUTS.items(): W["use_" + k] = W[c].notna()

norm = lambda d: re.sub(r"^https?://(dx\.)?doi\.org/", "", str(d).strip().lower())
F["_doi"] = F["doi"].map(norm); W["_doi"] = W["DOI"].fillna("").map(norm)
F["_t"] = F["paper"].astype(str).str.strip().str.lower(); W["_t"] = W["Paper"].astype(str).str.strip().str.lower()
used = lambda by: W.groupby(by).agg(fc=("use_fc", "sum"), eps=("use_eps", "sum"))
cnt = F.groupby("_doi").agg(rows=("doi", "size")).join(used("_doi")).fillna(0)
cnt_t = F.groupby("_t").agg(rows=("doi", "size")).join(used("_t")).fillna(0)

papers, seen = [], set()
for _, r in S.iterrows():
    title = str(r["article_title"]).strip()
    link = str(r["DOI_or_URL"]).strip()
    key = norm(link)
    if key in seen: continue
    seen.add(key)
    c = cnt.loc[key] if key in cnt.index else (cnt_t.loc[title.lower()] if title.lower() in cnt_t.index else None)
    papers.append({"title": title, "link": link if link.startswith("http") else "",
                   "added": str(r["date_added"])[:10],
                   "rows": int(c["rows"]) if c is not None else 0,
                   "fc": int(c["fc"]) if c is not None else 0,
                   "eps": int(c["eps"]) if c is not None else 0})
papers = [p for p in papers if p["rows"] > 0]
# papers added after 03 Dataset_ratio.xlsx (ml_spike/additions_v2/*.csv)
import glob
for f in sorted(glob.glob(os.path.join(here, "additions_v2", "*.csv"))):
    A = pd.read_csv(f, encoding="utf-8-sig")
    for (title, link), g in A.groupby(["Article Name", "DOI / URL"], sort=False):
        key = norm(link)
        if key in seen: continue
        seen.add(key)
        u = W[W["_doi"] == key]
        papers.append({"title": str(title).strip(), "link": str(link), "added": "2026-11",
                       "rows": int(len(g)), "fc": int(u["use_fc"].sum()), "eps": int(u["use_eps"].sum())})
# rows extracted for the new papers (all additions_v2 files, same de-duplication as above)
NEW = pd.concat([pd.read_csv(f, encoding="utf-8-sig") for f in sorted(glob.glob(os.path.join(here, "additions_v2", "*.csv")))], ignore_index=True)
NEW["_doi"] = NEW["DOI / URL"].map(norm)
NEW = NEW[~NEW["_doi"].isin(set(F["_doi"]))]
new_dois = set(NEW["_doi"])
W_old, W_new = W[~W["_doi"].isin(new_dois)], W[W["_doi"].isin(new_dois)]
num = lambda s: pd.to_numeric(s, errors="coerce").notna()
has_new = {"fc": int(num(NEW["Compressive strength (MPa)"]).sum()), "eps": int(num(NEW["Tensile strain capacity (%)"]).sum())}
summary = {"rows": int(len(F) + len(NEW)), "papers": len(papers),
           "papers_used": sum(1 for p in papers if p["fc"] or p["eps"]),
           "has": {t: int(F[f"has_{t}"].sum()) + has_new[t] for t in ("fc", "eps")},
           "use": {t: int(W[f"use_{t}"].sum()) for t in ("fc", "eps")},
           "why_not_fc": F.loc[F["has_fc"].astype(bool) & ~F["use_fc"].astype(bool), "why_not_fc"]
                          .fillna("").str.split(";").explode().str.strip().loc[lambda s: s != ""].replace("no fibre", "no fiber").value_counts().to_dict()}
lost = int(F["use_fc"].sum() - W_old["use_fc"].sum())      # passed cleaning but cannot be entered on the web
if lost > 0: summary["why_not_fc"]["uses a material outside the 20 (incl. PBO fiber)"] = lost
lost_new = has_new["fc"] - int(W_new["use_fc"].sum())       # new papers: rows left out by the build rules or checked by hand
if lost_new > 0: summary["why_not_fc"]["new papers: material outside the 20, missing W/B or age, or removed after checking"] = lost_new
os.makedirs(os.path.join(root, "data"), exist_ok=True)
json.dump({"summary": summary, "papers": papers}, open(os.path.join(root, "data", "sources.json"), "w", encoding="utf-8"),
          ensure_ascii=False, separators=(",", ":"))
print(summary, "papers listed:", len(papers), "unmatched sources:", len(S) - len(papers))

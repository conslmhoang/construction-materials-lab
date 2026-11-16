"""Write data/sources.json for data.html: every source paper with its DOI and how many of its
mixes are used for each model (from clean/dataset_clean.csv).
Usage: python build_sources_json.py      (run from ml_spike/)
"""
import os, json, re
import pandas as pd
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
S = pd.read_csv(os.path.join(root, "03 Dataset_sources.csv"), encoding="utf-8-sig")
F = pd.read_csv(os.path.join(here, "clean", "dataset_clean.csv"), encoding="utf-8-sig")

norm = lambda d: re.sub(r"^https?://(dx\.)?doi\.org/", "", str(d).strip().lower())
F["_doi"] = F["doi"].map(norm)
cnt = F.groupby("_doi").agg(rows=("doi", "size"), fc=("use_fc", "sum"), ft=("use_ft", "sum"), eps=("use_eps", "sum"))
F["_t"] = F["paper"].astype(str).str.strip().str.lower()
cnt_t = F.groupby("_t").agg(rows=("doi", "size"), fc=("use_fc", "sum"), ft=("use_ft", "sum"), eps=("use_eps", "sum"))

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
                   "fc": int(c["fc"]) if c is not None else 0, "ft": int(c["ft"]) if c is not None else 0,
                   "eps": int(c["eps"]) if c is not None else 0})
papers = [p for p in papers if p["rows"] > 0]
summary = {"rows": int(len(F)), "papers": len(papers),
           "has": {t: int(F[f"has_{t}"].sum()) for t in ("fc", "ft", "eps")},
           "use": {t: int(F[f"use_{t}"].sum()) for t in ("fc", "ft", "eps")},
           "why_not_fc": F.loc[F["has_fc"].astype(bool) & ~F["use_fc"].astype(bool), "why_not_fc"]
                          .fillna("").str.split(";").explode().str.strip().loc[lambda s: s != ""].replace("no fibre", "no fiber").value_counts().to_dict()}
os.makedirs(os.path.join(root, "data"), exist_ok=True)
json.dump({"summary": summary, "papers": papers}, open(os.path.join(root, "data", "sources.json"), "w", encoding="utf-8"),
          ensure_ascii=False, separators=(",", ":"))
print(summary, "papers listed:", len(papers), "unmatched sources:", len(S) - len(papers))

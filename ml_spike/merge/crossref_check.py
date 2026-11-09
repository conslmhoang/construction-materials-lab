"""Verify every added DOI against Crossref (title + first-author surname), per the workbook Guide rule 1.
Writes merge/crossref.json  {doi: {"ok": bool, "cr_title": ..., "cr_first_author": ..., "why": ...}}
"""
import json, os, re, sys, time, glob, urllib.request, urllib.parse, difflib
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
add = os.path.join(here, "..", "additions")
cache_f = os.path.join(here, "crossref.json")
cache = json.load(open(cache_f, encoding="utf-8")) if os.path.exists(cache_f) else {}

def norm_doi(s):
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", str(s).strip()).lower()
def norm_txt(s):
    return re.sub(r"[^a-z0-9]+", " ", re.sub(r"<[^>]+>", "", str(s)).lower()).strip()

papers = {}
for f in sorted(glob.glob(os.path.join(add, "*.csv"))):
    if f.endswith("TEMPLATE.csv"): continue
    a = pd.read_csv(f, encoding="utf-8-sig")
    for _, r in a.drop_duplicates("DOI / URL").iterrows():
        papers[norm_doi(r["DOI / URL"])] = (str(r["Article Name"]), str(r["Author"]))

for i, (doi, (title, authors)) in enumerate(papers.items()):
    if doi in cache: continue
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    req = urllib.request.Request(url, headers={"User-Agent": "ConstructionMaterialsLab-dataset-check/1.0"})
    try:
        js = json.load(urllib.request.urlopen(req, timeout=30))["message"]
        crt = (js.get("title") or [""])[0]
        fa = (js.get("author") or [{}])[0].get("family", "")
        sim = difflib.SequenceMatcher(None, norm_txt(crt), norm_txt(title)).ratio()
        first = norm_txt(authors.split(",")[0].split(";")[0])
        au_ok = bool(fa) and norm_txt(fa) in first
        ok = sim >= 0.85 and au_ok
        why = "" if ok else f"title similarity {sim:.2f}; first author Crossref='{fa}' vs sheet='{authors.split(',')[0][:40]}'"
        cache[doi] = dict(ok=ok, sim=round(sim, 3), cr_title=crt, cr_first_author=fa, why=why)
    except Exception as e:
        cache[doi] = dict(ok=False, why=f"Crossref lookup failed: {e}")
    if i % 20 == 0:
        json.dump(cache, open(cache_f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(i, len(papers), flush=True)
    time.sleep(0.15)
json.dump(cache, open(cache_f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
bad = {k: v for k, v in cache.items() if k in papers and not v["ok"]}
print(f"checked {len(papers)} DOIs, verified {len(papers) - len(bad)}, problems {len(bad)}")
for k, v in bad.items():
    print(" ", k, "|", v["why"], "|", v.get("cr_title", "")[:70])

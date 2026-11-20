"""For the 30 papers with the largest total strain error: one packet file each (dataset rows + predictions + source text path)."""
import os, re, glob, pandas as pd
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
R = pd.read_csv(os.path.join(root, "ml_spike", "audit", "eps_oof.csv")); P = pd.read_csv(os.path.join(root, "ml_spike", "audit", "eps_papers.csv")).head(30)
D = pd.read_excel(os.path.join(root, "excel", "04 Dataset_web.xlsx"), sheet_name="Data"); D["row"] = range(2, len(D) + 2)
txts = glob.glob(os.path.join(root, "Papers", "Paper news", "*_txt", "*.txt")) + glob.glob(os.path.join(root, "Papers", "Paper news", "download", "*.txt"))
pdfs = glob.glob(os.path.join(root, "Papers", "*.pdf")) + glob.glob(os.path.join(root, "Papers", "Paper news", "*.pdf")) + glob.glob(os.path.join(root, "Papers", "Paper news", "download", "*.pdf"))
def key(s): return re.sub(r"[^a-z0-9]", "", s.lower())
out = os.path.join(root, "ml_spike", "audit", "packets"); os.makedirs(out, exist_ok=True); idx = []
for i, p in P.iterrows():
    doi = re.search(r"10\.\S+", str(p.doi)); doi = doi.group(0) if doi else ""; k = key(doi)
    src = [f for f in txts + pdfs if k and k in key(os.path.basename(f))]
    rows = D[D.Paper == p.Paper].copy(); rows = rows.loc[:, rows.notna().any()]
    rows = rows.merge(R[["row", "pred"]], on="row", how="left")
    fn = os.path.join(out, f"{i+1:02d}.txt")
    with open(fn, "w", encoding="utf-8") as f:
        f.write(f"PAPER: {p.Paper}\nDOI: {doi}\nSOURCES: {src}\nStrain rows: {int(p.n)}  MAE {p.mae:.2f} %\n\n")
        f.write(rows.drop(columns=["Paper", "DOI"]).to_csv(index=False))
    idx.append((i + 1, p.Paper[:60], doi, len(src)))
for r in idx: print(r)

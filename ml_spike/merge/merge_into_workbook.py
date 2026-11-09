"""Append the agent-extracted rows (ml_spike/additions/*.csv) to 03 Dataset_ratio.xlsx, following the
workbook Guide: Title/Author/Year/DOI only on a paper's first row and merged down; traceability in the
four last columns; VERIFY flag cells yellow. Also appends one line per paper to 03 Dataset_sources.csv.
A backup must exist before running (made by hand in Backup/).
Usage: python merge/merge_into_workbook.py
"""
import os, re, json, glob, copy, datetime
import pandas as pd, openpyxl
from openpyxl.styles import PatternFill

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(here, "..", ".."))
XLSX = os.path.join(root, "03 Dataset_ratio.xlsx")
SRC = os.path.join(root, "03 Dataset_sources.csv")
ADD = os.path.join(here, "..", "additions")
cr = json.load(open(os.path.join(here, "crossref.json"), encoding="utf-8"))
YELLOW = PatternFill("solid", fgColor="00FFFF00")
TODAY = datetime.date.today().isoformat()

def norm_doi(s): return re.sub(r"^https?://(dx\.)?doi\.org/", "", str(s).strip()).lower()
def num(v):
    if v is None or (isinstance(v, float) and pd.isna(v)): return None
    if isinstance(v, str):
        s = v.strip()
        if s == "" or s.lower() == "nan": return None
        try: return float(s) if re.fullmatch(r"-?\d+(\.\d*)?([eE]-?\d+)?", s) else s
        except ValueError: return s
    return v

wb = openpyxl.load_workbook(XLSX)
ws = wb["Dataset"]
hdr = {ws.cell(2, c).value: c for c in range(1, ws.max_column + 1)}
C_NOTES, C_SRC, C_AI, C_VER = (hdr["Paper notes (as reported by the paper)"], hdr["Source location (Table / Figure / Page)"],
                               hdr["AI-derived values & reasoning (not from paper)"], hdr["Verify flag (OK / VERIFY: reason)"])
start = ws.max_row + 1
style_row = ws.max_row
if any(str(ws.cell(r, C_NOTES).value or "").startswith("[Agent-extracted") for r in range(3, ws.max_row + 1)):
    raise SystemExit("Agent-extracted rows are already in the workbook — stopping.")

files = [f for f in sorted(glob.glob(os.path.join(ADD, "*.csv"))) if not f.endswith("TEMPLATE.csv")]
order = ["pvaecc", "geopolymer", "uhpc_steel", "uhpecc"]            # wave 1 first, then w2_, w3_, w4_
files.sort(key=lambda f: (0, order.index(os.path.basename(f)[:-4])) if os.path.basename(f)[:-4] in order else (1, os.path.basename(f)))

r = start
log = []
for f in files:
    a = pd.read_csv(f, encoding="utf-8-sig", dtype=str)
    a["_doi"] = a["DOI / URL"].map(norm_doi)
    a["_ord"] = a["_doi"].map({d: i for i, d in enumerate(dict.fromkeys(a["_doi"]))})
    a = a.sort_values("_ord", kind="stable")
    for doi, g in a.groupby("_doi", sort=False):
        r0 = r
        for k, (_, row) in enumerate(g.iterrows()):
            for col in range(1, ws.max_column + 1):                  # style like the last original row, no fill
                c = ws.cell(r, col); c._style = copy.copy(ws.cell(style_row, col)._style); c.fill = PatternFill(None)
            for name, val in row.items():
                if name not in hdr: continue
                if hdr[name] <= 4 and k > 0: continue                 # title/author/year/DOI on first row only
                v = num(val)
                if name == "DOI / URL": v = "https://doi.org/" + doi
                if name == "Year" and v is not None: v = int(float(v))
                ws.cell(r, hdr[name]).value = v
            notes = "" if pd.isna(row.get("Conversions / notes")) else str(row["Conversions / notes"])
            ws.cell(r, C_NOTES).value = f"[Agent-extracted {TODAY[:7]}, {os.path.basename(f)}; full text via Europe PMC / publisher HTML]"
            ws.cell(r, C_SRC).value = None if pd.isna(row.get("Source table/page")) else str(row["Source table/page"])
            ws.cell(r, C_AI).value = notes or None
            if "verify" in notes.lower():
                m = re.search(r"verify[^.;|]*[.;|]?[^.;|]*", notes, re.I)
                ws.cell(r, C_VER).value = "VERIFY: " + (m.group(0) if m else notes)[:300]
                ws.cell(r, C_VER).fill = YELLOW
            else:
                ws.cell(r, C_VER).value = "OK"
            r += 1
        if r - r0 > 1:
            for col in range(1, 5): ws.merge_cells(start_row=r0, start_column=col, end_row=r - 1, end_column=col)
        info = cr.get(doi, {})
        doi_note = ("DOI verified via Crossref (title + first author)" if info.get("ok") or info.get("sim", 0) >= 0.99
                    else "DOI NOT verified via Crossref: " + info.get("why", "no lookup"))
        srcs = "; ".join(dict.fromkeys(s for s in g["Source table/page"].dropna().astype(str)))[:250]
        log.append([TODAY, g["Article Name"].iloc[0], "https://doi.org/" + doi, "",
                    f"{r0}-{r - 1}" if r - 1 > r0 else str(r0), srcs,
                    "see 'AI-derived values & reasoning' column (kg/m³ → ratio to binder, fibre kg/m³ → vol% where noted)",
                    f"Agent-extracted ({os.path.basename(f)}); {doi_note}."])

wb.save(XLSX)
tail = open(SRC, "rb").read()[-2:]
with open(SRC, "a", encoding="utf-8", newline="") as fh:
    if not tail.endswith(b"\n"): fh.write("\r\n")
    pd.DataFrame(log).to_csv(fh, header=False, index=False)
print(f"appended rows {start}-{r - 1} ({r - start} rows, {len(log)} papers) and {len(log)} source-log lines")

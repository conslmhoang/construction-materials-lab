"""Build excel/Materials_20.xlsx: density, embodied energy, CO2 and cost of the 20 web/model materials,
each value with its source.

Values and sources come from "Inventory of raw materials.xlsx" (rows: Specific gravity, Energy, CO2, Cost,
each followed by a "source" row). Density = specific gravity x 1000. Material names are the web names in
materials21.json, so the file can be loaded on the web page ("Load material database from Excel"):
the first sheet has the material names in row 1 and the property rows below, as the web loader expects.

Usage:  python build_materials_xlsx.py
"""
import os, json
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
INV = os.path.join(root, "Inventory of raw materials.xlsx")
OUT = os.path.join(root, "excel", "Materials_20.xlsx")
M21 = json.load(open(os.path.join(root, "materials21.json"), encoding="utf-8"))["materials"]

# column name in the inventory for each of the 20 materials
INV_COL = {"Cement": "OPC", "FA": "Fly ash", "GGBS": "GGBS", "SF": "Silica fume", "MK": "Metakaolin",
           "LP": "Limestone Powder", "Sand": "Silica sand", "CR": "Crumb rubber", "EPS": "EPS beads",
           "Water": "Water", "SP": "SP", "VMA": "VMA", "NaOH": "NaOH", "Na2SO4": "Na2SO4", "Na2SiO3": "Na2SiO3",
           "WG": "WG (water glass, sodium silicate solution)", "CaOH2": "Ca(OH)2", "PE": "PE fiber",
           "PVA": "PVA fiber", "Steel": "Steel fiber"}

ws_in = openpyxl.load_workbook(INV, data_only=True).active
rows = [list(r) for r in ws_in.iter_rows(values_only=True)]
label = {str(r[0]).strip(): i for i, r in enumerate(rows) if r[0] is not None and str(r[0]).strip() != "source"}
hdr = [str(h).strip() if h is not None else "" for h in rows[label["Materials"]]]
PROPS = [  # (label in the output, inventory row label, factor)
    ("Density (kg/m3)", "Specific gravity", 1000.0),
    ("Energy (MJ/kg)", "Energy (MJ/kg)", 1.0),
    ("CO2 (kg/kg)", "CO2 (kg/kg)", 1.0),
    ("Cost ($/kg)", "Cost ($/kg)", 1.0),
]

wb = openpyxl.Workbook()
ws = wb.active; ws.title = "Materials"
ws.append(["Materials"] + [m["name"] for m in M21])
missing = []
for out_label, inv_label, f in PROPS:
    i = label[inv_label]
    vals, srcs = [], []
    for m in M21:
        j = hdr.index(INV_COL[m["key"]])
        v, s = rows[i][j], rows[i + 1][j]          # the source row follows the value row
        if v is None:
            missing.append(f"{m['name']}: {out_label}")
            s = s or "Not found in the inventory yet (the web uses 0)"
        vals.append(round(float(v) * f, 6) if v is not None else None)
        srcs.append(s)
    ws.append([out_label] + vals)
    ws.append(["source"] + srcs)

# fiber length, diameter, tensile strength, elastic modulus: the values the web shows (materials21.json), each with its source
LEE = "fiber used in the papers of Prof. Bang Yeon Lee's lab (Chonnam National University) in excel/04 Dataset_web.xlsx"
GEOM_SRC = {
    "PE": "Luong Q.-H., Nguyen H.H., Nguyen P.H., Kang S.-T., Lee B.Y., Ceramics International 49 (2023) 12069-12078, "
          "Table 3 'Properties of PE fiber': diameter 12 um, length 18 mm (also tensile strength 2700 MPa, density 0.97 g/cm3, "
          "elastic modulus 88 GPa). https://doi.org/10.1016/j.ceramint.2022.12.057 . Same PE fiber in 13 of the 17 papers of the "
          "lab in the training data.",
    "PVA": "Choi S.-J., Choi J.-I., Song J.-K., Lee B.Y., Construction and Building Materials (2015), Table 4 'Properties of fiber': PVA, density 1.3, "
           "length 8 mm, diameter 40 um, tensile strength 1,600 MPa, Young's modulus 41 GPa. "
           "https://doi.org/10.1016/j.conbuildmat.2015.07.182 . Also 8 mm / 40 um (1560 MPa, 41 GPa) in "
           "https://doi.org/10.3390/ma15186339 (" + LEE + ").",
    "Steel": "Zuo Z., Zhang J., Li B., Shen C., Xin G., Chen X., Materials 15 (2022), 'Effect of Curing Regime on the Mechanical "
             "Strength, Hydration, and Microstructure of ...': steel fiber length 13 mm, diameter 0.2 mm (200 um), tensile strength "
             "2200 MPa. https://doi.org/10.3390/ma15051668 (no paper of the lab in the training data uses steel fiber). "
             "Elastic modulus is not stated there: 200 GPa = the most common steel modulus in excel/04 Dataset_web.xlsx "
             "(178 of 278 rows that report it).",
}
for out_label, k in (("Fiber length (mm)", "length_mm"), ("Fiber diameter (um)", "diameter_um"),
                     ("Fiber tensile strength (MPa)", "tensile_strength_mpa"), ("Fiber elastic modulus (GPa)", "elastic_modulus_gpa")):
    ws.append([out_label] + [m.get(k) if m["group"] == "fiber" else None for m in M21])
    ws.append(["source"] + [GEOM_SRC[m["key"]] + " Can be changed on the web." if m["group"] == "fiber" else None for m in M21])

bold, wrap = Font(bold=True), Alignment(wrap_text=True, vertical="top")
fill = PatternFill("solid", fgColor="E8EEF7")
for c in ws[1]:
    c.font = bold; c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center"); c.fill = fill
for r in range(2, ws.max_row + 1):
    ws.cell(r, 1).font = bold
    for c in ws[r][1:]:
        c.alignment = wrap if ws.cell(r, 1).value == "source" else Alignment(horizontal="center", vertical="top")
ws.column_dimensions["A"].width = 18
for j in range(2, len(M21) + 2):
    ws.column_dimensions[get_column_letter(j)].width = 34
for r in range(2, ws.max_row + 1):
    ws.row_dimensions[r].height = 150 if ws.cell(r, 1).value == "source" else 20
ws.freeze_panes = "B2"

info = wb.create_sheet("Info")
info.append(["Web name", "Model key", "Group", "Column in the inventory", "Meaning of the group"])
MEAN = {"binder": "Share of the binder (cement + FA + GGBS add up to 1)",
        "ratio": "Mass ratio to that binder", "fiber": "Volume % of the mix"}
for m in M21:
    info.append([m["name"], m["key"], m["group"], INV_COL[m["key"]], MEAN[m["group"]]])
info.append([])
info.append(["Built from \"Inventory of raw materials.xlsx\" (and the fiber properties from materials21.json) by ml_spike/build_materials_xlsx.py. "
             "Density = specific gravity x 1000. The web page can load the first sheet (Load material database from Excel)."])
for c in info[1]:
    c.font = bold; c.fill = fill
for col, w in zip("ABCDE", [28, 10, 8, 42, 52]):
    info.column_dimensions[col].width = w

os.makedirs(os.path.dirname(OUT), exist_ok=True)
wb.save(OUT)
print("wrote", OUT, "| materials:", len(M21), "| missing values:", missing or "none")

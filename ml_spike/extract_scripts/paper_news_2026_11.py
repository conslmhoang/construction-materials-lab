"""Rows from the two papers in Papers/Paper news that were not yet in 03 Dataset_ratio.xlsx.
Writes ml_spike/additions_v2/paper_news.csv (99-column TEMPLATE header).

1) Luong et al. (2025) Dev. Built Environ. 22, 100677 - rubberized alkali-activated slag composites
2) Luong et al. (2026) Dev. Built Environ. 28, 101095 - lightweight ambient-cured one-part EGCs
Ratios are per the papers' binder (GGBS + Ca(OH)2, resp. FA + GGBS + ASM); build_web_dataset.py
re-expresses everything per (cement + fly ash + GGBS).
"""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
add = os.path.join(here, "..", "additions")
out_dir = os.path.join(here, "..", "additions_v2"); os.makedirs(out_dir, exist_ok=True)
cols = list(pd.read_csv(os.path.join(add, "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
rows = []

# ---- 1) rubberized AAS composites (Table 1, Table 4, Table 5)
P1 = dict(**{"Article Name": "Achieving ultra-ductility exceeding 13 % and cost efficiency with rubberized alkali-activated slag-based cement-free composites",
             "Author": "Quang-Hieu Luong, Huy Hoang Nguyen, Phuong Hoang Nguyen, Se-Eon Park, Youngsang Kim, Bang Yeon Lee",
             "Year": 2025, "DOI / URL": "https://doi.org/10.1016/j.dibe.2025.100677"})
# mix: (id, SS/B, W/B, SP/B, PE vol%, selvage PE vol%, ft, eps, ft/fc %)
mix1 = [("PE30-S0", 0.0, 0.30, 0.009, 1.75, 0, 6.53, 11.89, 23.7),
        ("PE30-S4", 0.4, 0.30, 0.016, 1.75, 0, 6.04, 13.82, 18.2),
        ("PE30-S8", 0.8, 0.30, 0.029, 1.75, 0, 5.33, 15.64, 15.3),
        ("PE25-S4", 0.4, 0.25, 0.030, 1.75, 0, 5.94, 14.61, 16.0),
        ("SPE25-S4", 0.4, 0.25, 0.030, 0, 1.75, 6.36, 13.41, 17.2)]
for mid, ss, wb, sp, pe, spe, ft, eps, ratio in mix1:
    r = dict(P1)
    r.update({"GGBS": 0.9, "Ca(OH)2 / B": 0.1, "Crumb rubber / B": 0.05, "SS / B (Silica sand)": ss, "W / B": wb,
              "SP / B": sp, "PE fiber (vol%)": pe + spe, "PE length (mm)": 18,
              "PE diameter (µm)": 12 if pe else 18, "PE tensile strength (MPa)": 2700 if pe else 3000,
              "Total fiber (vol%)": 1.75,
              "Curing method": "covered with plastic sheet in air 23 °C, demolded at 4 d, then water tank 23 °C",
              "Curing time (days)": 28, "Curing temperature (°C)": 23, "Demolding age (days)": 4, "Test age (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
              "Tensile specimen": "dumbbell (JSCE)", "Tensile gauge length (mm)": 80, "Tensile test type": "direct (uniaxial)",
              "Compressive strength (MPa)": round(ft / (ratio / 100), 1), "Tensile strength (MPa)": ft,
              "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix), Table 4 (ft, strain), Table 5 (ft/fc), p.3-4 (curing)",
              "Conversions / notes": f"{mid}. Binder = GGBS 0.9 + Ca(OH)2 0.1. P-SP liquid; defoamer 0.001 (not listed). "
                                     f"{'Selvage PE fiber (SPE), stored in PE column. ' if spe else ''}"
                                     f"VERIFY: fc = ft / (ft/fc) from Table 5 (fc only plotted in Fig. 5)."})
    rows.append(r)

# ---- 2) lightweight one-part EGCs (Table 1, Table 4, Table 5)
P2 = dict(**{"Article Name": "Ultra-high tensile ductility up to 16.4% in lightweight, ambient-cured geopolymer composites at PE fiber contents of 0.5-1.5 vol%",
             "Author": "Quang-Hieu Luong, Phuong Hoang Nguyen, Se-Eon Park, Yun Yong Kim, Huy Hoang Nguyen, Bang Yeon Lee",
             "Year": 2026, "DOI / URL": "https://doi.org/10.1016/j.dibe.2026.101095"})
# (id, W/B, SP/B, VMA/B, PE vol%, ft, eps, ft/fc %, fcr)
mix2 = [("W35-F0.5", 0.35, 0.0, 0.0, 0.5, 2.82, 10.72, 18.1, 2.09),
        ("W35-F1.0", 0.35, 0.0034, 0.0011, 1.0, 5.47, 12.79, 24.7, 2.88),
        ("W35-F1.5", 0.35, 0.0057, 0.0034, 1.5, 5.68, 11.40, 25.5, 3.51),
        ("W40-F0.5", 0.40, 0.0, 0.0024, 0.5, 2.33, 11.04, 15.6, 1.50),
        ("W40-F1.0", 0.40, 0.0, 0.0024, 1.0, 4.04, 16.41, 25.2, 2.04),
        ("W40-F1.5", 0.40, 0.0, 0.0006, 1.5, 4.66, 12.00, 28.4, 2.86)]
for mid, wb, sp, vma, pe, ft, eps, ratio, fcr in mix2:
    r = dict(P2)
    r.update({"FA (Fly ash)": 0.45, "GGBS": 0.45, "SSM / B (Na2SiO3 anhydrous)": 0.1, "EPS / B": 0.01, "W / B": wb,
              "SP / B": sp, "VMA / B": vma, "PE fiber (vol%)": pe, "PE length (mm)": 18, "PE diameter (µm)": 12,
              "PE tensile strength (MPa)": 2700, "PE elastic modulus (GPa)": 88, "Total fiber (vol%)": pe,
              "Curing method": "sealed with plastic film at 23 °C, demolded at 48 h, cured at 23 °C",
              "Curing time (days)": 28, "Curing temperature (°C)": 23, "Demolding age (days)": 2, "Test age (days)": 28,
              "Tensile specimen": "dumbbell", "Tensile test type": "direct (uniaxial)",
              "Compressive strength (MPa)": round(ft / (ratio / 100), 1), "Tensile strength (MPa)": ft,
              "First-cracking strength (MPa)": fcr, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix), Table 4 (fcr, ft, strain), Table 5 (ft/fc), p.4 (curing)",
              "Conversions / notes": f"{mid}. Binder = FA 0.45 + GGBS 0.45 + ASM (anhydrous sodium metasilicate) 0.1. "
                                     f"VERIFY: fc = ft / (ft/fc) from Table 5; text gives 14.9-22.3 MPa, consistent."})
    rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "paper_news.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows ->", os.path.join(out_dir, "paper_news.csv"))
print(df[["Article Name", "Compressive strength (MPa)", "Tensile strain capacity (%)"]].to_string())

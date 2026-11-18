"""w7a: Lee-lab papers. Writes ml_spike/additions_v2/w7_w7a.csv (99-column TEMPLATE header).
1) Lee et al. 2026 ACC 22(3) - PE-AAS tap-water control AT-E only (NBW mixes and PBO-OPC excluded)
2) Hwang et al. 2025 JOBE 112964 - PE-15 mixture only (selvage/GF/PET mixes excluded)
"""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
add = os.path.join(here, "..", "additions")
out = os.path.join(here, "..", "additions_v2", "w7_w7a.csv")
cols = list(pd.read_csv(os.path.join(add, "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
rows = []

rows.append({
    "Article Name": "Contrasting effects of nanobubble water on the tensile behavior of PE-AAS and PBO-OPC composite systems",
    "Author": "Jaewon Lee, Se-Eon Park, Hyeongki Kim, Young-sang Kim, Bang Yeon Lee",
    "Year": 2026, "DOI / URL": "https://doi.org/10.12989/acc.2026.22.3.01",
    "GGBS": 0.9, "Ca(OH)2 / B": 0.1, "W / B": 0.3, "SP / B": 0.003, "VMA / B": 0.001,
    "PE fiber (vol%)": 1.75, "PE length (mm)": 12, "PE diameter (µm)": 16, "PE tensile strength (MPa)": 3030,
    "PE elastic modulus (GPa)": 112, "Total fiber (vol%)": 1.75,
    "Curing method": "air 23 °C RH 60% covered with plastic film 2 d, demolded, then water tank 23 °C",
    "Curing time (days)": 28, "Curing temperature (°C)": 23, "Curing RH (%)": 60, "Demolding age (days)": 2,
    "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": 50,
    "Tensile specimen": "dumbbell (JSCE)", "Tensile gauge length (mm)": 80, "Tensile test type": "direct (uniaxial)",
    "Tensile strength (MPa)": 7.84, "First-cracking strength (MPa)": 2.63, "Tensile strain capacity (%)": 6.33,
    "Source table/page": "Table 1 (mix), Table 2 (fiber), Table 3 (tensile), Sec. 2.2 (curing)",
    "Conversions / notes": "Mix AT-E (tap water control). Compressive strength only in Fig. 3 -> left empty. "
                           "Binder = GGBS + Ca(OH)2 at 10 wt% of binder (GGBS 0.9 / Ca(OH)2 0.1, same convention as Luong 2025 DIBE). "
                           "VERIFY: Table 1 is garbled in the text dump; SP 0.003 and VMA 0.001 (ratios to binder assumed) read from column order; W/B 0.3, PE 1.75 vol%. "
                           "Nanobubble-water mix AN-E and PBO-OPC mixes excluded."})

rows.append({
    "Article Name": "From textile waste to high-performance composites: investigating the role of selvage fibers in engineered cementitious composites",
    "Author": "Eunyoung Hwang, Se-Eon Park, Youngsang Kim, Huy Hoang Nguyen, Bang Yeon Lee",
    "Year": 2025, "DOI / URL": "https://doi.org/10.1016/j.jobe.2025.112964",
    "OPC / Cement": 1.0, "W / B": 0.38, "SP / B": 0.001, "VMA / B": 0.0018,
    "PE fiber (vol%)": 1.75, "PE length (mm)": 15, "PE diameter (µm)": 18, "PE tensile strength (MPa)": 3000,
    "PE elastic modulus (GPa)": 135, "Total fiber (vol%)": 1.75,
    "Curing method": "air 23 °C RH 60% for 48 h, then water 23 °C",
    "Curing time (days)": 28, "Curing temperature (°C)": 23, "Curing RH (%)": 60, "Demolding age (days)": 2,
    "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": 50,
    "Tensile specimen": "dumbbell (JSCE)", "Tensile gauge length (mm)": 80, "Tensile test type": "direct (uniaxial)",
    "Compressive strength (MPa)": 63.8, "Tensile strength (MPa)": 12.51, "First-cracking strength (MPa)": 3.57,
    "Tensile strain capacity (%)": 5.96,
    "Source table/page": "Table 1 (mix), Table 3 (fiber), Table 4 (fc), Table 5 (tensile), Sec. 2.2 (curing)",
    "Conversions / notes": "Mix PE-15 (pure PE fiber, 15 mm). Antifoamer 0.001 also used (allowed). "
                           "Selvage (SE-15), glass (GF-15) and PET (PET-15) mixes excluded."})

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(out, index=False, encoding="utf-8-sig")
print(df.shape)

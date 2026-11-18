"""Wave 7, agent w7c: Lee-lab papers. Writes additions_v2/w7_w7c.csv (TEMPLATE header)."""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
cols = list(pd.read_csv(os.path.join(here, "..", "additions", "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
P = {"Article Name": "Effect of calcium-based/CEA binders on mechanical properties and autogenous healing of high strength ECC with PE fiber",
     "Author": "Huy Hoang Nguyen et al.", "Year": 2020, "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2020.120857"}
rows = []
for mid, pc, gg, wb, fc, fcr, ft, eps in [("M-C", .75, .25, .35, 103.63, 3.65, 8.00, 5.25),
                                           ("M-S", .20, .80, .30, 95.47, 3.53, 8.24, 4.68)]:
    r = dict(P)
    r.update({"OPC / Cement": pc, "GGBS": gg, "W / B": wb, "SS / B (Silica sand)": 0.5, "SP / B": 0.01, "VMA / B": 0.001,
              "PE fiber (vol%)": 1.75, "PE length (mm)": 12, "PE diameter (µm)": 16, "PE tensile strength (MPa)": 3030,
              "PE elastic modulus (GPa)": 112, "Total fiber (vol%)": 1.75,
              "Curing method": "covered with plastic sheet in air at 23 °C for 2 d, demolded, then water at 23 °C",
              "Curing time (days)": 28, "Curing temperature (°C)": 23, "Demolding age (days)": 2, "Test age (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": 50, "Tensile specimen": "dumbbell (JSCE)",
              "Tensile gauge length (mm)": 80, "Tensile test type": "direct (uniaxial)",
              "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft, "First-cracking strength (MPa)": fcr,
              "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 2 (mix), Table 3 (fiber), Table 5 (fc), Table 6 (fcr, fts, strain), Sec 2.2 (curing)",
              "Conversions / notes": f"{mid}. Mass ratios of binder (PC + GGBS = 1). HRWRA given as SP / B 0.01; defoamer 0.001 (not a column). "
                                     "Silica sand 0.5 of binder. M-E (CaO expansive agent) rejected."})
    rows.append(r)
df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(here, "..", "additions_v2", "w7_w7c.csv"), index=False, encoding="utf-8-sig")
print(df.shape, list(df.columns) == cols)

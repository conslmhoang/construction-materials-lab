"""w8m1: Zahid & Shafiq 2020, Minerals 10(4), 333 (EGC, fly ash + NaOH/WG + PVA 2 vol%). 9 mixes, fc only."""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
cols = list(pd.read_csv(os.path.join(here, "..", "additions", "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
out = os.path.join(here, "..", "additions_v2", "w8_w8m1.csv")
P = {"Article Name": "Effects of Sand/Fly Ash and the Water/Solid Ratio on the Mechanical Properties of Engineered Geopolymer Composite and Mix Design Optimization",
     "Author": "Muhammad Zahid, Nasir Shafiq", "Year": 2020, "DOI / URL": "https://doi.org/10.3390/min10040333"}
# Table 6: (mix, W/GP, S/FA, extra water/FA); Table 7: fc
mixes = [("M1", .22, 0.0, .035, 77.5), ("M2", .22, .4, .035, 77.5), ("M3", .22, .8, .035, 73.0),
         ("M4", .24, 0.0, .058, 73.6), ("M5", .24, .4, .058, 75.0), ("M6", .24, .8, .058, 73.0),
         ("M7", .26, 0.0, .08, 67.0), ("M8", .26, .4, .08, 70.8), ("M9", .26, .8, .08, 72.0)]
SOL, RATIO = 0.36, 2.5                      # alkaline solution / FA ; Na2SiO3 / NaOH (Table 6)
wg = SOL * RATIO / (1 + RATIO)               # Na2SiO3 solution / FA
naoh_sol = SOL / (1 + RATIO)                 # 8 M NaOH solution / FA
naoh = naoh_sol * 0.26                       # Table 3: 8 M solution = 26 % NaOH
naoh_w = naoh_sol * 0.74                     # water of NaOH solution
rows = []
for mid, wgp, sfa, xw, fc in mixes:
    r = dict(P)
    r.update({"FA (Fly ash)": 1.0, "WG / B (Water glass)": round(wg, 4), "NaOH / B": round(naoh, 4),
              "NaOH molarity (M)": 8, "W / B": round(naoh_w + xw, 4), "Extra water / B": xw,
              "SS / B (Silica sand)": sfa, "PVA fiber (vol%)": 2, "PVA length (mm)": 8, "PVA diameter (µm)": 40,
              "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 41, "Total fiber (vol%)": 2,
              "Curing method": "demolded, wrapped in plastic wrap, oven 60 C for 24 h, then lab 23 C until test",
              "Curing time (days)": 28, "Curing temperature (°C)": 60, "Test age (days)": 28, "Heat curing duration (h)": 24,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
              "Compressive strength (MPa)": fc,
              "Source table/page": "Table 6 (mix), Table 3 (solution composition), Table 4 (PVA), Sec 2.3 (curing), Table 7 (fc)",
              "Conversions / notes": (f"{mid}. Binder = fly ash only (high-Ca, CaO 19 %). Table 6 gives alkaline solution 0.36 and "
              "Na2SiO3/NaOH 2.5 (taken as solution mass ratio) per FA: WG/B = 0.36*2.5/3.5 = 0.2571 (Na2O 14.7 %, SiO2 29.75 %, H2O 55.52 %); "
              "8 M NaOH solution = 0.36/3.5 = 0.1029 of FA with 26 % NaOH solids (Table 3) -> NaOH/B 0.0267, its 74 % water (0.0761) + extra water "
              f"{xw} -> W/B. Cross-check: stated W/GP solids {wgp} reproduced within 0.003. Water in WG not added. "
              "PVA 2 vol% of total volume. Flexural strength only (no direct tension), so no tensile columns. "
              "Compressive: 50 mm cube, ASTM C109, tested day 28 (curing time column = age at test).")})
    rows.append(r)
df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(out, index=False, encoding="utf-8-sig")
print(df.shape)

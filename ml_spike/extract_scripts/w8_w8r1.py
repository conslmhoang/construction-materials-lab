"""w8r1: Ramesh et al. 2023, Buildings 13(12), 3020 (PVA-EGC, FA+GGBS+SF, 10 M NaOH solution). Final mix (Table 5), fc at 1/7/14/28 d, 28-d dog-bone tensile strength."""
import os, sys
import pandas as pd
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "..", "additions_v2"))
from naoh_solution import naoh_split
cols = list(pd.read_csv(os.path.join(here, "..", "additions", "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
out = os.path.join(here, "..", "additions_v2", "w8_w8r1.csv")
P = {"Article Name": "Optimisation Investigation and Bond-Slip Behaviour of High Strength PVA-Engineered Geopolymer Composite (EGC) Cured in Ambient Temperatures",
     "Author": "Vishal Avinash Ramesh, Ehsan Nikbakht Jarghouyeh, Ahmed Saleh Alraeeini, Amin Al-Fakih", "Year": 2023,
     "DOI / URL": "https://doi.org/10.3390/buildings13123020"}
# Table 5 (kg/m3)
sand, fa, ggbs, sf, naoh_sol, wg, water, pva, sp = 330, 880, 220, 176, 112, 283, 88, 26, 17.6
B = fa + ggbs + sf
s = naoh_split(10, solution_mass=naoh_sol / B)
fc = {1: 12.58, 7: 46.42, 14: 47.45, 28: 60.0}   # Table 12 mix 4 (Table 14: 60 at 28 d)
rows = []
for age, f in fc.items():
    r = dict(P)
    r.update({"GGBS": round(ggbs / B, 4), "FA (Fly ash)": round(fa / B, 4), "SF (Silica fume)": round(sf / B, 4),
              "WG / B (Water glass)": round(wg / B, 4), "NaOH / B": round(s["NaOH"], 4), "NaOH molarity (M)": 10,
              "W / B": round(water / B + s["water"], 4), "SS / B (Silica sand)": round(sand / B, 4),
              "SP / B": round(sp / B, 4), "Binder content (kg/m³)": B,
              "PVA fiber (vol%)": 2, "PVA length (mm)": 18, "PVA diameter (µm)": 200, "PVA tensile strength (MPa)": 1600,
              "PVA elastic modulus (GPa)": 27, "Total fiber (vol%)": 2,
              "Curing method": "ambient temperature curing, no heat curing (humidity / sealing not stated)",
              "Curing time (days)": age, "Test age (days)": age,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "100",
              "Compressive strength (MPa)": f,
              "Source table/page": "Table 5 (mix), Table 2 (PVA), Sec 2.1/3.4 (ambient curing), Table 12 (fc, mix 4)",
              "Conversions / notes": ("Mix 4 (20 % silica fume replacement), the only mix with full proportions (Table 5, kg/m3). "
              f"Binder B = FA 880 + GGBS 220 + SF 176 = {B} kg/m3 (silica fume counted in binder; its 176 = 20 % of FA mass). "
              "Sodium silicate solution 283 kg/m3 -> WG/B (modulus and solids not stated). "
              f"NaOH solution 112 kg/m3 -> {s['note']}; paper also says 400 g NaOH per litre (= 10 M). NaOH/B = solids, solution water added to W/B (88 kg/m3 free water + solution water). "
              "SP 17.6 kg/m3 (text: 2 % of FA). PVA 26 kg/m3 / 1300 = 2.0 vol% (text: 2 vol%). "
              "Curing only described as ambient temperature (no temperature value). No tensile strain reported.")})
    if age == 28:
        r.update({"Tensile strength (MPa)": 4.003, "Tensile specimen": "dog-bone", "Tensile test type": "direct (uniaxial)"})
        r["Source table/page"] += ", Table 14 (tensile strength, mean of 2 dog-bone specimens, ASTM D3039)"
    rows.append(r)
df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(out, index=False, encoding="utf-8-sig")
print(df.shape); print(df[["GGBS","FA (Fly ash)","SF (Silica fume)","WG / B (Water glass)","NaOH / B","W / B","SS / B (Silica sand)","SP / B","Compressive strength (MPa)"]].to_string())

"""w8e3: Kan et al. 2024, J. Build. Eng. 110392 (alkali-activated slag/SF + PE 2 vol%, 4 curing regimes, direct tension)."""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
cols = list(pd.read_csv(os.path.join(here, "..", "additions", "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
out = os.path.join(here, "..", "additions_v2", "w8_w8e3.csv")
P = {"Article Name": "Curing-dependent behaviors of sustainable alkali-activated fiber reinforced composite: Temperature and humidity effects",
     "Author": "Lili Kan, Yuan-qiao Gan, Wei Dai, Luo-hao Lv, Lan-qing Dai, Jia-bao Zhai, Fei Wang", "Year": 2024,
     "DOI / URL": "https://doi.org/10.1016/j.jobe.2024.110392"}
# Table 1 (wt% of mix): GGBS 46.24, SF 11.56, sand 17.34, NaOH 2.08, Na2SiO3 solution 9.48, water 13.29, PE 2 vol%
B = 46.24 + 11.56
base = {"GGBS": round(46.24 / B, 4), "SF (Silica fume)": round(11.56 / B, 4),
        "WG / B (Water glass)": round(9.48 / B, 4), "NaOH / B": round(2.08 / B, 4),
        "W / B": round(13.29 / B, 4), "River sand / B": round(17.34 / B, 4),
        "PE fiber (vol%)": 2, "PE length (mm)": 12, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000,
        "PE elastic modulus (GPa)": 110, "Total fiber (vol%)": 2, "Demolding age (days)": 1, "Test age (days)": 28,
        "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
        "Tensile specimen": "dog-bone (JSCE)", "Tensile gauge length (mm)": 80, "Tensile test type": "direct (uniaxial)"}
# curing: (label, method, temp, RH, heat h, ft, strain %, first-crack)
cur = [("Dry curing", "sealed 24 h, demolded, dry curing 20 C RH 60 % to 27 d", 20, 60, None, 3.92, 7.96, 2.15),
       ("Standard curing", "sealed 24 h, demolded, standard curing 20 C RH 95 % to 27 d", 20, 95, None, 4.65, 9.60, 2.37),
       ("High-temperature curing", "sealed 24 h, demolded, 60 C for 1 d then dry curing (20 C RH 60 %) to 28 d", 60, 60, 24, 3.85, 12.2, 1.91),
       ("Low-temperature curing", "sealed 24 h, demolded, low-temperature curing at -5 C to 28 d", -5, None, None, 3.62, 5.12, 1.97)]
rows = []
for lab, meth, T, RH, hh, ft, eps, fcr in cur:
    r = dict(P); r.update(base)
    r.update({"Curing method": meth, "Curing time (days)": 28, "Curing temperature (°C)": T, "Curing RH (%)": RH,
              "Heat curing duration (h)": hh, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "First-cracking strength (MPa)": fcr,
              "Source table/page": "Table 1 (mix, wt%), Table 3 (PE), Sec 2.2 (curing), Table 4 (tensile)",
              "Conversions / notes": (f"{lab}. Table 1 gives mix in wt% of total mix (GGBS 46.24, SF 11.56, sand 17.34, NaOH 2.08, Na2SiO3 solution 9.48, "
              "water 13.29, PE 2 vol%); all ratios = wt% / binder wt% (B = GGBS + SF = 57.80 wt%). Sodium silicate solution is water glass "
              "(SiO2/Na2O 3.3, water 64.16 %); its water is not in W/B. Solid NaOH granules 99 %. Sand = river sand (Fig 2 caption). "
              "Tensile values are mean of >=3 dog-bone specimens, strain = strain at peak stress. Compressive strength only in Fig 8 (no number) so left blank. "
              "Test age 28 d is implied by curing 'to 27 d/28 d' after 24 h sealed (not stated as a separate sentence); curing time column = age at test. "
              "Compressive cube 50 mm (Sec 2.3.2). Low-temp RH not stated.")})
    rows.append(r)
df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(out, index=False, encoding="utf-8-sig")
print(df.shape)

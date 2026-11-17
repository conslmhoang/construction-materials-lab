"""Wave 6, agent e19: rows from Elsevier full texts. Writes additions_v2/w6_e19.csv.
Papers: cemconres.2007.04.001 (Sahmaran & Li), cemconres.2014.01.002 (Ranade et al.)"""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
cols = list(pd.read_csv(os.path.join(here, "..", "additions", "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
out = os.path.join(here, "..", "additions_v2", "w6_e19.csv")
rows = []
r4 = lambda x: round(x, 4)
D = "direct (uniaxial)"

# 1) De-icing salt scaling ECC: only unexposed reference specimens (7, 28 d, and 28+25 / 28+50 d lab air)
P = {"Article Name": "De-icing salt scaling resistance of mechanically loaded engineered cementitious composites",
     "Author": "Mustafa Sahmaran, Victor C. Li", "Year": 2007, "DOI / URL": "https://doi.org/10.1016/j.cemconres.2007.04.001"}
mixes = {"ECC-1 (M45)": (570, 684, 331, 455, 4.9, {7: (38.1, 3.48, 3.73), 28: (50.2, 3.16, 4.45), 53: (None, 3.075, 4.456), 78: (None, 2.93, 4.73)}),
         "ECC-2": (386, 847, 327, 448, 3.7, {7: (21.6, 4.21, 3.15), 28: (36.3, 3.40, 4.07), 53: (None, 3.37, 4.16), 78: (None, 3.43, 4.32)})}
for mid, (c, fa, w, s, hr, ages) in mixes.items():
    B = c + fa
    for age, (fc, eps, ft) in ages.items():
        r = dict(P)
        r.update({"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "W / B": r4(w / B), "Sand (type not stated) / B": r4(s / B),
                  "HRWR / B": r4(hr / B), "Binder content (kg/m³)": B, "PVA fiber (vol%)": 2.0, "PVA length (mm)": 8, "PVA diameter (µm)": 39,
                  "PVA tensile strength (MPa)": 1620, "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": 2.0,
                  "Curing method": "demoulded 24 h, moist cured in plastic bag 95 % RH 23 C 14 d, then lab air 50 % RH 23 C" if age > 7 else "demoulded 24 h, moist cured in plastic bag 95 % RH 23 C",
                  "Curing temperature (°C)": 23, "Curing RH (%)": 95 if age <= 14 else 50, "Demolding age (days)": 1, "Test age (days)": age,
                  "Tensile specimen": "coupon 152.4x76.2x12.7 mm", "Tensile test type": D,
                  "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
                  "Source table/page": "Table 2 (mix, fc), Table 6/7 (tensile), sect. 2.1",
                  "Conversions / notes": f"{mid}. kg/m3 / B (cement + FA). PVA 26 kg/m3 / 1300 = 2.0 vol% (density assumed). HRWR dose by eye. "
                  "Only unexposed specimens; pre-cracked / freeze-thaw de-icing salt rows and the fibre-free mortars skipped. Strain = ultimate tensile strain (strain at peak). "
                  "VERIFY: curing time for 7 d = moist period, ages 53/78 = 28 d + 25/50 d lab air from Table 6/7; Table 6/7 labels all 7 d as 'cured in laboratory air after 14 d moist'."})
        if age == 7 or age == 28:
            r.update({"Compressive strength (MPa)": fc, "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "75x150"})
        r["Curing time (days)"] = min(age, 14) if age <= 28 else age
        r["Curing time (days)"] = age
        rows.append(r)

# 2) Piezoresistive ECC: M45 and HFA, 28 d, direct tension (averages Table 2)
P = {"Article Name": "Influence of micro-cracking on the composite resistivity of Engineered Cementitious Composites",
     "Author": "Ravi Ranade, Jie Zhang, Jerome P. Lynch, Victor C. Li", "Year": 2014, "DOI / URL": "https://doi.org/10.1016/j.cemconres.2014.01.002"}
for mid, c, fa, w, s, hr, eps, ft, fcr in (("M45-ECC", 578, 693, 330, 455, 2.7, 2.1, 5.1, 3.4), ("HFA-ECC", 324, 906, 324, 453, 2.1, 4.5, 4.5, 3.1)):
    B = c + fa
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "W / B": r4(w / B), "SS / B (Silica sand)": r4(s / B), "HRWR / B": r4(hr / B),
              "Binder content (kg/m³)": B, "PVA fiber (vol%)": 2.0, "Total fiber (vol%)": 2.0,
              "Curing method": "24 h in mould at room temperature, demoulded, stored at room temperature 23 C RH 20 % until 28 d",
              "Curing time (days)": 28, "Curing temperature (°C)": 23, "Curing RH (%)": 20, "Demolding age (days)": 1, "Test age (days)": 28,
              "Tensile specimen": "coupon 12.7x76 mm", "Tensile test type": D, "First-cracking strength (MPa)": fcr,
              "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix), Table 2 (avg of 4 coupons), sect. 2.2",
              "Conversions / notes": f"{mid}. kg/m3 / B (cement Type I + class F FA). PVA 26 kg/m3 / 1300 = 2.0 vol% (REC15, SG 1.3 stated). No compressive strength reported. "
              "Fibre length/diameter not given. Values = average of Table 2 (strain capacity = eps_tu). HRWRA entered as HRWR."})
    rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(out, index=False, encoding="utf-8-sig")
print(len(df), "rows ->", out)

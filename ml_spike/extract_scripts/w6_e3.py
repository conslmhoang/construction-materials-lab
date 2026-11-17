"""Wave 6, agent e3: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e3.csv (99-column TEMPLATE header).
Papers: 10.1016/j.jobe.2025.112196, j.jobe.2026.116662, j.jobe.2026.117741, j.jobe.2025.115166, j.jobe.2026.115900
"""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
add = os.path.join(here, "..", "additions")
out_dir = os.path.join(here, "..", "additions_v2")
cols = list(pd.read_csv(os.path.join(add, "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
rows = []

# ---------------------------------------------------------------- 1) 3D-printable ECC, 8 mm PVA/PE (112196)
P = {"Article Name": "A study on achieving high tensile ductility in 3D-Printable engineered cementitious composites reinforced with 8 mm fibers",
     "Author": "Amir Bakhshi, Muhammad Saeed Zafar, Maryam Hojati", "Year": 2025,
     "DOI / URL": "https://doi.org/10.1016/j.jobe.2025.112196"}
mixes = {"FA50": ({"OPC / Cement": .5, "FA (Fly ash)": .5}, 0.23),
         "S50": ({"OPC / Cement": .5, "GGBS": .5}, 0.30),
         "FA40-SF10": ({"OPC / Cement": .5, "FA (Fly ash)": .4, "SF (Silica fume)": .1}, 0.27),
         "FA40-MK10": ({"OPC / Cement": .5, "FA (Fly ash)": .4, "Metakaolin": .1}, 0.27)}
# (mix, fiber, vol, first crack, ft, strain %)
t4 = [("FA50", "PVA", 1.5, 3.13, 3.82, 1.07), ("FA50", "PVA", 2, 2.71, 3.51, 1.18), ("FA50", "PE", 2, 3.68, 4.94, 7.35),
      ("FA40-MK10", "PVA", 1.5, 2.93, 3.76, 0.55), ("FA40-MK10", "PVA", 2, 2.39, 3.88, 2.11), ("FA40-MK10", "PE", 2, 3.99, 5.85, 8.67),
      ("FA40-SF10", "PVA", 1.5, 2.05, 2.62, 0.64), ("FA40-SF10", "PVA", 2, 3.17, 3.61, 1.14), ("FA40-SF10", "PE", 2, 1.76, 2.95, 9.71),
      ("S50", "PVA", 1.5, 2.95, 3.77, 0.53), ("S50", "PVA", 2, 2.59, 4.03, 1.54), ("S50", "PE", 2, 2.16, 4.73, 11.9)]
for mid, fib, vol, fcr, ft, eps in t4:
    r = dict(P)
    bf, wb = mixes[mid]
    r.update(bf)
    r.update({"W / B": wb, "River sand / B": 0.25, "HRWR / B": 0.006, "VMA / B": 0.01, "Total fiber (vol%)": vol,
              "Curing method": "demolded at 24 h, moist room 100 % RH, 23 C", "Curing time (days)": 28,
              "Curing temperature (°C)": 23, "Curing RH (%)": 100, "Demolding age (days)": 1, "Test age (days)": 28,
              "Tensile specimen": "dogbone (JSCE), 30 mm wide filament 3D printed in mold + cast ends", "Tensile test type": "direct (uniaxial)",
              "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 3 (mix), Table 4 (tensile), sect. 3.1/3.4 (curing)",
              "Conversions / notes": f"{mid}, {fib} {vol} vol%. Slag = GGBS (column S/B). MC (methylcellulose) 0.01 of B stored as VMA. "
                                     "VERIFY: Table 3 gives W/B 0.27 and 'Adjusted W/B' (0.23/0.30/0.27/0.27); adjusted value used. "
                                     "Tensile specimens 3D printed (fiber-oriented); fc only in Fig. 6, not entered."})
    if fib == "PVA":
        r.update({"PVA fiber (vol%)": vol, "PVA length (mm)": 8, "PVA diameter (µm)": 38, "PVA tensile strength (MPa)": 1600})
    else:
        r.update({"PE fiber (vol%)": vol, "PE length (mm)": 8, "PE diameter (µm)": 15, "PE tensile strength (MPa)": 3000})
    rows.append(r)

# ---------------------------------------------------------------- 2) ultra-high GGBS ECC (116662)
P = {"Article Name": "Mechanical and environmental performance of sustainable high-strength engineered cementitious composites (ECC) with ultra-high GGBS content",
     "Author": "Ke-Fan Weng, Yu-Qi Liu, Shi-Wen Han, Pan Gao, Cheng Hu, Jing Yu", "Year": 2026,
     "DOI / URL": "https://doi.org/10.1016/j.jobe.2026.116662"}
# mix: (cement, GGBS, SF, SP/B)
mx = {"GS70": (.25, .70, .05, .017), "GS75": (.20, .75, .05, .017), "GS80": (.15, .80, .05, .017),
      "GS85": (.10, .85, .05, .014), "GS90": (.05, .90, .05, .011),
      "SF0": (.20, .80, 0, .017), "SF2.5": (.175, .80, .025, .017), "SF7.5": (.125, .80, .075, .017), "SF10": (.10, .80, .10, .017)}
# (mix, regime, curing days after demolding, fc, ft, strain %, note)
t = [("GS70", "amb", 1, 18.2, None, None, "fc from text"),
     ("GS70", "amb", 28, 125.3, None, None, "VERIFY: Table 5 gives 125.3, text of sect. 3.1.1 says 126.3 MPa"),
     ("GS75", "amb", 28, 124.1, None, None, "fc Table 5"),
     ("GS80", "amb", 1, 16.6, None, None, "fc from text"),
     ("GS80", "amb", 28, 120.6, 9.47, 3.50, "GS80 = SA0.3 = SF5 reference mix; ft and strain from text (SF series, direct tension)"),
     ("GS80", "steam", 1, 123.7, None, None, "steam 90 C 1 d, fc Table 5/text"),
     ("GS80", "steam", 7, 126.2, None, None, "steam 90 C 7 d, fc from text"),
     ("GS85", "amb", 28, 113.5, None, None, "fc Table 5"),
     ("GS90", "amb", 1, 10.2, None, None, "fc from text"),
     ("GS90", "amb", 28, 89.5, None, None, "fc Table 5"),
     ("SF0", "amb", 1, 9.2, None, None, "fc from text"),
     ("SF0", "amb", 28, 65.1, 7.45, 2.11, "fc, ft, strain from text (Table 6 rounds ft to 7.4)"),
     ("SF2.5", "amb", 28, None, 9.2, 4.37, "ft from Table 6 (rounded, text gives no ft); VERIFY: Table 2 prints cement 0.075 but binder sums to 1 only with 0.175 (Table 6: 17.5 % cement), 0.175 used"),
     ("SF7.5", "amb", 1, 19.1, None, None, "fc from text"),
     ("SF7.5", "amb", 28, 137.3, 10.41, 3.67, "fc, ft, strain from text"),
     ("SF10", "amb", 28, None, 8.15, 3.42, "ft, strain from text")]
for mid, reg, d, fc, ft, eps, note in t:
    c, g, sf, sp = mx[mid]
    r = dict(P)
    r.update({"OPC / Cement": c, "GGBS": g, "SF (Silica fume)": sf, "W / B": 0.194, "SS / B (Silica sand)": 0.3, "SP / B": sp,
              "PE fiber (vol%)": 2.0, "Total fiber (vol%)": 2.0, "Demolding age (days)": 3, "Curing time (days)": d,
              "Test age (days)": 3 + d, "Compressive specimen": "cube", "Compressive specimen size (mm)": "40",
              "Source table/page": "Table 2 (mix), Table 5/6 and sect. 3.1-3.3 text (strengths, strain), sect. 2.1 (curing)",
              "Conversions / notes": f"{mid}. Covered in mold 72 h, demolded at 3 d, curing time counted from demolding; test age = 3 d + curing days (derived). {note}. "
                                     "Silica sand (quartz skeleton). PE fiber length/diameter not stated in text."})
    if reg == "amb":
        r.update({"Curing method": "covered 72 h then ambient 20 C, RH ~95 %", "Curing temperature (°C)": 20, "Curing RH (%)": 95})
    else:
        r.update({"Curing method": "covered 72 h then steam curing 90 C", "Curing temperature (°C)": 90, "Heat curing duration (h)": 24 * d})
    if fc is not None:
        r["Compressive strength (MPa)"] = fc
    if ft is not None:
        r.update({"Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps, "Tensile test type": "direct (uniaxial)",
                  "Tensile specimen": "coupon (DIC)"})
    rows.append(r)

# ---------------------------------------------------------------- 3) HS-HDCC, 0 d reference before sulfate exposure (117741)
P = {"Article Name": "Long-Term Mechanical Performance and Stage-Dependent Ductility Evolution of High-Strength High-Ductility Cementitious Composites Under Full Immersion in 5 wt% Na2SO4 Solution",
     "Author": "Yingjie Chu, Li-Ping Guo, Hao-Ran Shen, Guo-Tai Zhao, Jia-Yi Li, Hai-Tao Chen", "Year": 2026,
     "DOI / URL": "https://doi.org/10.1016/j.jobe.2026.117741"}
for mid, sf, lp, fc, eps in [("SF10", .1, .5, 91.2, 8.6), ("SF20", .2, .4, 98.6, None), ("SF30", .3, .3, 109.1, None)]:
    r = dict(P)
    r.update({"OPC / Cement": 0.4, "SF (Silica fume)": sf, "Limestone powder": lp, "W / B": 0.23, "River sand / B": 0.38,
              "SP / B": 0.02, "HPMC / B (hydroxypropyl methyl cellulose)": 0.0001, "PE fiber (vol%)": 2, "PE length (mm)": 12,
              "PE diameter (µm)": 24, "PE elastic modulus (GPa)": 100, "Total fiber (vol%)": 2,
              "Curing method": "sealed 24 h at 22 C, then 28 d at 22 C RH > 95 % (0 d = start of sulfate immersion)",
              "Curing time (days)": 28, "Curing temperature (°C)": 22, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 29,
              "Compressive specimen": "prism halves 40x40x160", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 1 (mix), sect. 3.1 text (0 d values), sect. 2.2 (curing)",
              "Conversions / notes": f"{mid}. Only the 0 d reference (before sulfate exposure) is used. SP 2 % of B, HPMC 0.1 permille of B. "
                                     "Test age 29 d = 1 d + 28 d curing (derived). "
                                     + ("Initial tensile strain 8.6 % stated in text for SF10 only; ft not given in text." if eps else "Initial tensile strain only given as % reduction, not entered.")})
    if eps is not None:
        r.update({"Tensile strain capacity (%)": eps, "Tensile specimen": "dumbbell", "Tensile gauge length (mm)": 100, "Tensile test type": "direct (uniaxial)"})
    rows.append(r)

# ---------------------------------------------------------------- 4) CR-ECC control mix CR0.00 (115166)
P = {"Article Name": "Enhancing the long-age ductile performance of Engineered Cementitious Composites (ECC) by replacing sand with crumb rubber",
     "Author": "Shichao Song, Xiuhua Guo, Guoju Ke, Jinyu Fu, Huqing Yang", "Year": 2025,
     "DOI / URL": "https://doi.org/10.1016/j.jobe.2025.115166"}
for age, fcr, ft, eps, cur in [(28, 4.83, 8.07, 9.51, "28 d standard curing box 20 C, RH 95 %"),
                               (60, 5.69, 9.21, 2.32, "28 d standard curing 20 C RH 95 %, then laboratory air 18.3 C RH 32 %"),
                               (90, 5.60, 9.35, 2.66, "28 d standard curing 20 C RH 95 %, then laboratory air 18.3 C RH 32 %")]:
    r = dict(P)
    r.update({"OPC / Cement": .55, "FA (Fly ash)": .21, "SF (Silica fume)": .16, "GGBS": .08, "W / B": 0.18, "SS / B (Silica sand)": 0.3,
              "SP / B": 0.015, "PE fiber (vol%)": 2.0, "PE length (mm)": 18, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3200,
              "PE elastic modulus (GPa)": 116, "Steel fiber (vol%)": 0.5, "Steel length (mm)": 13, "Steel diameter (µm)": 200,
              "Steel tensile strength (MPa)": 2400, "Steel elastic modulus (GPa)": 200, "Total fiber (vol%)": 2.5,
              "Curing method": cur, "Curing time (days)": age, "Curing temperature (°C)": 20 if age == 28 else None,
              "Curing RH (%)": 95 if age == 28 else None, "Demolding age (days)": 1, "Test age (days)": age,
              "Tensile specimen": "dogbone", "Tensile gauge length (mm)": 80, "Tensile test type": "direct (uniaxial)",
              "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 3 (mix), Table 4 (tensile, strain = epsilon_peak), sect. 2.1-2.2 (curing)",
              "Conversions / notes": f"CR0.00-D{age} (control, no crumb rubber; rubber mixes CR0.25-0.75 skipped because rubber mass/B is not stated, only vol% replacement of sand). "
                                     "Steel fiber 0.5 vol% + PE 2.0 vol%. Strain = strain at peak stress. fc only in Fig. 8."})
    rows.append(r)

# ---------------------------------------------------------------- 5) RPC with steel fiber, 20 C reference (115900)
P = {"Article Name": "Ultra-low temperature effects on tensile stress-strain relationships in reactive powder concrete",
     "Author": "Qin Rong, Junhua Zhang, Xiaomeng Hou, Boxin Wang", "Year": 2026,
     "DOI / URL": "https://doi.org/10.1016/j.jobe.2026.115900"}
r = dict(P)
r.update({"OPC / Cement": round(900 / 1305, 4), "SF (Silica fume)": round(270 / 1305, 4), "GGBS": round(135 / 1305, 4),
          "W / B": round(222 / 1305, 3), "SS / B (Silica sand)": round(1080 / 1305, 3), "SP / B": round(9 / 1305, 4),
          "Steel fiber (vol%)": round(156 / 7850 * 100, 2), "Total fiber (vol%)": round(156 / 7850 * 100, 2), "Binder content (kg/m³)": 1305,
          "Curing method": "20 C RH 95 % 24 h, demolded, then steam curing 90 C RH 95 % 3 d", "Curing time (days)": 3,
          "Curing temperature (°C)": 90, "Curing RH (%)": 95, "Demolding age (days)": 1, "Heat curing duration (h)": 72,
          "Compressive specimen": "cube", "Compressive strength (MPa)": 140,
          "Tensile specimen": "dog-bone 560x100x30", "Tensile gauge length (mm)": 200, "Tensile test type": "direct (uniaxial)",
          "Tensile strain capacity (%)": 0.5425,
          "Source table/page": "Table 2 (mix, cubic fc), Table 5 (eps_tu at 20 C)",
          "Conversions / notes": "Only the 20 C (room temperature) reference of a cryogenic study. kg/m3: clinker 900, SF 270, slag 135 (B = 1305), water 222, quartz sand 540+540, SP 9, "
                                 "steel fiber 156 (=1.99 vol% at 7850). VERIFY: Table 2 header misaligned (first column holds water 222 kg/m3); "
                                 "strain = eps_tu 5424.8 microstrain from Table 5 (ultimate strain, not clearly peak strain); test age not stated; "
                                 "tensile strength at 20 C not given as number (only 1.48x ratio) so not entered."})
rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e3.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows ->", os.path.join(out_dir, "w6_e3.csv"))

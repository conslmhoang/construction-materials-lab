"""Wave 6, agent e20: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e20.csv (99-column TEMPLATE header).
Papers: cemconres.2021.106388, cemconres.2024.107511, compositesb.2012.08.015, compositesb.2023.110993,
        conbuildmat.2015.07.039, 2015.07.182, 2015.08.041
Tables 1 and 4 of compositesb.2012.08.015 are parsed from the local text dump.
"""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
add = os.path.join(here, "..", "additions")
out_dir = os.path.join(here, "..", "additions_v2")
txt_dir = os.path.join(here, "..", "..", "Papers", "Paper news", "elsevier_txt")
cols = list(pd.read_csv(os.path.join(add, "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
rows = []
DIRECT = "direct (uniaxial)"


def r4(x):
    return round(x, 4)


# ---------------------------------------------------------------- 1) 3DP-ECC, cast reference rows only
P = {"Article Name": "3D-printable engineered cementitious composites (3DP-ECC): Fresh and hardened properties",
     "Author": "Kequan Yu, Wes McGee, Tsz Yan Ng, He Zhu, Victor C. Li", "Year": 2021,
     "DOI / URL": "https://doi.org/10.1016/j.cemconres.2021.106388"}
B = 309 + 1026
for mid, age, fcs, fc, fcr, ft, eps in (("C-13-3d", 3, None, None, 1.63, 2.25, 3.45), ("C-13-28d", 28, "cube", 31.20, 2.56, 3.36, 3.00)):
    r = dict(P)
    r.update({"OPC / Cement": r4(309 / B), "FA (Fly ash)": r4(1026 / B), "W / B": r4(321 / B), "SS / B (Silica sand)": r4(345 / B),
              "SP / B": r4(3 / B), "VMA / B": r4(2 / B), "Binder content (kg/m³)": B, "PVA fiber (vol%)": 2.0, "PVA length (mm)": 8,
              "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 30, "Total fiber (vol%)": 2.0,
              "Curing method": "not stated (curing age counted from casting)", "Curing time (days)": age, "Test age (days)": age,
              "Compressive specimen": fcs, "Compressive specimen size (mm)": "50" if fcs else None,
              "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
              "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft, "First-cracking strength (MPa)": fcr, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 3 (mix), Table 6 (cast tension), text sect. 3.2.1 (cast cube fc 31.20)",
              "Conversions / notes": f"{mid}: cast (not printed) specimens only. kg/m3 / B (cement + FA = 1335). Printed specimens skipped. "
                                     "VERIFY: curing temperature/humidity not stated; age = 'curing age' counted as test age. "
                                     + ("" if fc else "No cast-cube fc at 3 d (fc only given for 28 d).")})
    rows.append(r)

# ---------------------------------------------------------------- 2) river sand ECC (PE), 90 C oven
P = {"Article Name": "Multiple cracking and strain-hardening criteria of Engineered Cementitious Composites (ECC) with river sand",
     "Author": "Yazhao Li, Junxia Li, En-Hua Yang, Xinchun Guan", "Year": 2024,
     "DOI / URL": "https://doi.org/10.1016/j.cemconres.2024.107511"}
t2 = [("W/B-RS/B:0.16-0.45", 839, 419, 140, 224, 629, 20, 6.10, 10.37, 9.44, "hs"),
      ("W/B-RS/B:0.16-0.55", 789, 395, 132, 211, 724, 20, 5.67, 9.69, 10.00, "hs"),
      ("W/B-RS/B:0.16-0.65", 746, 373, 124, 199, 808, 23, 5.11, 7.81, 11.50, "hs"),
      ("W/B-RS/B:0.24-0.36", 502, 753, 0, 301, 452, 10, 3.24, 6.02, 10.12, "ns"),
      ("W/B-RS/B:0.24-0.45", 450, 673, 0, 269, 617, 11, 3.76, 6.05, 9.07, "ns"),
      ("W/B-RS/B:0.24-0.75", 404, 605, 0, 242, 756, 17, 4.06, 5.21, 4.09, "ns")]
for mid, c, fa, sf, w, rs, sp, fcr, ft, eps, lvl in t2:
    B = c + fa + sf
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "SF (Silica fume)": r4(sf / B) if sf else None, "W / B": r4(w / B),
              "River sand / B": r4(rs / B), "Sand max size (µm)": 4750, "SP / B": r4(sp / B), "Binder content (kg/m³)": B,
              "PE fiber (vol%)": 2.0, "PE length (mm)": 18 if lvl == "hs" else 12, "PE diameter (µm)": 19 if lvl == "hs" else 24,
              "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 110, "Total fiber (vol%)": 2.0,
              "Curing method": "covered with plastic film 24 h, demoulded, then oven 90 C for 3 d", "Curing time (days)": 3,
              "Curing temperature (°C)": 90, "Demolding age (days)": 1, "Test age (days)": 4, "Heat curing duration (h)": 72,
              "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
              "Tensile strength (MPa)": ft, "First-cracking strength (MPa)": fcr, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix), Table 3 (tension), sect. 4.1 (fibers, curing)",
              "Conversions / notes": f"{mid}. kg/m3 / B (binder = OPC + FA + SF = {B}). Fc not reported. First-cracking = matrix cracking strength. "
                                     "River sand 0-4.75 mm. VERIFY: test age 4 d = 24 h in mould + 3 d oven (paper says 'before testing'). "
                                     "Mixture '0.24-0.45' in Table 1/3 has RS/B 0.55 from the kg/m3 (Table 4 calls it 0.24-0.55); label kept from Table 3."})
    rows.append(r)

# ---------------------------------------------------------------- 3) ECC factorial mixes (Sahmaran et al.), fc of ECC with PVA
P = {"Article Name": "Improving the workability and rheological properties of Engineered Cementitious Composites using factorial experimental design",
     "Author": "Mustafa Sahmaran, Zafer Bilici, Erdogan Ozbay, Tahir K. Erdem, Hasan E. Yucel, Mohamed Lachemi", "Year": 2013,
     "DOI / URL": "https://doi.org/10.1016/j.compositesb.2012.08.015"}
lines = open(os.path.join(txt_dir, "ELS_10_1016_j_compositesb_2012_08_015.txt"), encoding="utf-8").read().splitlines()
mix, fcd = {}, {}
tab = None
for ln in lines:
    if ln.startswith("[[TABLE]]"):
        tab = ln.split(".")[0].replace("[[TABLE]] ", "")
        continue
    p = ln.split("\t")
    if p and p[0].startswith("M") and p[0][1:].isdigit():
        if tab == "Table 1" and len(p) == 11:
            mix[p[0]] = [float(x) for x in p[1:]]
        if tab == "Table 4" and len(p) == 5:
            fcd[p[0]] = float(p[4])
assert len(mix) == 36 and len(fcd) == 36, (len(mix), len(fcd))
for mid in sorted(mix, key=lambda s: int(s[1:])):
    wb, sb, spb, dmax, pc, fa, w, pva, sand, sp = mix[mid]
    B = pc + fa
    r = dict(P)
    r.update({"OPC / Cement": r4(pc / B), "FA (Fly ash)": r4(fa / B), "W / B": r4(w / B), "SS / B (Silica sand)": r4(sand / B),
              "Sand max size (µm)": dmax, "SP / B": r4(sp / B), "Binder content (kg/m³)": B, "PVA fiber (vol%)": 2.0, "PVA length (mm)": 8,
              "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600, "Total fiber (vol%)": 2.0,
              "Curing method": "demoulded 24 h, sealed plastic bags 23 C 7 d, then air 23 C RH 50 % to 28 d", "Curing time (days)": 28,
              "Curing temperature (°C)": 23, "Curing RH (%)": 50, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Compressive strength (MPa)": fcd[mid],
              "Source table/page": "Table 1 (mix), Table 4 (fc of ECC with PVA), sect. 2.2-2.3",
              "Conversions / notes": f"{mid}. kg/m3 / B (PC + FA = {B:.0f}). 'Fine quartz' aggregate (Dmax {int(dmax)} um) entered as silica sand. "
                                     "PVA 26 kg/m3 / 1300 = 2 vol% (stated 2 %). No tension test (flexure only). "
                                     "VERIFY: cube size 50 mm stated for the matrix cubes; same size assumed for fiber mixes."})
    rows.append(r)

# ---------------------------------------------------------------- 4) generative-AI designed PE-ECC
P = {"Article Name": "Generative AI for performance-based design of engineered cementitious composite",
     "Author": "Jie Yu, Yiwei Weng, Jiangtao Yu, Wenguang Chen, Shuainan Lu, Kequan Yu", "Year": 2023,
     "DOI / URL": "https://doi.org/10.1016/j.compositesb.2023.110993"}
# id, cement, fa, lp, ggbs, sf, sand, water, fiber%, len, hrwr, vma, ft, eps, table
t4 = [("No.1", 563, 256, 71, 379, 68, 408, 364, 1.3, 12, 3, .5, 4.66, 4.13, "Table 3, Table 5"),
      ("No.2", 698, 248, 36, 259, 45, 433, 375, 1.7, 18, 1, .5, 6.74, 8.06, "Table 3, Table 5"),
      ("No.3", 589, 49, 101, 626, 125, 436, 298, 1.6, 12, 5, 0, 8.46, 3.99, "Table 3, Table 5"),
      ("No.4", 611, 53, 75, 582, 118, 439, 313, 1.9, 18, 3, 0, 9.86, 8.03, "Table 3, Table 5"),
      ("No.5", 653, 25, 127, 752, 153, 460, 211, 1.9, 12, 11, 0, 12.16, 3.20, "Table 3, Table 5"),
      ("No.6", 678, 27, 101, 733, 153, 458, 237, 2.1, 18, 10, 0, 15.02, 6.18, "Table 3, Table 5"),
      ("Reference", 699, 321, 0, 210, 69, 449, 364, 1.9, 12, 2, .5, 6.63, 5.92, "Table 6, Table 8"),
      ("Low-cost", 826, 344, 0, 145, 29, 434, 361, 1.3, 18, 2, .5, 6.68, 5.79, "Table 6, Table 8"),
      ("Low-carbon", 450, 87, 96, 596, 101, 425, 349, 1.3, 18, 2, .5, 6.49, 5.98, "Table 6, Table 8")]
for mid, c, fa, lp, g, sf, sd, w, fv, ln_, hr, vma, ft, eps, tn in t4:
    B = c + fa + lp + g + sf
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B) or None, "Limestone powder": r4(lp / B) or None, "GGBS": r4(g / B),
              "SF (Silica fume)": r4(sf / B), "W / B": r4(w / B), "SS / B (Silica sand)": r4(sd / B), "HRWR / B": r4(hr / B),
              "VMA / B": r4(vma / B) or None, "Binder content (kg/m³)": B, "PE fiber (vol%)": fv, "PE length (mm)": ln_, "PE diameter (µm)": 24,
              "PE tensile strength (MPa)": 2400, "PE elastic modulus (GPa)": 100, "Total fiber (vol%)": fv,
              "Curing method": "demoulded 24 h, then air 28 d", "Curing time (days)": 28, "Demolding age (days)": 1, "Test age (days)": 29,
              "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
              "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps, "Source table/page": tn + ", sect. 4.2",
              "Conversions / notes": f"{mid}. Paper units g/L treated as kg/m3; B = cement + FA + LP + GGBS + SF = {B}. Fine silica sand. "
                                     "Experimental averages entered (not the model targets). Fc not reported. "
                                     "VERIFY: 'cured in air for 28 days' after 24 h demoulding; test age 29 d derived, curing temp/RH not stated."})
    rows.append(r)

# ---------------------------------------------------------------- 5) alkali-activated slag PVA composites
P = {"Article Name": "Rheological and mechanical properties of fiber-reinforced alkali-activated composite",
     "Author": "Se-Jin Choi, Jeong-Il Choi, Jin-Kyu Song, Bang Yeon Lee", "Year": 2015,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2015.07.182"}
t5 = [("M40-1.0", .40, 1.0, 18.5, 1.37, 1.66, 1.20), ("M40-1.3", .40, 1.3, 18.3, 1.53, 2.26, 2.38),
      ("M45-1.0", .45, 1.0, 16.2, 1.08, 1.46, 1.02), ("M45-1.3", .45, 1.3, 16.6, 1.14, 1.41, 1.10)]
for mid, w, fv, fc, fcr, ft, eps in t5:
    r = dict(P)
    r.update({"GGBS": 1.0, "Ca(OH)2 / B": r4(0.075 / 0.895), "Na2SO4 / B": r4(0.03 / 0.895), "W / B": r4(w / 0.895),
              "PVA fiber (vol%)": fv, "PVA length (mm)": 8, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 41,
              "Total fiber (vol%)": fv,
              "Curing method": "covered in air 23 C 1 d, demoulded, water 23 C 28 d", "Curing time (days)": 29, "Curing temperature (°C)": 23,
              "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
              "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
              "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft, "First-cracking strength (MPa)": fcr, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix), Table 5 (fc 28 d), Table 6 (tension), sect. 3.2",
              "Conversions / notes": f"{mid}. Table 1 binder = GGBS 0.895 + Ca(OH)2 0.075 + Na2SO4 0.03 (= 1); re-expressed with B = GGBS (all ratios / 0.895), "
                                     "same convention as w6_e8/e9. HRWRA column (0.27-0.36) has no unit in Table 1, left empty. No sand. "
                                     "VERIFY: curing 1 d air + 'cured in water for 28 days' while fc table says 28 days; test age 28 entered; "
                                     "tension test age not stated, taken as the same."})
    rows.append(r)

# ---------------------------------------------------------------- 6) thermal stability SHCC, unheated reference (22 C)
P = {"Article Name": "Thermal stability of PVA fiber strain hardening cement-based composites",
     "Author": "Margareth da Silva Magalhaes, Romildo Dias Toledo Filho, Eduardo de Moraes Rego Fairbairn", "Year": 2015,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2015.07.039"}
B = 505 + 605
r = dict(P)
r.update({"OPC / Cement": r4(505 / B), "FA (Fly ash)": r4(605 / B), "W / B": r4(404 / B), "SS / B (Silica sand)": r4(404 / B), "Sand max size (µm)": 212,
          "SP / B": r4(15 / B), "Binder content (kg/m³)": B, "PVA fiber (vol%)": 2.0, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1576,
          "PVA elastic modulus (GPa)": 39.93, "Total fiber (vol%)": 2.0,
          "Curing method": "demoulded 24 h (damp cloths), curing chamber 100 % RH 21 C 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 21,
          "Curing RH (%)": 100, "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cylinder",
          "Compressive specimen size (mm)": "50x100", "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
          "Compressive strength (MPa)": 37.00, "Tensile strength (MPa)": 2.97, "First-cracking strength (MPa)": 2.12, "Tensile strain capacity (%)": 2.98,
          "Source table/page": "Table 1 (mix), Table 3 (tension, 22 C), Table 5 (fc, 22 C), sect. 2",
          "Conversions / notes": "Unheated reference (22 C) only; preheated specimens (90-250 C) skipped. kg/m3 / B (cement CPII F-32 + FA = 1110). "
                                 "PVA 26 kg/m3 / 1310 = 1.98 vol%, entered 2.0. PVA length not given. Melamine SP (solid). "
                                 "Tensile strain = strain at localization."})
rows.append(r)

# ---------------------------------------------------------------- 7) SHCC at 1/3/7/28 d, control tension (08.041)
P = {"Article Name": "Residual compressive properties of strain-hardening cementitious composite with different curing ages exposed to high temperature",
     "Author": "Yu Ke-quan, Lu Zhou-dao, Yu Jiangtao", "Year": 2015,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2015.08.041"}
B = 678 + 291
for age, eps, ft in ((1, 4.2, 2.1), (3, 4.3, 3.0), (7, 4.4, 3.3), (28, 4.0, 4.2)):
    r = dict(P)
    r.update({"OPC / Cement": r4(678 / B), "FA (Fly ash)": r4(291 / B), "W / B": r4(380 / B), "SS / B (Silica sand)": r4(484 / B), "Sand max size (µm)": 180,
              "HRWR / B": r4(14 / B), "HPMC / B (hydroxypropyl methyl cellulose)": r4(1.91 / B), "Binder content (kg/m³)": B,
              "PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1620, "PVA elastic modulus (GPa)": 42.8,
              "Total fiber (vol%)": 2.0,
              "Curing method": "1 d in mould, then water tank until test age" if age > 1 else "1 d in mould (no water curing)",
              "Curing time (days)": age, "Demolding age (days)": 1, "Test age (days)": age, "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
              "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix and unheated tension results), sect. 2.2",
              "Conversions / notes": f"Age {age} d, unheated control. kg/m3 / B (cement + FA = 969). PVA 26 kg/m3 / 1300 = 2 vol% (density assumed 1300, not stated). "
                                     "Results after heating skipped. Compressive strength of controls only in figures (not entered). "
                                     "VERIFY: curing temperature not stated; PVA vol% derived."})
    rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e20.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows ->", os.path.join(out_dir, "w6_e20.csv"))

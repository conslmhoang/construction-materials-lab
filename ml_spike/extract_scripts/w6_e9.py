"""Wave 6, agent e9: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e9.csv (99-column TEMPLATE header).
Papers: cemconres.2013.11.002, cemconres.2017.04.004, cemconres.2019.105856, compositesb.2013.08.089,
        compositesb.2015.11.039, compstruct.2015.11.046, compstruct.2017.03.095, compstruct.2017.11.034
"""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
add = os.path.join(here, "..", "additions")
out_dir = os.path.join(here, "..", "additions_v2")
cols = list(pd.read_csv(os.path.join(add, "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
rows = []
DIRECT = "direct (uniaxial)"


def r4(x):
    return round(x, 4)


# ---------------- 1) UHPFRC mix design, UHPC1 and UHPC2 with 2.5 vol% steel fibre (cemconres.2013.11.002)
P = {"Article Name": "Mix design and properties assessment of Ultra-High Performance Fibre Reinforced Concrete (UHPFRC)",
     "Author": "R. Yu, P. Spiesz, H.J.H. Brouwers", "Year": 2014,
     "DOI / URL": "https://doi.org/10.1016/j.cemconres.2013.11.002"}
for mid, c, lp in (("UHPC1", 874.9, 0.0), ("UHPC2", 612.4, 262.5)):
    B = c + 43.7 + lp
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), "SF (Silica fume)": r4(43.7 / B), "Limestone powder": r4(lp / B) if lp else None,
              "W / B": r4(202.1 / B), "Sand (type not stated) / B": r4((218.7 + 1054.7) / B), "SP / B": r4(45.9 / B),
              "Binder content (kg/m³)": round(B, 1), "Steel fiber (vol%)": 2.5, "Total fiber (vol%)": 2.5,
              "Curing method": "demolded ~24 h after casting, then water curing ~21 C", "Curing time (days)": 28,
              "Curing temperature (°C)": 21, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive specimen": "prism halves (EN 196-1)", "Compressive specimen size (mm)": "40x40",
              "Compressive strength (MPa)": 156 if mid == "UHPC1" else 141.5,
              "Source table/page": "Table 2 (mix, kg/m3), sect. 2.2.5 (curing), sect. 3.3 text (fc at 2.5 vol% steel fibre)",
              "Conversions / notes": f"{mid}. B = cement + silica fume + limestone filler (918.6 kg/m3); limestone filler counted in B. "
                                     "Sand = microsand 218.7 + sand 0-2 mm 1054.7. Steel fibre 2.5 vol% of concrete (on top of Table 2 kg/m3); length/diameter not found. "
                                     "Water 202.1 kg/m3 as Table 2 (paper's W/B 0.19 differs, probably net of SP water). "
                                     "UHPC3 (quartz powder) skipped. fc at other fibre contents only in figures. No tensile test."})
    rows.append(r)

# ---------------- 2) HS-SHCC with HDPE / PBO fibers (cemconres.2017.04.004)
P = {"Article Name": "Tensile behavior of high-strength strain-hardening cement-based composites (HS-SHCC) made with high-performance polyethylene, aramid and PBO fibers",
     "Author": "Iurie Curosu, Marco Liebscher, Viktor Mechtcherine, Cornelia Bellmann, Stefan Michel", "Year": 2017,
     "DOI / URL": "https://doi.org/10.1016/j.cemconres.2017.04.004"}
B = 1460 + 292
fib = {"M-HDPE": ("PE", 133.5, 3.8, 7.6, 3.9, {"PE length (mm)": 6, "PE diameter (µm)": 20, "PE tensile strength (MPa)": 2500, "PE elastic modulus (GPa)": 80}, ""),
       "M-PBO-AS": ("PBO", 140.3, 5.5, 9.8, 1.4, {}, "PBO as-spun fiber 6 mm, 13 um, 5800 MPa, E 180 GPa. "),
       "M-PBO-HM": ("PBO", 142.9, 4.2, 8.4, 1.6, {}, "PBO high-modulus fiber 6 mm, 13 um, 5800 MPa, E 270 GPa. ")}
for mid, (ft_, fc, fcr, ft, eps, extra, note) in fib.items():
    r = dict(P)
    r.update({"OPC / Cement": r4(1460 / B), "SF (Silica fume)": r4(292 / B), "W / B": r4(315 / B), "SS / B (Silica sand)": r4(145 / B),
              "SP / B": r4(35 / B), "Binder content (kg/m³)": B, "Total fiber (vol%)": 2.0,
              "Curing method": "demolded after 24 h, sealed in plastic bags, climatic chamber 20 C RH 65 %, unsealed at 13 d, tested at 14 d",
              "Curing time (days)": 14, "Curing temperature (°C)": 20, "Curing RH (%)": 65, "Demolding age (days)": 1, "Test age (days)": 14,
              "Tensile specimen": "dumbbell, 24x40 mm narrowed section", "Tensile gauge length (mm)": 100, "Tensile test type": DIRECT,
              "Compressive strength (MPa)": fc, "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 2 (mix), Table 3 (results), sect. 4.2 (curing, age)",
              "Conversions / notes": f"{mid}. kg/m3 / B (cement + SF = 1752). Quartz sand 0.06-0.2 mm treated as silica sand. Fibers 2 vol% as stated. "
                                     + note + "Aramid mix skipped. Ultimate strain = strain at max stress. Compressive specimen type not read."})
    if ft_ == "PE":
        r.update({"PE fiber (vol%)": 2.0})
        r.update(extra)
    else:
        r.update({"PBO fiber (vol%)": 2.0})
    rows.append(r)

# ---------------- 3) SHCC M45 stochastic model, experimental values (cemconres.2019.105856)
P = {"Article Name": "Stochastic model of tensile behavior of strain-hardening cementitious composites (SHCCs)",
     "Author": "Junxia Li, Jian Weng, En-Hua Yang", "Year": 2019,
     "DOI / URL": "https://doi.org/10.1016/j.cemconres.2019.105856"}
B = 1.0 + 1.2
r = dict(P)
r.update({"OPC / Cement": r4(1 / B), "FA (Fly ash)": r4(1.2 / B), "W / B": r4(.53 / B), "Sand (type not stated) / B": r4(.8 / B), "HRWR / B": r4(.03 / B),
          "PVA fiber (vol%)": 2, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 900, "PVA elastic modulus (GPa)": 24,
          "Total fiber (vol%)": 2,
          "Curing method": "air, 28 C RH 65 % for 28 days", "Curing time (days)": 28, "Curing temperature (°C)": 28, "Curing RH (%)": 65, "Test age (days)": 28,
          "Tensile specimen": "coupon", "Tensile gauge length (mm)": 150, "Tensile test type": DIRECT,
          "First-cracking strength (MPa)": 3.6, "Tensile strength (MPa)": 4.0, "Tensile strain capacity (%)": 3.1,
          "Source table/page": "Table 1 (mix, ratios), Table 3 (Experiment row), sect. 3.1 (curing)",
          "Conversions / notes": "SHCC M45, experimental row only (simulation values ignored). Mass ratios to cement; B = 2.2. "
                                 "VERIFY: test age 28 d taken from 'cured in air for 28 days'. PVA strength 900 MPa / E 24 GPa from Table 2 (model inputs). No compressive strength."})
rows.append(r)

# ---------------- 4) PVA-ECC flaw size / fiber distribution (compositesb.2013.08.089)
P = {"Article Name": "The role of flaw size and fiber distribution on tensile ductility of PVA-ECC",
     "Author": "Kamile Tosun-Felekoglu, Burak Felekoglu, Ravi Ranade, Bang Y. Lee, Victor C. Li", "Year": 2014,
     "DOI / URL": "https://doi.org/10.1016/j.compositesb.2013.08.089"}
B = 570 + 684
for mid, hr, fcr, ft, eps in (("ECC-I", 10.2, 4.38, 6.30, 1.40), ("ECC-II", 6.6, 5.04, 6.80, 1.66)):
    r = dict(P)
    r.update({"OPC / Cement": r4(570 / B), "FA (Fly ash)": r4(684 / B), "W / B": r4(331 / B), "SS / B (Silica sand)": r4(455 / B),
              "HRWR / B": r4(hr / B), "Binder content (kg/m³)": B, "PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 39,
              "PVA tensile strength (MPa)": 1620, "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": 2.0,
              "Curing method": "demolded 24 h, sealed plastic bags 23 C for 7 d, then room temperature to 28 d", "Curing time (days)": 28,
              "Curing temperature (°C)": 23, "Demolding age (days)": 1, "Test age (days)": 28,
              "Tensile specimen": "dog-bone (JSCE)", "Tensile test type": DIRECT,
              "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 2 (mix), Table 3 (average of 4 specimens), sect. 3.2 (curing)",
              "Conversions / notes": f"{mid}. kg/m3 / B (1254). PVA 26 kg/m3 / 1300 = 2.0 vol%. ECC-I and ECC-II differ in HRWRA dose (flowability). "
                                     "Table 3 labels the average rows 'ECC-Ia' (typo); values are the per-mix averages. Cube fc tested but values not reported. Ductility = tensile strain capacity."})
    rows.append(r)

# ---------------- 5) fly ash geopolymer EGC (compositesb.2015.11.039)
P = {"Article Name": "Matrix design of strain hardening fiber reinforced engineered geopolymer composite",
     "Author": "Behzad Nematollahi, Jay Sanjayan, Faiz Uddin Ahmed Shaikh", "Year": 2016,
     "DOI / URL": "https://doi.org/10.1016/j.compositesb.2015.11.039"}
# id: (activator/FA, extra water/FA, sand/FA, fc composite, fcr, ft, eps)
t5 = [("EGC20", .35, .014, 0, 63.7, .66, 4.7, 4.3), ("EGC23", .45, 0, 0, 52.6, .45, 4.3, 3.0),
      ("EGC23-FS-30", .45, 0, .30, 56.8, 1.3, 5.0, 3.6), ("EGC23-FS-60", .45, 0, .60, 60.7, 1.6, 5.2, 1.3),
      ("EGC23-CS-30", .45, 0, .30, 51.2, .67, 3.9, 1.3), ("EGC23-CS-60", .45, 0, .60, 49.2, 1.1, 4.0, 1.0)]
for mid, a, xw, s, fc, fcr, ft, eps in t5:
    ss_sol = a * 2.5 / 3.5       # Na2SiO3 solution / FA
    na_sol = a / 3.5             # 8 M NaOH solution / FA
    naoh_solid = .262 * na_sol   # 262 g NaOH per kg of 8 M solution (Hardjito & Rangan)
    w_naoh = na_sol - naoh_solid
    r = dict(P)
    r.update({"FA (Fly ash)": 1.0, "WG / B (Water glass)": r4(ss_sol), "NaOH / B": r4(naoh_solid), "Activator modulus Ms (SiO2/Na2O)": 2.0, "NaOH molarity (M)": 8,
              "W / B": r4(w_naoh + xw), "Extra water / B": xw or None, "SS / B (Silica sand)": s or None,
              "PVA fiber (vol%)": 2.0, "PVA length (mm)": 8, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 41,
              "Total fiber (vol%)": 2.0,
              "Curing method": "sealed molds, oven 60 C for 24 h, then ambient lab until test at 3 days after casting", "Curing time (days)": 3,
              "Curing temperature (°C)": 60, "Test age (days)": 3, "Heat curing duration (h)": 24,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
              "Tensile specimen": "coupon 400x75x10 mm", "Tensile test type": DIRECT,
              "Compressive strength (MPa)": fc, "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 3 (mix), Table 5 (composite results), sect. 4.2 (curing, age 3 d)",
              "Conversions / notes": f"{mid}. B = class F fly ash. Activator/FA {a} (mass) = 8 M NaOH solution + D-grade Na2SiO3 solution (Ms 2.0, Na2O 14.7 %, SiO2 29.4 %), "
                                     "Na2SiO3/NaOH solution mass ratio 2.5. WG/B = silicate solution as dosed. "
                                     "VERIFY: NaOH solid derived using 262 g NaOH per kg of 8 M solution (Hardjito & Rangan); W/B = NaOH-solution water + extra water, excludes water-glass water "
                                     f"(total water {r4(w_naoh + xw + .559 * ss_sol)} per FA; paper W/GP solids {0.20 if mid == 'EGC20' else 0.23}). "
                                     "First-crack strength estimated by the paper (Kim method). Fine silica sand (FS, <212 um) / coarse silica sand (CS)."})
    rows.append(r)

# ---------------- 6) PE fiber cement / alkali-activated slag composites (compstruct.2015.11.046)
P = {"Article Name": "Composite properties of high-strength polyethylene fiber-reinforced cement and cementless composites",
     "Author": "Jeong-Il Choi, Keum-Il Song, Jin-Kyu Song, Bang Yeon Lee", "Year": 2016,
     "DOI / URL": "https://doi.org/10.1016/j.compstruct.2015.11.046"}
act = 0.895
t6 = [("C34", "C", .34, .0007, .0002, 75.9, 3.97, 9.80, 4.88), ("C38", "C", .38, None, .0002, 60.8, 3.43, 9.53, 3.91),
      ("S34", "S", .34, .004, .0001, 43.0, 2.64, 7.89, 5.32), ("S38", "S", .38, .002, .0003, 31.3, 1.80, 5.96, 5.92)]
for mid, kind, w, sp, vma, fc, fcr, ft, eps in t6:
    k = 1.0 if kind == "C" else 1 / act
    r = dict(P)
    r.update({"W / B": r4(w * k), "SP / B": r4(sp * k) if sp else None, "VMA / B": r4(vma * k),
              "PE fiber (vol%)": 1.75, "PE length (mm)": 12, "PE diameter (µm)": 16, "PE tensile strength (MPa)": 3030, "PE elastic modulus (GPa)": 112,
              "Total fiber (vol%)": 1.75,
              "Curing method": "air 23 C for 2 days, demolded, then water 23 C until 28 days", "Curing time (days)": 28, "Curing temperature (°C)": 23,
              "Demolding age (days)": 2, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
              "Tensile specimen": "dog-bone (JSCE)", "Tensile test type": DIRECT, "Compressive strength (MPa)": fc,
              "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix), Table 5 (fc), Table 6 (tensile), sect. 2.2 (curing)"})
    if kind == "C":
        r.update({"OPC / Cement": 1.0, "Conversions / notes": f"{mid}. Mass ratios to cement. Anti-foaming agent 0.001 (defoamer). Paste composite (no sand)."
                  + (" VERIFY: SP cell empty in Table 1 for C38 (left blank)." if mid == "C38" else "")})
    else:
        r.update({"GGBS": 1.0, "Ca(OH)2 / B": r4(.075 / act), "Na2SO4 / B": r4(.03 / act),
                  "Conversions / notes": f"{mid}. B = GGBS. VERIFY: Table 1 'AAS = 1' assumed to include the powder activators (Ca(OH)2 8.38 % and Na2SO4 3.35 % of GGBS; same system as the "
                                         "defoamer study, binder 0.895 GGBS + 0.075 + 0.03), so water, SP, VMA ratios divided by 0.895. Anti-foaming agent 0.001 (defoamer). Paste composite (no sand)."})
    rows.append(r)

# ---------------- 7) defoamer in alkali-activated slag PE composite (compstruct.2017.03.095)
P = {"Article Name": "Effects of a defoamer on the compressive strength and tensile behavior of alkali-activated slag-based cementless composite reinforced by polyethylene fiber",
     "Author": "Yun Lee, Jeong-Il Choi, Hyeong-Ki Kim, Bang Yeon Lee", "Year": 2017,
     "DOI / URL": "https://doi.org/10.1016/j.compstruct.2017.03.095"}
t7 = [("D0", .004, 0, 34.5, 3.40, 6.93, 5.83), ("D1", .005, .001, 41.3, 3.49, 8.74, 6.48), ("D2", .005, .002, 41.4, 3.50, 8.82, 7.18)]
for mid, hr, df_, fc, fcr, ft, eps in t7:
    r = dict(P)
    r.update({"GGBS": 1.0, "Ca(OH)2 / B": r4(.075 / .895), "Na2SO4 / B": r4(.03 / .895), "W / B": r4(.30 / .895), "HRWR / B": r4(hr / .895),
              "PE fiber (vol%)": 1.75, "PE length (mm)": 18, "PE diameter (µm)": 12, "PE tensile strength (MPa)": 2700, "PE elastic modulus (GPa)": 88,
              "Total fiber (vol%)": 1.75,
              "Curing method": "23 C in mold 2 days, demolded, water 23 C until 28 days", "Curing time (days)": 28, "Curing temperature (°C)": 23,
              "Demolding age (days)": 2, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
              "Tensile specimen": "dog-bone", "Tensile test type": DIRECT, "Compressive strength (MPa)": fc,
              "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix), Table 4 (fc), Table 5 (tensile), sect. 2.2 (curing)",
              "Conversions / notes": f"{mid}. Table 1 binding material = GGBS 0.895 + Ca(OH)2 0.075 + Na2SO4 0.03 (= 1); re-expressed with B = GGBS (all ratios / 0.895). "
                                     f"Defoamer {df_} (mass ratio of binding material; none in D0), HRWRA {hr}. Paste composite (no sand)."})
    rows.append(r)

# ---------------- 8) UHDCC 40 to 120 MPa (compstruct.2017.11.034)
P = {"Article Name": "Basic mechanical properties of ultra-high ductility cementitious composites: From 40 MPa to 120 MPa",
     "Author": "Yao Ding, Jiang-tao Yu, Ke-Quan Yu, Shi-lang Xu", "Year": 2018,
     "DOI / URL": "https://doi.org/10.1016/j.compstruct.2017.11.034"}
t8 = [(700, 100, 150, 750, 500, 230, 25, 115, 9.19, 16.46, 8.00, .14), (687, 96, 144, 736, 485, 267, 20, 94, 8.81, 13.21, 10.13, .16),
      (647, 91, 136, 693, 458, 284, 12, 77, 7.50, 11.35, 9.02, .18), (605, 85, 127, 648, 446, 320, 8, 64, 7.22, 9.53, 11.14, .22),
      (528, 74, 111, 566, 446, 388, 3, 43, 4.94, 6.17, 10.64, .32)]
for c, lp, sf, gg, sa, w, hr, fc, fcr, ft, eps, wb in t8:
    B = c + lp + sf + gg
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), "Limestone powder": r4(lp / B), "SF (Silica fume)": r4(sf / B), "GGBS": r4(gg / B), "W / B": r4(w / B),
              "SS / B (Silica sand)": r4(sa / B), "HRWR / B": r4(hr / B), "Binder content (kg/m³)": B,
              "PE fiber (vol%)": 2.06, "PE length (mm)": 18, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 2400, "PE elastic modulus (GPa)": 100,
              "Total fiber (vol%)": 2.06,
              "Curing method": "demolded after 24 h, water tank 28 days", "Curing time (days)": 28, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100x200",
              "Tensile specimen": "dog-bone (JSCE)", "Tensile test type": DIRECT, "Compressive strength (MPa)": fc,
              "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 2 (mix, kg/m3), Table 4 (results by w/b), sect. 2.2 (curing)",
              "Conversions / notes": f"Paper w/b {wb}. kg/m3 / B, B = cement + limestone powder + SF + GGBFS = {B}. PE 20 kg/m3 / 970 = 2.06 vol%. "
                                     f"VERIFY: Table 2 water/(C+SF+GGBFS) = {r4(w / (c + sf + gg))} vs Table 4 w/b {wb} (Table 2 water used; W/B here includes LP in B); "
                                     "Table 2 columns matched to Table 4 rows in order of increasing w/b. Strain = tensile strain capacity at peak stress."})
    rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e9.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows ->", os.path.join(out_dir, "w6_e9.csv"))

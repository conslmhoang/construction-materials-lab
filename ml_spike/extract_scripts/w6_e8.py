"""Wave 6, agent e8: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e8.csv (99-column TEMPLATE header).
Papers: cemconcomp.2011.11.019, 2016.04.002, 2018.02.001, 2018.07.016, 2019.04.007, 2019.103370,
        2020.103704, 2020.103766, 2021.104050, cemconres.2007.04.006, 2007.12.006
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


# ---------------------------------------------------- 1) mixing sequence ECC, Table 3/4 (S1, S2, S2A)
P = {"Article Name": "Improved fiber distribution and mechanical properties of engineered cementitious composites by adjusting the mixing sequence",
     "Author": "Jian Zhou, Shunzhi Qian, Guang Ye, Oguzhan Copuroglu, Klaas van Breugel, Victor C. Li", "Year": 2011,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2011.11.019"}
# id: (PC, LP, BFS, SF, sand, water, SP, PVA kg, eps, ft, note)
t1 = [("S1", 235, 782, 547, 78, 0, 410, 15.6, 26, 3.7, 3.8, "standard mixing sequence"),
      ("S2", 145, 482, 337, 48, 1012, 253, 9.6, 16.1, 0.5, 2.9, "standard mixing sequence, high-volume sand"),
      ("S2A", 145, 482, 337, 48, 1012, 253, 9.6, 16.1, 2.2, 3.5, "adjusted (two-step water) mixing sequence, high-volume sand")]
for mid, c, lp, bfs, sf, sa, w, sp, pva, eps, ft, nt in t1:
    B = c + lp + bfs + sf
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), "Limestone powder": r4(lp / B), "GGBS": r4(bfs / B), "SF (Silica fume)": r4(sf / B),
              "W / B": r4(w / B), "River sand / B": r4(sa / B) if sa else None, "SP / B": r4(sp / B), "Binder content (kg/m³)": B,
              "PVA fiber (vol%)": r4(pva / 1300 * 100), "PVA length (mm)": 8, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600,
              "Total fiber (vol%)": r4(pva / 1300 * 100),
              "Curing method": "covered 1 d at 20 C, demoulded, sealed curing at 20 C for 27 d", "Curing time (days)": 28,
              "Curing temperature (°C)": 20, "Demolding age (days)": 1, "Test age (days)": 28,
              "Tensile specimen": "coupon 240x60x10 mm", "Tensile gauge length (mm)": 70, "Tensile test type": DIRECT,
              "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 3 (mix), Table 4 (tensile), sect. 2.3/2.4 (curing, age)",
              "Conversions / notes": f"{mid}: {nt}. kg/m3 / B, B = cement + limestone + BFS + SF = {B} (paper w/p 0.25 on this powder). "
                                     f"PVA {pva} kg/m3 / 1300 = {r4(pva / 1300 * 100)} vol% (paper text says 2 vol% for all; Table 3 value used). "
                                     "M1/M2 mixes skipped (results only in figures). No compressive strength reported."})
    rows.append(r)

# ---------------------------------------------------- 2) PE fiber alkali-activated slag composite (Choi et al.)
P = {"Article Name": "Ultra-high-ductile behavior of a polyethylene fiber-reinforced alkali-activated slag-based composite",
     "Author": "Jeong-Il Choi, Bang Yeon Lee, Ravi Ranade, Victor C. Li, Yun Lee", "Year": 2016,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2016.04.002"}
f = 1 + 0.0838 + 0.0335
# id: (water, hrwra, vma, fc, fcr, ft, eps)
t2 = [("M26", .26, .024, 0, 54.8, 4.87, 13.06, 7.50), ("M30", .30, .009, 0, 49.0, 4.61, 11.46, 6.33),
      ("M34", .34, .004, .0001, 42.3, 3.92, 7.64, 5.35), ("M38", .38, .002, .0003, 36.3, 3.37, 5.06, 4.58)]
for mid, w, hr, vma, fc, fcr, ft, eps in t2:
    r = dict(P)
    r.update({"GGBS": 1.0, "Ca(OH)2 / B": 0.0838, "Na2SO4 / B": 0.0335, "W / B": r4(w * f), "HRWR / B": r4(hr * f),
              "VMA / B": r4(vma * f) if vma else None, "PE fiber (vol%)": 1.75, "PE length (mm)": 18, "PE diameter (µm)": 12,
              "PE tensile strength (MPa)": 2700, "PE elastic modulus (GPa)": 88, "Total fiber (vol%)": 1.75,
              "Curing method": "air 23 C for 2 d, demolded, then water 23 C for 28 d", "Curing time (days)": 28,
              "Curing temperature (°C)": 23, "Demolding age (days)": 2, "Test age (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Tensile specimen": "dog-bone (see Fig. 1)",
              "Tensile test type": DIRECT, "Compressive strength (MPa)": fc, "First-cracking strength (MPa)": fcr,
              "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix), Table 5 (fc), Table 7 (tensile), sect. 2.1/2.2",
              "Conversions / notes": f"{mid}. Cementless: GGBS activated by Ca(OH)2 8.38 % and Na2SO4 3.35 % of GGBS mass; B = GGBS. "
                                     f"VERIFY: Table 1 ratios are 'of binder weight'; here the paper's binder is taken to include the activators, so W, HRWRA, VMA were multiplied "
                                     f"by {f:.4f} to express per GGBS (if binder = GGBS only, the ratios would be 10 percent lower). Antifoamer 0.001 present (not a column). "
                                     "VERIFY: cubes 'tested at 28 days' (curing 2 d air + 28 d water), 28 assumed as test age. No sand."})
    rows.append(r)

# ---------------------------------------------------- 3) Engineered Geopolymer Composite, optimum matrix (Ohno & Li)
P = {"Article Name": "An integrated design method of Engineered Geopolymer Composite",
     "Author": "Motohiro Ohno, Victor C. Li", "Year": 2018,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2018.02.001"}
t3 = [(1.0, 38.5, 3.0, 2.5, 3.5), (1.5, 43.1, 4.7, 2.9, 5.3), (2.0, 43.3, 4.4, 3.5, 5.4)]
for vf, fc, eps, fcr, ft in t3:
    r = dict(P)
    r.update({"FA (Fly ash)": 1.0, "WG / B (Water glass)": 0.225, "NaOH / B": 0.052, "W / B": 0.123, "SS / B (Silica sand)": 0.4,
              "PVA fiber (vol%)": vf, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": vf,
              "Curing method": "mould 24 h at 23 C, oven 60 C for 24 h, then air at room temperature until 28 d", "Curing time (days)": 28,
              "Curing temperature (°C)": 60, "Heat curing duration (h)": 24, "Test age (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "51", "Tensile specimen": "dog-bone",
              "Tensile test type": DIRECT, "Compressive strength (MPa)": fc, "First-cracking strength (MPa)": fcr,
              "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 6 (optimum matrix, mass ratio), Table 11 (results), sect. 3.1/4.4 (curing, age)",
              "Conversions / notes": f"EGC Vf {vf} %. Optimum matrix: fly ash A 0.6 + B 0.4 (both class F) = 1.0; Ottawa F-75 sand 0.4; Na2SiO3 solution (8.9 % Na2O, 28.7 % SiO2, 62.5 % H2O) 0.225 "
                                     "entered as WG / B; NaOH pellets 0.052; W/B = pre-mix water 0.023 + mix water 0.10 (water inside the water glass, 0.14, not added). "
                                     "L18 matrices without fiber skipped. Table 13 (kg/m3) agrees with ratios."})
    rows.append(r)

# ---------------------------------------------------- 4) UHP-ECC, quasi-static rate (Yu et al.)
P = {"Article Name": "Rate-dependent tensile properties of ultra-high performance engineered cementitious composites (UHP-ECC)",
     "Author": "Ke-Quan Yu, Jian-Guo Dai, Zhou-Dao Lu, Chi-Sun Poon", "Year": 2018,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2018.07.016"}
B = 700 + 100 + 200 + 750
# id: (dia, len, first cracking, peak, strain)
t4 = [("UHP-ECC-900", 20, 18, 10.04, 17.40, 7.56), ("UHP-ECC-750", 24, 18, 10.19, 16.46, 8.00), ("UHP-ECC-500", 24, 12, 9.45, 11.03, 5.93)]
for mid, d, l, fcr, ft, eps in t4:
    r = dict(P)
    r.update({"OPC / Cement": r4(700 / B), "Limestone powder": r4(100 / B), "SF (Silica fume)": r4(200 / B), "GGBS": r4(750 / B),
              "W / B": r4(230 / B), "SS / B (Silica sand)": r4(500 / B), "HRWR / B": r4(25 / B), "Binder content (kg/m³)": B,
              "PE fiber (vol%)": 2.06, "PE length (mm)": l, "PE diameter (µm)": d, "PE tensile strength (MPa)": 2800,
              "PE elastic modulus (GPa)": 120, "Total fiber (vol%)": 2.06, "Test age (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Tensile specimen": "dumbbell",
              "Tensile test type": DIRECT, "Compressive strength (MPa)": 149, "First-cracking strength (MPa)": fcr,
              "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 2 (mix), Table 3 (fiber), Table 6 (tensile, strain rate 0.0001 s-1), sect. 3.2/4.1 (28 d, fc)",
              "Conversions / notes": f"{mid} (Lf/df = {int(l * 1000 / d)}), quasi-static strain rate 0.0001 s-1 only (higher rates skipped). "
                                     "B = cement + limestone + SF + GGBS = 1750 (paper W/(C+SF+GGBS) = 0.135 stated, 230/1650 = 0.139). "
                                     "PE 20 kg/m3 / 970 = 2.06 vol%. VERIFY: fc 149 MPa is given for 'the UHP-ECC' at 0.0001 s-1 (not per fiber type), attached to all three rows; "
                                     "curing conditions not stated in text; peak stress/strain used as tensile strength / strain capacity."})
    rows.append(r)

# ---------------------------------------------------- 5) natural sand ECC (Wu et al.)
P = {"Article Name": "Effect of morphological parameters of natural sand on mechanical properties of engineered cementitious composites",
     "Author": "Hao-Liang Wu, Jing Yu, Duo Zhang, Jun-Xing Zheng, Victor C. Li", "Year": 2019,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2019.04.007"}
B = 3.2
sandcol = {"Ottawa-ECC": "SS / B (Silica sand)", "Gabbro-ECC": "M-sand / B", "MI-ECC": "Dune sand / B", "2NS-ECC": "Sand (type not stated) / B"}
sandnote = {"Ottawa-ECC": "Ottawa silica sand", "Gabbro-ECC": "crushed gabbro sand (entered as manufactured sand)",
            "MI-ECC": "Michigan dune sand", "2NS-ECC": "2NS natural sand"}
sp = {"Ottawa-ECC": .024, "Gabbro-ECC": .027, "MI-ECC": .022, "2NS-ECC": .025}
# id: (fc28, fc7, fcr, UTS, TSC)
t5 = {"Ottawa-ECC": (None, None, 1.72, 3.81, 1.45), "Gabbro-ECC": (44.6, 39.8, 1.92, 4.98, 1.88),
      "MI-ECC": (None, None, 1.78, 4.15, 0.83), "2NS-ECC": (None, 38.2, 1.85, 3.38, 1.17)}
for mid, (fc28, fc7, fcr, ft, eps) in t5.items():
    base = dict(P)
    base.update({"OPC / Cement": r4(1 / B), "FA (Fly ash)": r4(2.2 / B), "W / B": r4(0.8 / B), sandcol[mid]: r4(1.2 / B),
                 "SP / B": r4(sp[mid] / B), "PVA fiber (vol%)": 2, "PVA length (mm)": 8, "PVA diameter (µm)": 39,
                 "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": 2,
                 "Curing method": "air 20 C RH 65 %, demolded at 24 h, air curing until test", "Curing temperature (°C)": 20,
                 "Curing RH (%)": 65, "Demolding age (days)": 1, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
                 "Source table/page": "Table 1 (mix, ratio to OPC), Table 4 (tensile), sect. 2.2/3.3 text (fc)",
                 "Conversions / notes": f"{mid}: {sandnote[mid]}, 300-310 um. Ratios to OPC (OPC 1, FA 2.2), B = 3.2. "})
    r = dict(base)
    r.update({"Curing time (days)": 28, "Test age (days)": 28, "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
              "Compressive strength (MPa)": fc28, "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft,
              "Tensile strain capacity (%)": eps})
    r["Conversions / notes"] += ("fc of Ottawa/MI (Fig. 6) and 2NS 28 d (only '7 % lower than Gabbro') not entered." if fc28 is None else
                                 "fc 28 d Gabbro from text (44.6).")
    rows.append(r)
    if fc7:
        r = dict(base)
        r.update({"Curing time (days)": 7, "Test age (days)": 7, "Compressive strength (MPa)": fc7})
        r["Conversions / notes"] += "7 d compressive row (text)."
        rows.append(r)

# ---------------------------------------------------- 6) HSHLW-ECC, FAC-free reference mix only (Zhou et al.)
P = {"Article Name": "Development of high strain-hardening lightweight engineered cementitious composites: Design and performance",
     "Author": "Yingwu Zhou, Bin Xi, Lili Sui, Shuyue Zheng, Feng Xing, L. Li", "Year": 2019,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2019.103370"}
B = 700 + 750 + 230
r = dict(P)
r.update({"OPC / Cement": r4(700 / B), "GGBS": r4(750 / B), "SF (Silica fume)": r4(230 / B), "W / B": r4(230 / B),
          "Sand (type not stated) / B": r4(500 / B), "HRWR / B": r4(45 / B), "Binder content (kg/m³)": B,
          "PE fiber (vol%)": 2.06, "PE length (mm)": 18, "PE diameter (µm)": 25, "PE tensile strength (MPa)": 2900,
          "PE elastic modulus (GPa)": 116, "Total fiber (vol%)": 2.06,
          "Curing method": "demolded 24 h, curing room 23 C 95 % RH for 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 23,
          "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube",
          "Compressive strength (MPa)": 100.9,
          "Source table/page": "Table 1 (mix), sect. 3.2 (curing), sect. 4.2 (fc)",
          "Conversions / notes": "HSHLW-ECC-0% (no fly ash cenosphere, FAC mixes skipped). kg/m3 / B, B = cement + GGBFS + SF = 1680. PE 20 kg/m3 / 970 = 2.06 vol%. "
                                 "VERIFY: Table 1 prints W/B 0.11 (not reproducible from the kg/m3 values; 230/1680 = 0.137 used). Tensile strain 'more than 8 %' only in text, "
                                 "stress-strain in Fig. 13, so not entered. Cube size not stated. Sand 500 kg/m3 (type not stated)."})
rows.append(r)

# ---------------------------------------------------- 7) hybrid PE/steel ultra-high strength SHCC (Liu et al.)
P = {"Article Name": "Optimization of fiber volume fraction to enhance reinforcing efficiency in hybrid fiber reinforced strain hardening cementitious composite",
     "Author": "Tianan Liu, Yingzi Yang, Zhitao Chen, Yazhao Li, Ruixiang Bai", "Year": 2020,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2020.103704"}
B = 1 + 1 + 0.22
# id: (steel vol, fc, fcr, ft, eps)
t7 = [("PE1.5", 0, 141.13, 6.5, 10.89, 4.42), ("PE1.5ST0.5", .5, 175.6, 8.49, 11.67, 5.11),
      ("PE1.5ST1", 1.0, 180.4, 10.05, 11.17, 3.13), ("PE1.5ST1.5", 1.5, 187.9, 11.34, 12.4, 2.04)]
for mid, st, fc, fcr, ft, eps in t7:
    r = dict(P)
    r.update({"OPC / Cement": r4(1 / B), "FA (Fly ash)": r4(1 / B), "SF (Silica fume)": r4(.22 / B), "W / B": 0.18,
              "Sand (type not stated) / B": 0.89, "SP / B": 0.033, "PE fiber (vol%)": 1.5, "PE length (mm)": 18, "PE diameter (µm)": 20,
              "PE tensile strength (MPa)": 3800, "PE elastic modulus (GPa)": 113,
              "Steel fiber (vol%)": st or None, "Steel length (mm)": 13 if st else None, "Steel diameter (µm)": 160 if st else None,
              "Steel tensile strength (MPa)": 2500 if st else None, "Steel elastic modulus (GPa)": 210 if st else None,
              "Total fiber (vol%)": 1.5 + st, "Curing method": "steam curing 90 C for 7 d", "Curing time (days)": 7,
              "Curing temperature (°C)": 90, "Test age (days)": 7, "Heat curing duration (h)": 168,
              "Tensile specimen": "dog-bone (JSCE)", "Tensile test type": DIRECT, "Compressive strength (MPa)": fc,
              "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix, fc), Table 4 (tensile), sect. 6.1 (curing)",
              "Conversions / notes": f"{mid}. Binder weight ratio cement : fly ash : SF = 1 : 1 : 0.22 (B = 2.22). "
                                     "VERIFY: fine aggregate 0.89 and SP 3.3 % taken as ratios to B (type of fine aggregate not stated); defoamer 0.007 % present. "
                                     "VERIFY: test age not stated, 7 d = duration of 90 C steam curing (tests assumed right after the curing)."})
    rows.append(r)

# ---------------------------------------------------- 8) ECC with limestone calcined clay cement (Zhang et al.)
P = {"Article Name": "Engineered Cementitious Composites (ECC) with limestone calcined clay cement (LC3)",
     "Author": "Duo Zhang, Beata Jaworska, He Zhu, Kensey Dahlquist, Victor C. Li", "Year": 2020,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2020.103766"}
B = 3.2
# id: (opc, fa, mk, lp, water, hrwra, eps, note)
t8 = [("ECC-Ref", 1, 2.2, 0, 0, .79, .013, 4.2, "strain capacity 'approximately 4.2 %' (VERIFY, rounded in text)"),
      ("ECC-L3", .55, 2.2, .3, .15, .95, .022, 6.5, "limestone Dv50 3 um"),
      ("ECC-L12", .55, 2.2, .3, .15, .95, .022, 5.2, "limestone Dv50 12 um")]
for mid, c, fa, mk, lp, w, hr, eps, nt in t8:
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "Metakaolin": r4(mk / B) if mk else None,
              "Limestone powder": r4(lp / B) if lp else None, "W / B": r4(w / B), "SS / B (Silica sand)": r4(1.16 / B),
              "HRWR / B": r4(hr / B), "PVA fiber (vol%)": 2, "PVA length (mm)": 8, "PVA diameter (µm)": 39,
              "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": 2, "Test age (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Tensile specimen": "dog-bone",
              "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 4 (mix, mass ratios), sect. 3.2 text (28 d strain capacity)",
              "Conversions / notes": f"{mid}: {nt}. Ratios to OPC of the Ref mix; B = OPC + FA + MK + limestone = 3.2 (w/s 0.25 Ref, 0.30 LC3). "
                                     "Curing conditions not stated. fc and tensile strength only in figures, not entered."})
    rows.append(r)

# ---------------------------------------------------- 9) eco-efficient self-compacting UHPC with 1 % steel fiber (Ferdosian & Camoes)
P = {"Article Name": "Mechanical performance and post-cracking behavior of self-compacting steel-fiber reinforced eco-efficient ultra-high performance concrete",
     "Author": "Iman Ferdosian, Aires Camoes", "Year": 2021,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2021.104050"}
B = 640 + 56.3 + 361.1
fc9 = {1: 45.5, 3: 84.2, 7: 106.6, 14: 129.1, 28: 152.1, 56: 168.3, 91: 172.9, 121: 171.6}
for age, fc in fc9.items():
    r = dict(P)
    r.update({"OPC / Cement": r4(640 / B), "FA (Fly ash)": r4(361.1 / B), "SF (Silica fume)": r4(56.3 / B), "W / B": r4(167.1 / B),
              "SS / B (Silica sand)": r4(1131.2 / B), "SP / B": r4(25.61 / B), "Binder content (kg/m³)": round(B, 1),
              "Steel fiber (vol%)": 1.0, "Total fiber (vol%)": 1.0,
              "Curing method": "covered 24 h, demolded, water bath 20 C until test", "Curing time (days)": max(age - 1, 0),
              "Curing temperature (°C)": 20, "Demolding age (days)": 1, "Test age (days)": age, "Compressive specimen": "cube",
              "Compressive specimen size (mm)": "50", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 5 (mix), Table 6 (fc), sect. 3.2 (curing)",
              "Conversions / notes": "EEUHPC. kg/m3 / B, B = cement + ultra-fine fly ash + SF = 1057.4. Total water 167.1 includes water of the SP (paper: w/c 26.4 %); SP liquid 30 % solids as dosed. "
                                     "Steel fiber 78.7 kg/m3 = 1 vol% (fiber geometry not stated). Sand SiO2 99.4 % (entered as silica sand). "
                                     "Direct tension (first crack 4.45, max 7.94 MPa, one crack, CMOD) has no test age or strain, not entered."})
    rows.append(r)

# ---------------------------------------------------- 10) ECC with GGBS (Kim et al.)
P = {"Article Name": "Tensile and fiber dispersion performance of ECC (engineered cementitious composites) produced with ground granulated blast furnace slag",
     "Author": "Jin-Keun Kim, Jeong-Su Kim, Gee Joo Ha, Yun Yong Kim", "Year": 2007,
     "DOI / URL": "https://doi.org/10.1016/j.cemconres.2007.04.006"}
for mid, c, sl, w, sa, vma, eps, ft in [("Slag-ECC W/B 0.48 (W/C 0.60)", 1.0, 0.25, .60, .8, .001, 3.6, 5.2),
                                        ("ECC W/C 0.60 (no slag)", 1.0, 0, .60, .8, .001, 2.4, 3.4)]:
    B = c + sl
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), "GGBS": r4(sl / B) if sl else None, "W / B": r4(w / B), "SS / B (Silica sand)": r4(sa / B),
              "VMA / B": r4(vma / B), "PVA fiber (vol%)": 2, "PVA length (mm)": 12, "Total fiber (vol%)": 2, "Test age (days)": 28,
              "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 150, "Tensile test type": DIRECT,
              "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix, ratio to cement), sect. 4.3/4.4 and conclusions (tensile, 28 d)",
              "Conversions / notes": f"{mid}. HPMC 0.001 of cement as VMA, no HRWR. Slag 25 % of cement mass. "
                                     "VERIFY: PVA 2 vol% (REC15, 12 mm) stated in the fiber-bridging analysis section, assumed for the tensile specimens; fiber diameter not stated. "
                                     "Curing of tensile specimens not stated. Ultimate tensile strain used as strain capacity. W/C 0.48 mixes had no numeric tensile results."})
    rows.append(r)

# ---------------------------------------------------- 11) UHPFRC, 28 d compressive strength (Charron et al.)
P = {"Article Name": "Transport properties of water and glycol in an ultra high performance fiber reinforced concrete (UHPFRC) under high tensile deformation",
     "Author": "Jean-Philippe Charron, Emmanuel Denarie, Eugen Bruhwiler", "Year": 2008,
     "DOI / URL": "https://doi.org/10.1016/j.cemconres.2007.12.006"}
B = 1051 + 273
r = dict(P)
r.update({"OPC / Cement": r4(1051 / B), "SF (Silica fume)": r4(273 / B), "W / B": r4(165 / B), "SS / B (Silica sand)": r4(733 / B),
          "SP / B": r4(35 / B), "Binder content (kg/m³)": B, "Steel fiber (vol%)": 5.96, "Steel length (mm)": 10, "Steel diameter (µm)": 200,
          "Total fiber (vol%)": 5.96, "Curing method": "sealed in mould 3 d, then wet curing until 28 d, no thermal treatment",
          "Curing time (days)": 28, "Demolding age (days)": 3, "Test age (days)": 28, "Compressive strength (MPa)": 168,
          "Source table/page": "Table 3 (mix), sect. 2.2 text (curing, fc)",
          "Conversions / notes": "kg/m3 / B, B = CEM I 52.5 + SF = 1324. Steel 468 kg/m3 / 7850 = 5.96 vol%. Fontainebleau sand (dmax 0.5 mm) entered as silica sand. "
                                 "VERIFY: SP dosage as dosed (solid content not stated), W/B 0.125 excludes SP water; fc 168 MPa is quoted from ref [12] as 'average at 28 d'. "
                                 "ft = 11 MPa also quoted, test type not stated, not entered. Fiber vol% at upper end (6 %)."})
rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e8.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows ->", os.path.join(out_dir, "w6_e8.csv"))

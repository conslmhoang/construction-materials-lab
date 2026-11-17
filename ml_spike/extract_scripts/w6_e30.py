"""Wave 6, agent e30: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e30.csv (99-column TEMPLATE header).
Papers: conbuildmat.2022.127665, 2022.129299, 2023.131895, 2024.139446, 2024.139840, 2025.141711,
        2026.145748, 2026.145983, 2026.146158, 2026.146183, 2026.146895
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


def paper(name, author, year, doi):
    return {"Article Name": name, "Author": author, "Year": year, "DOI / URL": "https://doi.org/" + doi}


# ---------- 1) Aslani et al. 2022: rubberised ECC (PVA, crumb rubber), 28-d peak stress of compressive curves
P = paper("Mechanical and shrinkage performance of 3D-printed rubberised engineered cementitious composites",
          "Farhad Aslani, Ryan Dale, Fatemeh Hamidi, Afsaneh Valizadeh", 2022, "10.1016/j.conbuildmat.2022.127665")
# name, FA ratio (to C=1), CR % vol of FA, 28-d peak stress (Table 6)
for nm, fa, cr, fc in [("CECC", 1.33, 0, 42), ("ECC-R5%", 1.26, 5, 32.5), ("ECC-R10%", 1.20, 10, 29),
                       ("ECC-R15%", 1.13, 15, 21), ("ECC-R20%", 1.06, 20, 26.5)]:
    B = 1 + fa + 0.11
    r = dict(P)
    r.update({"OPC / Cement": r4(1 / B), "FA (Fly ash)": r4(fa / B), "SF (Silica fume)": r4(0.11 / B), "W / B": r4(0.65 / B),
              "Sand (type not stated) / B": r4(0.89 / B), "PVA fiber (vol%)": 1.75, "PVA length (mm)": 12, "PVA diameter (µm)": 39,
              "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": 1.75,
              "Curing method": "24 h in mould at 23 C, demoulded, then 23 +/- 2 C and 50 +/- 5 % RH until test",
              "Curing time (days)": 28, "Curing temperature (°C)": 23, "Curing RH (%)": 50, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
              "Compressive strength (MPa)": fc,
              "Source table/page": "Table 5 (mix ratios by weight), Table 6 (peak stress 28 d), Table 2-4, sect. 2.3.1"})
    if cr:
        r["Crumb rubber / B"] = r4(1.33 * cr / 100 * 1.15 / 2.29 / B)
    note = (f"{nm}. Mix ratios by weight to cement = 1 (Table 5); binder B = cement + FA + densified silica fume = {r4(B)}; densified SF counted as silica fume. "
            "fc = peak stress of the 28-d compressive stress-strain curve (Table 6); 7-d / 28-d bar values only in Fig. 7. "
            "VERIFY: PVA given as 1.75 % vol. 'of binder' in Table 5, entered as total vol%. SP given in ml only (not entered). "
            "Cube size 50 mm stated as '50 mm3'. 'Standard moist curing' stated as 23 C / 50 % RH. Control CM (no PVA, fc 38) skipped (no fibre).")
    if cr:
        note += (f" Crumb rubber = {cr} % of FA volume replaced (FA 1.33 -> {fa}); mass = 1.33 x {cr/100} x (1.15 / 2.29) per cement, densities from Tables 2-3 (VERIFY derived).")
    r["Conversions / notes"] = note
    rows.append(r)

# ---------- 2) Qasim et al. 2022: PVA-ECC and hybrid SPH-ECC (PVA + steel), 28 d
P = paper("An experimental study on interfacial bond strength between hybrid engineered cementitious composite and concrete",
          "M. Qasim, C.K. Lee, Y.X. Zhang", 2022, "10.1016/j.conbuildmat.2022.129299")
B = 571 + 456
for nm, pva, st, fc, ts, eps in [("PVA-ECC", 2.2, 0, 62.40, 4.64, 0.74), ("SPH-ECC", 1.47, 0.73, 69.70, 5.72, 0.66)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(571 / B), "FA (Fly ash)": r4(456 / B), "W / B": r4(343 / B), "Sand (type not stated) / B": r4(685 / B),
              "HRWR / B": r4(7.4 / B), "Binder content (kg/m³)": B, "PVA fiber (vol%)": pva, "PVA length (mm)": 12, "PVA diameter (µm)": 39,
              "PVA tensile strength (MPa)": 1620, "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": r4(pva + st),
              "Curing method": "curing room, 100 % humidity (VERIFY: ECC curing assumed equal to composite specimens)", "Curing time (days)": 28,
              "Curing RH (%)": 100, "Test age (days)": 28, "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100 x 200",
              "Tensile specimen": "dog-bone", "Tensile test type": DIRECT, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ts,
              "Tensile strain capacity (%)": eps, "Source table/page": "Table 2 (mix), Table 3 (fibres), Table 5 (fc, tensile), sect. 5.1",
              "Conversions / notes": f"{nm}. kg/m3 / B (cement + FA = {B}). Sand 685 kg/m3 (type not stated). HRWRA entered as HRWR / B. "
                                     "Tensile strain = 'tensile strain for ECC' in Table 5 (ultimate tensile strain, dog-bone, 28 d). "
                                     "VERIFY: curing of the bare ECC cylinders / dog-bones not described; 28 d stated for tests."})
    if st:
        r.update({"Steel fiber (vol%)": st, "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2750,
                  "Steel elastic modulus (GPa)": 210})
    rows.append(r)

# ---------- 3) Yang et al. 2023: SMAF-ECC, reference ECC S-0 (PVA 2 vol%)
P = paper("Study on the self-recovery performance of SMAF-ECC under cyclic tensile loading", "Zhao Yang, Zheng Xiong, Yu Liu",
          2023, "10.1016/j.conbuildmat.2023.131895")
B = 5
r = dict(P)
r.update({"OPC / Cement": 0.2, "FA (Fly ash)": 0.8, "W / B": r4(1.1 / B), "SS / B (Silica sand)": r4(1 / B), "SP / B": r4(0.008 / B),
          "PVA fiber (vol%)": 2, "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 40,
          "Total fiber (vol%)": 2, "Curing method": "24 h thermostatic chamber, demoulded, standard curing room 28 d", "Curing time (days)": 28,
          "Demolding age (days)": 1, "Test age (days)": 28, "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
          "Tensile strength (MPa)": 3.03, "Tensile strain capacity (%)": 3.91,
          "Source table/page": "Table 2 (mix, ratio to cement), Table 1 (PVA), Table 5 (S-0), sect. 2.2.2",
          "Conversions / notes": "Reference ECC S-0 only (SMA fibre mixes skipped). Weight ratios C : FA : sand : water : WR = 1 : 4 : 1 : 1.1 : 0.008, B = 5. "
                                 "Ultimate tensile stress / strain of Table 5 = peak. VERIFY: 'standard curing room 28 d' after 24 h demoulding, so age may be 29 d; temperature / RH not stated. Silica sand."})
rows.append(r)

# ---------- 4) Teng et al. 2024: rubber ECC, XR-0 control and NR-40 (normal crumb rubber 40 % of sand)
P = paper("Self-healing and mechanical properties of a designed Zn2 + ionic clusters rubber engineered cementitious composites with tight bonding",
          "Xiaodan Teng, Jiawei Weng, Huijie Wu, Yu Zhang, Yuan Cui, Zheng Chen", 2024, "10.1016/j.conbuildmat.2024.139446")
B = 415 + 830
for nm, sand, cr, fc, scr, ts, eps in [("XR-0 (control)", 450, 0, 38.369, 3.30, 4.88, 0.66), ("NR-40 (normal rubber, 40 % of sand)", 275, 81, 33.625, 2.22, 3.36, 3.43)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(415 / B), "FA (Fly ash)": r4(830 / B), "W / B": r4(300 / B), "SS / B (Silica sand)": r4(sand / B),
              "HRWR / B": r4(10 / B), "Binder content (kg/m³)": B, "PVA fiber (vol%)": 2, "PVA length (mm)": 12, "PVA diameter (µm)": 40,
              "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": 2,
              "Curing method": "covered with film 24 h at 20 C, demoulded, curing box 20 +/- 1 C RH >= 95 % for 28 d", "Curing time (days)": 28,
              "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28, "Tensile specimen": "dog-bone",
              "Tensile test type": DIRECT, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ts, "First-cracking strength (MPa)": scr,
              "Tensile strain capacity (%)": eps, "Source table/page": "Table 3 (mix, kg/m3), Table 2 (PVA), sect. 3.3 text (tensile, fc)",
              "Conversions / notes": f"{nm}. kg/m3 / B (cement + FA = {B}). Other mixes (XSBR/ZDMA modified rubber) skipped. "
                                     "Tensile strain = 'tensile ductility' in text; strengths = ultimate. VERIFY: fc age not stated (assumed same 28 d curing)."})
    if cr:
        r["Crumb rubber / B"] = r4(cr / B)
    rows.append(r)

# ---------- 5) Umar et al. 2024: SMAF-ECC, reference ECC-PE
P = paper("Self-recovery and mechanical behavior of SMAF-ECC under monotonic and cyclic tensile loading with constitutive model",
          "Muhammad Umar, Hui Qian, Muhammad Faizan Ali, Shi Yifei, Ali Raza, Aneel Manan, Fei Li", 2024, "10.1016/j.conbuildmat.2024.139840")
B = 2
r = dict(P)
r.update({"OPC / Cement": 0.5, "FA (Fly ash)": 0.5, "W / B": 0.33, "SS / B (Silica sand)": 0.365, "SP / B": 0.00075,
          "PE fiber (vol%)": 2, "PE length (mm)": 12, "PE diameter (µm)": 15, "PE tensile strength (MPa)": 3800, "PE elastic modulus (GPa)": 44,
          "Total fiber (vol%)": 2, "Curing method": "temperature-controlled chamber 24 h, then standard curing room 28 d", "Curing time (days)": 28,
          "Demolding age (days)": 1, "Test age (days)": 28, "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
          "First-cracking strength (MPa)": 2.89, "Tensile strength (MPa)": 2.80, "Tensile strain capacity (%)": 5.77,
          "Source table/page": "Table 1 (mix), Table 3 (PE), Table 6 (ECC-PE), sect. 2.2.2",
          "Conversions / notes": "ECC-PE reference only (SMA mixes skipped). Weight proportions C : FA : quartz sand : water : SP = 1 : 1 : 0.73 : 0.66 : 0.0015 (B = 2). "
                                 "Strain = peak strain 5.77 % (ultimate strain 6.09 %). VERIFY: Table 6 peak stress 2.80 MPa is below the initial-crack stress 2.89 MPa. Quartz sand used as sand."})
rows.append(r)

# ---------- 6) Zhu et al. 2025: PVA-reinforced matrices, 3 / 7 / 28 d
P = paper("Enhanced interfacial bonding performance through novel stranded steel fibers in PVA-ECC: Experimental and theoretical analysis",
          "Juntao Zhu, Ziyuan Li, Kai Zhang, Hu Feng, Jiajun Fan, Ke Li", 2025, "10.1016/j.conbuildmat.2025.141711")
B = 1 + 3 + 0.073
# pva vol%, w/b, water ratio, fc(3,7,28), strain(3,7,28), strength(3,7,28)
data = [(1, .25, 1.02, (9.63, 20.68, 28.45), (2.10, 2.38, 3.45), (1.93, 2.17, 3.48)),
        (1, .28, 1.15, (7.55, 17.05, 24.78), (2.68, 3.98, 4.69), (2.31, 3.21, 3.55)),
        (2, .25, 1.02, (10.32, 19.83, 31.82), (2.51, 3.91, 2.19), (2.11, 2.84, 3.60)),
        (2, .28, 1.15, (8.96, 16.71, 26.55), (2.97, 5.43, 7.45), (2.49, 3.43, 3.77))]
for vol, wb, w, fcs, eps, ts in data:
    for i, age in enumerate((3, 7, 28)):
        r = dict(P)
        r.update({"OPC / Cement": r4(1 / B), "FA (Fly ash)": r4(3 / B), "SF (Silica fume)": r4(0.073 / B), "W / B": r4(w / B),
                  "SS / B (Silica sand)": r4(0.4 / B), "SP / B": r4(0.04 / B), "VMA / B": r4(0.001 / B), "Sand max size (µm)": 200,
                  "PVA fiber (vol%)": vol, "PVA length (mm)": 12, "PVA diameter (µm)": 12, "Total fiber (vol%)": vol,
                  "Curing method": "standard curing chamber 20 +/- 2 C, RH 95 +/- 5 % (VERIFY: stated for pull-out specimens, assumed for matrix tests)",
                  "Curing time (days)": age, "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Test age (days)": age,
                  "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7", "Tensile test type": DIRECT,
                  "Compressive strength (MPa)": fcs[i], "Tensile strength (MPa)": ts[i], "Tensile strain capacity (%)": eps[i],
                  "Source table/page": "Table 2 (mix, weight ratios), Table 3 (strength, ultimate tensile strain), sect. 2.2",
                  "Conversions / notes": f"PVA {vol} vol%, w/b {wb}. Weight ratios to cement: FA 3, SF 0.073, quartz sand 0.4 (0.2 mm), water {w}, SP 0.04, HEMC thickener 0.001; "
                                         f"B = cement + FA + SF = {r4(B)}. Thickener entered as VMA / B. Tensile specimen shape not described for matrix tests. "
                                         "VERIFY: 2 % PVA, w/b 0.25: 28-d strain (2.19 %) lower than 7-d (3.91 %) as published."})
        rows.append(r)

# ---------- 7) Wan et al. 2026: HS-ECC with PE and steel (ST) fibres, strain / strength only
P = paper("Effects of hybrid PE-steel fibers in high-strength ECC: Reinforcement mechanisms, performance-cost optimization, and flexural behavior prediction",
          "Siyu Wan, Sanqing Su, Zhen Cao, Zhaoyao Wang", 2026, "10.1016/j.conbuildmat.2026.145748")
B = 490.8 * 2 + 122.7 * 2
t7 = [("09PE", .9, 0, 2.28, 3.17, 1.42), ("09PE03ST", .9, .3, 3.84, 5.54, 2.53), ("09PE06ST", .9, .6, 4.43, 6.16, 2.66),
      ("09PE09ST", .9, .9, 4.98, 6.73, 1.30), ("12PE", 1.2, 0, 2.51, 3.66, 1.51), ("12PE03ST", 1.2, .3, 3.67, 5.46, 3.38),
      ("12PE06ST", 1.2, .6, 4.22, 6.05, 4.81), ("12PE09ST", 1.2, .9, 4.54, 6.65, 1.66), ("15PE", 1.5, 0, 2.63, 3.99, 1.63),
      ("15PE03ST", 1.5, .3, 3.27, 5.39, 5.85), ("15PE06ST", 1.5, .6, 3.66, 5.74, 5.02), ("15PE09ST", 1.5, .9, 3.38, 5.33, 1.79)]
for nm, pe, st, scr, ts, eps in t7:
    r = dict(P)
    r.update({"OPC / Cement": 0.4, "FA (Fly ash)": 0.4, "GGBS": 0.1, "SF (Silica fume)": 0.1, "W / B": r4(319.02 / B),
              "SS / B (Silica sand)": r4(453.99 / B), "SP / B": r4(3.68 / B), "Binder content (kg/m³)": B, "PE fiber (vol%)": pe,
              "PE length (mm)": 12, "PE diameter (µm)": 25, "PE tensile strength (MPa)": 3100, "PE elastic modulus (GPa)": 122,
              "Total fiber (vol%)": r4(pe + st),
              "Curing method": "48 h ambient indoor, demoulded, standard curing chamber RH >= 90 % ~20 C", "Curing time (days)": 28,
              "Curing temperature (°C)": 20, "Curing RH (%)": 90, "Demolding age (days)": 2, "Test age (days)": 28, "Tensile test type": DIRECT,
              "First-cracking strength (MPa)": scr, "Tensile strength (MPa)": ts, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 3 (mix, kg/m3), Table 2 (fibres), Table 4 (tensile), sect. 2.3-2.4",
              "Conversions / notes": f"{nm}. kg/m3 / B (cement + FA + GGBFS + SF = {B}). SS = silica sand (Fig. 1). Strain = peak strain eps_tu of Table 4; "
                                     "fc only in Fig. 5/6 (not entered). VERIFY: tensile test age not stated explicitly (28 d used for compression and curing); "
                                     "tensile specimen shape not checked. Matrix (no fibre) skipped."})
    if st:
        r.update({"Steel fiber (vol%)": st, "Steel length (mm)": 14, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2850,
                  "Steel elastic modulus (GPa)": 205})
    rows.append(r)

# ---------- 8) Bai et al. 2026: lithium-slag ECC, control Li0 only
P = paper("Development of low-carbon engineered cementitious composites incorporating lithium slag: Mechanical properties, microstructure evolution, and life cycle assessment",
          "Meiyan Bai, Long Song, Qinchuan Xiao, Junbo Sun, Haoran Liu", 2026, "10.1016/j.conbuildmat.2026.145983")
B = 656 + 118 + 604
r = dict(P)
r.update({"OPC / Cement": r4(656 / B), "FA (Fly ash)": r4(604 / B), "SF (Silica fume)": r4(118 / B), "W / B": r4(363 / B),
          "Sand (type not stated) / B": r4(410 / B), "SP / B": r4(2 / B), "Binder content (kg/m³)": B, "PE fiber (vol%)": 1.5, "Total fiber (vol%)": 1.5,
          "Curing method": "standard curing (28 d)", "Curing time (days)": 28, "Test age (days)": 28, "Tensile specimen": "dog-bone",
          "Tensile test type": DIRECT, "First-cracking strength (MPa)": 2.89, "Tensile strength (MPa)": 6.42, "Tensile strain capacity (%)": 3.21,
          "Source table/page": "Table 1 (mix Li0), Table 4 (tensile, peak state)",
          "Conversions / notes": f"Control Li0 only (lithium slag mixes skipped). kg/m3 / B (cement + SF + FA = {B}); SF counted in binder. Sand 410 kg/m3 (quartz sand per sect. 3.4.2). "
                                 "Strain = peak-state strain eps_p. fc in Fig. only. VERIFY: tensile test age taken as 28 d (compression stated at 28 d standard curing); PE properties not found."})
rows.append(r)

# ---------- 9) Cao et al. 2026: SFRCC quasi-static fc (steel 1, 3, 6 vol%)
P = paper("Experimental study on dynamic compressive properties of steel fiber reinforced cementitious composite (SFRCC): Coupling effect of high strain rate and high steel fiber content",
          "Shaojun Cao, Ziyuan Feng, Sijia Liu, Junhao Wang, Songhang Liu, Yu Liu, Yuheng Li, Yi Ren, Yifei Hao", 2026, "10.1016/j.conbuildmat.2026.146158")
B = 1.45
for nm, vf, fc in [("S-1", 1, 87.5), ("S-3", 3, 94.3), ("S-6", 6, 126.1)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(1 / B), "GGBS": r4(0.15 / B), "SF (Silica fume)": r4(0.3 / B), "W / B": 0.19, "SS / B (Silica sand)": r4(1.12 / B),
              "SP / B": 0.007, "Steel fiber (vol%)": vf, "Steel length (mm)": 50, "Steel diameter (µm)": 950, "Steel tensile strength (MPa)": 1100,
              "Steel elastic modulus (GPa)": 210, "Total fiber (vol%)": vf,
              "Curing method": "sealed with film, demoulded, natural curing 28 d", "Curing time (days)": 28, "Test age (days)": 28,
              "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "70 x 140", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 3 (mix ratios), Table 2 (fibre), Table 6 (quasi-static fc), sect. 2.2-2.3",
              "Conversions / notes": f"{nm}. Weight ratios cement 1 : GGBS 0.15 : SF 0.3 (B = 1.45); quartz sand 0.56 + 0.56 (40-70 and 70-120 mesh) = 1.12 per cement, entered per B. "
                                     "VERIFY: SP 0.7 % taken as % of binder. Fibre 1 / 3 % by conventional mixing, 6 % by pre-placed fibre network + grout infiltration. "
                                     "Specimens cored / cut from 900x800x380 mm blocks. S-0 (no fibre), S-8, S-10 (> 6 vol%) skipped. Quasi-static test only."})
    rows.append(r)

# ---------- 10) Feng et al. 2026: BE-ECC (PVA unoiled UP / oiled REC), fibre group and HPMC group
P = paper("Study on interfacial bonding and mechanical performance of low-cost polymer-modified engineered cementitious composites",
          "Jing Feng, Kang Yuan, Zihao Li, Xinquan Zhao, Daxing Chen", 2026, "10.1016/j.conbuildmat.2026.146183")
B = 2.2
t10 = [("F1-R", 0, 1, 0, 1.88, 2.36, 1.07), ("F2-U", 2, 0, 0, 2.09, 2.27, 0.31), ("F2-R", 0, 2, 0, 2.70, 3.54, 4.09),
       ("F2-35", .7, 1.3, 0, 2.26, 2.82, 2.48), ("F2-50 (control)", 1, 1, 0, 2.05, 2.65, 1.41), ("F2-65", 1.3, .7, 0, 1.63, 2.34, 0.55),
       ("HPMC-0.05", 1, 1, .05, 1.64, 2.05, 1.53), ("HPMC-0.10", 1, 1, .10, 1.57, 2.00, 1.41), ("HPMC-0.15", 1, 1, .15, 1.53, 1.88, 1.44),
       ("HPMC-0.20", 1, 1, .20, 1.43, 1.81, 0.84)]
for nm, up, rec, hp, scr, ts, eps in t10:
    r = dict(P)
    r.update({"OPC / Cement": r4(1 / B), "FA (Fly ash)": r4(1.2 / B), "W / B": 0.30, "SS / B (Silica sand)": 0.36, "SP / B": 0.004,
              "PVA fiber (vol%)": up + rec, "PVA length (mm)": 12, "Total fiber (vol%)": up + rec,
              "Curing method": "demoulded after 24 h, 20 +/- 2 C and 95 % RH for 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 20,
              "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28, "Tensile test type": DIRECT,
              "First-cracking strength (MPa)": scr, "Tensile strength (MPa)": ts, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 6 (mix), Table 5 (PVA), Table 7 (fibre group) / Table 9 (HPMC group), sect. 2",
              "Conversions / notes": f"{nm}. Cement 1 : FA 1.2 (B = 2.2), sand/B 0.36 (quartz sand), W/B 0.30. PVA vol% = unoiled (UP, 12 um, 1300 MPa, 30 GPa) {up} + oiled (REC, 40 um, 1560 MPa, 41 GPa) {rec}; "
                                     "fibre diameter / strength left empty (two PVA types). VERIFY: SP 0.004 taken as ratio to binder. Mixes with EVA polymer skipped; F0 (no fibre) skipped."})
    if up == 0 or rec == 0:
        if up == 0:
            r.update({"PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1560, "PVA elastic modulus (GPa)": 41})
        else:
            r.update({"PVA diameter (µm)": 12, "PVA tensile strength (MPa)": 1300, "PVA elastic modulus (GPa)": 30})
    if hp:
        r["HPMC / B (hydroxypropyl methyl cellulose)"] = hp / 100
        r["Conversions / notes"] += f" HPMC {hp} % (VERIFY: taken as % of binder), base mix = F2-50."
    rows.append(r)

# ---------- 11) Zhang et al. 2026: HS-ECC overlay material, PE 1.0 / 1.5 / 2.0 vol%
P = paper("Mixed-mode interfacial fracture behavior of ultra-thin overlay system with high-strength ECC: Kinking-and-trapping mechanism",
          "Zhi-Liang Zhang, Li-Feng Zhang, Rui-Yang Ma, Ze-Ming Yang, Ling-Yu Xu, Dan-Dan Shi, Ji-Xiang Zhu, Bo-Tao Huang", 2026,
          "10.1016/j.conbuildmat.2026.146895")
B = 912 + 228
for nm, vf, fc, eps, ts, scr in [("E-1.0%", 1.0, 92.4, 2.1, 4.4, 3.5), ("E-1.5%", 1.5, 89.0, 3.1, 5.0, 3.5), ("E-2.0%", 2.0, 86.1, 3.4, 5.7, 3.6)]:
    r = dict(P)
    r.update({"OPC / Cement": 0.8, "SF (Silica fume)": 0.2, "W / B": r4(365 / B), "SS / B (Silica sand)": r4(342 / B), "SP / B": r4(5 / B),
              "Binder content (kg/m³)": B, "PE fiber (vol%)": vf, "PE length (mm)": 12, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000,
              "PE elastic modulus (GPa)": 100, "Total fiber (vol%)": vf,
              "Curing method": "covered 24 h, demoulded, standard curing until test at 28 d", "Curing time (days)": 28, "Demolding age (days)": 1,
              "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Tensile specimen": "dumbbell",
              "Tensile test type": DIRECT, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ts, "First-cracking strength (MPa)": scr,
              "Tensile strain capacity (%)": eps, "Source table/page": "Table 2 (mix, kg/m3), Table 1 (PE), Table 4 (properties), sect. 2",
              "Conversions / notes": f"{nm}. kg/m3 / B (cement + SF = {B}). SP given as solid content. VERIFY: FSS interpreted as fine silica sand (not defined in text); curing temperature / RH not stated."})
    rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e30.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows;", df["DOI / URL"].nunique(), "papers")

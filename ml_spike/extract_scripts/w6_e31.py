"""Wave 6, agent e31: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e31.csv (99-column TEMPLATE header).
Papers: conbuildmat.2026.148419, cscm.2021.e00525, cscm.2022.e01321, dibe.2024.100462, jclepro.2024.141570,
        istruc.2024.106579, istruc.2022.02.055, istruc.2022.11.052
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


# ---------- 1) Dong et al.: aeolian-sand UHPC, steel fibre, direct tension (AS-30 only; other mixes only in Fig. 8)
P = {"Article Name": "Meso-scale association between aeolian sand content and uniaxial tensile properties of UHPC: Quantitative characterization of steel fiber spatial distribution and constitutive modeling",
     "Author": "Wei Dong, Zeyuan Lin, Gang Xue, Yanjie Lin", "Year": 2026, "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2026.148419"}
B = 770 + 110 + 220
r = dict(P)
r.update({"OPC / Cement": r4(770 / B), "SF (Silica fume)": r4(110 / B), "GGBS": r4(220 / B), "W / B": r4(198 / B),
          "River sand / B": r4(847 / B), "Dune sand / B": r4(363 / B), "SP / B": r4(22 / B), "Binder content (kg/m³)": B,
          "Steel fiber (vol%)": 2.0, "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2800,
          "Steel elastic modulus (GPa)": 200, "Total fiber (vol%)": 2.0,
          "Curing method": "demoulded 24 h, standard curing 20 +/- 2 C RH >= 95 % for 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 20,
          "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28, "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 280,
          "Tensile test type": DIRECT, "First-cracking strength (MPa)": 6.2, "Tensile strength (MPa)": 7.7, "Tensile strain capacity (%)": 0.3227,
          "Source table/page": "Table 3 (mix AS-30), Table 2 (fibre), sect. 3.3 text (AS-30 values: 6.2 MPa, 7.7 MPa, 3227 microstrain)",
          "Conversions / notes": "AS-30 (30 % of river sand replaced by aeolian sand 'AS', entered as Dune sand). kg/m3 / B (cement + SF + GGBS = 1100). Steel 158 kg/m3 / 7900 = 2.0 vol%. "
                                 "Antifoaming agent 4.4 kg/m3 (noted). Water = standard mixing water 198 (additional 2.5 kg/m3 for AS absorption not added). Other mixes only in Fig. 8 (not entered). "
                                 "VERIFY: test age 28 d derived from 28 d curing; peak strain 3227 microstrain = 0.3227 %."})
rows.append(r)

# ---------- 2) Abdulkadir et al.: SC HVFA-ECC (RSM), PVA, 28 d, water curing
P = {"Article Name": "Modelling and multi-objective optimization of the fresh and mechanical properties of self-compacting high volume fly ash ECC (HVFA-ECC) using response surface methodology (RSM)",
     "Author": "Isyaka Abdulkadir, Bashar S. Mohammed, M.S. Liew, M.M.A. Wahab", "Year": 2021, "DOI / URL": "https://doi.org/10.1016/j.cscm.2021.e00525"}
# name, PVA vol%, FA kg, cement kg, PVA kg, fc list, strain list
mixes = [("M8", 1.5, 898, 385, 19.5, [47.66], [6.76]), ("M6", 2.0, 770, 513, 26.0, [50.82], [6.59]), ("M7", 1.5, 642, 642, 19.5, [56.25], [5.54]),
         ("M4", 2.0, 898, 385, 26.0, [45.15], [7.02]), ("M5", 1.0, 770, 513, 13.0, [48.85], [4.10]), ("M3", 1.0, 898, 385, 13.0, [46.79], [4.50]),
         ("M1", 1.0, 642, 642, 13.0, [50.09], [3.47]), ("M2", 2.0, 642, 642, 26.0, [54.87], [4.50]),
         ("M9-M13 centre point", 1.5, 770, 513, 19.5, [52.96, 51.185, 53.03, 52.55, 52.91], [6.10, 5.98, 6.77, 5.88, 6.40])]
for nm, v, fa, c, pk, fcs, eps in mixes:
    B = fa + c
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "W / B": r4(320 / B), "Sand (type not stated) / B": r4(467 / B), "Binder content (kg/m³)": B,
              "PVA fiber (vol%)": v, "PVA length (mm)": 18, "PVA diameter (µm)": 200, "PVA tensile strength (MPa)": 750, "PVA elastic modulus (GPa)": 27,
              "Total fiber (vol%)": v, "Curing method": "demoulded after 24 h, water curing 20 C RH 95 % until 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 20,
              "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28, "Tensile test type": DIRECT, "Tensile specimen": "dog-bone (JSCE)",
              "Compressive strength (MPa)": r4(sum(fcs) / len(fcs)), "Tensile strain capacity (%)": r4(sum(eps) / len(eps)),
              "Source table/page": "Table 3 (mix, kg/m3), Table 4 (fc, tensile strain), Table 2 (PVA), sect. 2.2-2.5",
              "Conversions / notes": f"{nm}. kg/m3 / B (cement + FA). PVA kg/m3 consistent with vol% at 1.3 g/cm3. Self-compacting mix but no superplasticizer dose given in the paper (SP left empty, VERIFY). "
                                     "Table 4 'Tensile strain' (direct tensile test, JSCE) used; tensile strength not reported."})
    if len(fcs) > 1:
        r["Conversions / notes"] += " Mean of the 5 replicated centre-point runs (M11, M12, M9, M10, M13) of the RSM design."
    rows.append(r)

# ---------- 3) Xu et al.: UHPC U2 (silica fume + steel fibre), standard and steam curing
P = {"Article Name": "Impact properties of Ultra High Performance Concrete (UHPC) cured by steam curing and standard curing",
     "Author": "Xiangbo Xu, Zuquan Jin, Yong Yu, Ning Li", "Year": 2022, "DOI / URL": "https://doi.org/10.1016/j.cscm.2022.e01321"}
B = 826 + 206
for tag, fc, cm, ct, tt, age, heat, note in [
        ("standard", 104.0, "demoulded 24 h, standard curing 20 C RH 95 % until 28 d", 28, 20, 28, None, ""),
        ("steam", 138.9, "demoulded 24 h, steam 90 C for 3 d", 3, 90, 4, 72, " VERIFY: test age 4 d derived (1 d + 3 d steam).")]:
    r = dict(P)
    r.update({"OPC / Cement": r4(826 / B), "SF (Silica fume)": r4(206 / B), "W / B": r4(172 / B), "M-sand / B": r4(1204 / B), "SP / B": r4(20.6 / B),
              "Binder content (kg/m³)": B, "Steel fiber (vol%)": 1.0, "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2900,
              "Steel elastic modulus (GPa)": 200, "Total fiber (vol%)": 1.0, "Curing method": cm, "Curing time (days)": ct, "Curing temperature (°C)": tt,
              "Demolding age (days)": 1, "Test age (days)": age, "Heat curing duration (h)": heat, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100",
              "Compressive strength (MPa)": fc, "Source table/page": "Table 3 (mix U2), Table 2 (fibre), Table 4 (fc), sect. 2.2",
              "Conversions / notes": "Mix U2 only (U0 / U1 have no fibre). kg/m3 / B (cement + SF = 1032). Steel 78 kg/m3 / 7800 = 1.0 vol%. Machine-made sand as M-sand. Tensile not tested." + note})
    if tag == "standard":
        r["Curing RH (%)"] = 95
    rows.append(r)

# ---------- 4) Zhang et al.: PE-ECC reference (20 C) of PE-CW ECC
P = {"Article Name": "Effect of high temperature on mechanical properties of polyethylene fibre-calcium carbonate whisker engineered cementitious composites",
     "Author": "Xutao Zhang, Xikuan Lyu, Xuwei Zhang, Chao Lou", "Year": 2024, "DOI / URL": "https://doi.org/10.1016/j.dibe.2024.100462"}
B = 827 + 596 + 75
r = dict(P)
r.update({"OPC / Cement": r4(827 / B), "FA (Fly ash)": r4(596 / B), "SF (Silica fume)": r4(75 / B), "W / B": r4(239 / B), "Sand (type not stated) / B": r4(389 / B),
          "SP / B": r4(35 / B), "Binder content (kg/m³)": B, "PE fiber (vol%)": r4(17 / 970 * 100), "PE length (mm)": 18, "PE diameter (µm)": 24,
          "PE tensile strength (MPa)": 2800, "PE elastic modulus (GPa)": 100, "Total fiber (vol%)": r4(17 / 970 * 100),
          "Curing method": "demoulded after 24 h, standard curing room to 28 d, then oven 45 C 48 h (moisture equalisation), tested at room temperature (20 C group)",
          "Curing time (days)": 28, "Demolding age (days)": 1, "Test age (days)": 30, "Tensile specimen": "dumbbell", "Tensile test type": DIRECT,
          "Compressive specimen": "cube", "Compressive strength (MPa)": 70.85, "Tensile strength (MPa)": 4.74, "Tensile strain capacity (%)": 6.09,
          "Source table/page": "Table 3 (mix PE-ECC), Table 1 (fibre), Table 5 (fc, 20 C), Table 6 (tensile, 20 C), sect. 2.2",
          "Conversions / notes": "PE-ECC (no whisker) at 20 C reference only; PECW-ECC skipped (calcium carbonate whisker). kg/m3 / B (cement + FA + SF = 1498). "
                                 "PE 17 kg/m3 / 970 = 1.75 vol% (VERIFY: derived). Water reducer 35 kg/m3 entered as SP. "
                                 "VERIFY: test age 30 d derived (28 d curing + 45 C oven 48 h); curing temperature / RH not stated; cube size not stated."})
rows.append(r)

# ---------- 5) Wang et al.: quartz-sand (QS) ECC, different W/B, PE 1.6 vol%
P = {"Article Name": "Performance enhancement of engineered cementitious composite through tailoring recycled iron sand",
     "Author": "Fei Wang, Jiangtao Yu, Yao Ding, Jiaxing Ma, Kequan Yu", "Year": 2024, "DOI / URL": "https://doi.org/10.1016/j.jclepro.2024.141570"}
qs = [("0.2-0.6-QS", 513, 492, 128, 128, 757, 252, 3.1, 0.0, 5.35, 14.17, 7.43), ("0.25-0.6-QS", 483, 464, 121, 121, 714, 297, 2.6, 0.7, 4.18, 12.07, 7.73),
      ("0.3-0.6-QS", 456, 437, 114, 114, 673, 336, 1.6, 0.7, 3.42, 8.55, 7.66), ("0.35-0.6-QS", 432, 414, 108, 108, 637, 372, 1.1, 0.8, 2.77, 6.78, 8.03)]
for nm, c, g, fa, sf, s, w, sp, hp, scr, smax, eps in qs:
    B = c + g + fa + sf
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), "GGBS": r4(g / B), "FA (Fly ash)": r4(fa / B), "SF (Silica fume)": r4(sf / B), "W / B": r4(w / B), "SS / B (Silica sand)": r4(s / B),
              "SP / B": r4(sp / B), "Binder content (kg/m³)": B, "PE fiber (vol%)": 1.6, "PE length (mm)": 18, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 2900,
              "PE elastic modulus (GPa)": 116, "Total fiber (vol%)": 1.6, "Curing method": "demoulded after 24 h, air storage 20 C RH 70 % until 28 d",
              "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 70, "Demolding age (days)": 1, "Test age (days)": 28,
              "Tensile specimen": "dog-bone", "Tensile test type": DIRECT, "First-cracking strength (MPa)": scr, "Tensile strength (MPa)": smax, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 3 (mix, kg/m3), Table 2 (PE), Table 4 (tensile), sect. 3 (curing)",
              "Conversions / notes": f"{nm} (quartz sand, S/B 0.6). kg/m3 / B (cement + GGBS + FA + SF = {B}). Iron-sand mixes skipped. PE 1.6 vol% as stated. "
                                     "fc and tensile of S/B 0.4 / 0.8 mixes only in figures (not entered)."})
    if hp:
        r["HPMC / B (hydroxypropyl methyl cellulose)"] = r4(hp / B)
    rows.append(r)

# ---------- 6) Wen & Cao: seawater sea-sand ECC with PE (+ stainless steel fibre), no CW
P = {"Article Name": "Reinforcement effects on the tensile properties of seawater sea-sand engineered cementitious composites reinforced with multi-scale hybrid fibers",
     "Author": "Shaoyong Wen, Mingli Cao", "Year": 2024, "DOI / URL": "https://doi.org/10.1016/j.istruc.2024.106579"}
B = 974 + 283 + 158 + 158
for nm, ssf, fcv, st, eps in [("C0/P2/S0", 0, 124.3, 7.0, 5.9), ("C0/P2/S0.5", 39.5, 147.8, 10.3, 4.3)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(974 / B), "SF (Silica fume)": r4(283 / B), "Metakaolin": r4(158 / B), "GGBS": r4(158 / B), "W / B": r4(315 / B),
              "Sea sand / B": r4(472 / B), "SP / B": r4(25 / B), "Binder content (kg/m³)": B, "PE fiber (vol%)": 2.0, "PE length (mm)": 12, "PE diameter (µm)": 24,
              "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 100, "Total fiber (vol%)": 2.0 + (0.5 if ssf else 0),
              "Curing method": "demoulded 24 h, cured 28 d at 20 +/- 2 C RH >= 95 %", "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95,
              "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Tensile specimen": "dog-bone",
              "Tensile test type": DIRECT, "Compressive strength (MPa)": fcv, "Tensile strength (MPa)": st, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix), Table 3 (fibres), Table 4 (properties), sect. 2.3",
              "Conversions / notes": f"{nm}. kg/m3 / B (cement + SF + MK + slag = {B}). Water is seawater (315 kg/m3, salts not counted). Sea sand as Sea sand. "
                                     "PE 19.4 kg/m3 = 2.0 vol%; stainless steel fibre 39.5 kg/m3 / 7950 = 0.5 vol%. CW (calcium whisker) mixes skipped."})
    if ssf:
        r.update({"Steel fiber (vol%)": 0.5, "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2560, "Steel elastic modulus (GPa)": 195})
    rows.append(r)

# ---------- 7) Zhang et al.: UHPC under axial compression, non-steam vs steam curing (cube fc, direct tension ft)
P = {"Article Name": "Damage of non-steam-cured UHPC under axial compression with and without short-term sustained loading history",
     "Author": "Ziyang Zhang, Tengfei Xu, Arnaud Castel", "Year": 2022, "DOI / URL": "https://doi.org/10.1016/j.istruc.2022.02.055"}
B = 680 + 200 + 170
for cm, ct, tt, age, heat, fcv, ft in [("sealed, 23 C RH 95 % curing room until 28 d (non-steam)", 28, 23, 28, None, 118.89, 9.07),
                                       ("demoulded after 48 h, steam 90 C 48 h (15 C/h ramps), then curing room", 2, 90, 7, 48, 137.64, 11.04)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(680 / B), "FA (Fly ash)": r4(200 / B), "SF (Silica fume)": r4(170 / B), "W / B": 0.152, "SS / B (Silica sand)": r4(1150 / B),
              "Binder content (kg/m³)": B, "Steel fiber (vol%)": r4(100 / 7850 * 100), "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 850,
              "Total fiber (vol%)": r4(100 / 7850 * 100), "Curing method": cm, "Curing time (days)": ct, "Curing temperature (°C)": tt, "Demolding age (days)": 2,
              "Test age (days)": age, "Heat curing duration (h)": heat, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100", "Tensile specimen": "dog-bone",
              "Tensile test type": DIRECT, "Compressive strength (MPa)": fcv, "Tensile strength (MPa)": ft,
              "Source table/page": "Table 1 (mix), Table 2 (fc cube, ft), sect. 2.1-2.2",
              "Conversions / notes": "kg/m3 / B (cement + FA + SF = 1050). W/B 0.152 as stated (water 156 / 1050 = 0.149). Crushed quartz 1150 kg/m3 entered as silica sand (VERIFY: particle size not stated, "
                                     "could be quartz powder). Steel fibre 100 kg/m3 / 7850 = 1.27 vol%. SP 180 kg/m3 and water reducer 14 kg/m3 in Table 1 look implausible, SP left empty (VERIFY)."})
    if heat is None:
        r["Curing RH (%)"] = 95
    rows.append(r)

# ---------- 8) Cao et al.: UHPC for steel tube bond-slip; cube fcu
P = {"Article Name": "Bond-slip behavior between high-strength steel tube and Ultra-high Performance Concrete",
     "Author": "Xuan Cao, Xiang-Dong Xie, Tian-Yi Zhang, Guo-Feng Du", "Year": 2022, "DOI / URL": "https://doi.org/10.1016/j.istruc.2022.11.052"}
B = 700 + 210 + 105
for cm, tt, fcv in [("covered 24 h, natural curing: plastic wrap, laboratory, watered regularly, 28 d", None, 128), ("24 h in laboratory, then standard curing room 20 +/- 3 C RH > 90 % for 28 d", 20, 136)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(700 / B), "SF (Silica fume)": r4(210 / B), "GGBS": r4(105 / B), "W / B": r4(203 / B), "SS / B (Silica sand)": r4(820 / B),
              "SP / B": r4(35.525 / B), "Binder content (kg/m³)": B, "Steel fiber (vol%)": r4(235.5 / 7850 * 100), "Total fiber (vol%)": r4(235.5 / 7850 * 100),
              "Curing method": cm, "Curing time (days)": 28, "Curing temperature (°C)": tt, "Curing RH (%)": 90 if tt else None, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "100", "Compressive strength (MPa)": fcv,
              "Source table/page": "Table 2 (mix), Table 3 (fcu), sect. 2",
              "Conversions / notes": "kg/m3 / B (cement + SF + slag = 1015). Quartz sand 40-70 mesh 410 + 70-140 mesh 410 kg/m3 entered as silica sand. "
                                     "VERIFY: steel fibre 235.5 kg/m3 (3.0 vol% at 7850) read from the Table 2 column order, fibre geometry not stated. fcu = cube strength (fc column is prism)."})
    rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e31.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows;", df["DOI / URL"].nunique(), "papers")

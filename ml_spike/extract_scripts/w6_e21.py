"""Wave 6, agent e21: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e21.csv (99-column TEMPLATE header).
Papers: conbuildmat.2016.09.009, 2018.08.128, 2018.08.188, 2019.117161, 2019.117987, 2020.119956, 2020.121698
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


# ---------- 1) Georgiou & Pantazopoulou: PVA SHCC, fibre length (uncoated mixes M8, M12)
P = {"Article Name": "Effect of fiber length and surface characteristics on the mechanical properties of cementitious composites",
     "Author": "Antroula V. Georgiou, Stavroula J. Pantazopoulou", "Year": 2016,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2016.09.009"}
B = 21.23 + 25.48
for mid, L, fc, fty, ftu, etu in [("M8", 8, 55.51, 2.36, 2.38, 0.3403), ("M12", 12, 54.64, 2.62, 3.45, 1.082)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(21.23 / B), "FA (Fly ash)": r4(25.48 / B), "W / B": r4(13.14 / B), "SS / B (Silica sand)": r4(17.0 / B),
              "Sand max size (µm)": 300, "SP / B": r4(0.255 / B), "PVA fiber (vol%)": 2.0, "PVA length (mm)": L, "PVA diameter (µm)": 39,
              "Total fiber (vol%)": 2.0, "Curing method": "covered in mould 24 h, then under water until test at 100 d",
              "Curing time (days)": 100, "Demolding age (days)": 1, "Test age (days)": 100, "Compressive specimen": "cylinder",
              "Compressive specimen size (mm)": "100x200", "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
              "Compressive strength (MPa)": fc, "First-cracking strength (MPa)": fty, "Tensile strength (MPa)": ftu,
              "Tensile strain capacity (%)": etu,
              "Source table/page": "Table 1 (batch masses), Table 2 (fc = sigma_c,o), Table 3 (direct tension), sect. 2.4",
              "Conversions / notes": f"{mid}. Batch masses (kg) / B (cement + FA = {B:.2f} kg). Coated-fibre mixes (M8C, M12C, surfactant coating) and plain matrix skipped. "
                                     "Tensile strength = f_tu, strain = eps_tu (mm/mm x 100); first-cracking column = f_ty ('yield' point of tension curve) "
                                     "VERIFY. fc = peak stress of cylinder compression test. Water temperature not stated. Year from DOI/volume."})
    rows.append(r)

# ---------- 2) Sun et al.: hybrid steel-PVA, cylinders in compression (fc only)
P = {"Article Name": "Stress strain behavior of hybrid steel-PVA fiber reinforced cementitious composites under uniaxial compression",
     "Author": "Linzhu Sun, Qiang Hao, Junliang Zhao, Dongyan Wu, Fang Yang", "Year": 2018,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2018.08.128"}
mixes = {"A": (393.6, 118.1, 59.1, 256.9, 1263.5, 12.2, 0.45), "B": (484.2, 145.3, 72.6, 266.8, 1134.3, 15.0, 0.38)}
fib = {1: (0, 0), 2: (0, .5), 3: (0, 1), 4: (.5, 0), 5: (.5, .5), 6: (.5, 1), 7: (1, 0), 8: (1, .5), 9: (1, 1), 10: (1.5, 0), 11: (1.5, .5), 12: (2, 0)}
fcs = {"A": [31.0, 31.8, 34.9, 45.8, 40.4, 40.9, 43.7, 42.8, 39.5, 44.9, 42.8, 42.4],
       "B": [37.62, 39.92, 43.13, 46.91, 52.28, 50.29, 59.43, 57.06, 60.85, 56.52, 57.18, 60.52]}
for s, (c, fa, sf, w, sa, sp, wb) in mixes.items():
    B = c + fa + sf
    for i in range(2, 13):
        st, pv = fib[i]
        r = dict(P)
        r.update({"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "SF (Silica fume)": r4(sf / B), "W / B": r4(w / B),
                  "River sand / B": r4(sa / B), "SP / B": r4(sp / B), "Binder content (kg/m³)": round(B, 1),
                  "Total fiber (vol%)": st + pv, "Curing method": "standard fog room 28 d", "Curing time (days)": 28, "Test age (days)": 28,
                  "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "150x300", "Compressive strength (MPa)": fcs[s][i - 1],
                  "Source table/page": "Table 1 (mix), Table 2 (fibres), Table 3 (fibre content), Table 4 (fc)",
                  "Conversions / notes": f"{s}{i}. kg/m3 / B (cement + FA + SF = {B:.1f}); W/B stated {wb}. Plain mixes A1, B1 skipped (no fibre). "
                                         "No tension test; strain at peak in compression not entered. Fog room temperature not stated."})
        if st:
            r.update({"Steel fiber (vol%)": st, "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2800,
                      "Steel elastic modulus (GPa)": 200})
        if pv:
            r.update({"PVA fiber (vol%)": pv, "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1560,
                      "PVA elastic modulus (GPa)": 41})
        rows.append(r)

# ---------- 3) Mohammed et al.: tirewire + PVA ECC, validation mixes (Table 7 experimental)
P = {"Article Name": "Optimization of hybrid fibres in engineered cementitious composites",
     "Author": "Bashar S. Mohammed, Veerendrakumar C. Khed, Mohd Shahir Liew", "Year": 2018,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2018.08.188"}
B = 583 + 700
for pv, fc, fl, ft, eps in [(1.5, 101.54, 10.028, 5.146, 3.5), (1.33, 97.6, 10.35, 5.328, 3.566), (1.029, 100.86, 9.88, 5.15, 3.156)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(583 / B), "FA (Fly ash)": r4(700 / B), "W / B": r4(187 / B), "River sand / B": r4(467 / B),
              "Sand max size (µm)": 450, "Binder content (kg/m³)": B, "Steel fiber (vol%)": 0.5, "PVA fiber (vol%)": pv,
              "Total fiber (vol%)": round(0.5 + pv, 3),
              "Curing method": "demoulded 24 h, curing tank 28 d at 23 +/- 2 C, RH about 80 %", "Curing time (days)": 28,
              "Curing temperature (°C)": 23, "Curing RH (%)": 80, "Demolding age (days)": 1, "Test age (days)": 28,
              "Tensile test type": DIRECT, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 3 (mix, kg/m3), Table 7 (validation, experimental values), sect. 2 (curing)",
              "Conversions / notes": f"Validation mix tirewire 0.5 %, PVA {pv} %. kg/m3 / B (cement + FA = 1283). Steel = recycled tirewire fibre from waste tyres. "
                                     "VERIFY: tirewire/PVA % taken as vol%; SP dose of validation mixes not given (SP/B left empty); fibre dimensions not entered; "
                                     "ultimate tensile strength and strain of the 'direct tensile' test (Table 7). Mix proportions of the 3 validation mixes assume the same matrix as Table 3."})
    rows.append(r)

# ---------- 4) Kan et al.: fly ash EGC, zeolite-free reference 0%ZFA-EGC
P = {"Article Name": "Properties of polyvinyl alcohol fiber reinforced fly ash based Engineered Geopolymer Composites with zeolite replacement",
     "Author": "Lili Kan, Li Zhang, Yujing Zhao, Min Wu", "Year": 2019,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2019.117161"}
B = 42.5 + 11.0
for age, ft, eps, fcr, fcube in [(3, 2.15, 4.63, 1.63, 14.98), (7, 2.48, 5.23, 1.57, 17.21), (28, 2.84, 4.01, 1.86, 18.85)]:
    r = dict(P)
    r.update({"FA (Fly ash)": 1.0, "WG / B (Water glass)": r4(13.7 / B), "NaOH / B": r4(3.0 / B), "W / B": r4(12.7 / B),
              "Sand (type not stated) / B": r4(16.0 / B), "PVA fiber (vol%)": 1.5, "PVA length (mm)": 12, "PVA diameter (µm)": 39,
              "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": 1.5,
              "Curing method": "lab 24 h, demoulded, covered with plastic and oven 80 C 2 h, then 20 C RH 70 % until test",
              "Curing time (days)": age, "Curing temperature (°C)": 20, "Curing RH (%)": 70, "Demolding age (days)": 1, "Test age (days)": age,
              "Heat curing duration (h)": 2, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
              "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
              "Compressive strength (MPa)": fcube, "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 3 (mix, wt%), Table 4 (tensile), Table 6 (fc), sect. 2.2 (curing)",
              "Conversions / notes": "Reference 0%ZFA-EGC only (zeolite mixes skipped). Mix in wt% of total; B = low-Ca FA 42.5 + high-Ca FA 11.0 = 53.5. "
                                     "WG = Na2SiO3 solution (modulus 3.3) 13.7, NaOH 3.0, sand 16.0, water 12.7 (water in WG not added). "
                                     "fc = 50 mm cube; phi50x100 cylinder was 4.22/9.65/12.16 MPa. "
                                     "VERIFY: PVA fibre 1.1 wt% converted to about 1.5 vol% with assumed component densities (FA 2.2, WG 1.4, NaOH 2.1, sand 2.65 g/cm3); paper gives only wt%."})
    rows.append(r)

# ---------- 5) Guo et al.: HDCC with RAP, control A1-0 (river sand only), strain only
P = {"Article Name": "Effect of incorporating reclaimed asphalt pavement on macroscopic and microstructural properties of high ductility cementitious composites",
     "Author": "Li-Ping Guo, Miao Wang, Cong Ding, Li-Juan Chai", "Year": 2020,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2020.119956"}
r = dict(P)
r.update({"OPC / Cement": r4(1 / 2.5), "FA (Fly ash)": r4(1.5 / 2.5), "W / B": r4(0.625 / 2.5), "River sand / B": r4(0.75 / 2.5),
          "SP / B": r4(0.01 / 2.5), "PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 39,
          "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 30, "Total fiber (vol%)": 2.0,
          "Curing method": "demoulded 24 h, standard curing room 20 +/- 2 C, RH 95 +/- 5 % until 28 d", "Curing time (days)": 28,
          "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
          "Tensile specimen": "dog-bone", "Tensile test type": DIRECT, "First-cracking strength (MPa)": 3.10, "Tensile strength (MPa)": 5.25,
          "Tensile strain capacity (%)": 1.43, "Source table/page": "Table 3 (mix), Table 1 (fibre), Table 5 (tensile), sect. 3.2 (curing)",
          "Conversions / notes": "Control A1-0 only (RAP mixes skipped). Mass ratios C:FA:S:W:WR = 1:1.5:0.75:0.625:0.01, B = 2.5. "
                                 "fc only in Fig. 5, not entered. VERIFY: water reducer (WR) entered as SP; ratios assumed by mass; PVA E = 30 GPa as stated in Table 1."})
rows.append(r)

# ---------- 6) Rong et al.: RPC with steel fibres, mixes of Table 2 without quartz powder and with fibres
P = {"Article Name": "Quantifying curing and composition effects on compressive and tensile strength of 160-250 MPa RPC",
     "Author": "Qin Rong, Xiaomeng Hou, Chao Ge", "Year": 2019,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2019.117987"}
# id, SG, quartz sand (CQ+FQ), RS, SP%, S vol%, w/b, fc
t = [("A-7", .15, 1.2, 0, 2.5, 1, .17, 141), ("A-8", .15, 1.2, 0, 2.5, 2, .17, 155), ("A-9", .15, 1.2, 0, 2.5, 3, .17, 162),
     ("A-10", .15, 1.2, 0, 2.5, 5, .17, 165), ("A-11", .15, 0, 1.75, 3, 3, .19, 142),
     ("C-1", .15, 1.2, 0, 2.5, 3, .16, 215), ("C-2", .25, 1.2, 0, 2.5, 3, .16, 202), ("C-3", .15, 1.2, 0, 2.5, 3, .17, 240),
     ("C-4", .15, 1.17, 0, 2.5, 3, .17, 231), ("C-5", .25, 1.2, 0, 2.5, 3, .17, 219), ("C-6", .25, 1.17, 0, 2.5, 3, .17, 218),
     ("C-7", .15, 0, 1.75, 3, 3, .17, 214)]
for mid, sg, qs, rs, sp, sv, wb, fc in t:
    B = 1 + .3 + sg
    cond = mid[0]
    r = dict(P)
    r.update({"OPC / Cement": r4(1 / B), "SF (Silica fume)": r4(.3 / B), "GGBS": r4(sg / B), "W / B": wb, "SP / B": r4(sp / 100),
              "Binder content (kg/m³)": round(800 * B, 1), "Steel fiber (vol%)": sv, "Steel length (mm)": 13, "Steel diameter (µm)": 220,
              "Steel tensile strength (MPa)": 2850, "Total fiber (vol%)": sv, "Compressive specimen": "cube",
              "Compressive specimen size (mm)": "70.7", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 2 (mix, fc), note 2 (curing conditions A-D), sect. 2.3",
              "Conversions / notes": f"{mid}. Ratios to cement (800 kg/m3); binder = C + SF + SG. SP dosage is % of binder (40 % solids PCE). "
                                     "Copper-coated straight steel fibre. Mixes with quartz powder (Q), fibre-free A-6, and groups B / D skipped. "})
    if rs:
        r["River sand / B"] = r4(rs / B)
    else:
        r["SS / B (Silica sand)"] = r4(qs / B)
    if cond == "A":
        r.update({"Curing method": "cast, 24 h ambient, then 90 C steam 3 d", "Curing time (days)": 3, "Curing temperature (°C)": 90,
                  "Demolding age (days)": 1, "Test age (days)": 4, "Heat curing duration (h)": 72})
        r["Conversions / notes"] += "VERIFY: test age 4 d derived (1 d ambient + 3 d steam); testing time after curing not stated explicitly."
    else:
        r.update({"Curing method": "cast, 24 h ambient, 90 C steam 7 d, then dry heat 250 C 8 h", "Curing time (days)": 7,
                  "Curing temperature (°C)": 250, "Demolding age (days)": 1, "Test age (days)": 8.3, "Heat curing duration (h)": 176})
        r["Conversions / notes"] += ("VERIFY: test age 8.3 d derived (1 d + 7 d steam + 8 h heat); heat curing duration = 168 h steam + 8 h at 250 C. "
                                     + ("C-4/C-6: CQ 0.78 + FQ 0.39 = 1.17 quartz sand." if mid in ("C-4", "C-6") else ""))
    rows.append(r)

# ---------- 7) Fan et al.: UHPC with hybrid steel fibres, optimised mix HF2
P = {"Article Name": "Optimized design of steel fibres reinforced ultra-high performance concrete (UHPC) composites: Towards to dense structure and efficient fibre application",
     "Author": "Dingqiang Fan, Rui Yu, Kangning Liu, Junhui Tan, Zhonghe Shui, Chunfeng Wu, Shuo Wang, Zhenfeng Guan, Zhengdong Hu, Qiqi Su",
     "Year": 2020, "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2020.121698"}
B = 750 + 144 + 200
r = dict(P)
r.update({"OPC / Cement": r4(750 / B), "SF (Silica fume)": r4(144 / B), "Limestone powder": r4(200 / B), "W / B": r4(190 / B),
          "River sand / B": r4(990 / B), "SP / B": r4(35 / B), "Binder content (kg/m³)": B, "Steel fiber (vol%)": 2.0, "Steel length (mm)": 13,
          "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2000, "Steel elastic modulus (GPa)": 200, "Total fiber (vol%)": 2.0,
          "Test age (days)": 28, "Compressive specimen": "prism (EN 196-1)", "Compressive specimen size (mm)": "40x40x160 prism",
          "Compressive strength (MPa)": 161.7,
          "Source table/page": "Table 8 (mix, kg/m3), Table 3 (fibres), sect. 3 text (fc 161.7 MPa)",
          "Conversions / notes": "HF2 hybrid mix: 0.9 vol% long straight + 1.1 vol% hooked-end fibres (13 mm, 0.2 mm). kg/m3 / B with B = cement + SF + limestone powder (1094). "
                                 "Sand = RS-1 770 + RS-2 220. Other mixes (LSF2, SSF2, HEF2, NON) skipped: fc only as % change in text. "
                                 "VERIFY: curing regime not stated in text; 28 d from text; SP kg/m3 as dosed."})
rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e21.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows;", df["DOI / URL"].nunique(), "papers")

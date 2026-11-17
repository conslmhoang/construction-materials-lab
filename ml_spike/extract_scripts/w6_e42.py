"""Wave 6, agent e42: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e42.csv (99-column TEMPLATE header).
Papers: conbuildmat.2026.147466, 2026.148277, 2026.148363, cscm.2025.e04272, engstruct.2017.04.019,
        engstruct.2018.09.030, engstruct.2021.113675, istruc.2022.08.095, istruc.2025.109251,
        istruc.2025.109785, istruc.2025.110697, jclepro.2025.146867
"""
import os
import re
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


def paper(name, author, year, doi):
    return {"Article Name": name, "Author": author, "Year": year, "DOI / URL": "https://doi.org/" + doi}


# ---------- 1) Shen et al. 2026: nano-CaCO3 / nano-Al2O3 ECC, reference mix only
P = paper("Comparative multiscale investigations of nano-CaCO3 and nano-Al2O3 on the strength and ductility of ECC",
          "Qiang Shen, Chenyu Lu, Jamal A. Abdalla, Zhigang Zhang", 2026, "10.1016/j.conbuildmat.2026.147466")
B = 718 + 574 + 128
r = dict(P)
r.update({"OPC / Cement": r4(718 / B), "FA (Fly ash)": r4(574 / B), "SF (Silica fume)": r4(128 / B), "W / B": r4(290 / B),
          "SS / B (Silica sand)": r4(430 / B), "SP / B": r4(18 / B), "Binder content (kg/m³)": B,
          "PE fiber (vol%)": 2, "Total fiber (vol%)": 2,
          "Curing method": "demoulded after 24 h, standard curing chamber 25 +/- 2 C, RH 95 +/- 2 %", "Curing time (days)": 28,
          "Curing temperature (°C)": 25, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
          "Compressive specimen": "cube", "Compressive specimen size (mm)": "50.8", "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
          "Compressive strength (MPa)": 76.4, "First-cracking strength (MPa)": 3.63, "Tensile strength (MPa)": 6.65, "Tensile strain capacity (%)": 3.92,
          "Source table/page": "Table 1 (mix, kg/m3), Table 2 (tensile), sect. 2.2, 3.3 text (fc 76.4 MPa)",
          "Conversions / notes": f"Ref. mix only (nano-CaCO3 / nano-Al2O3 mixes skipped). kg/m3 / B (C + FA + SF = {B}). Sand = silica sand 70-140 mesh. "
                                 "PE 19 kg/m3, paper states 2 vol%. Paper states sand/binder 0.2 but Table 1 gives 430/1420 = 0.30 (Table value used). "
                                 "VERIFY: PE length / diameter not found in text; fc value from text, tests at 28 d after 28 d curing."})
rows.append(r)

# ---------- 2) Ye et al. 2026: sand morphology and size, PE-ECC (natural sands, standard sand only)
P = paper("Sand morphology and size effects on fracture and tensile behaviors of engineered cementitious composites with a roughness-based size effect model",
          "Junhong Ye, Zhaoliang Sheng, Yute Chen, Zhihang Xue, Bakhadir Mirzaev, Kequan Yu, Jiangtao Yu", 2026, "10.1016/j.conbuildmat.2026.148363")
B = 936.7 + 401.4
# name, sand column, sand label, max size um, fc, ts, strain %, note
t2 = [("DS-ECC", "Dune sand / B", "dune sand, unsieved", None, 71.628, 7.850, 8.11, "strain 8.11 % from text (Table 4: 0.081)"),
      ("NS-ECC", "Sand (type not stated) / B", "normal sand, unsieved", None, 80.459, 5.921, 7.3, "strain from Table 4 (0.073)"),
      ("SeaS-ECC", "Sea sand / B", "sea sand, unsieved", None, 60.447, 5.082, 6.48, "strain 6.48 % from text (Table 4: 0.065)"),
      ("WS-ECC", "Sand (type not stated) / B", "wind sand, unsieved", None, 46.062, 6.484, 6.5, "strain from Table 4 (0.065)"),
      ("DS-100-ECC", "Dune sand / B", "dune sand 100-120 mesh (0.12-0.15 mm)", 150, 74.928, 8.400, 8.0, "strain from Table 4 (0.080)"),
      ("NS-100-ECC", "Sand (type not stated) / B", "normal sand 100-120 mesh (0.12-0.15 mm)", 150, 72.952, 9.795, 10.8, "strain from Table 4 (0.108)"),
      ("StdS-100-ECC", "SS / B (Silica sand)", "standard sand 100-120 mesh (0.12-0.15 mm)", 150, 75.423, 8.303, 8.8, "strain from Table 4 (0.088)"),
      ("StdS-26-ECC", "SS / B (Silica sand)", "standard sand 26-28 mesh (0.68-0.71 mm)", 710, None, 4.616, 11.5,
       "strain from Table 4 (0.115); fc not reported for standard sand 26 mesh"),
      ("StdS-40-ECC", "SS / B (Silica sand)", "standard sand 40-45 mesh (0.40-0.45 mm)", 450, None, 6.070, 7.5,
       "strain from Table 4 (0.075); fc not reported for standard sand 40 mesh")]
for nm, scol, slab, smax, fc, ts, eps, nt in t2:
    r = dict(P)
    r.update({"OPC / Cement": r4(936.7 / B), "FA (Fly ash)": r4(401.4 / B), "W / B": r4(361.3 / B), scol: r4(401.4 / B),
              "HRWR / B": r4(4 / B), "VMA / B": r4(1 / B), "Binder content (kg/m³)": r4(B),
              "PE fiber (vol%)": 2, "PE length (mm)": 18, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 2900, "PE elastic modulus (GPa)": 116,
              "Total fiber (vol%)": 2, "Curing method": "demoulded after 24 h, air curing under ambient laboratory conditions 28 d",
              "Curing time (days)": 28, "Demolding age (days)": 1, "Test age (days)": 28, "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80,
              "Tensile test type": DIRECT, "Tensile strength (MPa)": ts, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix, kg/m3), Table 2 (series), Table 4 (tensile), Table 8 (fc) , sect. 2.1-2.2",
              "Conversions / notes": f"{nm}: {slab}. kg/m3 / B (cement + FA = {r4(B)}); sand 401.4 kg/m3. Peak strain = Table 4 value x 100 ({nt}). "
                                     "Glass sand and acrylic sand mixes skipped. Curing temperature / RH not stated (ambient air)."})
    if smax:
        r["Sand max size (µm)"] = smax
    if fc is not None:
        r["Compressive strength (MPa)"] = fc
        r["Compressive specimen"] = "cube"
        r["Compressive specimen size (mm)"] = "40"
    rows.append(r)

# ---------- 3) Zhang et al. 2026: BA-ECC, reference B0-T25 (no bamboo aggregate, 25 C)
P = paper("Engineering properties of sustainable bamboo aggregate engineered cementitious composite (BA-ECC) at subzero temperatures",
          "Yuhang Zhang, Yang Wei, Binrong Zhu, Hang Yang, Mingmin Ding, Jiawei Chen", 2026, "10.1016/j.conbuildmat.2026.148277")
B = 350.0 + 353.3 + 66.7
r = dict(P)
r.update({"OPC / Cement": r4(350 / B), "FA (Fly ash)": r4(353.3 / B), "SF (Silica fume)": r4(66.7 / B), "W / B": r4(200 / B),
          "SS / B (Silica sand)": r4(200 / B), "HRWR / B": r4(5 / B), "HPMC / B (hydroxypropyl methyl cellulose)": r4(0.33 / B),
          "Binder content (kg/m³)": B, "PE fiber (vol%)": 2, "PE length (mm)": 9, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000,
          "PE elastic modulus (GPa)": 110, "Total fiber (vol%)": 2,
          "Curing method": "covered with film, demoulded after 24 h, standard curing 28 d", "Curing time (days)": 28, "Demolding age (days)": 1,
          "Test age (days)": 28, "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
          "First-cracking strength (MPa)": 2.77, "Tensile strength (MPa)": 5.89, "Tensile strain capacity (%)": 7.19,
          "Source table/page": "Table 4 (mix, kg/m3), Table 3 (PE), sect. 3.3.1 text (tensile)",
          "Conversions / notes": f"B0-T25 only (0 % bamboo aggregate, ambient 25 C reference). Other mixes (bamboo aggregate, subzero exposure) skipped. "
                                 f"kg/m3 / B (OPC + FA + SF = {B}). Quartz sand (QS) 200 kg/m3 used as sand. fc of B0-T25 only in Fig. 8 (not entered). "
                                 "VERIFY: curing temperature / RH 'standard conditions' not specified."})
rows.append(r)

# ---------- 4) Wang et al. 2025: thickener, PVA and PE ECC (fibre-free and steel / basalt rows not used)
P = paper("Study on the correlation between mobility and dispersion of different types of fibers in engineered cementitious composites (ECC)",
          "Xiao Wang, Haowen Jing, Ruonan Deng, Bin Meng, Xiaolin Huo", 2025, "10.1016/j.cscm.2025.e04272")
t4 = [("PVA", 0.0, 122.06), ("PVA", 0.1, 84.49), ("PVA", 0.2, 99.77), ("PVA", 0.3, 92.37),
      ("PE", 0.0, 82.86), ("PE", 0.1, 100.41), ("PE", 0.2, 82.26), ("PE", 0.3, 96.59)]
for ft, th, fc in t4:
    r = dict(P)
    r.update({"OPC / Cement": 0.5, "FA (Fly ash)": 0.4, "SF (Silica fume)": 0.1, "W / B": 0.20, "SS / B (Silica sand)": 0.36,
              "VMA / B": r4(th / 1000), "PVA fiber (vol%)" if ft == "PVA" else "PE fiber (vol%)": 2, "Total fiber (vol%)": 2,
              "Curing method": "natural curing 28 d", "Curing time (days)": 28, "Test age (days)": 28,
              "Compressive specimen": "prism half (40x40x160 mortar prism)", "Compressive specimen size (mm)": "40",
              "Compressive strength (MPa)": fc,
              "Source table/page": "Table 1 (binder %), note under Table 1 (w/c, s/c, fibre), Table 7 (28 d fc)",
              "Conversions / notes": f"ECC-{'A' if ft == 'PVA' else 'E'}-{int(th * 10)}: {ft} fibre 12 mm, thickener {th} permille. "
                                     "VERIFY: binder = cement 50 / FA 40 / SF 10 %; the 'water cement ratio 0.20' and 'sand cement ratio 0.36' taken as W/B and S/B; "
                                     "'fiber content 0.02' taken as 2 vol%; thickener (permille, taken as share of binder mass, type not stated) entered as VMA / B; "
                                     "SP dosage not given. Compressive test on 40x40x160 mm mortar-machine prisms (GB/T 17671 type). Steel / basalt / fibre-free rows skipped. "
                                     "Strength pattern irregular as published (e.g. PVA 0 permille 122 MPa)."})
    rows.append(r)

# ---------- 5) Kang et al. 2017: ECC-GGBS and ECC-FA (28 d air-cured cylinders)
P = paper("Experimental investigation on shear strength of engineered cementitious composites",
          "Shao-Bo Kang, Kang Hai Tan, Xu-Hong Zhou, Bo Yang", 2017, "10.1016/j.engstruct.2017.04.019")
for nm, c, scm, scmcol, w, s, fc in [("ECC-GGBS", 430, 1004, "GGBS", 387, 287, 59.8), ("ECC-FA", 391, 727, "FA (Fly ash)", 360, 504, 30.4)]:
    B = c + scm
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), scmcol: r4(scm / B), "W / B": r4(w / B), "Sand (type not stated) / B": r4(s / B),
              "Binder content (kg/m³)": B, "PVA fiber (vol%)": 2.0, "Total fiber (vol%)": 2.0,
              "Curing method": "air curing 28 d", "Curing time (days)": 28, "Test age (days)": 28,
              "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "150 x 300", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 1 (mix, kg/m3), Table 3 (fc), sect. 3.1",
              "Conversions / notes": f"{nm}. kg/m3 / B (cement + {scmcol.split(' ')[0]} = {B}). PVA 26 kg/m3 = 2.0 vol% (VERIFY: derived with density 1300). "
                                     "No superplasticizer listed. Tension / strain capacity not measured in uniaxial tension (only 4-point bending of plates). Concrete and mortar mixes skipped."})
    rows.append(r)

# ---------- 6) Li et al. 2018: cyclic constitutive model; ECC1 (moisture-cured 28 d)
P = paper("A modified cyclic constitutive model for engineered cementitious composites",
          "Xiaopeng Li, Xiaoyong Zhou, Ying Tian, Mo Li", 2018, "10.1016/j.engstruct.2018.09.030")
B = 292 + 935
r = dict(P)
r.update({"OPC / Cement": r4(292 / B), "FA (Fly ash)": r4(935 / B), "W / B": r4(312 / B), "Sand (type not stated) / B": r4(456 / B),
          "SP / B": r4(2.7 / B), "Binder content (kg/m³)": B, "PVA fiber (vol%)": 2.0, "Total fiber (vol%)": 2.0,
          "Curing method": "moisture curing until 28 d", "Curing time (days)": 28, "Test age (days)": 28,
          "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "102 x 203", "Tensile specimen": "coupon",
          "Tensile gauge length (mm)": 101.6, "Tensile test type": DIRECT, "Compressive strength (MPa)": 43,
          "First-cracking strength (MPa)": 4.2, "Tensile strength (MPa)": 4.5, "Tensile strain capacity (%)": 2.1,
          "Source table/page": "Table 1 (mix, kg/m3), Table 2 (ECC1 properties), sect. 2.5, 3",
          "Conversions / notes": f"ECC1. kg/m3 / B (cement + FA = {B}). PVA 26 kg/m3 = 2.0 vol% (VERIFY: derived with density 1300). "
                                 "VERIFY: ECC1 in Table 2 (w/b 0.25, FA/C 3.2, S/C 1.6) matches the Table 1 mix; tensile values come from cyclic-tension coupon tests "
                                 "(peak stress / strain of the envelope); fc of Table 2 (cylinders 102x203 are described in sect. 2.4). ECC2-ECC6 skipped (mix not in kg/m3 or from other papers)."})
rows.append(r)

# ---------- 7) Ding et al. 2021: HECC (PE + steel) bond paper, material properties
P = paper("Bond behavior and anchorage length of deformed bars in steel-polyethylene hybrid fiber engineered cementitious composites",
          "Yao Ding, Wei-Hao Mao, Wei Wei, Jie-Peng Liu, Y. Frank Chen", 2021, "10.1016/j.engstruct.2021.113675")
B = 465 + 543 + 112
r = dict(P)
r.update({"OPC / Cement": r4(465 / B), "Limestone powder": r4(543 / B), "SF (Silica fume)": r4(112 / B), "W / B": r4(194 / B),
          "Sand (type not stated) / B": r4(919 / B), "HRWR / B": r4(50 / B), "Binder content (kg/m³)": B,
          "PE fiber (vol%)": r4(10 / 970 * 100), "PE length (mm)": 18, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 2400, "PE elastic modulus (GPa)": 100,
          "Steel fiber (vol%)": r4(78 / 7850 * 100), "Steel length (mm)": 13, "Steel diameter (µm)": 220, "Steel tensile strength (MPa)": 2850, "Steel elastic modulus (GPa)": 210,
          "Total fiber (vol%)": r4(10 / 970 * 100 + 78 / 7850 * 100),
          "Curing method": "covered 24 h, demoulded, standard curing room 20 +/- 2 C, RH > 95 % for 28 d", "Curing time (days)": 28,
          "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28, "Tensile specimen": "dog-bone",
          "Tensile test type": DIRECT, "Compressive strength (MPa)": 70, "Tensile strength (MPa)": 6.8, "Tensile strain capacity (%)": 4.1,
          "Source table/page": "Table 2 (mix, kg/m3), Table 1 (fibres), Table 3 (properties), sect. 2.2",
          "Conversions / notes": f"HECC. kg/m3 / B (cement + LP + SF = {B}). Note under Table 2: w includes the water in HRWR (solid content 40 %); the 194 kg/m3 is the free water "
                                 "(194 + 0.6 x 50 = 224 = 0.2 x 1120 matches the stated w/b 0.2), W/B = 194 / 1120 entered. Sand = 'sand' (type not stated, s/b 0.82). "
                                 "PE 10 kg/m3 and steel 78 kg/m3 converted to vol% with 970 / 7850 kg/m3 (VERIFY, paper rounds to about 1 % + 1 %). "
                                 "VERIFY: age of the Table 3 property tests not stated explicitly (28 d curing before testing assumed)."})
rows.append(r)

# ---------- 8) Alraeeini and Nikbakht 2022: ECC of CFDST beams, 7 / 14 / 28 d fc, 28 d tensile strain
P = paper("Corrosion effect on the flexural behaviour of concrete filled steel tubulars with single and double skins using engineered cementitious composite",
          "Ahmed Saleh Alraeeini, Ehsan Nikbakht", 2022, "10.1016/j.istruc.2022.08.095")
B = 583 + 699.6
for age, fc in [(7, 42.5), (14, 47.6), (28, 51.2)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(583 / B), "FA (Fly ash)": r4(699.6 / B), "W / B": r4(298 / B), "Sand (type not stated) / B": r4(466.4 / B),
              "SP / B": r4(25.652 / B), "Binder content (kg/m³)": r4(B), "PVA fiber (vol%)": r4(19 / 1300 * 100),
              "PVA length (mm)": 18, "PVA diameter (µm)": 200, "PVA tensile strength (MPa)": 750, "PVA elastic modulus (GPa)": 27,
              "Total fiber (vol%)": r4(19 / 1300 * 100), "Curing time (days)": age, "Test age (days)": age, "Compressive strength (MPa)": fc,
              "Source table/page": "Table 2 (mix), Table 1 (PVA), sect. 3.1 text (fc 7/14/28 d, tensile strain 6.66 %)",
              "Conversions / notes": f"ECC used for the CFST tube fill. kg/m3 / B (cement + FA = {r4(B)}). PVA 19 kg/m3 -> vol% with 1300 kg/m3 (VERIFY derived). "
                                     "Curing method / temperature not stated. fc specimen shape not stated."})
    if age == 28:
        r.update({"Tensile specimen": "dog-bone", "Tensile test type": DIRECT, "Tensile strain capacity (%)": 6.66})
        r["Conversions / notes"] += " Tensile strain 6.66 % from JSCE dog-bone test 'after 28 d of curing' (sect. 2.1.1, 3.1); tensile strength not given."
    rows.append(r)

# ---------- 9) Zhang et al. 2025: EGC with dune sand (PE fibres), 28 d cube fc
P = paper("Compressive and flexural properties of engineered geopolymer composites incorporating dune sands",
          "Tianhe Zhang, Qinghe Wang, Qingxin Ren, Tong Li, Haoyue Sun, Ji-nan Ding", 2025, "10.1016/j.istruc.2025.109251")
txt = open(os.path.join(txt_dir, "ELS_10_1016_j_istruc_2025_109251.txt"), encoding="utf-8", errors="replace").read().splitlines()
mix, res = {}, {}
for ln in txt:
    m = re.match(r"^(EGC\S+)\t(.+)$", ln)
    if not m:
        continue
    f = m.group(2).split("\t")
    if len(f) == 10:
        mix[m.group(1)] = [float(x) for x in f]
    elif len(f) == 6:
        res[m.group(1)] = [float(x) for x in f]
assert len(mix) == 16 and len(res) == 16, (len(mix), len(res))
for key, (fa, gb, ss, ds, wg, wat, naoh, fib, hr, hp) in mix.items():
    fcu, fcp = res[key][1], res[key][2]
    B = fa + gb
    conc = re.findall(r"\d+", key)[0]
    r = dict(P)
    r.update({"GGBS": r4(gb / B), "FA (Fly ash)": r4(fa / B), "WG / B (Water glass)": r4(wg / B), "NaOH / B": r4(naoh / B),
              "Activator modulus Ms (SiO2/Na2O)": 2.23, "W / B": r4(wat / B), "Sand (type not stated) / B": r4(ss / B),
              "Dune sand / B": r4(ds / B), "HRWR / B": r4(hr / B), "HPMC / B (hydroxypropyl methyl cellulose)": r4(hp / B), "Binder content (kg/m³)": r4(B),
              "PE fiber (vol%)": 2, "PE length (mm)": 12, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 116,
              "Total fiber (vol%)": 2, "Curing method": "underwater (pH 12.5 NaOH solution) at 20 +/- 2 C for 28 d", "Curing time (days)": 28,
              "Curing temperature (°C)": 20, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
              "Compressive strength (MPa)": fcu,
              "Source table/page": "Table 3 (mix, kg/m3), Table 4 (fcu), Table 2 (PE), sect. 2.2-2.3",
              "Conversions / notes": f"{key}. kg/m3 / B (FA + GBFS = {r4(B)}). WG = sodium silicate solution (modulus 2.23, 14.34 % Na2O, 32 % SiO2); the Ms entered is "
                                     "that of the solution before the NaOH solution is added. W / B = free water (NaOH solution water, 'Water' column) only; water in the "
                                     f"silicate solution not added (paper total w/b 0.35). NaOH solution mass concentration {conc} %. 'SS' sand (type not stated) / dune sand (DS) "
                                     f"replacement by mass. fcu = 50 mm cube strength; prism / cylinder fc column (Table 4) = {fcp} MPa. Flexural properties not entered."})
    rows.append(r)

# ---------- 10) Liu et al. 2025: SRRPC (RPC) bond paper, RPC cubes
P = paper("Research on bond-slip behavior of I-shaped steel and reactive powder concrete",
          "Chang Liu, Tiangui Xu, Yangting Chen, Yuzhuo Wang, Yuming Zhang, Jinsheng Du", 2025, "10.1016/j.istruc.2025.109785")
B = 1 + 0.3 + 0.2 + 0.2
r = dict(P)
r.update({"OPC / Cement": r4(1 / B), "SF (Silica fume)": r4(0.3 / B), "GGBS": r4(0.2 / B), "FA (Fly ash)": r4(0.2 / B), "W / B": 0.2,
          "Sand (type not stated) / B": r4(1.2 / B), "SP / B": r4(0.1 / B), "Steel fiber (vol%)": 2, "Total fiber (vol%)": 2,
          "Curing method": "demoulded after 7 d, 50 C 24 h then 120 C 24 h (curing box), then left about one month", "Curing time (days)": 39,
          "Demolding age (days)": 7, "Test age (days)": 39, "Heat curing duration (h)": 48, "Compressive specimen": "cube",
          "Compressive specimen size (mm)": "150", "Compressive strength (MPa)": 123.6,
          "Source table/page": "sect. 2.2 (mix ratios), 2.3 (curing), Table 2 (fc, six cubes)",
          "Conversions / notes": f"RPC mass ratios cement : SF : slag : FA : fine sand : water reducer = 1 : 0.3 : 0.2 : 0.2 : 1.2 : 0.1, B = {B}; W/B 0.2 stated; steel fibre 2 vol%. "
                                 "VERIFY: test age derived as 7 d + 2 d heat + 'one month' (about 39 d), curing applied to the push-out specimens and assumed for the cubes; "
                                 "water reducer 0.1 per cement entered as SP / B = 0.1 / B (very high); fine sand type not stated; fibre dimensions not given."})
rows.append(r)

# ---------- 11) Alarrak et al. 2025: steel-fibre mortar (uniform 0.5 and 1 % cylinders)
P = paper("Flexural models exploration for functionally graded steel fiber-reinforced mortar considering fiber dosage and orientation",
          "Rashed Alarrak, Carin L. Roberts-Wollmann, Alexander S. Brand", 2025, "10.1016/j.istruc.2025.110697")
for vf, fc in [(0.5, 39.3), (1.0, 40.2)]:
    r = dict(P)
    r.update({"OPC / Cement": 1.0, "W / B": 0.40, "Sand (type not stated) / B": r4(1042 / 688), "Binder content (kg/m³)": 688,
              "Steel fiber (vol%)": vf, "Steel length (mm)": 30, "Steel diameter (µm)": 380, "Steel tensile strength (MPa)": 3070,
              "Total fiber (vol%)": vf, "Curing method": "moist curing 28 d", "Curing time (days)": 28, "Test age (days)": 28,
              "Compressive specimen": "cylinder", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 2 (mix), Table 3 (fibre), Table 4 (fc), sect. 2.3-2.4",
              "Conversions / notes": f"Mortar with Dramix steel fibre {vf} vol% (uniform dosage; 0 % skipped as no fibre). Type I cement 688, fine aggregate 1042 kg/m3 "
                                     "(max 4.75 mm, FM 2.6), w/c 0.40. Mean of three cylinders (Table 4). Cylinder size and temperature / RH not stated. No admixture listed."})
    rows.append(r)

# ---------- 12) Shen et al. 2025: lightweight EPS-ECC
P = paper("Tailoring sustainable lightweight insulating ECC for structural use via incorporating recycled expanded polystyrene: Microstructural and mechanical properties",
          "Qiang Shen, Chenyu Lu, Zhigang Zhang, Jamal A. Abdalla, Rami A. Hawileh, Xiaoyue Zhang", 2025, "10.1016/j.jclepro.2025.146867")
B = 1 + 0.8 + 0.16
# name, SS ratio, EPS ratio (to cement), SP ratio, fc, ts, strain, note
t12 = [("EPS0", 0.59, 0.0, 0.024, 83.9, 7.9, 3.5, "VERIFY: strain derived from 10.0 % / 2.85 (text: EPS100 strain is 2.85 times EPS0)"),
       ("EPS25", 0.44, 0.0025, 0.022, 45.4, None, 6.0, "VERIFY: EPS ratio printed 0.0245 in Table 1 (apparent typo; scaled from EPS50 0.0048 / EPS100 0.0099 -> 0.0025 used)"),
       ("EPS50", 0.30, 0.0048, 0.021, 43.7, None, 7.7, ""),
       ("EPS75", 0.15, 0.0072, 0.019, 39.9, None, 9.6, ""),
       ("EPS100", 0.0, 0.0099, 0.018, 27.8, 3.9, 10.0, "")]
for nm, ss, eps_r, sp, fc, ts, eps, nt in t12:
    r = dict(P)
    r.update({"OPC / Cement": r4(1 / B), "FA (Fly ash)": r4(0.8 / B), "SF (Silica fume)": r4(0.16 / B), "W / B": r4(0.39 / B),
              "SS / B (Silica sand)": r4(ss / B), "SP / B": r4(sp / B), "PE fiber (vol%)": 2, "PE length (mm)": 12, "PE diameter (µm)": 26,
              "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 120, "Total fiber (vol%)": 2,
              "Curing method": "demoulded after 24 h, air curing in laboratory 25 +/- 3 C, RH 50-60 % for 28 d", "Curing time (days)": 28,
              "Curing temperature (°C)": 25, "Curing RH (%)": 55, "Demolding age (days)": 1, "Test age (days)": 28, "Tensile specimen": "dog-bone",
              "Tensile test type": DIRECT, "Compressive strength (MPa)": fc, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix, weight ratios), sect. 2.1 (PE), 3.2 text (fc), 3.3 text (tensile)",
              "Conversions / notes": f"{nm}. Weight ratios to cement = 1; B = cement + ultra-fine FA + SF = {B}; ratios divided by B. EPS (2-4 mm) replaces silica sand by equal volume "
                                     f"({int(nm[3:])} %). Curing RH 50-60 % entered as 55. fc from text (Fig. 11), strain from text (Fig. 13). Tensile strength only stated for EPS0 and EPS100. "
                                     + nt})
    if eps_r:
        r["EPS / B"] = r4(eps_r / B)
    if ts is not None:
        r["Tensile strength (MPa)"] = ts
    rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e42.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows;", df["DOI / URL"].nunique(), "papers")

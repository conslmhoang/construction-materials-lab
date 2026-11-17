"""Wave 6, agent e37: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e37.csv (99-column TEMPLATE header)."""
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


# ---------- 138127 Zhang et al. 2024: MSFUHPC; only mix SP (steel + PE, no CNT/CSW/CF) at 25 C
P = paper("Revealing the role of multi-scale fibers in the compressive behavior of a novel ultra-high performance concrete subjected to elevated temperatures",
          "Yao Zhang, Zihan An, Yibo Chen, Weigang Zhao, Zhiguo Yan, Hehua Zhu", 2024, "10.1016/j.conbuildmat.2024.138127")
B = 1.5
r = dict(P)
r.update({"OPC / Cement": r4(1 / B), "FA (Fly ash)": r4(0.2 / B), "SF (Silica fume)": r4(0.3 / B), "W / B": r4(0.3 / B),
          "Sand (type not stated) / B": r4(0.93 / B), "SP / B": r4(0.01 / B), "PE fiber (vol%)": 1, "PE length (mm)": 12, "PE diameter (µm)": 31,
          "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 120, "Steel fiber (vol%)": 1, "Steel length (mm)": 13, "Steel diameter (µm)": 200,
          "Steel tensile strength (MPa)": 2850, "Steel elastic modulus (GPa)": 210, "Total fiber (vol%)": 2,
          "Curing method": "demoulded after 24 h, 28 d at RH >= 95 % and 20 +/- 2 C", "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95,
          "Demolding age (days)": 1, "Test age (days)": 28, "Compressive strength (MPa)": 123.15,
          "Source table/page": "Table 2 (mix, mass fractions to cement), Table 1 (fibres), Table 3 (fc at 25 C), sect. 2.2",
          "Conversions / notes": "Mix 'SP' only (1 vol% steel + 1 vol% PE; no CNT / CSW / carbon fibre / cenosphere). Mass fractions to cement = 1: sand 0.93, SF 0.3, FA 0.2, water 0.3, SP 0.01; "
                                 "B = cement + FA + SF = 1.5. 25 C value only (heated specimens skipped). VERIFY: test age taken as the stated 28 d curing; sand type not stated."})
rows.append(r)

# ---------- 139183 Ye et al. 2024: UHP-ECC with crumb rubber, quasi-static direct tension 28 d
P = paper("Dynamic splitting tensile properties of crumb rubber modified ultra-high performance engineered cementitious composites (UHP-ECC)",
          "Huzi Ye, Jinlong Pan, Binrong Zhu, Yuanzheng Lin, Jingming Cai", 2024, "10.1016/j.conbuildmat.2024.139183")
B = 1050 + 225 + 750 + 250
for nm, rs, cr, scr, ts, eps in [("PE-2%-R0", 750, 0, 6.95, 13.55, 3.37), ("PE-2%-R5", 722.5, 27.5, 6.10, 12.32, 4.96),
                                 ("PE-2%-R10", 695, 55, 3.96, 11.97, 8.05), ("PE-2%-R15", 667.5, 82.5, 3.72, 10.95, 6.03)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(1050 / B), "FA (Fly ash)": r4(225 / B), "GGBS": r4(750 / B), "SF (Silica fume)": r4(250 / B), "W / B": 0.18,
              "Sand (type not stated) / B": r4(rs / B), "HRWR / B": r4(33 / B), "Binder content (kg/m³)": B, "PE fiber (vol%)": 2, "PE length (mm)": 18,
              "PE diameter (µm)": 25, "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 140, "Total fiber (vol%)": 2,
              "Curing method": "demoulded after 1 d, 20 +/- 3 C and RH 60-80 % for 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 70,
              "Demolding age (days)": 1, "Test age (days)": 28, "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
              "First-cracking strength (MPa)": scr, "Tensile strength (MPa)": ts, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 2 (mix, kg/m3), Table 1 (PE), Table 3 (tensile), sect. 2.2, 3.1",
              "Conversions / notes": f"{nm}. kg/m3 / B (OPC + FA + GGBS + SF = {B}); W/B 0.18 as stated; sand = river sand (RS, 'RS' fine aggregate); CR replaces RS by volume. "
                                     "PE length 18 mm from aspect ratio 720 x 25 um (VERIFY). Curing RH 60-80 % entered as 70. Text quotes 3.12 % for R0 strain vs 3.37 % in Table 3 (table used)."})
    if cr:
        r["Crumb rubber / B"] = r4(cr / B)
    rows.append(r)

# ---------- 140884 Xie et al. 2025: engineered geopolymer composite, control CC0 (no CNT)
P = paper("Enhanced mechanical and thermal performance of high-strength engineered geopolymer composites reinforced by hybrid polyethylene fibres and carbon nanotubes",
          "Yuekai Xie et al.", 2025, "10.1016/j.conbuildmat.2025.140884")
r = dict(P)
r.update({"GGBS": 0.8, "FA (Fly ash)": 0.2, "WG / B (Water glass)": 0.30, "NaOH / B": 0.03, "W / B": 0.19, "Sand (type not stated) / B": 0.6, "SP / B": 0.01,
          "PE fiber (vol%)": 2, "PE length (mm)": 12, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 116, "Total fiber (vol%)": 2,
          "Curing method": "moulds, 23 +/- 2 C and RH 60 +/- 5 % for 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 23, "Curing RH (%)": 60,
          "Test age (days)": 28, "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 100, "Tensile test type": DIRECT,
          "First-cracking strength (MPa)": 3.66, "Tensile strength (MPa)": 6.27, "Tensile strain capacity (%)": 8.46,
          "Source table/page": "Table 2 (mix, weight ratios to precursor), sect. 2.1-2.4, 3.3.2 text",
          "Conversions / notes": "Control CC0 only (CNT mixes skipped). Weight ratios to precursor (GGBFS 0.8 + FA 0.2 = 1): natural sand 0.60, SH (8 M NaOH solution) 0.12, WG 0.30 (44.1 % solids, Ms 2.05), added water 0.10, SP 0.01. "
                                 "VERIFY: NaOH / B = 0.12 x ~25 % (8 M solution, assumed density ~1.25) = 0.03 and its ~0.09 water added to W/B (0.10 + 0.09 = 0.19). Compressive strength of CC0 only in Fig. 5 (not entered)."})
rows.append(r)

# ---------- 142584 LC3 / desert sand ECC: OPC-based mixes MS150, MS300, DS150, DS300 (LC3 mixes contain gypsum -> skipped)
P = paper("Engineered cementitious composites (ECC) with limestone calcined clay cement (LC3) and desert sand: Mechanical properties, microstructures and carbon footprint",
          "Guoqi Han, Qing Chen, Yao Zhang, Zhenxiao Bi, Kai Cao, Yonggang Wang, Qian Zhang", 2025, "10.1016/j.conbuildmat.2025.142584")
B = 490 + 735
for nm, sandcol, size, fc, scr, ts in [("MS150", "M-sand / B", "0-150", 43.6, 3.58, 6.38), ("MS300", "M-sand / B", "150-300", 43.7, 3.54, 5.79),
                                       ("DS150", "Dune sand / B", "0-150", 45.7, 3.47, 5.46), ("DS300", "Dune sand / B", "150-300", 44.2, 3.03, 5.24)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(490 / B), "FA (Fly ash)": r4(735 / B), "W / B": r4(343 / B), sandcol: r4(429 / B), "HRWR / B": r4(3.7 / B), "VMA / B": r4(1.2 / B),
              "Binder content (kg/m³)": B, "PE fiber (vol%)": r4(18 / 970 * 100), "PE length (mm)": 18, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 2900,
              "Total fiber (vol%)": r4(18 / 970 * 100),
              "Curing method": "sealed 24 h, demoulded, curing chamber 20 +/- 2 C, RH 95 % until test", "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95,
              "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7",
              "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
              "Compressive strength (MPa)": fc, "First-cracking strength (MPa)": scr, "Tensile strength (MPa)": ts,
              "Source table/page": "Table 3 (mix, kg/m3), fibre table, sect. 3 text (fc 28 d, first-crack, ultimate strength)",
              "Conversions / notes": f"{nm} (sand {size} um; {'manufactured sand' if nm[0]=='M' else 'desert sand'}). kg/m3 / B (OPC + FA = {B}). PE 18 kg/m3 -> {r4(18/970*100)} vol% with density 0.97 (VERIFY derived). "
                                     "VERIFY: tensile test age not stated (taken as 28 d, same as fc). Tensile strain capacity of OPC mixes not stated numerically (only +27 % / +40 % relative to LC3 mixes), left empty. LC3 mixes skipped (gypsum)."})
    rows.append(r)

# ---------- 142906 Shen et al. 2025: high-strength PE-ECC with expanded vermiculite; reference EV0 only
P = paper("Incorporating expanded vermiculites into high strength ECC: Improving its tensile properties and autogenous self-healing behavior",
          "Qiang Shen, Zhigang Zhang, Xiaoyue Zhang, Jamal A. Abdalla, Rami A. Hawileh", 2025, "10.1016/j.conbuildmat.2025.142906")
B = 1.96
r = dict(P)
r.update({"OPC / Cement": r4(1 / B), "FA (Fly ash)": r4(0.8 / B), "SF (Silica fume)": r4(0.16 / B), "W / B": 0.2, "SS / B (Silica sand)": 0.3, "SP / B": r4(0.024 / B),
          "PE fiber (vol%)": 2, "PE length (mm)": 12, "PE diameter (µm)": 26, "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 120, "Total fiber (vol%)": 2,
          "Curing method": "demoulded after 24 h, 25 +/- 3 C and RH 50-60 % for 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 25, "Curing RH (%)": 55,
          "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube", "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80,
          "Tensile test type": DIRECT, "Compressive strength (MPa)": 85.7, "First-cracking strength (MPa)": 5.53, "Tensile strength (MPa)": 7.87, "Tensile strain capacity (%)": 2.53,
          "Source table/page": "Table 1 (mix, weight ratios), sect. 2.1 / 3.2 / 3.3 text (EV0)",
          "Conversions / notes": "Reference mix EV0 only (expanded vermiculite mixes skipped). Weight ratios C 1 : FA 0.8 : SF 0.16 (B = 1.96); SS 0.59 / 1.96 = 0.3, W 0.39 / 1.96 = 0.2, SP 0.024 / 1.96. Curing RH 50-60 % entered as 55."})
rows.append(r)

# ---------- 143871 Bai et al. 2025: 3D graphene UHDC, control M0 (no graphene); tensile only (fc only in a figure)
P = paper("Effect of 3D porous graphene on the mechanical properties and microstructure of ultra-high ductility concrete",
          "Meiyan Bai, Long Song, Feng Xie, Zhenyuan Lv, Haoran Liu et al.", 2025, "10.1016/j.conbuildmat.2025.143871")
B = 656 + 118 + 604
r = dict(P)
r.update({"OPC / Cement": r4(656 / B), "SF (Silica fume)": r4(118 / B), "FA (Fly ash)": r4(604 / B), "W / B": r4(363 / B), "Fine sand / B": r4(410 / B), "SP / B": r4(2 / B),
          "Binder content (kg/m³)": B, "PE fiber (vol%)": 1.5, "PE length (mm)": 12, "PE diameter (µm)": 24, "Total fiber (vol%)": 1.5,
          "Curing method": "sealed with film, 25 C 24 h, then standard curing chamber 25 C / 95 % RH for 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 25, "Curing RH (%)": 95,
          "Demolding age (days)": 1, "Test age (days)": 28, "Tensile test type": DIRECT, "First-cracking strength (MPa)": 2.41, "Tensile strength (MPa)": 8.56, "Tensile strain capacity (%)": 4.00,
          "Source table/page": "Table 2 (mix, kg/m3), Table 4 (tensile, peak stress / peak strain), sect. 2.1-2.2",
          "Conversions / notes": f"Control M0 only (graphene mixes skipped). kg/m3 / B (cement + SF + FA = {B}); 'FS' read as fine sand (type not stated); PE 15 kg/m3 ~ 1.5 vol% as stated in text. "
                                 "Peak stress / peak strain of Table 4 used (ultimate strain 5.03 %, ultimate stress 6.17 MPa also given). VERIFY: peak strain unit assumed % (initial-crack strain given as 0.0024 absolute); "
                                 "test age taken as 28 d curing (+1 d pre-cure); fc of M0 only in Fig. 4, not entered."})
rows.append(r)

# ---------- 146542 Yu et al. 2026: HS-ECC with PE (reference tensile at 28 d)
P = paper("Role of moisture content in governing elevated-temperature spalling of high-strength engineered cementitious composites",
          "Jianqiao Yu, Zhigang Zhang et al.", 2026, "10.1016/j.conbuildmat.2026.146542")
B = 717 + 574 + 115
r = dict(P)
r.update({"OPC / Cement": r4(717 / B), "FA (Fly ash)": r4(574 / B), "SF (Silica fume)": r4(115 / B), "W / B": r4(281 / B), "SS / B (Silica sand)": r4(422 / B), "SP / B": r4(20 / B),
          "Binder content (kg/m³)": B, "PE fiber (vol%)": 2.0, "PE length (mm)": 12, "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 100, "Total fiber (vol%)": 2.0,
          "Curing method": "covered 24 h, demoulded, ~25 C and 55 % RH until test", "Curing time (days)": 28, "Curing temperature (°C)": 25, "Curing RH (%)": 55, "Demolding age (days)": 1,
          "Test age (days)": 28, "Tensile specimen": "dog-bone", "Tensile test type": DIRECT, "First-cracking strength (MPa)": 4.95, "Tensile strength (MPa)": 8.26, "Tensile strain capacity (%)": 5.16,
          "Source table/page": "Table 2 (mix, kg/m3), Table 3 (tensile), sect. 2.1-2.2",
          "Conversions / notes": f"kg/m3 / B (C + FA + SF = {B}); W/B 0.2 as stated. PE 2.0 vol% as stated (19.4 kg/m3). fc not entered: 25 C compressive values (92.6-98.5 MPa) belong to moisture-conditioned (dried / re-wetted) specimens."})
rows.append(r)

# ---------- dibe 2023.100212 Zhu et al.: UHPC, reference R0A0 only (no recycled mixed powder, river sand only), 28 d
P = paper("Feasibility analysis of treating aeolian sand and recycled mixed powder as environmentally friendly materials in the ultra-high-performance concrete",
          "Chao Zhu, Teng Yi, Xin Lin, Guoliang Bai, Chao Liu", 2023, "10.1016/j.dibe.2023.100212")
B = 595 + 85 + 170
r = dict(P)
r.update({"OPC / Cement": r4(595 / B), "SF (Silica fume)": r4(85 / B), "FA (Fly ash)": r4(170 / B), "W / B": r4(136 / B), "River sand / B": r4(850 / B), "SP / B": r4(21.25 / B),
          "Binder content (kg/m³)": B, "Steel fiber (vol%)": 2.5, "Steel length (mm)": 13, "Steel diameter (µm)": 220, "Total fiber (vol%)": 2.5,
          "Curing method": "24 h standard curing 20 C / 95 % RH; steam 40 C 24 h; steam 70 C 48 h (85 % RH); then standard curing room 24 d", "Curing time (days)": 28,
          "Curing temperature (°C)": 70, "Curing RH (%)": 85, "Heat curing duration (h)": 72, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100",
          "Compressive strength (MPa)": 120.35, "Source table/page": "Table 3 (mix, kg/m3), sect. 2.3.2 (curing), 3.x text (fc of R0A0)",
          "Conversions / notes": f"Reference R0A0 only (aeolian sand and recycled mixed powder mixes skipped). kg/m3 / B (cement + SF + ultra-fine fly ash = {B}); SP 21.25 kg/m3 as dosed (40 % solids). "
                                 "VERIFY: steel fibre '2.5 %' assumed vol%; test age 28 d taken from text 'curing ages of 28 days' although the schedule (3 d steam + 24 d) is ~28 d after casting. 3 d / 7 d values (75.21 / 99.28 MPa) not entered (age unclear with steam curing)."})
rows.append(r)

# ---------- engstruct 2025.119856: UHPFRC with 1.5 / 2.0 / 2.5 vol% steel, fc of 100 mm cubes (hot-water cured)
P = paper("Failure criteria and stress-strain constitutive envelope surfaces for UHPFRC with different volume fractions of steel fibers under triaxial compression",
          "Lu Ke, Bin Han, Zheng Chen, Zheng Feng, Jianan Qi, Doo-Yeol Yoo", 2025, "10.1016/j.engstruct.2025.119856")
B = 1140 + 627
for vf, fc in [(1.5, 146.57), (2.0, 159.07), (2.5, 153.03)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(1140 / B), "SF (Silica fume)": r4(627 / B), "W / B": r4(250.8 / B), "M-sand / B": r4(1254 / B), "SP / B": r4(48 / B), "Binder content (kg/m³)": B,
              "Steel fiber (vol%)": vf, "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2450, "Steel elastic modulus (GPa)": 210, "Total fiber (vol%)": vf,
              "Curing method": "24 h room temperature, demoulded, hot water 90 +/- 3 C for 48 h", "Curing time (days)": 3, "Curing temperature (°C)": 90, "Curing RH (%)": 100,
              "Demolding age (days)": 1, "Heat curing duration (h)": 48, "Test age (days)": 3, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100",
              "Compressive strength (MPa)": fc, "Source table/page": "Table 1 (mix, kg/m3), Table 2 (fibre), Table 3 (fc), sect. 2.1-2.2",
              "Conversions / notes": f"UHPFRC steel {vf} vol%. kg/m3 / B (cement + SF = {B}); machine-made sand 0.2-1.25 mm. VERIFY: test age not stated, derived as 24 h + 48 h hot-water curing = 3 d. "
                                     "Table 3 'tensile strength' not entered (test type not described)."})
    rows.append(r)

# ---------- ijimpeng 2009 Rong, Sun, Zhang: UHPCC, steel 3 / 4 vol%, static fc (text and Table 2)
P = paper("Dynamic compression behavior of ultra-high performance cement based composites",
          "Zhidan Rong, Wei Sun, Yunsheng Zhang", 2009, "10.1016/j.ijimpeng.2009.11.005")
B = 400 + 100 + 250 + 250
for vf, age, fc, src in [(3, 28, 170.3, "text sect. 3.1"), (3, 60, 186, "Table 2"), (3, 90, 202.5, "text sect. 3.1"), (3, 180, 212.4, "text sect. 3.1"), (4, 60, 204, "Table 2")]:
    r = dict(P)
    r.update({"OPC / Cement": r4(400 / B), "SF (Silica fume)": r4(100 / B), "FA (Fly ash)": r4(250 / B), "GGBS": r4(250 / B), "W / B": 0.15, "Sand (type not stated) / B": 1.2,
              "SP / B": r4(20 / B), "Binder content (kg/m³)": B, "Steel fiber (vol%)": vf, "Total fiber (vol%)": vf,
              "Curing method": "demoulded after 24 h, standard curing 20 C, RH > 95 % to test age", "Curing time (days)": age, "Curing temperature (°C)": 20, "Curing RH (%)": 95,
              "Demolding age (days)": 1, "Test age (days)": age, "Compressive specimen": "prism half (40 x 40 x 80 mm)", "Compressive strength (MPa)": fc,
              "Source table/page": f"Table 1 (mix, kg/m3), {src}",
              "Conversions / notes": f"UHPCC(V{vf}). kg/m3 / B (cement + SF + ultra-fine FA + ultra-fine slag = {B}); sand natural, max 2.5 mm; W/B 0.15 and sand/binder 1.2 as stated. Steel fibre 'Vf' 234 / 312 kg/m3 = 3 / 4 vol%. "
                                     "Fibre dimensions not given in the extract. V0 (no fibre) skipped. Same-batch ages 28 / 90 / 180 d for V3 read from text of sect. 3.1."})
    rows.append(r)

# ---------- jclepro 2022.130507 Shao et al.: steel-fibre dry-cast UHPC (FR-DUHPC), fc at 1/3, 7, 28 d under 6 curing regimes
P = paper("Development of sustainable steel fibre-reinforced dry ultra-high performance concrete (DUHPC)",
          "Ruizhe Shao, Chengqing Wu, Jun Li, Zhongxian Liu", 2022, "10.1016/j.jclepro.2022.130507")
B = 1 + 0.15 + 0.31 + 0.08
T14 = {0.5: [(72.8, 98.4, 110.8), (52.9, 84.4, 107.7), (69.4, 90.6, 106.5), (86.9, 95.9, 102.6), (93.8, 102.6, 105.8), (109.9, 117.2, 120.4)],
       1.0: [(94.6, 117.5, 139.3), (64.4, 94.1, 140.9), (77.9, 98.4, 135.3), (89.3, 104.1, 133.7), (102.9, 115.6, 130.4), (120.7, 133.9, 141.9)],
       1.5: [(110.5, 128.1, 162.6), (70.7, 108.6, 152.9), (98.8, 120.9, 144.4), (124.8, 132.0, 144.6), (129.7, 141.1, 147.0), (146.3, 155.6, 163.3)],
       2.0: []}
T14[2.0] = [(115.2, 125.3, 168.9), (78.9, 121.2, 163.7), (123.1, 137.8, 167.7), (129.3, 142.4, 159.3), (135.6, 139.3, 154.6), (150.3, 159.5, 167.6)]
regimes = [("W20", 20, "24 h humid room 20 C, demoulded, then 20 C water", None, 3, 0),
           ("M30", 30, "24 h moist/steam 30 C in insulated container, demoulded, then 20 C water", 30, 1, 24),
           ("M40", 40, "24 h moist/steam 40 C in insulated container, demoulded, then 20 C water", 40, 1, 24),
           ("M50", 50, "24 h moist/steam 50 C in insulated container, demoulded, then 20 C water", 50, 1, 24),
           ("M60", 60, "24 h moist/steam 60 C in insulated container, demoulded, then 20 C water", 60, 1, 24),
           ("H90", 90, "24 h humid room 20 C, demoulded, 24 h hot-water bath 90 C, then 20 C water", 90, 3, 24)]
for vf, vals in T14.items():
    for (nm, tmp, cur, heat, age0, hh), fcs in zip(regimes, vals):
        for age, fc in zip((age0, 7, 28), fcs):
            r = dict(P)
            r.update({"OPC / Cement": r4(1 / B), "SF (Silica fume)": r4(0.15 / B), "FA (Fly ash)": r4(0.31 / B), "GGBS": r4(0.08 / B), "W / B": r4(0.25 / B),
                      "SS / B (Silica sand)": r4(2.84 / B), "SP / B": r4(0.03 / B), "Steel fiber (vol%)": vf, "Steel length (mm)": 10, "Steel diameter (µm)": 120,
                      "Steel tensile strength (MPa)": 4000, "Total fiber (vol%)": vf, "Curing method": cur, "Curing time (days)": age,
                      "Curing temperature (°C)": heat if heat else 20, "Demolding age (days)": 1, "Test age (days)": age, "Compressive strength (MPa)": fc,
                      "Source table/page": "Sect. 5.2 (mass ratios), Table 14 (fc), sect. 3.1, 4.2",
                      "Conversions / notes": f"{nm}, steel {vf} vol%. Mass ratios C 1 : SF 0.15 : FA 0.31 : GGBS 0.08 : quartz sand (0.12-1.18 mm) 2.84 : W 0.25 : SP 0.03 (B = {r4(B)}); dry-cast mixture. "
                                             "Steel fibre 0.12 mm dia, L/D 83.3 (10 mm), > 4000 MPa. Test age 1 d for M regimes, 3 d for W20 / H90 (Table 14 headers 1/3-day). "
                                             "Split tensile and flexural strengths not entered. VERIFY: composite Portland cement 42.5 treated as cement; specimen size not extracted."})
            if heat and hh:
                r["Heat curing duration (h)"] = hh
            rows.append(r)

# ---------- jclepro 2017.06.137 Mohammed et al.: SC-ECC, PVA 0.5 / 1 / 1.5 / 2 vol%, nano-silica 0 (control) mixes only
P = paper("Properties of nano-silica-modified self-compacting engineered cementitious composites",
          "Bashar S. Mohammed, Bitrus Emmanuel Achara, Muhd Fadhil Nuruddin, Melvin Yaw, Mohd. Z. Zulkefli", 2017, "10.1016/j.jclepro.2017.06.137")
B = 583 + 700
for vf, mid, sp, fc in [(0.5, "M1", 0.74, 70.98), (1.0, "M2", 0.82, 76.86), (1.5, "M3", 0.89, 85.87), (2.0, "M4", 0.99, 97.57)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(583 / B), "FA (Fly ash)": r4(700 / B), "W / B": r4(187 / B), "River sand / B": r4(467 / B), "HRWR / B": sp / 100,
              "Binder content (kg/m³)": B, "PVA fiber (vol%)": vf, "Total fiber (vol%)": vf,
              "Curing method": "demoulded after 24 h, curing tank 23 +/- 2 C, RH ~80 % until test at 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 23, "Curing RH (%)": 80,
              "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 4 (mix, kg/m3), Table 9 (RSM runs, measured fc), sect. 2 (curing)",
              "Conversions / notes": f"{mid}: PVA {vf} vol%, no nano-silica (NS mixes skipped). kg/m3 / B (cement + FA = {B}); river sand 450 um. HRWR {sp} % of cementitious. "
                                     "fc from Table 9 (RSM experimental matrix, NS = 0 runs). PVA fibre dimensions not extracted. VERIFY: Table 9 values used as measured fc (Fig. 1 holds the bars)."})
    rows.append(r)

# ---------- engstruct 2019.109424 (HDC overlay material properties)
P = paper("Shaking table tests of a half-scale 2-storey URM building retrofitted with a high ductility fibre reinforced concrete overlay system",
          "Mingke Deng, Zhifang Dong, Xuesong Wang, Yangxi Zhang, Tiegang Zhou", 2019, "10.1016/j.engstruct.2019.109424")
r = dict(P)
r.update({"OPC / Cement": 0.5, "FA (Fly ash)": 0.5, "W / B": 0.29, "Sand (type not stated) / B": 0.36, "PVA fiber (vol%)": 2, "PVA length (mm)": 12, "PVA diameter (µm)": 39,
          "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 32, "Total fiber (vol%)": 2, "Curing method": "not described (28 d test age stated)", "Curing time (days)": 28,
          "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100", "Tensile specimen": "plate (15 mm thick)", "Tensile test type": DIRECT,
          "Compressive strength (MPa)": 61.15, "Tensile strength (MPa)": 5.83, "Tensile strain capacity (%)": 1.0,
          "Source table/page": "Sect. 2.3.1 (mix ratio 1:1:0.72:0.58, fc, tensile), Table 2 (PVA), Table 3",
          "Conversions / notes": "HDC mass ratio cement : fly ash : sand : water = 1 : 1 : 0.72 : 0.58 (B = 2). HRWR 8 kg/m3 not entered (binder content in kg/m3 not given). "
                                 "VERIFY: tensile test described as 15-mm-thick plates per DBJ61/T112-2016 (taken as direct tension); strain 'reached 1.0 %' from text (stress-strain curve in Fig. 6); curing conditions not stated."})
rows.append(r)

# ---------- 146439 GO-modified HVFA-ECC: reference mixes REF-0.8 and REF-1.4 (no graphene oxide)
P = paper("Enhancing mechanical and self-healing properties of high volume-fly ash-ECC via graphene oxide modification",
          "Weizhe Wu, Rami A. Hawileh, Jamal A. Abdalla, Zhigang Zhang", 2026, "10.1016/j.conbuildmat.2026.146439")
B = 717 + 574 + 115
for nm, c, fa, fc, scr, eps in [("REF-0.8", 717, 574, 76.76, 4.48, None), ("REF-1.4", 538, 753, 63.69, None, 8.4)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "SF (Silica fume)": r4(115 / B), "W / B": r4(281 / B), "SS / B (Silica sand)": r4(422 / B), "SP / B": r4(20 / B),
              "Binder content (kg/m³)": B, "PE fiber (vol%)": r4(20 / 970 * 100), "Total fiber (vol%)": r4(20 / 970 * 100),
              "Curing method": "demoulded after 24 h, cured at room temperature until test", "Curing time (days)": 28, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive strength (MPa)": fc, "Tensile test type": DIRECT, "Source table/page": "Table 2 (mix, g/L), sect. 3.2 / 3.x text, conclusions",
              "Conversions / notes": f"{nm} (FA/C = {fa/c:.2f}, no GO; GO mixes skipped). g/L / B (C + FA + SF = {B}); fibre '20' (g/L, 0 for matrix specimens) read as PE 20 kg/m3 = {r4(20/970*100)} vol% with 970 kg/m3 (VERIFY derived; fibre type 'PE', properties not extracted). "
                                     "fc = 28-d value quoted in text (Fig. 4). Tensile test: 1 mm/min with two gauges (direct tension). Room temperature / RH not stated."})
    if scr:
        r["First-cracking strength (MPa)"] = scr
    if eps:
        r["Tensile strain capacity (%)"] = eps
        r["Conversions / notes"] += " Strain 8.4 % quoted in the conclusions for the control of FA/C-1.4."
    rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e37.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows;", df["DOI / URL"].nunique(), "papers")

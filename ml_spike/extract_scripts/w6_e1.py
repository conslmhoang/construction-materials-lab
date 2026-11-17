"""Wave 6, agent e1: rows from Elsevier full-text dumps (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e1.csv (99-column TEMPLATE header). All numbers are from text/tables, none from figures.
Papers: 105347 (1 row), 106064 (10), 106068 (5), 106248 (4), 106576 (2), 106600 (5), 106647 (1).
"""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
add = os.path.join(here, "..", "additions")
out_dir = os.path.join(here, "..", "additions_v2")
cols = list(pd.read_csv(os.path.join(add, "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
rows = []


def paper(name, author, year, doi):
    return {"Article Name": name, "Author": author, "Year": year, "DOI / URL": "https://doi.org/" + doi}


# ---- 1) 105347 (reference mix FS0.27 only)
P = paper("Using special coarse aggregate to enhance the tensile strain capacity of engineered cementitious composites",
          "Zhifu Dong, Hailong Tan, Jiangtao Yu, Fangming Jiang", 2023, "10.1016/j.cemconcomp.2023.105347")
B = 649 + 779
r = dict(P)
r.update({"OPC / Cement": round(649 / B, 4), "FA (Fly ash)": round(779 / B, 4), "W / B": round(342 / B, 4),
          "SS / B (Silica sand)": round(286 / B, 4), "SP / B": round(4 / B, 4), "Binder content (kg/m³)": B,
          "PE fiber (vol%)": 1.5, "PE length (mm)": 18, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000,
          "PE elastic modulus (GPa)": 100, "Total fiber (vol%)": 1.5,
          "Curing method": "demolded after 1 d, then room temperature (no further detail)", "Curing time (days)": 28,
          "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube",
          "Compressive specimen size (mm)": "100", "Tensile specimen": "dog-bone", "Tensile test type": "direct (uniaxial)",
          "Tensile strength (MPa)": 6.73, "Tensile strain capacity (%)": 5.00,
          "Source table/page": "Table 2 (mix, FS0.27), Table 4 (strain), text 3.3 (ft)",
          "Conversions / notes": "Only reference mix FS0.27 (the CA-ECC mixes contain fly-ash coarse aggregate: excluded). kg/m3 / (649+779). "
                                 "Fiber 15.6 kg/m3 given as 1.5 vol% in text (15.6/970 = 1.6). Text says w/b 21 % but Table 2 gives 342/1428 = 0.24 (used table). "
                                 "VERIFY: fc of FS0.27 only in Fig. 4b (not entered); sand = silica sand (max 0.27 mm)."})
rows.append(r)

# ---- 2) 106064 UHPGC steel fiber hybrids
P = paper("Influence of steel fiber hybridization on the static mechanical performance of ultra-high performance geopolymer concrete (UHPGC)",
          "Yiwei Liu, Yanan Ren, Qi Li, Caijun Shi", 2025, "10.1016/j.cemconcomp.2025.106064")
B = 508 + 127 + 270
# id, (SS, SM, SL) vol%, first-crack MPa, ultimate strain %, ultimate strength MPa
m = [("A", (0, 0, 2), 3.46, 0.1183, 5.98), ("B", (1, 0, 1), 3.27, 0.1208, 5.78), ("C", (2, 0, 0), 1.84, 0.0769, 4.77),
     ("D", (1, 1, 0), 2.74, 0.0748, 4.90), ("E", (0, 2, 0), 3.54, 0.1870, 6.69), ("F", (0, 1, 1), 3.34, 0.2701, 5.98),
     ("G", (.67, .67, .67), 3.64, 0.1318, 6.33), ("H", (.33, 1.34, .33), 3.75, 0.0822, 5.18),
     ("I", (.33, .33, 1.34), 4.05, 0.1260, 6.55), ("J", (1.34, .33, .33), 2.95, 0.1153, 5.51)]
geo = {0: (6, 120), 1: (8, 120), 2: (13, 120)}
for mid, v, fcr, eps, ft in m:
    r = dict(P)
    single = [i for i in range(3) if v[i] == 2]
    r.update({"GGBS": round(508 / B, 4), "FA (Fly ash)": round(127 / B, 4), "SF (Silica fume)": round(270 / B, 4),
              "NaOH / B": round(45 / B, 4), "WG / B (Water glass)": round(314 / B, 4), "W / B": round(87 / B, 4),
              "River sand / B": round(905 / B, 4), "Binder content (kg/m³)": B, "Steel fiber (vol%)": 2.0,
              "Steel tensile strength (MPa)": 2500, "Total fiber (vol%)": 2.0,
              "Curing method": "covered 24 h at 20 C 65 % RH, demolded, steam chamber 80 C 24 h", "Curing time (days)": 2,
              "Curing temperature (°C)": 80, "Demolding age (days)": 1, "Heat curing duration (h)": 24,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "100", "Tensile specimen": "dog-bone",
              "Tensile gauge length (mm)": 150, "Tensile test type": "direct (uniaxial)",
              "Tensile strength (MPa)": ft, "First-cracking strength (MPa)": fcr, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 3 (mix), Table 5 (tension), Table 2 (fibers)",
              "Conversions / notes": f"Mix {mid} = SS {v[0]} % + SM {v[1]} % + SL {v[2]} % straight steel fibers (6/8/13 mm x 0.12 mm). "
                                     "kg/m3 / 905. Water glass 8.35 % Na2O, 27.15 % SiO2, 64.5 % H2O (its water NOT in W/B: paper w/b = 0.32 incl. it, "
                                     "so W/B here is only 0.096). No SP. Strain = 'ultimate tensile strain' (strain at peak) from Table 5, tiny (<0.3 %). "
                                     "Test age not stated (after steam curing). VERIFY: fc only in Fig. 8 (not entered)."})
    if len(single) == 1:
        r["Steel length (mm)"], r["Steel diameter (µm)"] = geo[single[0]]
    rows.append(r)

# ---- 3) 106068 PVA-SHCC flowability
P = paper("Fiber distribution in strain-hardening cementitious composites (SHCC): Experimental investigation and its correlation with matrix flowability and tensile strength",
          "Zhenghao Li, Jiajia Zhou, Christopher K.Y. Leung", 2025, "10.1016/j.cemconcomp.2025.106068")
m = [("T19", 0.00500, 3.13, 5.00), ("T23", 0.00450, 4.18, 5.03), ("T30", 0.00400, 5.07, 5.53), ("T37", 0.00372, 4.11, 5.25),
     ("T48", 0.00360, 2.87, 5.51)]
for mid, sp, eps, ft in m:
    r = dict(P)
    r.update({"OPC / Cement": 0.2, "FA (Fly ash)": 0.8, "W / B": 0.22, "Sand (type not stated) / B": 0.20,
              "Sand max size (µm)": 180, "SP / B": sp, "PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 39,
              "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 42, "Total fiber (vol%)": 2.0,
              "Curing method": "standard curing", "Curing time (days)": 28, "Test age (days)": 28,
              "Tensile specimen": "dumbbell (JSCE)", "Tensile gauge length (mm)": 80, "Tensile test type": "direct (uniaxial)",
              "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix), Table 2 (fiber), Table 3 (results)",
              "Conversions / notes": f"{mid} (Marsh-cone flow time of matrix). Mix ratios by weight; sand 125-180 um. Table 1 lists T47, Table 3 T48 (same mix, typo). "
                                     "No compressive data in paper."})
    rows.append(r)

# ---- 4) 106248 ECC filler effect (slag-filled mixes only; quartz-filled excluded)
P = paper("Breaking strength-ductility trade-off dilemma for Engineered Cementitious Composites (ECC) through filler effect",
          "Junsheng Li, Victor C. Li, Duo Zhang", 2025, "10.1016/j.cemconcomp.2025.106248")
m = [("S15", 0.29, 0.64, 0.006, 0.004, 32.33, 3.29, 5.76, 7.42), ("S20", 0.39, 0.60, 0.009, 0.002, 41.86, 3.94, 5.82, 4.98),
     ("S25", 0.49, 0.56, 0.013, 0.0, 52.68, 4.14, 6.55, 3.60), ("S30", 0.59, 0.52, 0.019, 0.0, 56.73, 4.98, 6.97, 2.97)]
for mid, sl, w, hr, vma, fcm, fcr, ft, eps in m:
    B = 1 + 0.875 + sl
    r = dict(P)
    r.update({"OPC / Cement": round(1 / B, 4), "FA (Fly ash)": round(0.875 / B, 4), "GGBS": round(sl / B, 4),
              "W / B": round(w / B, 4), "HRWR / B": round(hr / B, 5), "VMA / B": round(vma / B, 5) if vma else None,
              "PE fiber (vol%)": 2.0, "PE length (mm)": 12, "PE diameter (µm)": 22, "PE tensile strength (MPa)": 3360,
              "PE elastic modulus (GPa)": 115, "Total fiber (vol%)": 2.0,
              "Curing method": "demolded after 24 h, then cured (conditions not stated)", "Curing time (days)": 28,
              "Demolding age (days)": 1, "Test age (days)": 28, "Tensile specimen": "dog-bone (JSCE)",
              "Tensile gauge length (mm)": 80, "Tensile test type": "direct (uniaxial)",
              "Tensile strength (MPa)": ft, "First-cracking strength (MPa)": fcr, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 3 (mix), Table 5 (tension), Table 2 (fiber)",
              "Conversions / notes": f"Slag-filled ECC {mid}; mass ratios per OPC = 1 re-divided by B = OPC + FA + slag = {B:.3f}. No sand in the mix. "
                                     f"Quartz-filled mixes excluded. fc not entered: Table 4 gives only the MATRIX (no fiber) fc = {fcm} MPa. "
                                     "VMA = viscosity modifying agent as listed."})
    rows.append(r)

# ---- 5) 106576 Ca(OH)2-activated slag SHSC with crumb rubber (Pl and CR60 only: others only in figures)
P = paper("Sustainability and mechanical performance of hydrated lime-activated, strain-hardening slag composites incorporating crumb rubber",
          "Seong Yun Woo, Seong-Jae Kim, Soonho Kim, Nemkumar Banthia, Doo-Yeol Yoo", 2026, "10.1016/j.cemconcomp.2026.106576")
B = 1201.12 + 240.2 + 120.11
for mid, sand, cr, ft, eps, fcr in [("Pl", 312.29, 0, 7.10, 5.45, 4.65), ("CR60", 124.91, 86.26, 8.25, 8.16, None)]:
    r = dict(P)
    r.update({"GGBS": round(1201.12 / B, 4), "SF (Silica fume)": round(240.2 / B, 4), "Ca(OH)2 / B": round(120.11 / B, 4),
              "W / B": round(222.7 / B, 4), "SS / B (Silica sand)": round(sand / B, 4),
              "Crumb rubber / B": round(cr / B, 4) if cr else None, "SP / B": round(83.3 / B, 4), "Binder content (kg/m³)": round(B, 1),
              "PE fiber (vol%)": 2.0, "PE length (mm)": 18, "PE diameter (µm)": 20, "PE tensile strength (MPa)": 3000,
              "PE elastic modulus (GPa)": 100, "Total fiber (vol%)": 2.0,
              "Curing method": "air curing at room temperature, specimens sealed with plastic sheet when cast", "Curing time (days)": 28,
              "Curing temperature (°C)": 24, "Curing RH (%)": 30, "Test age (days)": 28, "Compressive specimen": "cube",
              "Compressive specimen size (mm)": "50", "Tensile specimen": "dogbone (JSCE)", "Tensile test type": "direct (uniaxial)",
              "Tensile strength (MPa)": ft, "First-cracking strength (MPa)": fcr, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 4 (mix), text 3.3.2 (ft, strain, initial cracking), abstract",
              "Conversions / notes": f"{mid}. Binder B = GGBS + SF + Ca(OH)2 (kg/m3 sum {B:.1f}). SP is liquid as dosed (70 % water, 30 % solids). "
                                     "NaOH-pretreated crumb rubber replaces silica sand (60 % replacement in CR60). "
                                     "Other mixes (CR20-CR80) have results only in Fig. 16 (not entered). fc of fiber mixes only in Fig. 7 (not entered)."})
    rows.append(r)

# ---- 6) 106600 SH-UHPC low fiber (steel mixes that are strain-hardening)
P = paper("Tailoring fiber-matrix interaction to achieve Strain-Hardening Ultra-High-Performance Concrete (SH-UHPC) at low fiber volumes",
          "A.A. Moman, S.H. Chu, D. Sundar, A. Alarab, J. Tatar, F. Rajabipour", 2026, "10.1016/j.cemconcomp.2026.106600")
B = 1081 + 236
# id, vol%, L mm, d um, fiber strength MPa, E GPa, sigma_cc, sigma_pc, eps_pc (mm/mm)
m = [("MS-2.0%", 2.0, 13, 200, 2850, 210, 6.51, 8.96, 0.0047), ("MS-1.0%", 1.0, 13, 200, 2850, 210, 5.99, 6.30, 0.0042),
     ("LS-2.0%", 2.0, 19.5, 300, 2850, 210, 5.57, 7.51, 0.0032), ("HS-2.0%", 2.0, 13, 200, 2100, 210, 7.39, 8.76, 0.0048),
     ("SS-1.0%", 1.0, 13, 200, 2850, 210, 7.42, 7.96, 0.0056)]
for mid, vf, L, d, fs, E, scc, spc, eps in m:
    r = dict(P)
    r.update({"OPC / Cement": round(1081 / B, 4), "SF (Silica fume)": round(236 / B, 4), "W / B": round(205 / B, 4),
              "Sand (type not stated) / B": round(732 / B, 4), "SP / B": round(21.2 / B, 4), "VMA / B": round(3.5 / B, 4),
              "Binder content (kg/m³)": B, "Steel fiber (vol%)": vf, "Steel length (mm)": L, "Steel diameter (µm)": d,
              "Steel tensile strength (MPa)": fs, "Steel elastic modulus (GPa)": E, "Total fiber (vol%)": vf,
              "Curing method": "cubes: moist room 23 C RH>95 % 24 h then limewater (tensile prism curing not stated)",
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50.8",
              "Tensile specimen": "prism 50.8x50.8x431.8 with GFRP plates",
              "Tensile test type": "direct (uniaxial)", "Tensile strength (MPa)": spc, "First-cracking strength (MPa)": scc,
              "Tensile strain capacity (%)": round(eps * 100, 3),
              "Source table/page": "Table 3 (mix), Table 2 (fibers), Table 4 (tension)",
              "Conversions / notes": f"{mid}. kg/m3 / 1317. HRWR 21.2 kg/m3 (40 % solids) as SP; workability extender (WE, 20 % solids) 3.5 kg/m3 entered as VMA (VERIFY). "
                                     "75 % of mixing water as ice/chilled water. Strain = eps_pc (mm/mm x 100) at post-cracking peak, average curve (AASHTO T397). "
                                     "Test age not stated; fc only in Fig. 9 (not entered). Non-strain-hardening mixes (LS-1.0, HS-1.0, IS, TS, non-steel) left out."})
    rows.append(r)

# ---- 7) 106647 ECC with CFB slag (reference ECC-C0 only; CFBS not allowed)
P = paper("Dual-function regulation of hydration and strain hardening in high-strength ECC incorporating circulating fluidized bed slag",
          "Zhijun Cheng, Taidong Guo, Rui Sun, Dong Xu, Xiao Zhang, Jinxia Liang, Zhi Cheng, Dongmin Wang", 2026,
          "10.1016/j.cemconcomp.2026.106647")
r = dict(P)
r.update({"OPC / Cement": 0.8, "GGBS": 0.1, "SF (Silica fume)": 0.1, "W / B": 0.18, "SS / B (Silica sand)": 0.3, "HRWR / B": 0.02,
          "PE fiber (vol%)": 2.0, "PE length (mm)": 18, "PE diameter (µm)": 21.7, "PE tensile strength (MPa)": 3360,
          "PE elastic modulus (GPa)": 115, "Total fiber (vol%)": 2.0, "Curing time (days)": 28,
          "Test age (days)": 28, "Tensile specimen": "dog-bone", "Tensile test type": "direct (uniaxial)",
          "Compressive strength (MPa)": 117.37, "Tensile strength (MPa)": 5.87, "First-cracking strength (MPa)": 4.26,
          "Tensile strain capacity (%)": 4.26, "Source table/page": "Table 2 (mix, ECC-C0), Table 3 (results)",
          "Conversions / notes": "Only ECC-C0 (0 % CFB slag); CFBS mixes excluded (material not in list). VERIFY: Table 2 gives 'binder-to-sand ratio 0.3' "
                                 "and 'Water reducer 2' (unit not stated): entered as sand/B = 0.3 and HRWR/B = 0.02. Quartz sand used. "
                                 "Curing method not stated. fc 28-day stated; tensile test age assumed 28 d."})
rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e1.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows ->", os.path.join(out_dir, "w6_e1.csv"))

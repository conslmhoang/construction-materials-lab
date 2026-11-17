"""Wave 6, agent e47: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e47.csv (99-column TEMPLATE header)."""
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


# ---------- 1) Zhang et al. 2026: EGC with FA + fine silica sand (F10C0-SS only; coal-gangue mixes skipped)
P = paper("Beyond performance-cost trade-off: Engineered Geopolymer Composites (EGC) incorporating ultra-high-volume coal gangue wastes",
          "Zhi-Liang Zhang, Ze-Ming Yang, Ling-Yu Xu, Jian-Cong Lao, Hui Zhang, Yu-Jie Huang, Linghua Shen, Dan-Dan Shi, Bo-Tao Huang",
          2026, "10.1016/j.jclepro.2026.148729")
r = dict(P)
r.update({"FA (Fly ash)": 1.0, "WG / B (Water glass)": 0.14, "SSM / B (Na2SiO3 anhydrous)": 0.076, "W / B": 0.265,
          "SS / B (Silica sand)": 0.298, "PE fiber (vol%)": 1.2, "PE length (mm)": 12, "PE diameter (µm)": 24,
          "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 100, "Total fiber (vol%)": 1.2,
          "Curing method": "covered 48 h at ambient temperature, demoulded, heat-cured 80 C for 72 h, cooled to ambient before test",
          "Curing time (days)": 5, "Curing temperature (°C)": 80, "Demolding age (days)": 2, "Test age (days)": 5,
          "Heat curing duration (h)": 72, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
          "Tensile specimen": "dumbbell", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
          "Compressive strength (MPa)": 46.5, "Tensile strength (MPa)": 5.6, "First-cracking strength (MPa)": 3.6,
          "Tensile strain capacity (%)": 5.6, "Source table/page": "Table 5 (mix, by weight), Table 6 (results), sect. 2.2-2.3",
          "Conversions / notes": "F10C0-SS only (FA 100 %, fine silica sand); CCG / coal gangue mixes skipped. Weight ratios to FA = 1. "
                                 "W/B = extra water 0.265 (water inside waterglass 8.7 % Na2O / 27.7 % SiO2 / 56.8 % H2O not added; paper total water 0.355). "
                                 "VERIFY: test age not stated, derived as 2 d + 72 h heat = 5 d. Sand 0.298 dry (SSD 0.300)."})
rows.append(r)

# ---------- 2) Cao et al. 2024: steel-fibre RPC (1 and 2 vol% fibre; plain RPC skipped)
P = paper("Experimental study on dynamic direct tensile performances of steel fiber-reinforced RPC at high strain rates",
          "Shaojun Cao, Xiaomeng Hou, Zhijun Dong", 2024, "10.1016/j.jobe.2024.109673")
B = 800.53 + 240.16 + 120.08
for vf, fc, ft in [(1, 133.23, 11.61), (2, 159.07, 13.26)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(800.53 / B), "SF (Silica fume)": r4(240.16 / B), "GGBS": r4(120.08 / B), "W / B": r4(208.94 / B),
              "SS / B (Silica sand)": r4(960.64 / B), "SP / B": r4(46.43 / B), "Binder content (kg/m³)": r4(B),
              "Steel fiber (vol%)": vf, "Total fiber (vol%)": vf,
              "Curing method": "24 h at ~20 C, demoulded, steam 90 C 3 d, then 20 C / 75 % RH 28 d",
              "Curing time (days)": 31, "Curing temperature (°C)": 20, "Curing RH (%)": 75, "Demolding age (days)": 1, "Test age (days)": 32,
              "Heat curing duration (h)": 72, "Tensile specimen": "dumbbell (circular section)", "Tensile test type": DIRECT,
              "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft,
              "Source table/page": "Table 1 (mix kg/m3), sect. 2 text (fc), Table 4 (quasi-static tensile strength fst)",
              "Conversions / notes": f"RPC with {vf} vol% steel fibre (fibre dimensions not given). kg/m3 / B (cement + SF + slag = {r4(B)}); quartz sand as sand. "
                                     "fc as stated in text for 1 % and 2 % fibre RPC. Tensile strength = quasi-static direct tensile strength fst (Table 4, dumbbell, strain rate 1e-6 /s). "
                                     "VERIFY: test age derived 1 + 3 + 28 = 32 d; fc specimen shape not stated; SP 46.43 kg/m3 as listed."})
    rows.append(r)

# ---------- 3) Gan et al. 2026: fly-ash EGC (LFA + HFA), reference 28-d air-cured cube fc only
P = paper("Environmental dependence of self-healing behavior for high-ductility fly ash-based engineered geopolymer composite",
          "Yuanqiao Gan, Luohao Lv, Benrui Chen, Bixiong Li, Lili Kan", 2026, "10.1016/j.jobe.2026.115305")
B = 44.56 + 11.14
r = dict(P)
r.update({"FA (Fly ash)": 1.0, "WG / B (Water glass)": r4(13.85 / B), "NaOH / B": r4(3.03 / B), "W / B": r4(12.75 / B),
          "Sand (type not stated) / B": r4(14.66 / B), "PVA fiber (vol%)": 2, "PVA length (mm)": 12, "PVA diameter (µm)": 19,
          "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": 2,
          "Curing method": "air, 20 +/- 2 C, 70 +/- 5 % RH, 24 h in mould then 27 d after demoulding", "Curing time (days)": 28,
          "Curing temperature (°C)": 20, "Curing RH (%)": 70, "Demolding age (days)": 1, "Test age (days)": 28,
          "Compressive specimen": "cube", "Compressive strength (MPa)": 12.83,
          "Source table/page": "Table 1 (mix, wt%), Table 3 (PVA), sect. 2.2 and 3.3 text (fc)",
          "Conversions / notes": "Mix in wt% of total: LFA 44.56, HFA 11.14 (both fly ash, B = 55.70), sand 14.66, Na2SiO3 solution 13.85 (27.3 % SiO2, 8.54 % Na2O, 64.16 % H2O), "
                                 "NaOH 3.03, water 12.75. W/B = added water only (water in waterglass not added). Cube fc only; "
                                 "tensile values of the paper (Table 6) are for self-healed specimens with unknown exposure age, not used. Cube size not stated."})
rows.append(r)

# ---------- 4) Zheng et al. 2026: slag/FA/SF EGC with PE fibre, control without SAP (W0.28S0.0)
P = paper("Study on the early-age mechanical properties and autogenous shrinkage of Engineered Geopolymer Composites internally cured with superabsorbent polymers",
          "Yi Zheng, Bicheng Jiang, Wenyuan Guo, Jiangtao Yu, Biao Li", 2026, "10.1016/j.jobe.2026.116041")
B = 770.9 + 144.5 + 48.2
for age, fc, extra in [(3, 76.9, {}), (7, 85.4, {"Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
                                               "Tensile strength (MPa)": 10.89, "First-cracking strength (MPa)": 7.56, "Tensile strain capacity (%)": 7.09}),
                       (28, 92.6, {})]:
    r = dict(P)
    r.update({"GGBS": r4(770.9 / B), "FA (Fly ash)": r4(144.5 / B), "SF (Silica fume)": r4(48.2 / B), "WG / B (Water glass)": r4(254.7 / B),
              "W / B": r4(129.6 / B), "SS / B (Silica sand)": r4(289.1 / B), "SP / B": 0.01, "Binder content (kg/m³)": r4(B),
              "PE fiber (vol%)": 2, "PE tensile strength (MPa)": 2900, "PE elastic modulus (GPa)": 116, "Total fiber (vol%)": 2,
              "Curing method": "sealed 24 h, demoulded, then 20 +/- 2 C / 95 % RH to test age", "Curing time (days)": age,
              "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": age,
              "Compressive strength (MPa)": fc, "Source table/page": "Table 3 (mix kg/m3), Table 4 (results), sect. 2.2-2.4",
              "Conversions / notes": "Control mix W0.28S0.0 only (no SAP; SAP mixes skipped). kg/m3 / B (GGBS + FA + SF = 963.6). "
                                     "Alkaline activator (254.7 kg/m3: Na2SiO3 solution 13.75 % Na2O / 29.99 % SiO2 adjusted to Ms 2.0 with NaOH, split not given) entered as WG / B. "
                                     "W/B = 129.6 free (mixing) water only; paper's w/b 0.28 includes activator water. SP 1 % of binder (text). "
                                     "Quartz sand as sand. VERIFY: PE length given as 18 (units garbled), not entered."})
    r.update(extra)
    rows.append(r)

# ---------- 5) Dong et al. 2026: ECC reference (0 F-T cycles); CA-ECC mixes skipped (coarse aggregate)
P = paper("Tensile ductility evolution of sustainable engineered cementitious composites incorporating fly ash coarse aggregate under freeze-thaw cycling",
          "Zhifu Dong, Yuheng Bai, Fangming Jiang, Jiangtao Yu", 2026, "10.1016/j.jobe.2026.117565")
B = 596 + 715
r = dict(P)
r.update({"OPC / Cement": r4(596 / B), "FA (Fly ash)": r4(715 / B), "W / B": r4(315 / B), "River sand / B": r4(286 / B), "SP / B": r4(4 / B),
          "Binder content (kg/m³)": B, "PE fiber (vol%)": r4(14.5 / 970 * 100), "Total fiber (vol%)": r4(14.5 / 970 * 100),
          "Curing method": "demoulded after 24 h, cured at ambient temperature 27 d", "Curing time (days)": 28, "Demolding age (days)": 1,
          "Test age (days)": 28, "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
          "Tensile strength (MPa)": 7.56, "Tensile strain capacity (%)": 6.70,
          "Source table/page": "Table 1 (mix kg/m3), Table 2 (strain, 0 F-T), sect. 3.3 text (strength 7.56)",
          "Conversions / notes": "ECC reference at 0 freeze-thaw cycles only (FCA-/NCA-ECC contain coarse aggregate, skipped). kg/m3 / B (cement + FA = 1311). "
                                 "PE fibre 14.5 kg/m3 -> vol% with density 970 (VERIFY: derived). VERIFY: test age derived from 24 h + 27 d at 'ambient temperature' (temperature / RH not stated); "
                                 "test of the 0-cycle group assumed at 28 d. River sand."})
rows.append(r)

# ---------- 6) Che et al. 2022: ECC and alkali-excited ECC (cement 50 % / FA 50 %, PVA 26 kg/m3)
P = paper("Research on basic mechanical properties of different modulus alkaline excited ECC", "Jialing Che, Renze Yang, Jun Wang, Haifeng Liu, Yunxiang Zhang",
          2022, "10.1016/j.pce.2022.103233")
# name, T, modulus, NaOH, Na2SiO3, W/B, S/B, [(age, fc, ts, strain), ...]
mixes = [
    ("T1-0", 1, 0, 0, 0, 0.35, 0.46, [(7, 10.0, 7.5, 7.0), (28, 31.3, 9.1, 4.1)]),
    ("T1-1", 1, 1, 11.69, 48.37, 0.35, 0.46, [(7, 14.5, 8.1, 3.0), (28, 30.1, 8.2, 0.7)]),
    ("T1-1.5", 1, 1.5, 6.70, 53.36, 0.35, 0.46, [(7, 17.0, 8.8, 3.7), (28, 35.8, 8.4, 3.7)]),
    ("T1-2", 1, 2, 3.78, 56.28, 0.35, 0.46, [(7, 12.4, 7.7, 3.7), (28, 30.2, 7.8, 1.4)]),
    ("T2-0", 2, 0, 0, 0, 0.29, 0.50, [(7, 23.8, 8.4, 4.3), (28, 49.8, 7.6, 4.1)]),
    ("T2-1", 2, 1, 11.82, 48.91, 0.29, 0.50, [(7, 16.1, 8.6, 1.3), (28, 30.5, 8.6, 2.1)]),
    ("T2-1.5", 2, 1.5, 6.78, 53.95, 0.29, 0.50, [(7, 21.6, 7.6, 2.5), (28, 34.9, 9.1, 2.4)]),
    ("T2-2", 2, 2, 3.82, 56.91, 0.29, 0.50, [(7, 22.6, 8.0, 3.7), (28, 38.7, 8.2, 2.4)]),
]
for nm, T, ms, naoh, wg, wb, sb, res in mixes:
    # binder from the fixed activator dose: NaOH + Na2SiO3 = 5 % of cementitious material (T1 60.06, T2 60.73 kg/m3)
    B = (11.69 + 48.37) / 0.05 if T == 1 else (11.82 + 48.91) / 0.05
    for age, fc, ts, eps in res:
        r = dict(P)
        r.update({"OPC / Cement": 0.5, "FA (Fly ash)": 0.5, "W / B": wb, "Sand (type not stated) / B": sb, "SP / B": 0.001,
                  "Binder content (kg/m³)": r4(B), "PVA fiber (vol%)": r4(26 / 1300 * 100), "Total fiber (vol%)": r4(26 / 1300 * 100),
                  "Curing time (days)": age, "Test age (days)": age, "Compressive specimen": "cube",
                  "Tensile specimen": "dumbbell", "Tensile test type": DIRECT, "Compressive strength (MPa)": fc,
                  "Tensile strength (MPa)": ts, "Tensile strain capacity (%)": eps,
                  "Source table/page": "Table 3 (mix), Table 4 (results), sect. 2.1.2",
                  "Conversions / notes": f"{nm}. Cement : FA = 50 : 50 by mass. Alkali activator dose fixed at 5 % of binder (NaOH + Na2SiO3 solution, 26.2 % SiO2 / 8.3 % Na2O, "
                                         "modulus adjusted with NaOH); T-1 binder ~1201 kg/m3 and T-2 ~1215 kg/m3 derived from 5 % dose (VERIFY). "
                                         "PVA 26 kg/m3 -> 2.0 vol% with density 1300 (VERIFY: derived). W/B as stated (unclear whether activator water is included). "
                                         "SP = 0.1 % of binder. VERIFY: curing conditions not described, only ages 7 / 28 d. DOUBTFUL: 7-d tensile strength 7-9 MPa exceeds fc (10-24 MPa) for several mixes."})
        if naoh:
            r["NaOH / B"] = r4(naoh / B)
            r["WG / B (Water glass)"] = r4(wg / B)
            r["Activator modulus Ms (SiO2/Na2O)"] = ms
        rows.append(r)

# ---------- 7) Wang et al. 2020: UHPCC (control specimens of the UHPCC-FST study)
P = paper("Experimental study on the residual seismic resistance of ultra high performance cementitious composite filled steel tube (UHPCC-FST) after contact explosion",
          "Z.G. Wang, H. Wu, J. Wu, Q. Fang", 2020, "10.1016/j.tws.2020.106852")
B = 700 + 140 + 60 + 50
r = dict(P)
r.update({"OPC / Cement": r4(700 / B), "SF (Silica fume)": r4(140 / B), "FA (Fly ash)": r4(60 / B), "GGBS": r4(50 / B), "W / B": r4(152 / B),
          "Sand (type not stated) / B": r4(1200 / B), "SP / B": r4(22.8 / B), "Binder content (kg/m³)": B,
          "Steel fiber (vol%)": r4(156 / 7850 * 100), "Total fiber (vol%)": r4(156 / 7850 * 100),
          "Curing method": "room temperature 21 +/- 2 C, RH 98.4 %, 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 21, "Curing RH (%)": 98.4,
          "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100", "Tensile test type": DIRECT,
          "Compressive strength (MPa)": 135.1, "Tensile strength (MPa)": 9,
          "Source table/page": "Table 1 (mix kg/m3), sect. 2.2 text (fc, direct tensile strength)",
          "Conversions / notes": "kg/m3 / B (cement + SF + FA + ultra-fine slag = 950). Steel fibre 156 kg/m3 -> vol% with density 7850 (VERIFY: derived; fibre dimensions not given). "
                                 "Sand type not stated. Tensile strength 9 MPa from the direct tensile test (strain only in a figure, not entered)."})
rows.append(r)

df = pd.DataFrame(rows)
for c in cols:
    if c not in df.columns:
        df[c] = None
df = df[cols]
df.to_csv(os.path.join(out_dir, "w6_e47.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows,", df["DOI / URL"].nunique(), "papers")

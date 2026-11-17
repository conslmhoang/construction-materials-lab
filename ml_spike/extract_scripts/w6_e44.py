"""Wave 6, agent e44: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e44.csv (99-column TEMPLATE header).
Papers: cemconcomp.2024.105553, 2019.103500, 2022.104650, 2024.105896, 2025.106378,
        compstruct.2020.113433, conbuildmat.2012.04.047
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


# ---------- 1) Hiew et al. 2024: UHPC (OPC + SF + silica sand) + straight / hooked / hybrid steel fibre, fc at 7/28/56 d
P = paper("A unified tensile constitutive model for mono/hybrid fibre-reinforced ultra-high-performance concrete (UHPC)",
          "Shack Yee Hiew, Keat Bin Teoh, Sudharshan N. Raman, Chung-Chan Hung, Ya Xuan Chaen, Daniel Kong, Milad Hafezolghorani",
          2024, "10.1016/j.cemconcomp.2024.105553")
B = 850 + 200
water = {1.0: 170.2, 1.5: 170.9, 2.0: 171.5}
fc = {  # series: (SL, HL, 7d, 28d, 56d) from Table 5
    "SL-1.0": (1.0, 0, 118.9, 124.3, 128.2), "SL-1.5": (1.5, 0, 125.9, 129.3, 136.0), "SL-2.0": (2.0, 0, 136.9, 137.9, 145.8),
    "HL-1.0": (0, 1.0, 121.8, 124.6, 129.4), "HL-1.5": (0, 1.5, 128.3, 136.9, 138.1), "HL-2.0": (0, 2.0, 138.4, 143.1, 145.9),
    "SL-HL-1.0": (0.5, 0.5, 123.5, 127.2, 132.3), "SL-HL-1.5": (0.75, 0.75, 134.2, 139.7, 141.4), "SL-HL-2.0": (1.0, 1.0, 141.2, 145.7, 149.4),
}
for nm, (sl, hl, f7, f28, f56) in fc.items():
    vf = sl + hl
    for age, val in [(7, f7), (28, f28), (56, f56)]:
        r = dict(P)
        r.update({"OPC / Cement": r4(850 / B), "SF (Silica fume)": r4(200 / B), "W / B": r4(water[vf] / B),
                  "SS / B (Silica sand)": r4(1030 / B), "SP / B": r4(28 / B), "Binder content (kg/m³)": B,
                  "Steel fiber (vol%)": vf, "Steel length (mm)": 20, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2500,
                  "Total fiber (vol%)": vf,
                  "Curing method": "24 h room temp. in mould, demoulded, heat cured 90 C / 95 % RH for 48 h, then room temperature until test",
                  "Curing time (days)": age, "Curing temperature (°C)": 90, "Curing RH (%)": 95, "Demolding age (days)": 1,
                  "Heat curing duration (h)": 48, "Test age (days)": age,
                  "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "75 x 150", "Compressive strength (MPa)": val,
                  "Source table/page": "Table 3 (mix), Table 4 (steel fibre), Table 5 (fc), sect. 3.2",
                  "Conversions / notes": f"{nm} (SL = straight, HL = hooked-end fibre, 20 mm x 0.2 mm). kg/m3 / B (cement + SF = {B}); "
                                         "water = free water of Table 3 (paper quotes W/B ~0.18 counting SP water). Silica sand from the proprietary premix, SP in kg/m3 as dosed. "
                                         "Hybrid series: total Vf = SL + HL. Tensile (direct, dog-bone) results of this paper NOT entered because the tensile test age is not stated. "
                                         "Plain UHPC (no fibre) skipped."})
        rows.append(r)

# ---------- 2) Wang et al. 2019: EDCC (ECC with FA + SF), 28-d uniaxial tension
P = paper("Water permeability of Eco-Friendly Ductile Cementitious Composites (EDCC) under an applied compressive stress",
          "Qiannan Wang, Nemkumar Banthia, Wei Sun, Chunping Gu", 2019, "10.1016/j.cemconcomp.2019.103500")
B = 385 + 770 + 77
r = dict(P)
r.update({"OPC / Cement": r4(385 / B), "FA (Fly ash)": r4(770 / B), "SF (Silica fume)": r4(77 / B), "W / B": r4(333 / B),
          "Sand (type not stated) / B": r4(462 / B), "Binder content (kg/m³)": B,
          "PVA fiber (vol%)": 2.0, "PVA length (mm)": 8, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1560, "PVA elastic modulus (GPa)": 40,
          "Total fiber (vol%)": 2.0,
          "Curing method": "water curing at 20 C until test (stated for compressive specimens)", "Curing time (days)": 28, "Curing temperature (°C)": 20,
          "Test age (days)": 28, "Tensile specimen": "contoured (dog-bone)", "Tensile test type": DIRECT,
          "Tensile strength (MPa)": 4.43, "Tensile strain capacity (%)": 3.89,
          "Source table/page": "Table 1 (mix), Table 2 (PVA), sect. 3.2 text (tensile at 28 d)",
          "Conversions / notes": f"EDCC. kg/m3 / B (cement + FA + SF = {B}). PVA 26 kg/m3 / 1300 kg/m3 = 2.0 vol% (Table 2 prints density as '13'; VERIFY). "
                                 "Superplasticiser 2 l/m3 not converted (density not given). Natural sand max 1.19 mm. "
                                 "Strain = 'inelastic strain capacity as high as 3.89 %' (VERIFY: may be max, not mean). "
                                 "VERIFY: curing of tensile specimens not stated, 20 C water assumed as for compressive specimens. "
                                 "Compressive strength only in Fig. 3 (not entered). PCC (no fibre) skipped."})
rows.append(r)

# ---------- 3) Kang et al. 2022: cementless UHPFC (lime-activated FA + SF), steel fibre 2 vol%
P = paper("Development of cementless ultra-high performance fly ash composite (UHPFC) using nucleated pozzolanic reaction of low Ca fly ash",
          "Sung-Hoon Kang, Hyunuk Kang, Nankyoung Lee, Yang-Hee Kwon, Juhyuk Moon", 2022, "10.1016/j.cemconcomp.2022.104650")
B = 616 + 264 + 220
base = {"FA (Fly ash)": r4(616 / B), "SF (Silica fume)": r4(220 / B), "Ca(OH)2 / B": r4(264 / B), "W / B": r4(220 / B),
        "Sand (type not stated) / B": r4(968 / B), "SP / B": r4(11 / B), "Binder content (kg/m³)": B,
        "Steel fiber (vol%)": 2.0, "Total fiber (vol%)": 2.0}
for lab, age, val, cur, ctemp, hdur, note in [
    ("UHPFC_amb", 28, 45, "sealed moulds, ambient 20 C until test", 20, None, "VERIFY: '~45 MPa at 28 days' is approximate text value."),
    ("UHPFC_amb", 180, 100, "sealed moulds, ambient 20 C until test", 20, None, "VERIFY: '~100 MPa' reached after 180 d (approximate text value)."),
    ("UHPFC_stm", 7, 111, "sealed moulds, 20 C; steam 60 C for 3 days between day 1 and day 4", 60, 72, "Strength 111 MPa at 7 d (text)."),
]:
    r = dict(P)
    r.update(base)
    r.update({"Curing method": cur, "Curing time (days)": age, "Curing temperature (°C)": ctemp, "Test age (days)": age,
              "Compressive strength (MPa)": val, "Source table/page": "Table 2 (mix), sect. 3.1 text (strength; Fig. 4 not used)"})
    if hdur:
        r["Heat curing duration (h)"] = hdur
    r["Conversions / notes"] = (f"{lab}. kg/m3 / B (FA + hydrated lime + SF = {B}); hydrated lime entered as Ca(OH)2 / B, FA and SF as fractions of the same B (sum 0.76 + lime 0.24). "
                                "Cement-free. 'Fine aggregate' type not stated. SP = PCE solids. Steel fibre 157 kg/m3 = 2 vol% (stated 2 % of composite); fibre dimensions not given. "
                                + note)
    rows.append(r)

# ---------- 4) Alarrak & Brand 2024: steel fibre mortar, fc 28 d
P = paper("Mechanical performance of extruded functionally graded fiber-reinforced mortar with targeted fiber injection",
          "Rashed Alarrak, Alexander S. Brand", 2024, "10.1016/j.cemconcomp.2024.105896")
for vf, val in [(0.5, 39.3), (1.0, 40.2)]:
    r = dict(P)
    r.update({"OPC / Cement": 1.0, "W / B": 0.40, "Sand (type not stated) / B": r4(1042 / 688), "Binder content (kg/m³)": 688,
              "Steel fiber (vol%)": vf, "Steel length (mm)": 30, "Steel diameter (µm)": 380, "Steel tensile strength (MPa)": 1020,
              "Total fiber (vol%)": vf, "Curing method": "moist curing 28 d", "Curing time (days)": 28, "Test age (days)": 28,
              "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100 x 200", "Compressive strength (MPa)": val,
              "Source table/page": "Table 1 (mix), Table 2 (fibre), Table 3 (fc mean)",
              "Conversions / notes": f"Uniform fibre dosage {vf} vol% (mixture series, not graded). Type I cement 688 kg/m3, 'fine aggregate' 1042 kg/m3 (type not stated), w/c 0.40. "
                                     "Moist curing temperature / RH not stated. Mean of 3 cylinders. 0 % mixture skipped (no fibre)."})
    rows.append(r)

# ---------- 5) Sun et al. 2025: reference ECC (OPC + FA, PVA), uniaxial tension
P = paper("Developing sustainable engineered cementitious composites with carbonated recycled concrete fines: Feasibility and engineering properties",
          "Hao Sun, Meng Chen, Yihan Tian, Yuting Wang, Tong Zhang, Xiaowei Ouyang, Mingzhong Zhang", 2025, "10.1016/j.cemconcomp.2025.106378")
B = 544.0 + 652.8
r = dict(P)
r.update({"OPC / Cement": r4(544 / B), "FA (Fly ash)": r4(652.8 / B), "W / B": r4(323.1 / B), "SS / B (Silica sand)": r4(435.2 / B),
          "VMA / B": r4(1.2 / B), "SP / B": r4(12.0 / B), "Binder content (kg/m³)": r4(B),
          "PVA fiber (vol%)": 2.03, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 40,
          "Total fiber (vol%)": 2.03,
          "Curing method": "demoulded after 1 d, curing chamber 20 +/- 2 C, 95 % RH, up to 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 20,
          "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28, "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
          "Tensile strength (MPa)": 3.38, "Tensile strain capacity (%)": 4.02,
          "Source table/page": "Table 3 (mix, kg/m3), Table 2 (PVA), sect. 3.3 text (tensile of Ref)",
          "Conversions / notes": f"Ref ECC only (RCF / CRCF mixes skipped, recycled fines). kg/m3 / B (OPC + FA = {r4(B)}). PVA 26 kg/m3 / 1280 = 2.03 vol%. Quartz sand as sand. "
                                 "VERIFY: tensile test age taken as 28 d ('cured for up to 28 d'). Compressive strength only in Fig. 13 (not entered)."})
rows.append(r)

# ---------- 6) Donnini et al. 2020: UHPFRC with hooked steel fibres, direct tension 28 d
P = paper("Uniaxial tensile behavior of ultra-high performance fiber-reinforced concrete (UHPFRC): Experiments and modeling",
          "Jacopo Donnini, Giovanni Lancioni, Gianluca Chiappini, Valeria Corinaldesi", 2020, "10.1016/j.compstruct.2020.113433")
B = 1 + 0.125
for nm, vf, sc, smax, ec, emax in [("UHPFRC_0.6%", 0.6, 3.74, 4.49, 0.029, 0.07), ("UHPFRC_1.25%", 1.25, 4.90, 5.40, 0.035, 0.20),
                                  ("UHPFRC_1.9%", 1.9, 3.93, 5.88, 0.036, 0.56), ("UHPFRC_2.55%", 2.55, 6.14, 8.11, 0.062, 0.87)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(1 / B), "SF (Silica fume)": r4(0.125 / B), "W / B": r4(0.2 / B), "Sand (type not stated) / B": r4(1.0 / B),
              "SP / B": r4(0.011 / B), "Steel fiber (vol%)": vf, "Steel length (mm)": 30, "Steel diameter (µm)": 700,
              "Steel tensile strength (MPa)": 450, "Steel elastic modulus (GPa)": 170, "Total fiber (vol%)": vf,
              "Curing method": "demoulded after 2 d, laboratory conditions 20 C / 70 % RH up to 28 d", "Curing time (days)": 28,
              "Curing temperature (°C)": 20, "Curing RH (%)": 70, "Demolding age (days)": 2, "Test age (days)": 28,
              "Tensile specimen": "dog-bone", "Tensile test type": DIRECT, "Tensile strength (MPa)": smax,
              "First-cracking strength (MPa)": sc, "Tensile strain capacity (%)": emax,
              "Source table/page": "Table 1 (mix by weight), Table 2 (fibre), Table 5 (tensile)",
              "Conversions / notes": f"{nm}. Weight ratios to cement = 1 (Table 1): SF 0.125, water 0.2, sand 0/0.6 mm 0.4 + sand 0.6/1.0 mm 0.6, WRA 0.011; B = cement + SF = {B}. "
                                     "Fibre vol% = nominal (Table 4). Tensile strength = sigma_t,max, strain = strain at maximum stress (eps_t,max), mean of 3 dog-bones. "
                                     "VERIFY: fibre tensile strength printed as 450 MPa (hooked 30 x 0.7 mm). WRA entered as SP / B. Sand type not stated. "
                                     "UHPC_0% (no fibre) skipped; fc only for the no-fibre matrix."})
    rows.append(r)

# ---------- 7) Hassan et al. 2012: UHPFRC (OPC + GGBS + SF), 2 vol% steel, fc 7/14/28 d
P = paper("Non-destructive testing of ultra high performance fibre reinforced concrete (UHPFRC): A feasibility study for using ultrasonic and resonant frequency testing techniques",
          "A.M.T. Hassan, S.W. Jones", 2012, "10.1016/j.conbuildmat.2012.04.047")
B = 657 + 418 + 119
for age, cyl, cube in [(7, 140.9, 160.8), (14, 141.6, 163.1), (28, 149.4, 164.3)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(657 / B), "GGBS": r4(418 / B), "SF (Silica fume)": r4(119 / B), "W / B": r4(185 / B),
              "SS / B (Silica sand)": r4(1051 / B), "SP / B": r4(40 / B), "Binder content (kg/m³)": B,
              "Steel fiber (vol%)": 2.0, "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2000, "Total fiber (vol%)": 2.0,
              "Curing method": "20 C for 24 h, hot water tank 90 C for 48 h, then dry at laboratory temperature until test",
              "Curing time (days)": age, "Heat curing duration (h)": 48, "Curing temperature (°C)": 90, "Test age (days)": age,
              "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "50 x 100", "Compressive strength (MPa)": cyl,
              "Source table/page": "Table 2 (mix, kg/m3), sect. 2.2-2.3 (curing, ages), Table 5 (fc)",
              "Conversions / notes": f"kg/m3 / B (cement + GGBS + SF = {B}). Cylinder 50 x 100 mm strength entered; 100 mm cube strength = {cube} MPa at this age. "
                                     "SP (Structuro 11180) entered as kg/m3 / B. Silica sand mean size 0.27 mm. Steel fibre 2 vol% (157 kg/m3), straight 13 x 0.20 mm. "
                                     "Demolding age not stated."})
    rows.append(r)

df = pd.DataFrame(rows)
for c in cols:
    if c not in df.columns:
        df[c] = None
df = df[cols]
df.to_csv(os.path.join(out_dir, "w6_e44.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows;", df["DOI / URL"].nunique(), "papers")

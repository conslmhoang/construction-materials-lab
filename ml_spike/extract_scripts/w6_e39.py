"""Wave 6, agent e39: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e39.csv (99-column TEMPLATE header).
Papers: apenergy.2014.02.007, cemconcomp.2019.103343, cemconcomp.2024.105893, cemconcomp.2025.106424, cemconres.2009.07.012
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


# ---------- 1) Applied Energy 2014: normal FRCC (PVA 2 vol%, silica sand), 28 d
P = paper("Performance of novel thermal energy storage engineered cementitious composites incorporating a paraffin/diatomite composite phase change material",
          "Biwan Xu, Zongjin Li", 2014, "10.1016/j.apenergy.2014.02.007")
r = dict(P)
r.update({"OPC / Cement": 1.0, "W / B": 0.27, "SS / B (Silica sand)": 0.25, "HRWR / B": 0.04, "VMA / B": 0.001,
          "PVA fiber (vol%)": 2, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1530,
          "PVA elastic modulus (GPa)": 33, "Total fiber (vol%)": 2,
          "Curing method": "24 h in mould, demoulded, then room 23 +/- 2 C, RH 95 +/- 5 % until test", "Curing time (days)": 28,
          "Curing temperature (°C)": 23, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
          "Compressive specimen": "cube", "Compressive specimen size (mm)": "40", "Tensile specimen": "prism (15 x 50 x 350 mm)",
          "Tensile test type": DIRECT, "Compressive strength (MPa)": 54.43, "Tensile strength (MPa)": 5.85,
          "First-cracking strength (MPa)": 4.84, "Tensile strain capacity (%)": 0.18,
          "Source table/page": "Table 2 (mix, weight ratio), sect. 3.1 text (fc, tensile)",
          "Conversions / notes": "Normal FRCC only (TES-ECC mixes contain paraffin/diatomite PCM, skipped). Weight ratios to cement (B = cement = 1): "
                                 "sand 0.25, HRWRA 0.040, methyl-cellulose 0.001 (entered as VMA / B), W/B 0.27. PVA oil-coated 1.2 wt%. "
                                 "28-d values from text; 7 and 56 d fc only in Fig. 4 (not used). Tensile strain = strain at max stress (single crack, 0.18 %). "
                                 "Tensile: 27 d curing after 24 h demoulding = 28 d."})
rows.append(r)

# ---------- 2) Fibre reinforced geopolymer composites (dynamic splitting paper): quasi-static fc, 28 d
P = paper("Mechanical properties and behaviour of high-strength plain and hybrid-fiber reinforced geopolymer composites under dynamic splitting tension",
          "Musaad Zaheer Nazir Khan, Yifei Hao, Hong Hao, Faiz uddin Ahmed Shaikh", 2019, "10.1016/j.cemconcomp.2019.103343")
B = 412 + 275
wg = 295.0
wg_solids = 0.441 * wg          # 55.9 % H2O, 14.7 % Na2O, 29.4 % SiO2
wg_water = 0.559 * wg
naoh_sol = 118.0                # 12 M NaOH solution (Na2SiO3/NaOH mass ratio 2.5 = 295/118)
# water-to-solids ratio 0.28 -> solve NaOH solids x: (wg_water + naoh_sol - x) = 0.28 * (B + wg_solids + x)
x = (wg_water + naoh_sol - 0.28 * (B + wg_solids)) / 1.28
free_w = naoh_sol - x
for nm, hs, ss, pe, fc in [("SFRGC-1", 0.5, 0.5, 0, 106.95), ("SFRGC-2", 1.0, 1.0, 0, 110.09), ("HFRGC", 0.8, 0.8, 0.4, 87.95)]:
    steel = hs + ss
    r = dict(P)
    r.update({"GGBS": r4(275 / B), "FA (Fly ash)": r4(412 / B), "WG / B (Water glass)": r4(wg / B), "NaOH / B": r4(x / B),
              "W / B": r4(free_w / B), "SS / B (Silica sand)": r4(1100 / B), "Binder content (kg/m³)": B,
              "Steel fiber (vol%)": steel, "Steel length (mm)": 25, "Steel elastic modulus (GPa)": 200,
              "Total fiber (vol%)": r4(steel + pe),
              "Curing method": "sealed with cling sheet 24 h, demoulded, then air at 23 +/- 2 C, RH 50 +/- 5 % for 27 d (ambient)", "Curing time (days)": 28,
              "Curing temperature (°C)": 23, "Curing RH (%)": 50, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100 x 200", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 3 (mix, kg/m3), Table 4 (fc), sect. 2.1-2.3",
              "Conversions / notes": f"{nm}. B = fly ash 412 + slag 275 = {B} kg/m3. Activator: Na2SiO3 solution (D-grade, 55.9 % H2O, 14.7 % Na2O, 29.4 % SiO2, Ms 2.0) 295 kg/m3 entered as WG / B (liquid as dosed; solids = {r4(wg_solids / B)} of B); "
                                     f"NaOH given as 118 kg/m3 of 12 M solution. VERIFY: NaOH solids ({r4(x)} kg/m3) and free water ({r4(free_w)} kg/m3 = water of the NaOH solution only) derived from the stated water-to-solids ratio 0.28 "
                                     "(water = water in both solutions; solids = FA + slag + silicate solids + NaOH solids); water inside water glass not in W / B. "
                                     "Silica sand 1100 kg/m3. Fibres: HS hooked-end steel (25 mm, 0.30 mm dia, 2500 MPa) and SS spiral steel (25 mm, 0.55 mm dia, 2000 MPa), equal parts; steel diameter / strength left empty (two types). "
                                     + ("HSPE fibre 0.4 vol% (12 mm, 12 um, 3500 MPa, 123 GPa) entered as PE. " if pe else "")
                                     + "Plain geopolymer (no fibre, fc 94.53) skipped. Splitting tensile strengths not entered (not direct tension)."})
    if pe:
        r.update({"PE fiber (vol%)": pe, "PE length (mm)": 12, "PE diameter (µm)": 12, "PE tensile strength (MPa)": 3500, "PE elastic modulus (GPa)": 123})
    rows.append(r)

# ---------- 3) Artificial flaws in ECC (PE fibres), uncoated reference mixes
P = paper("Introducing artificial flaws in Engineered cementitious composites (ECC) through nanocomposite coating of aggregates: A novel approach and mechanism",
          "Zhuo Tang, Cheng Li, Jing Zhong et al.", 2024, "10.1016/j.cemconcomp.2024.105893")
for nm, sand, sp, fcs, ts, eps in [("ECC-FSS-0.75", 0.75, 0.54, 4.73, 6.79, 2.82), ("ECC-FSS-0.36", 0.36, 0.43, 4.53, 6.65, 5.02)]:
    r = dict(P)
    r.update({"OPC / Cement": 0.405, "FA (Fly ash)": 0.567, "SF (Silica fume)": 0.028, "W / B": 0.24, "SS / B (Silica sand)": sand,
              "SP / B": r4(sp / 100), "PE fiber (vol%)": 1.5, "PE length (mm)": 18, "PE diameter (µm)": 19, "PE tensile strength (MPa)": 3000,
              "PE elastic modulus (GPa)": 110, "Total fiber (vol%)": 1.5,
              "Curing method": "sealed 1 d, demoulded, steam 75 C for 3 d, then standard curing 7 d", "Curing time (days)": 10,
              "Curing temperature (°C)": 75, "Demolding age (days)": 1, "Test age (days)": 11, "Heat curing duration (h)": 72,
              "Tensile specimen": "dog-bone (JSCE)", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
              "First-cracking strength (MPa)": fcs, "Tensile strength (MPa)": ts, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 3 (mix, weight ratio), Table 4 (tensile), sect. 2.3-2.4",
              "Conversions / notes": f"{nm}. Weight ratios, binder = OPC + FA + SF = 1.000; fine silica sand 96-212 um. Nanocomposite (CNT/PAE) coated sand mixes skipped. "
                                     "VERIFY: test age 11 d derived (1 d + 3 d at 75 C + 7 d standard curing; tensile test age not stated explicitly); standard curing T/RH not stated. "
                                     "VERIFY: SP given as 'SP (%)', taken as % of binder. Ultimate tensile strength / strain = Table 4 values. Compressive strength mentioned but not tabulated."})
    rows.append(r)

# ---------- 4) UHS-ECC size effect (PE fibres 6/12/18 mm), fc from text
P = paper("Size effect and mechanism-based multiphase modeling of strain-hardening behavior of Ultra-High-Strength Engineered Cementitious Composites (UHS-ECC)",
          "Ji-Xiang Zhu, Bo-Tao Huang, Wei-He Liu, Ling-Yu Xu, Kai-Di Peng, Jian-Guo Dai", 2025, "10.1016/j.cemconcomp.2025.106424")
B = 1.3
for L, fc in [(6, 153.2), (12, 152.7), (18, 153.5)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(1 / B), "SF (Silica fume)": r4(0.3 / B), "W / B": r4(0.2 / B), "SS / B (Silica sand)": r4(0.52 / B),
              "SP / B": r4(0.018 / B), "PE fiber (vol%)": 2, "PE length (mm)": L, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000,
              "PE elastic modulus (GPa)": 100, "Total fiber (vol%)": 2,
              "Curing method": "20 C 24 h, demoulded, water at 90 C for 3 d, then room temperature 12 h", "Curing time (days)": 3.5,
              "Curing temperature (°C)": 90, "Demolding age (days)": 1, "Test age (days)": 4.5, "Heat curing duration (h)": 72,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 1 (mix, weight ratio), Table 2 (PE), sect. 2.2-2.4 text (fc)",
              "Conversions / notes": f"PE fibre length {L} mm. Weight ratios to cement (Table 1): SF 0.3, sand 0.52, water 0.2, SP (solid) 0.018; B = cement + SF = 1.3 "
                                     "(text: W/B 0.154, sand/B 0.4, SP/B 0.014). VERIFY: test age 4.5 d derived (24 h + 3 d at 90 C + 12 h; cube curing not described separately). "
                                     "Tensile strength / strain only in figures (not entered); specimen thickness 10-30 mm."})
    rows.append(r)

# ---------- 5) Lai & Sun 2009: UHPCC with steel fibres, 60 d static fc
P = paper("Dynamic behaviour and visco-elastic damage model of ultra-high performance cementitious composite",
          "Jianzhong Lai, Wei Sun", 2009, "10.1016/j.cemconres.2009.07.012")
for nm, vf, fc in [("UPCV3", 3, 186), ("UPCV4", 4, 204)]:
    r = dict(P)
    r.update({"OPC / Cement": 0.40, "GGBS": 0.25, "FA (Fly ash)": 0.25, "SF (Silica fume)": 0.10, "W / B": 0.16,
              "Sand (type not stated) / B": 1.2, "SP / B": 0.02, "Steel fiber (vol%)": vf, "Steel length (mm)": 13, "Steel diameter (µm)": 200,
              "Steel tensile strength (MPa)": 1800, "Total fiber (vol%)": vf,
              "Curing method": "20 +/- 2 C, RH > 90 %, demoulded 24 h, then same conditions for 60 d", "Curing time (days)": 60,
              "Curing temperature (°C)": 20, "Curing RH (%)": 90, "Demolding age (days)": 1, "Test age (days)": 60, "Compressive strength (MPa)": fc,
              "Source table/page": "Table 2 (mix, fc), sect. 2",
              "Conversions / notes": f"{nm}. Binder wt% cement 40 / SF 10 / FA 25 / slag 25. Natural sand (max 2.5 mm, FM 2.6), sand/B 1.2. "
                                     "VERIFY: SP/binder 0.02 taken as mass ratio (column header says %); PCE solids 42 %. Static uniaxial compressive strength at 60 d; specimen size not stated. "
                                     "UPCV0 (no fibre, 143 MPa) skipped."})
    rows.append(r)

df = pd.DataFrame(rows)
for c in cols:
    if c not in df.columns:
        df[c] = ""
df = df[cols]
df.to_csv(os.path.join(out_dir, "w6_e39.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows")

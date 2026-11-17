"""Wave 6, agent e2: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e2.csv (99-column TEMPLATE header). Ratios per the papers' binder."""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
add = os.path.join(here, "..", "additions")
out = os.path.join(here, "..", "additions_v2", "w6_e2.csv")
cols = list(pd.read_csv(os.path.join(add, "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
rows = []

# ---- 1) ultra-lightweight ECC, control mix L0 only (FAC / HGM mixes excluded)
P = {"Article Name": "Development and performance of ultra-lightweight engineered cementitious composite with eco-friendly lightweight fillers: Balancing strength and ductility",
     "Author": "Pan Gao, Jianhu Liu, Yulei Bai, Weihao Mao, Tomoya Nishiwaki, Yao Ding", "Year": 2025,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2025.141403"}
B = 454.5 + 454.5 + 136.4
r = dict(P)
r.update({"OPC / Cement": round(454.5 / B, 4), "FA (Fly ash)": round(454.5 / B, 4), "SF (Silica fume)": round(136.4 / B, 4),
          "W / B": round(261.4 / B, 3), "SS / B (Silica sand)": round(909.1 / B, 3), "Binder content (kg/m³)": round(B, 1),
          "PE fiber (vol%)": 1.0, "PE length (mm)": 18, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 2400,
          "PE elastic modulus (GPa)": 100, "Total fiber (vol%)": 1.0,
          "Curing method": "demolded 24 h, standard curing room 20 °C RH 95 %", "Curing time (days)": 28,
          "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
          "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Tensile specimen": "dog-bone",
          "Tensile test type": "direct (uniaxial)", "Compressive strength (MPa)": 69.1, "Tensile strength (MPa)": 4.10,
          "First-cracking strength (MPa)": 1.60, "Tensile strain capacity (%)": 3.77,
          "Source table/page": "Table 2 (mix), Table 3 (ft, fcr, strain), Sec. 3.2 text (fc L0 = 69.1 MPa)",
          "Conversions / notes": "Mix L0 only (control, no FAC/HGM/carbon fiber). kg/m3 / binder 1045.4 (OPC+FA+SF). "
                                 "HRWR dosed as 10 g/L (unit unclear) -> SP/B left empty. Sand = silica sand. "
                                 "VERIFY: fc of L0 taken from the sentence 'compressive strength of L0 decreased from 69.1 MPa to 42.8 MPa' (L1)."})
rows.append(r)

# ---- 2) PE-ECC anti-cavitation (PE-0.5 .. PE-2; PE-0 has no fiber and is skipped)
P = {"Article Name": "Anti-cavitation behaviors and failure mechanism of polyethylene fiber reinforced cementitious composite: The role of fiber content",
     "Author": "Qingshun Nong, Bixiong Li, Zhiwen Wang, Lianghui Li, Baoguo He, Zhibo Zhang, Guiming Wu", "Year": 2025,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2025.143553"}
B = 1408 + 192
# id, PE kg/m3, ft, fcr, strain
mix = [("PE-0.5", 4.9, 9.4, 9.4, 0.048), ("PE-1", 9.7, 9.0, 7.0, 0.9),
       ("PE-1.5", 14.6, 9.6, 5.5, 3.9), ("PE-2", 19.4, 9.0, 4.5, 2.6)]
for mid, pe, ft, fcr, eps in mix:
    r = dict(P)
    vol = round(pe / 970 * 100, 2)  # kg/m3 -> vol% (density 970 kg/m3)
    r.update({"OPC / Cement": round(1408 / B, 3), "SF (Silica fume)": round(192 / B, 3), "W / B": round(320 / B, 3),
              "SS / B (Silica sand)": round(480 / B, 3), "SP / B": round(20 / B, 4), "Binder content (kg/m³)": B,
              "PE fiber (vol%)": vol, "PE length (mm)": 18, "PE diameter (µm)": 26, "PE tensile strength (MPa)": 3100,
              "PE elastic modulus (GPa)": 110, "Total fiber (vol%)": vol,
              "Curing method": "24 h in room 20+-5 °C RH>50 %, demolded, curing room 27 d 20+-2 °C RH>95 %",
              "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1,
              "Test age (days)": 28, "Tensile specimen": "dumbbell (JSCE)", "Tensile gauge length (mm)": 80,
              "Tensile test type": "direct (uniaxial)", "Tensile strength (MPa)": ft, "First-cracking strength (MPa)": fcr,
              "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 2 (mix), Table 4 (fiber), Table 5 (tensile)",
              "Conversions / notes": f"{mid}. kg/m3 / binder 1600 (P.O 52.5 cement 1408 + SF 192). Quartz sand 240+240 = 480 kg/m3 stored as silica sand. "
                                     f"Water-reducing agent 20 kg/m3 -> SP/B; defoamer 8 kg/m3 (not listed). PE {pe} kg/m3 -> {vol} vol% (970 kg/m3). "
                                     "Strain = 'ultimate strain ratio' of Table 5. fc only in Fig. 6 -> left empty."})
    rows.append(r)

# ---- 3) PVA / PP hybrid ECC: keep only mixes with PVA fibers only
P = {"Article Name": "Beyond tensile performance: Efficiency-oriented hybrid fiber design for sustainable Engineered/Strain-Hardening Cementitious Composites (ECC/SHCC)",
     "Author": "Liangwen Wei, Nan Zhang, Bo-Tao Huang, Shin Hau Bong, Xin Qin, Hao Wang", "Year": 2026,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2026.147206"}
# id, total PVA vol%, PVA length, dia, strength, modulus, {age: (fcr, ft, strain)}
t = {"V6-1": (1.0, 6, 12, 1400, 35, {7: (1.5, 1.8, 2.1), 28: (2.2, 2.6, 1.8)}),
     "V6-2": (2.0, 6, 12, 1400, 35, {7: (1.5, 1.9, 2.7), 28: (2.5, 3.0, 2.5)}),
     "V12-1": (1.0, 12, 40, 1560, 41, {7: (2.1, 2.5, 3.3), 28: (2.6, 3.2, 2.7)}),
     "V12-2": (2.0, 12, 40, 1560, 41, {7: (2.5, 3.0, 4.7), 28: (3.7, 4.3, 4.1)}),
     "V6+V12 0.5+0.5": (1.0, None, None, None, None, {7: (1.5, 1.9, 2.7), 28: (2.3, 2.7, 2.3)}),
     "V6+V12 1+1": (2.0, None, None, None, None, {7: (1.7, 2.2, 3.5), 28: (2.8, 3.4, 3.0)})}
idmap = {"V6-1": "V-bar10 (1% PVA6)", "V6-2": "V-bar20 (2% PVA6)", "V12-1": "V10 (1% PVA12)", "V12-2": "V20 (2% PVA12)",
         "V6+V12 0.5+0.5": "V5V-bar5 (0.5% PVA12 + 0.5% PVA6)", "V6+V12 1+1": "V10V-bar10 (1% PVA12 + 1% PVA6)"}
for k, (vol, ln, dia, ts, E, ages) in t.items():
    for age, (fcr, ft, eps) in ages.items():
        r = dict(P)
        r.update({"OPC / Cement": 0.4, "FA (Fly ash)": 0.6, "W / B": 0.3, "Sand (type not stated) / B": 0.36, "SP / B": 0.003,
                  "PVA fiber (vol%)": vol, "PVA length (mm)": ln, "PVA diameter (µm)": dia, "PVA tensile strength (MPa)": ts,
                  "PVA elastic modulus (GPa)": E, "Total fiber (vol%)": vol,
                  "Curing method": "sealed with plastic film 24 h, demolded, curing chamber 20+-2 °C RH 90+-5 % until testing",
                  "Curing time (days)": age, "Curing temperature (°C)": 20, "Curing RH (%)": 90, "Demolding age (days)": 1,
                  "Test age (days)": age, "Tensile specimen": "dumbbell (JC/T 2461)", "Tensile gauge length (mm)": 80,
                  "Tensile test type": "direct (uniaxial)", "Tensile strength (MPa)": ft, "First-cracking strength (MPa)": fcr,
                  "Tensile strain capacity (%)": eps,
                  "Source table/page": "Table 2 (mix), Table 3/4 (tensile), Sec. 3.3, 4.2",
                  "Conversions / notes": f"{idmap[k]}. Binder = cement 0.4 + FA 0.6; sand/binder 0.36, SP (PCE) 0.3 % of binder. "
                                         "Only PVA-only mixes taken (PP and PVA+PP mixes and fiber-free control excluded). "
                                         "fc only in Fig. 4 -> empty."
                                         + (" Hybrid: PVA12 and PVA6 fibers, per-fiber properties left empty." if ln is None else "")})
        rows.append(r)

# ---- 4) SHCC plate paper, material properties (Table 2, Table 3)
P = {"Article Name": "Deflection and thickness threshold of high-strength strain-hardening cementitious composite stay-in-place formwork for modular integrated construction",
     "Author": "Yangqing Liu, Zewen Chen, Xianjun Su, Bo Wu, Jie Yao, Jishen Qiu, Baojun Zhao", "Year": 2025,
     "DOI / URL": "https://doi.org/10.1016/j.engstruct.2025.119798"}
B = 1400 + 74
r = dict(P)
r.update({"OPC / Cement": round(1400 / B, 4), "SF (Silica fume)": round(74 / B, 4), "W / B": round(280 / B, 3),
          "SS / B (Silica sand)": round(589 / B, 3), "SP / B": round(70 / B, 4), "Binder content (kg/m³)": B,
          "PE fiber (vol%)": 2.0, "PE length (mm)": 12, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000,
          "PE elastic modulus (GPa)": 116, "Total fiber (vol%)": 2.0,
          "Curing method": "covered with plastic sheet 24 h, demolded, standard curing room 28 d", "Curing time (days)": 28,
          "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100",
          "Tensile specimen": "dog-bone", "Tensile test type": "direct (uniaxial)", "Compressive strength (MPa)": 118.1,
          "Tensile strength (MPa)": 8.02, "First-cracking strength (MPa)": 4.49, "Tensile strain capacity (%)": 6.65,
          "Source table/page": "Table 2 (mix), Table 3 (properties), Sec. 2.2",
          "Conversions / notes": "kg/m3 / binder 1474 (PC 1400 + SF 74). Silica sand 120-180 um. "
                                 "VERIFY: SP 70 kg/m3 as printed in Table 2 (high; liquid dose?)."})
rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(out, index=False, encoding="utf-8-sig")
print(len(df), "rows ->", out)

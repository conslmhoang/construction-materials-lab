# -*- coding: utf-8 -*-
"""Wave 5 (agent 'geo'): fiber-reinforced geopolymer / alkali-activated composites (EGC, SHGC, AAS-ECC).
Writes ml_spike/additions_v2/w5_geo.csv with the 99-column TEMPLATE header.
Full texts read as HTML text (ScienceDirect OA articles: CSCM, JMRT, Cleaner Materials; MDPI; etc.).

Conventions: binder B = the paper's binder; X / B = mass ratio. NaOH given as a solution of known molarity:
"NaOH / B" = solid NaOH and the solution's water goes into W / B (water inside water glass NOT added), using
NaOH-solution densities from standard tables (CRC): wt% NaOH = 40*M/(1000*rho). Such rows carry VERIFY in notes.
"""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
add_dir = os.path.join(here, "..", "additions")
out_dir = os.path.join(here, "..", "additions_v2")
cols = list(pd.read_csv(os.path.join(add_dir, "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
rows = []
FIBS = ["PE fiber (vol%)", "PVA fiber (vol%)", "Steel fiber (vol%)", "PBO fiber (vol%)"]
WG = "WG / B (Water glass)"
SSM = "SSM / B (Na2SiO3 anhydrous)"
SS = "SS / B (Silica sand)"

# density (g/mL) of NaOH solutions at ~20 °C (CRC Handbook, interpolated)
RHO = {6: 1.20, 8: 1.26, 10: 1.32, 12: 1.37, 14: 1.43, 16: 1.48}


def naoh_split(sol, M):
    """mass of solution -> (solid NaOH, water)"""
    w = 40.0 * M / (1000.0 * RHO[M])
    return sol * w, sol * (1 - w)


def R(x, n=4):
    return None if x is None else round(x, n)


def add(base, **kw):
    r = dict(base)
    r.update(kw)
    for k in r:
        assert k in cols, k
    if not r.get("Total fiber (vol%)"):
        r["Total fiber (vol%)"] = round(sum(float(r.get(k) or 0) for k in FIBS), 4)
    rows.append(r)


def paper(title, authors, year, doi):
    return {"Article Name": title, "Author": authors, "Year": year, "DOI / URL": "https://doi.org/" + doi}

# =====================================================================================
# 1) Yuan et al. 2024, CSCM 20, e02701 - high-calcium vs low-calcium FA EGC (Table 3 mix, Table 4 results)
P = paper("Feasibility study of engineered geopolymer composites based high-calcium fly ash and micromechanics analysis",
          "Zhen Yuan, Zhiming Pang, Cong Lu, Yiming Yao", 2024, "10.1016/j.cscm.2023.e02701")
P.update({"FA (Fly ash)": 0.8, "GGBS": 0.2, SS: 0.2, "Sand max size (µm)": 180, "NaOH molarity (M)": 8,
          "Activator modulus Ms (SiO2/Na2O)": 3.3,
          "PE fiber (vol%)": 2, "PE length (mm)": 12, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000,
          "PE elastic modulus (GPa)": 110,
          "Curing method": "covered with plastic film at room temperature 24 h, demolded, then steam cured 80 °C for 2 days",
          "Curing time (days)": 2, "Curing temperature (°C)": 80, "Heat curing duration (h)": 48, "Demolding age (days)": 1,
          "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
          "Tensile specimen": "dog-bone (JSCE)", "Tensile gauge length (mm)": 80, "Tensile test type": "direct (uniaxial)",
          "Source table/page": "Table 3 (mix), Table 4 (fc, fcr, ft, strain), Sect. 2.1-2.2"})
for mid, fa, ss, sh, fc, fcr, ft, eps in [("L-Na1", "low-Ca FA", 0.225, 0.225, 68.04, 2.69, 5.08, 5.27),
                                          ("L-Na2", "low-Ca FA", 0.30, 0.15, 70.98, 3.94, 5.41, 1.57),
                                          ("H-Na1", "high-Ca FA (CaO 11.2%)", 0.225, 0.225, 74.73, 1.66, 6.53, 8.02)]:
    naoh, w = naoh_split(sh, 8)
    add(P, **{WG: ss, "NaOH / B": R(naoh), "W / B": R(w, 3),
              "Compressive strength (MPa)": fc, "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft,
              "Tensile strain capacity (%)": eps,
              "Conversions / notes": f"{mid}. B = precursor ({fa} 0.8 + GGBS 0.2). Sodium silicate solution/P {ss} (27.3% SiO2, 8.54% Na2O, "
                                     f"modulus 3.3); 8 M NaOH solution/P {sh}. VERIFY: NaOH solid and W/B derived from 8 M solution "
                                     f"(density 1.26 assumed), W/B excludes water-glass water; paper gives water/geopolymer-solids "
                                     f"{0.28 if ss == 0.225 else 0.27}. {'SP (CBMA-150A) used for LFA mixes, dosage not reported. ' if fa.startswith('low') else 'No SP. '}"
                                     f"Test age after steam curing not stated (left blank)."})

# =====================================================================================
# 2) Liu et al. 2025, CSCM 23, e05459 - UEGC with waterglass modulus 1.0-1.6 (Table 3); results in text only for 3 mixes
P = paper("Investigation on the flexural-tensile properties of ultra-high-strength engineered geopolymer composites (UEGC) with varied waterglass modulus",
          "Junxia Liu, Anbang Li, Ran Hai, Cun Hui, Fei Yang, Shiguang Yan", 2025, "10.1016/j.cscm.2025.e05459")
P.update({"FA (Fly ash)": 0.5, "GGBS": 0.5, "W / B": 0.28, SS: 0.30, "Sand max size (µm)": 425,
          "PE fiber (vol%)": 2, "PE diameter (µm)": 15.6,
          "Curing method": "standard curing box 20±2 °C, RH ≥95% for 24 h, demolded, then standard curing to test age",
          "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
          "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
          "Tensile specimen": "dog-bone 330x60x13 (JC/T 2461)", "Tensile gauge length (mm)": 80, "Tensile test type": "direct (uniaxial)"})
NB = ("Paper's binder (Table 3) = FA 0.4 + slag 0.4 + waterglass 0.2, the waterglass being its SOLIDS (companion paper 10.1016/j.cscm.2026.e06485: "
      "waterglass solids = 25% of FA+slag); here B = FA + slag (0.5/0.5), WG solids/B = 0.25, WG solution mass not reported (WG / B blank). "
      "Waterglass (modulus 3.29, 39.8 °Bé) adjusted to the target modulus with NaOH (amount not reported). VERIFY: W/B 0.28 as printed "
      "(basis - paper binder incl. WG solids or FA+slag - not stated). Quartz sand 0.106-0.425 mm, S/B 0.30 as printed. ")
add(P, **{"Activator modulus Ms (SiO2/Na2O)": 1.0, "Tensile strength (MPa)": 5.4, "Tensile strain capacity (%)": 5.8,
          "Source table/page": "Table 3 (mix), Sect. 3.3.3 text (ft, strain)",
          "Conversions / notes": "UEGC-1.0. " + NB + "fc only in Fig. 12 (not entered)."})
add(P, **{"Activator modulus Ms (SiO2/Na2O)": 1.2, "Compressive strength (MPa)": 115.6, "Tensile strength (MPa)": 5.95,
          "Tensile strain capacity (%)": 9.1, "Source table/page": "Table 3 (mix), Abstract & Sect. 3.1.2/3.3.3 text",
          "Conversions / notes": "UEGC-1.2. " + NB + "Also fc 74.9 (3 d) and 87.8 MPa (7 d)."})
add(P, **{"Activator modulus Ms (SiO2/Na2O)": 1.2, "Compressive strength (MPa)": 74.9, "Test age (days)": 3, "Curing time (days)": 3,
          "Source table/page": "Table 3 (mix), Sect. 3.1.2 text", "Conversions / notes": "UEGC-1.2 at 3 d. " + NB})
add(P, **{"Activator modulus Ms (SiO2/Na2O)": 1.2, "Compressive strength (MPa)": 87.8, "Test age (days)": 7, "Curing time (days)": 7,
          "Source table/page": "Table 3 (mix), Sect. 3.1.2 text", "Conversions / notes": "UEGC-1.2 at 7 d. " + NB})
add(P, **{"Activator modulus Ms (SiO2/Na2O)": 1.6, "Tensile strength (MPa)": 3.5, "Tensile strain capacity (%)": 5.6,
          "Source table/page": "Table 3 (mix), Sect. 3.3.3 text (ft, strain)",
          "Conversions / notes": "UEGC-1.6. " + NB + "fc only in Fig. 12 (not entered)."})
# =====================================================================================
# 3) Zahid et al. 2024, JMRT 32, 1772-1787 - one-part FA geopolymer with steel / PVA (mono + hybrid) fibers (Table 3, Table 4)
P = paper("Achieving superior mechanical performance in one-part geopolymer composites through innovative hybrid fiber systems of recycled steel and PVA fibers",
          "Muhammad Zahid, M. Iqbal Khan, Nasir Shafiq, Yassir M. Abbas, Jamal M. Khatib", 2024, "10.1016/j.jmrt.2024.08.002")
P.update({"FA (Fly ash)": 1.0, SSM: 0.12, "W / B": R(0.24 * 1.12, 3),
          "Curing method": "in mould 1 day at laboratory conditions, demolded, then cured at room temperature (air) to 28 d",
          "Curing time (days)": 28, "Demolding age (days)": 1, "Test age (days)": 28,
          "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
          "Source table/page": "Table 2 (fibers), Table 3 (mix), Table 4 (fc)"})
STEEL = {"S": dict(L=20, d=200, ts=2300, E=200, name="straight"), "H": dict(L=20, d=200, ts=2300, E=200, name="hooked-end"),
         "W": dict(L=None, d=None, ts=None, E=200, name="recycled tire wire (10-35 mm, 0.2-0.4 mm, 1750-2300 MPa)")}
PVA = {"TK": dict(L=18, d=200, ts=1000, E=27, name="thick PVA"), "TN": dict(L=12, d=40, ts=1600, E=41, name="thin PVA")}
NZ = ("B = high-calcium fly ash (CaO 19%). Anhydrous sodium metasilicate (Na2O 50-51%, SiO2 46%) 0.12 of FA. "
      "VERIFY: W/B = W/GP-solids 0.24 x (FA + SSM)/FA = 0.269 (derived). No aggregate. Fibers 2 vol% total. ")
for mid, fc in [("S2", 58), ("H2", 55), ("W2", 53), ("TK2", 47), ("TN2", 42), ("S1H1", 55), ("S1W1", 56), ("S1TK1", 52),
                ("S1TN1", 45), ("H1W1", 52), ("H1TK1", 49), ("H1TN1", 45), ("W1TK1", 49), ("W1TN1", 44), ("TK1TN1", 46)]:
    import re
    parts = re.findall(r"(TK|TN|S|H|W)(\d)", mid)
    kw = {"Compressive strength (MPa)": fc}
    st = [k for k, v in parts if k in STEEL]; pv = [k for k, v in parts if k in PVA]
    sv = sum(int(v) for k, v in parts if k in STEEL); pvv = sum(int(v) for k, v in parts if k in PVA)
    if sv:
        kw["Steel fiber (vol%)"] = sv
        if len(st) == 1:
            s = STEEL[st[0]]
            kw.update({"Steel length (mm)": s["L"], "Steel diameter (µm)": s["d"], "Steel tensile strength (MPa)": s["ts"],
                       "Steel elastic modulus (GPa)": s["E"]})
        else:
            kw["Steel elastic modulus (GPa)"] = 200
    if pvv:
        kw["PVA fiber (vol%)"] = pvv
        if len(pv) == 1:
            p = PVA[pv[0]]
            kw.update({"PVA length (mm)": p["L"], "PVA diameter (µm)": p["d"], "PVA tensile strength (MPa)": p["ts"],
                       "PVA elastic modulus (GPa)": p["E"]})
    desc = " + ".join(f"{v}% {(STEEL.get(k) or PVA.get(k))['name']}" for k, v in parts)
    kw["Conversions / notes"] = f"{mid}: {desc}. " + NZ + ("Hybrid of two fiber types in one column: geometry left blank. " if (len(st) > 1 or len(pv) > 1) else "") \
        + "Flexural tests only (no direct tension). Control GP (no fiber, 49 MPa) not entered."
    add(P, **kw)
# =====================================================================================
# 4) Xie 2025, Cleaner Materials 18, 100345 - biochar EGC; only the biochar-free control EGC qualifies (Table 3, Table 4)
P = paper("Effects of biochar on the shrinkage and mechanical properties of sustainable engineered geopolymer composites: A comparative study between biochar sources, pyrolysis temperatures, and particle sizes",
          "Yuekai Xie", 2025, "10.1016/j.clema.2025.100345")
B = 585 + 390
naoh, wsh = naoh_split(117, 8)
add(P, **{"GGBS": R(585 / B), "FA (Fly ash)": R(390 / B), "Binder content (kg/m³)": B, SS: R(585 / B), "Sand max size (µm)": 300,
          WG: R(293 / B), "NaOH / B": R(naoh / B), "NaOH molarity (M)": 8, "Activator modulus Ms (SiO2/Na2O)": 2.05,
          "W / B": R((91 + wsh) / B, 3), "Extra water / B": R(91 / B), "SP / B": R(9.8 / B),
          "PE fiber (vol%)": 2, "PE length (mm)": 12, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 116,
          "Curing method": "air curing 23±3 °C, RH 55±5% for 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 23,
          "Curing RH (%)": 55, "Test age (days)": 28,
          "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
          "Tensile specimen": "dog-bone 366x80x20 (30x20 gauge section)", "Tensile gauge length (mm)": 100, "Tensile test type": "direct (uniaxial)",
          "Compressive strength (MPa)": 81.9, "First-cracking strength (MPa)": 3.483, "Tensile strength (MPa)": 5.901,
          "Tensile strain capacity (%)": 8.83,
          "Source table/page": "Table 3 (mix, kg/m3), Table 4 (tension), Sect. 3.4.1 text (fc 81.9 MPa)",
          "Conversions / notes": "Control EGC (biochar-free); biochar mixes excluded (biochar not allowed). kg/m3 / (GGBFS 585 + FA 390). "
                                 "Sodium silicate solution 293 (44.1% solids, Ms 2.05), 8 M NaOH solution 117, water 91, PCE SP 9.8, PE 19.4 kg/m3 = 2 vol%. "
                                 "VERIFY: NaOH solid / its water from 8 M solution (density 1.26 assumed); W/B = (91 + NaOH-solution water)/B, "
                                 "water-glass water excluded. Natural silica sand <300 µm."})
# =====================================================================================
# 5) Ahmed, Atmaca, Khoshnaw 2024, CSCM 20, e02863 - recycled brick powder EGC; only the brick-free controls qualify
P = paper("Building a sustainable future: An experimental study on recycled brick waste powder in engineered geopolymer composites",
          "Junaid K. Ahmed, Nihat Atmaca, Ganjeena J. Khoshnaw", 2024, "10.1016/j.cscm.2024.e02863")
naoh, wsh = naoh_split(0.094, 10)
P.update({WG: 0.235, "NaOH / B": R(naoh), "NaOH molarity (M)": 10, "Activator modulus Ms (SiO2/Na2O)": 2.65, SS: 0.2,
          "PVA fiber (vol%)": 2, "PVA length (mm)": 12, "PVA diameter (µm)": 40,
          "Curing method": "sealed in nylon bags at room temperature 24 h, oven heat curing 70 °C for 24 h, then room temperature to 28 d",
          "Curing time (days)": 28, "Curing temperature (°C)": 70, "Heat curing duration (h)": 24, "Test age (days)": 28,
          "Tensile specimen": "dog-bone", "Tensile test type": "direct (uniaxial)"})
NA = ("Activator: 10 M NaOH solution 0.094 + sodium silicate solution 0.235 (Ms 2.65; 34.4% SiO2, 13% Na2O, 52% H2O) per binder. "
      "VERIFY: NaOH solid/water from 10 M solution (density 1.32 assumed); W/B = NaOH-solution water + extra water (Table 2), WG water excluded. ")
add(P, **{"FA (Fly ash)": 1.0, "W / B": R(wsh, 3), "Compressive strength (MPa)": 34.5, "First-cracking strength (MPa)": 1.59,
          "Tensile strength (MPa)": 2.8, "Tensile strain capacity (%)": 4.19,
          "Source table/page": "Table 2 (mix), Table 4 (tension), Sect. 4 text (fc: 71.13 MPa = +106% over control)",
          "Conversions / notes": "Mix 100 F+0B (control, no brick powder). " + NA + "No extra water, no HRWR. Table 3 lists total W/B 0.19 (consistent with incl. WG water). "
                                 "VERIFY: fc 34.5 MPa = lower bound of the reported range 34.5-71.13 MPa, and 71.13 = +106% of control."})
add(P, **{"GGBS": 1.0, "W / B": R(wsh + 0.109, 3), "Extra water / B": 0.109, "SP / B": 0.054,
          "Compressive strength (MPa)": 127.39, "First-cracking strength (MPa)": 5.42, "Tensile strength (MPa)": 5.51,
          "Tensile strain capacity (%)": 1.03,
          "Source table/page": "Table 2 (mix), Table 5 (tension), Sect. 4 text (fc 127.39 MPa)",
          "Conversions / notes": "Mix 100 S+0B (control, no brick powder). " + NA + "Naphthalene-based HRWR 0.054 and extra water 0.109 (Table 2). "
                                 "VERIFY: Table 3 gives SP 6.0% and W/B 0.24 for this mix, inconsistent with Table 2 (0.054 / 0.109)."})
# =====================================================================================
# 6) Choi, Kim, Lee 2020, Applied Sciences 10, 4300 - Ca(OH)2/Na2SO4-activated slag PE composite (Table 1, Sect. 3.1 text)
P = paper("Mechanical and Fiber-Bridging Behavior of Slag-Based Composite with High Tensile Ductility",
          "Jeong-Il Choi, Hyeong-Ki Kim, Bang Yeon Lee", 2020, "10.3390/app10124300")
add(P, **{"GGBS": 0.895, "Ca(OH)2 / B": 0.075, "Na2SO4 / B": 0.030, "W / B": 0.30, "SP / B": 0.005, "VMA / B": 0.002,
          "PE fiber (vol%)": 1.5, "PE length (mm)": 18, "PE diameter (µm)": 12, "PE tensile strength (MPa)": 2700, "PE elastic modulus (GPa)": 88,
          "Curing method": "covered with plastic sheet in moulds 23±3 °C, 60% RH for 2 d, then water 23±3 °C to 28 d",
          "Curing time (days)": 28, "Curing temperature (°C)": 23, "Demolding age (days)": 2, "Test age (days)": 28,
          "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
          "Tensile specimen": "dumbbell (JSCE), 30x13 mm gauge section", "Tensile gauge length (mm)": 80, "Tensile test type": "direct (uniaxial)",
          "Compressive strength (MPa)": 36.8, "First-cracking strength (MPa)": 3.4, "Tensile strength (MPa)": 8.5,
          "Tensile strain capacity (%)": 7.5, "Source table/page": "Table 1 (mix), Sect. 3.1 text / Table 3 (results)",
          "Conversions / notes": "Binder = GGBS 0.895 + Ca(OH)2 0.075 + Na2SO4 0.030 (paper's binder, powders >95% purity). "
                                 "Ratios per that binder: water 0.30, PCE SP 0.005, VMA 0.002, anti-foam 0.001 (defoamer, not a column). No sand."})
# =====================================================================================
# 7) Wang, Xu, Yang 2026, CivilEng 7, 66 - FA-based PVA-EGC, ambient vs 60 °C (2/4/6 h) curing, 3/7/28 d (Table 3, Tables 4-6)
P = paper("The Preparation of the Engineered Geopolymer Composites and Their Tensile Strain Capacity Research",
          "Qiwei Wang, Chao Xu, Dingtao Yang", 2026, "10.3390/civileng7040066")
B = 44.3 + 11.1
P.update({"FA (Fly ash)": 1.0, WG: R(14.1 / B), "NaOH / B": R(3.1 / B), "W / B": R(10.8 / B, 3), "Extra water / B": R(10.8 / B),
          "Sand (type not stated) / B": R(16.7 / B),
          "PVA fiber (vol%)": 2, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 42.8,
          "Demolding age (days)": 1, "Curing temperature (°C)": 20, "Curing RH (%)": 60,
          "Tensile specimen": "dumbbell", "Tensile gauge length (mm)": 80, "Tensile test type": "direct (uniaxial)"})
NW = ("B = low-Ca FA 44.3 + high-Ca FA 11.1 (wt% of mix, Table 3) -> FA 1.0 (LFA 0.8 / HFA 0.2). Water glass 14.1, NaOH 3.1, water 10.8, "
      "sand 16.7 wt% divided by B. VERIFY: Table 3 column is labelled 'Na2SiO3' but the text says water glass (solution) - entered as WG; "
      "NaOH taken as solid (activator prepared from NaOH + water + water glass). Tensile values = averages of 3. No compressive test. ")
res = {"R": {3: (0.94, 2.8), 7: (2.36, 4.11), 28: (3.11, 4.55)},
       "T60-2": {3: (1.22, 3.65), 7: (2.31, 4.06), 28: (3.1, 3.7)},
       "T60-4": {3: (2.4, 3.49), 7: (3.38, 3.6), 28: (3.83, 3.76)},
       "T60-6": {3: (3.62, 4.19), 7: (4.13, 3.9), 28: (4.2, 4.05)}}
for reg, d in res.items():
    for age, (ft, eps) in d.items():
        kw = {"Test age (days)": age, "Curing time (days)": age, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": f"Table 3 (mix), Table {4 if age == 3 else 5 if age == 7 else 6} (tension)"}
        if reg == "R":
            kw["Curing method"] = "sealed with plastic film 24 h, demolded, then laboratory air 20±2 °C, RH 60±5% to test age"
        else:
            h = int(reg.split("-")[1])
            kw.update({"Curing method": f"sealed 24 h, demolded, oven 60 °C for {h} h, then laboratory air 20±2 °C, RH 60±5% to test age",
                       "Heat curing duration (h)": h, "Curing temperature (°C)": 60})
        kw["Conversions / notes"] = f"{reg}, {age} d. " + NW
        add(P, **kw)
# =====================================================================================
# 8) Zhang et al. 2024, Buildings 14, 449 - highly flowable FA/slag geopolymer with 0.1-0.2 vol% PVA (Table 3 mix, Table 5 fc)
P = paper("Mechanical Properties and Microstructure of Highly Flowable Geopolymer Composites with Low-Content Polyvinyl Alcohol Fiber",
          "Hongmei Zhang, Fan Hu, Yuanfeng Duan, Jian Liao, Jiaqi Yang", 2024, "10.3390/buildings14020449")
B = 80.2 + 641.6 + 80.2
P.update({"GGBS": R(80.2 / B), "FA (Fly ash)": R(641.6 / B), "SF (Silica fume)": R(80.2 / B), "Binder content (kg/m³)": B,
          SS: R(962.4 / B), WG: R(270.8 / B), "NaOH / B": R(24.3 / B), "Activator modulus Ms (SiO2/Na2O)": 1.5,
          "W / B": R(104.3 / B, 3), "Extra water / B": R(104.3 / B), "PVA length (mm)": 6,
          "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7",
          "Source table/page": "Table 3 (mix, kg/m3), Table 5 (cube fc 3 d / 28 d)"})
NZ2 = ("kg/m3 / (slag 80.2 + FA 641.6 + SF 80.2). Quartz sand 962.4, aqueous sodium silicate 270.8 (modulus adjusted to 1.5 with NaOH), "
       "NaOH granules 24.3 (solid), water 104.3. W/B excludes water-glass water. Curing regime not stated in the text (left blank). "
       "Dog-bone tension results only in figures (not entered); fiber-free control not entered.")
for vf, kg, fc3, fc28 in [(0.1, 1.29, 21.66, 49.12), (0.15, 1.935, 22.04, 50.04), (0.2, 2.58, 21.04, 47.56)]:
    for age, fc in [(3, fc3), (28, fc28)]:
        add(P, **{"PVA fiber (vol%)": vf, "Test age (days)": age, "Compressive strength (MPa)": fc,
                  "Conversions / notes": f"PVA {vf} vol% ({kg} kg/m3). " + NZ2})
# =====================================================================================
# 9) Wang et al. 2025, Buildings 15, 3792 - PVA-EGC under sustained 60 °C; only the standard-cured (T20-28d) rows entered (Table 2, Table 3)
P = paper("Study on Engineering Geopolymer Composites (EGCs) Under Sustained Thermal Environment: Linking Strain-Hardening Characteristics, Static/Impact Load Mechanical Properties, and Evolution Mechanism",
          "Shuo Wang, Wei Wang, Haoxing Liu, Ao Huang, Hongqiang Ma", 2025, "10.3390/buildings15203792")
P.update({"Na2O / B": 0.06, "Activator modulus Ms (SiO2/Na2O)": 1.3, "Mixing liquid / B": 0.3, SS: 0.3,
          "PVA fiber (vol%)": 2, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1560, "PVA elastic modulus (GPa)": 41,
          "Curing method": "covered with plastic wrap in standard curing chamber 20±2 °C, RH 95% for 24 h, demolded, standard curing to 28 d",
          "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
          "Source table/page": "Table 2 (mix), Table 3 (quasi-static compressive strength, T20-28d)"})
NW9 = ("Activator = NaOH (analytical grade) + sodium silicate solution (modulus 3.22) dosed as Na2O 6% of binder at modulus 1.3; "
       "liquid-solid ratio 0.3 entered as Mixing liquid / B (NaOH/WG split and WG composition not reported). Sustained-60 °C rows excluded. "
       "Quasi-static compressive strength (specimen: 50 mm cube or 50x50 cylinder, not specified for this test). Tension only in figures.")
add(P, **{"FA (Fly ash)": 0.5, "GGBS": 0.5, "Compressive strength (MPa)": 78.5, "Conversions / notes": "S50-6 (FA 50 / slag 50). " + NW9})
add(P, **{"GGBS": 1.0, "Compressive strength (MPa)": 88.3, "Conversions / notes": "S100-6 (slag 100). " + NW9})
# =====================================================================================
# 10) Kan et al. 2024, CSCM 21, e03306 - ambient-cured slag/SF AAFRC with PE, 1/28/365 d (Table 1, Table 4, text fc)
P = paper("Long-term behaviors of fiber reinforced alkali-activated composite cured at ambient condition: Mechanical characterization",
          "Lili Kan, Benrui Chen, Jiabao Zhai, Lanqing Dai, Fei Wang, Mingfeng Xu, Pingjiang Bai", 2024, "10.1016/j.cscm.2024.e03306")
B = 0.89 + 0.21
P.update({"GGBS": R(0.89 / B), "SF (Silica fume)": R(0.21 / B), "River sand / B": R(0.29 / B), WG: R(0.14 / B), "NaOH / B": R(0.03 / B),
          "Activator modulus Ms (SiO2/Na2O)": 3.3, "W / B": R(0.30 / B, 3), "Extra water / B": R(0.30 / B),
          "PE fiber (vol%)": 2, "PE length (mm)": 12, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 110,
          "Curing method": "wrapped in plastic film at room temperature 24 h, demolded, then air (ambient) curing to test age",
          "Demolding age (days)": 1, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
          "Tensile specimen": "dumbbell", "Tensile test type": "direct (uniaxial)",
          "Source table/page": "Table 1 (mix), Table 4 (tension), Sect. 3 text (fc)"})
NK = ("Table 1 (labelled wt%) lists GGBS 0.89, SF 0.21, sand 0.29, water glass (modulus 3.3) 0.14, NaOH particles 0.03, water 0.30. "
      "VERIFY: GGBS + SF = 1.10 (possible typo for SF 0.11); B taken as GGBS + SF as printed and all ratios divided by 1.10. "
      "River sand 0.1-1 mm. W/B excludes water-glass water.")
for age, fc, ft, eps, fcr in [(1, 34.62, 2.66, 2.59, 1.31), (28, 74.9, 4.95, 4.10, 2.74), (365, 74.4, 7.75, 4.51, 2.59)]:
    add(P, **{"Curing time (days)": age, "Test age (days)": age, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft,
              "Tensile strain capacity (%)": eps, "First-cracking strength (MPa)": fcr, "Conversions / notes": f"{age} d. " + NK})

# =====================================================================================
# 11) Liu, Yan, Chu, Wang 2026, CSCM, e06485 - HS-EGC with FA/slag 70/30-40/60 (Table 3 mix, Table 4 fc 3/7/28 d)
P = paper("The bending deformation behavior and its geometry effect of high-strength engineered geopolymer composites with varying slag and fly ash dosages",
          "Junxia Liu, Shiguang Yan, Jinyi Chu, Jinyan Wang", 2026, "10.1016/j.cscm.2026.e06485")
P.update({"Activator modulus Ms (SiO2/Na2O)": 1.2, "W / B": 0.28, SS: 0.30, "Sand max size (µm)": 425,
          "PE fiber (vol%)": 2, "PE length (mm)": 12, "PE diameter (µm)": 22, "PE tensile strength (MPa)": 3360, "PE elastic modulus (GPa)": 115,
          "Curing method": "24 h at room temperature, demolded, sealed with plastic film, curing box 20±2 °C, RH 95% to test age",
          "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1,
          "Compressive specimen": "cube", "Source table/page": "Table 3 (mix), Table 4 (fc), Sect. 2.1-2.2"})
N11 = ("B = FA + slag. Activator = waterglass (modulus 3.29, 39.8 °Bé) adjusted with NaOH (97%) to modulus 1.2; waterglass SOLIDS = 25% of "
       "FA+slag (WG solution mass not reported, WG / B blank). VERIFY: W/B 0.28 as printed (basis not stated). Quartz sand 106-425 µm. "
       "Only flexural (no direct tension) tests. FA50S50 has the same fc as UEGC-1.2 of 10.1016/j.cscm.2025.e05459 (same group/mix).")
for mid, fa, fcs in [("FA70S30", 0.7, (51.6, 70.3, 80.8)), ("FA60S40", 0.6, (55.7, 84.6, 102.0)),
                     ("FA50S50", 0.5, (74.9, 87.8, 115.6)), ("FA40S60", 0.4, (89.0, 94.1, 110.5))]:
    for age, fc in zip((3, 7, 28), fcs):
        add(P, **{"FA (Fly ash)": fa, "GGBS": R(1 - fa), "Curing time (days)": age, "Test age (days)": age,
                  "Compressive strength (MPa)": fc, "Conversions / notes": f"{mid}, {age} d. " + N11})

# =====================================================================================
# 12) Cheng, Chen, Cao, Zhao 2023, CSCM 18, e01919 - AAS mortar with steel fibre; only unheated (20 °C) rows of fibre mixes (Tables 3-5)
P = paper("Effect of steel fibre and manufactured sand on mechanical properties of alkali-activated slag green cementitious material after high temperature",
          "Hao Cheng, Pang Chen, Shaojun Cao, Wenzhong Zhao", 2023, "10.1016/j.cscm.2023.e01919")
B = 625
P.update({"GGBS": 1.0, "Binder content (kg/m³)": B, WG: R(164 / B), "NaOH / B": R(27.8 / B), "Activator modulus Ms (SiO2/Na2O)": 1.7,
          "W / B": R(183.7 / B, 3), "Extra water / B": R(183.7 / B), "River sand / B": R(1250 / B),
          "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2969, "Steel elastic modulus (GPa)": 200,
          "Curing method": "standard curing room (20 °C) for 60 d; reference (unheated, 20 °C) specimens",
          "Curing time (days)": 60, "Curing temperature (°C)": 20, "Test age (days)": 60,
          "Compressive specimen": "cube", "Compressive specimen size (mm)": "100",
          "Tensile specimen": "dumbbell (axial tension)", "Tensile test type": "direct (uniaxial)",
          "Source table/page": "Table 3 (mix, kg/m3), Table 4 (fc, 20 °C column), Table 5 (ft, 20 °C column)"})
N12 = ("kg/m3 / slag 625. Sodium silicate solution 164 (56% water, Ms 1.7), solid NaOH 27.8 (98%), water 183.7, natural river sand 1250 "
       "(FM 2.54). W/B excludes water-glass water (paper's W/B 0.44 includes it). Only the 20 °C (unheated) results entered; heated rows and "
       "fibre-free / manufactured-sand controls not entered. VERIFY: test age taken as 60 d (standard curing 60 d before testing; abstract mentions 28-day strength).")
for mid, vf, fc, ft in [("N-0.5", 0.5, 70.3, 2.85), ("N-1.0", 1.0, 79.3, 2.9), ("N-1.5", 1.5, 81.1, 3.78)]:
    add(P, **{"Steel fiber (vol%)": vf, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft,
              "Conversions / notes": f"{mid}: steel fibre {vf} vol% ({round(78.5 * vf, 2)} kg/m3). " + N12})

# =====================================================================================
# write (drop DOIs already in existing_dois.txt or in other agents' w5 files)
import glob
df = pd.DataFrame(rows).reindex(columns=cols)
taken = set(l.strip().lower() for l in open(os.path.join(out_dir, "existing_dois.txt"), encoding="utf-8") if l.strip())
for f in glob.glob(os.path.join(out_dir, "w5_*.csv")) + glob.glob(os.path.join(out_dir, "w5_*_rejected.txt")):
    if os.path.basename(f).startswith("w5_geo"):
        continue
    txt = open(f, encoding="utf-8-sig", errors="ignore").read().lower()
    taken |= {d for d in df["DOI / URL"].str.replace("https://doi.org/", "").str.lower() if d in txt}
key = df["DOI / URL"].str.replace("https://doi.org/", "").str.lower()
dropped = sorted(set(key[key.isin(taken)]))
if dropped:
    print("dropped (already taken):", dropped)
df = df[~key.isin(taken)]
df.to_csv(os.path.join(out_dir, "w5_geo.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows,", df["DOI / URL"].nunique(), "papers ->", os.path.join(out_dir, "w5_geo.csv"))

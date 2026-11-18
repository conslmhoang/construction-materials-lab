"""Wave 7, agent w7d: Bang Yeon Lee lab papers 044, 045, 050 (HDFRC mix only), 054, 075 (L1-L3, L5).
Writes ml_spike/additions_v2/w7_w7d.csv (99-column TEMPLATE header).
Binder convention (as in paper_news_2026_11.py): GGBS column = GGBS share of the paper's binder (AAS = GGBS + activator = 1),
activator given as 'X / B' of that same binder.
"""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
cols = list(pd.read_csv(os.path.join(here, "..", "additions", "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
out = os.path.join(here, "..", "additions_v2", "w7_w7d.csv")
rows = []

PE18 = {"PE length (mm)": 18, "PE diameter (µm)": 12, "PE tensile strength (MPa)": 2700, "PE elastic modulus (GPa)": 88}
CUBE = {"Compressive specimen": "cube", "Compressive specimen size (mm)": "50"}
DB = {"Tensile specimen": "dog-bone (JSCE)", "Tensile gauge length (mm)": 80, "Tensile test type": "direct (uniaxial)"}
SSM_NOTE = "Na2SiO3 powder: hydration state not stated, entered as anhydrous SSM. "

# ---------------- 044 (Table 1, 3, 4, 5)
P44 = {"Article Name": "Mechanical properties and self-healing capacity of eco-friendly ultra-high ductile fiber-reinforced slag-based composites",
       "Author": "Huy Hoàng Nguyễn, Jeong-Il Choi, Hyeong-Ki Kim, Bang Yeon Lee", "Year": 2019,
       "DOI / URL": "https://doi.org/10.1016/j.compstruct.2019.111401"}
m44 = [("PE-S-Ca", "Ca(OH)2 / B", 0.002, 42.8, (3.03, 7.47, 7.22), (3.05, 7.67, 8.75)),
       ("PE-S-Na", "NaOH / B", 0.003, 33.2, (2.86, 4.83, 7.94), (2.99, 6.08, 8.26)),
       ("PE-S-NaS", "SSM / B (Na2SiO3 anhydrous)", 0.003, 45.0, (3.05, 6.54, 7.20), (3.21, 6.82, 6.37))]
for mid, act, sp, fc, t7, t28 in m44:
    for age, t in ((7, t7), (28, t28)):
        r = dict(P44); r.update(PE18); r.update(CUBE); r.update(DB)
        r.update({"GGBS": 0.9, act: 0.1, "W / B": 0.3, "SP / B": sp, "VMA / B": 0.001,
                  "PE fiber (vol%)": 1.75, "Total fiber (vol%)": 1.75,
                  "Curing method": "covered with plastic sheet in air 23 °C ± 3 for ~2 d, demolded, then water tank until test",
                  "Curing time (days)": age, "Curing temperature (°C)": 23, "Demolding age (days)": 2, "Test age (days)": age,
                  "Compressive strength (MPa)": fc if age == 28 else None,
                  "First-cracking strength (MPa)": t[0], "Tensile strength (MPa)": t[1], "Tensile strain capacity (%)": t[2],
                  "Source table/page": "Table 1 (mix), Table 3 (fiber), Table 4 (fc 28 d), Table 5 (tension 7 and 28 d), Sec 2.1-2.3 (curing)",
                  "Conversions / notes": f"{mid}. Binder = GGBS 0.90 + activator 0.10 (10 wt% of binder). Deformer 0.001 (defoamer) not a column. "
                  f"Activators in powder form except NaOH (dissolved in mixing water, W/B 0.3 as listed). "
                  f"{SSM_NOTE if act.startswith('SSM') else ''}"
                  f"{'Compressive strength only measured at 28 d, empty in 7 d row. ' if age == 7 else ''}"
                  f"Ultimate tensile strength from Table 5."})
        rows.append(r)

# ---------------- 045 (Table 1, 3, 4)
P45 = {"Article Name": "Effects of the type of activator on the self-healing ability of fiber-reinforced alkali-activated slag-based composites at an early age",
       "Author": "Huy Hoàng Nguyễn, Jeong-Il Choi, Hyeong-Ki Kim, Bang Yeon Lee", "Year": 2019,
       "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2019.07.113"}
m45 = [("AAS-Ca", "Ca(OH)2 / B", 0.002, 38.44, 2.62, 6.13, 6.33),
       ("AAS-Na", "NaOH / B", 0.003, 43.83, 3.27, 6.56, 5.11),
       ("AAS-NaS", "SSM / B (Na2SiO3 anhydrous)", 0.002, 30.58, 2.26, 5.34, 7.26)]
for mid, act, sp, fc, fcr, ft, eps in m45:
    base = dict(P45); base.update(PE18)
    base.update({"GGBS": 0.95, act: 0.05, "W / B": 0.3, "SP / B": sp, "VMA / B": 0.001,
                 "PE fiber (vol%)": 1.75, "Total fiber (vol%)": 1.75,
                 "Curing method": "covered with plastic sheet in air 23 °C ± 3 for 2 d, demolded, then water immersion until test",
                 "Curing temperature (°C)": 23, "Demolding age (days)": 2,
                 "Source table/page": "Table 1 (mix), Table 3 (fiber), Table 4 (fc 28 d; tension 7 d), Sec 2.2-2.3 (curing, ages)"})
    note = (f"{mid}. Binder = GGBS 0.95 + activator 0.05 (5 wt% of binder). Deformer 0.001 (defoamer) not a column. "
            f"{SSM_NOTE if act.startswith('SSM') else ''}")
    r = dict(base); r.update(CUBE)
    r.update({"Curing time (days)": 28, "Test age (days)": 28, "Compressive strength (MPa)": fc,
              "Conversions / notes": note + "Compressive test at 28 d; tension in this paper only at 7 d, so no tension values in this row."})
    rows.append(r)
    r = dict(base); r.update(DB)
    r.update({"Curing time (days)": 7, "Test age (days)": 7, "First-cracking strength (MPa)": fcr,
              "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Conversions / notes": note + "Tension at 7 d (Table 4); compressive strength was measured at 28 d only (see 28 d row)."})
    rows.append(r)

# ---------------- 050 (HDFRC only; UHPFRC rejected: expansive admixture + SRA)
r = {"Article Name": "Response of UHPFRC and HDFRC under static and high-velocity projectile impact loads",
     "Author": "Gyu-Yong Kim, Jeong-Il Choi, Se-Eon Park, Hongseop Kim, Yun Lee, Bang Yeon Lee", "Year": 2018,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2018.08.135"}
r.update(PE18); r.update(CUBE); r.update(DB)
r.update({"GGBS": 0.895, "Ca(OH)2 / B": 0.075, "Na2SO4 / B": 0.030, "W / B": 0.32, "SP / B": 0.013,
          "PE fiber (vol%)": 1.75, "Total fiber (vol%)": 1.75,
          "Curing method": "in air 23 °C ± 3 for 2 d, demolded, then water 23 °C ± 3 until 28 d",
          "Curing time (days)": 28, "Curing temperature (°C)": 23, "Demolding age (days)": 2, "Test age (days)": 28,
          "Compressive strength (MPa)": 32.9, "First-cracking strength (MPa)": 3.36, "Tensile strength (MPa)": 8.27,
          "Tensile strain capacity (%)": 7.89,
          "Source table/page": "Table 1 (mix), Table 3 (fiber), Table 5 (fc), Table 6 (tension), Sec 2.1-2.3 (curing, tests)",
          "Conversions / notes": "HDFRC. VERIFY: Table 1 gives AAS = 1 (binder), w/b 0.32, SP 0.013, defoamer 0.001, no sand/filler; text gives Ca(OH)2 = 8.38 wt% "
          "and Na2SO4 = 3.35 wt% of the slag. Read as AAS = slag + activators: slag 0.895, Ca(OH)2 0.075, Na2SO4 0.030 per unit AAS "
          "(0.075/0.895 = 8.38%, 0.030/0.895 = 3.35%, exact match). Binder fraction columns therefore sum to 0.895 (activators as X/B)."})
rows.append(r)

# ---------------- 054 (Table 2, 3)
P54 = {"Article Name": "Self-healing properties of cement-based and alkali-activated slag-based fiber-reinforced composites",
       "Author": "Huy Hoàng Nguyễn, Jeong-Il Choi, Keum-Il Song, Jin-Kyu Song, Jungwon Huh, Bang Yeon Lee", "Year": 2018,
       "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2018.01.023"}
m54 = [("C30", {"OPC / Cement": 1.0}, 0.001, 0.001, 86.3, 3.10, 8.17, 2.66, "Cement binder = 1."),
       ("S30", {"GGBS": 0.9, "Ca(OH)2 / B": 0.1}, 0.003, 0.0004, 46.1, 1.91, 8.55, 5.46,
        "VERIFY: AAS binder = 1 = GGBS + Ca(OH)2; Ca(OH)2 is 11.1 wt% of GGBS (text) -> GGBS 0.9, Ca(OH)2 0.1 per unit binder (0.1/0.9 = 11.1%).")]
for mid, comp, sp, vma, fc, fcr, ft, eps, nt in m54:
    r = dict(P54); r.update(PE18); r.update(CUBE); r.update(DB); r.update(comp)
    r.update({"W / B": 0.3, "SP / B": sp, "VMA / B": vma,
              "PE fiber (vol%)": 1.75, "Total fiber (vol%)": 1.75,
              "Curing method": "covered with plastic sheet in air 23 °C ± 3 for 2 d, demolded, then water 23 °C ± 3 until 28 d",
              "Curing time (days)": 28, "Curing temperature (°C)": 23, "Demolding age (days)": 2, "Test age (days)": 28,
              "Compressive strength (MPa)": fc, "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft,
              "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 2 (mix), Sec 2.1 (fiber, activator), Table 3 (fc, tension), Sec 2.2-2.3 (curing, tests)",
              "Conversions / notes": f"{mid}. {nt} Anti-foaming agent 0.001 (not a column). SP, VMA in powder form."})
    rows.append(r)

# ---------------- 075 (Table 2, 3; L4 rejected: text contradicts Table 3)
P75 = {"Article Name": "Experiments and performances of strain-hardening fiber low cementitious composites",
       "Author": "Cho et al.", "Year": 2015, "DOI / URL": "https://doi.org/10.1177/1687814015585420"}
m75 = [("L1", 1.0, 0, 0, 0.40, 72.5, 2.94, 3.99, 2.32, 0.003),
       ("L2", 0.4, 0.6, 0, 0.35, 82.4, 3.72, 4.70, 2.22, 0.002),
       ("L3", 0.4, 0.6, 0, 0.40, 81.5, 3.57, 4.52, 3.05, 0.002),
       ("L5", 0.4, 0, 0.6, 0.40, 23.2, 2.31, 3.30, 4.79, 0.003)]
for mid, c, g, f, wb, fc, fcr, ft, eps, adm in m75:
    r = dict(P75)
    r.update({"PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1620,
              "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": 2.0})
    r.update({"OPC / Cement": c, "GGBS": g or None, "FA (Fly ash)": f or None, "SS / B (Silica sand)": 0.4, "W / B": wb,
              "Curing method": "covered with plastic sheet in air 23 °C ± 3 for 1 d, demolded, then water 23 °C ± 3 until 28 d",
              "Curing time (days)": 28, "Curing temperature (°C)": 23, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
              "Tensile specimen": "dog-bone", "Tensile test type": "direct (uniaxial)",
              "Compressive strength (MPa)": fc, "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft,
              "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 2 (mix, fc), Table 3 (tension), text sections Low cement binder / Mixing (fiber, curing)",
              "Conversions / notes": f"{mid}. Sand = quartz sand, S/B 0.4. Admixtures (SP + methyl cellulose + deformer) given only as one total "
              f"{adm} of binder, so SP/B and VMA/B left empty. Text says fc range 23-85 MPa while Table 2 max is 82.4 (table value used). "
              f"Tensile gauge length not stated in text (cross-section 35 x 20 mm)."})
    rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(out, index=False, encoding="utf-8-sig")
print(len(df), "rows ->", out)

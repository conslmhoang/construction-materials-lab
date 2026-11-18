"""Wave 7, agent w7b: Lee-lab papers 018, 019, 022 (021 rejected: selvedge fibers)."""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
add = os.path.join(here, "..", "additions")
out_dir = os.path.join(here, "..", "additions_v2")
cols = list(pd.read_csv(os.path.join(add, "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
rows = []

# ---------------- 018: ED-EGC, Table 1 / Table 4 ----------------
A18 = {"Article Name": "Micromechanical and mineralogy analyses on extremely ductile engineered geopolymer composites with different activator pretreatments",
       "Author": "Huy Hoàng Nguyễn, Quang-Hiếu Lương, Phương Hoàng Nguyễn, Hyeong-Ki Kim, Youngsang Kim, Bang Yeon Lee", "Year": 2023,
       "DOI / URL": "https://doi.org/10.1016/j.jobe.2023.108093",
       "FA (Fly ash)": 0.7, "NaOH / B": 0.1, "SSM / B (Na2SiO3 anhydrous)": 0.115, "W / B": 0.43, "SP / B": 0.003,
       "PE fiber (vol%)": 1.75, "PE length (mm)": 18, "PE diameter (µm)": 12, "PE tensile strength (MPa)": 2700, "PE elastic modulus (GPa)": 88,
       "Total fiber (vol%)": 1.75,
       "Curing method": "ambient 23 C 5 d, demolded, oven 80 C 2 d, then curing room 23 C until 28 d",
       "Curing time (days)": 28, "Curing temperature (°C)": 80, "Test age (days)": 28, "Heat curing duration (h)": 48,
       "Tensile specimen": "dumbbell (JSCE, 30 x 13 mm section)", "Tensile gauge length (mm)": 80, "Tensile test type": "direct (uniaxial)",
       "Source table/page": "Table 1 (mix), Table 3 (fiber), Table 4 (tensile), Sect. 2.1-2.3"}
note18 = ("B = FA 0.7 + SH 0.1 + SMP 0.2 (paper's weight ratios of binder; activators inside B, given as X/B). "
          "SMP 0.2 x 0.575 = 0.115 anhydrous Na2SiO3, water 0.345 + 0.2 x 0.425 = 0.43. "
          "VERIFY: SH taken as solid NaOH mass ratio (paper says 'SH solution'; whether 0.345 water includes the SH solution water is not stated). "
          "Defoamer 0.001 of B. P-SP 0.003. Fiber 1.75 vol% (paper's Table 1). Compressive strength only in Fig. 8 (not entered). ")
for mid, pre, fcs, fts, eps in [("ED-EGC-WP", "warming pretreatment (activator cooled in 5 min)", 4.67, 8.72, 10.97),
                                ("ED-EGC-CP", "cooling pretreatment (activator cooled 24 h)", 3.40, 5.54, 18.62)]:
    r = dict(A18)
    r.update({"First-cracking strength (MPa)": fcs, "Tensile strength (MPa)": fts, "Tensile strain capacity (%)": eps,
              "Conversions / notes": f"{mid}: {pre}. " + note18})
    rows.append(r)

# ---------------- 019: HSUD-EGC, Table 1 / Table 5 ----------------
A19 = {"Article Name": "Mechanical and autogenous healing properties of high-strength and ultra-ductility engineered geopolymer composites reinforced by PE-PVA hybrid fibers",
       "Author": "Huy Hoàng Nguyễn, Phương Hoàng Nguyễn, Quang-Hiếu Lương, Weina Meng, Bang Yeon Lee", "Year": 2023,
       "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2023.105155",
       "SF (Silica fume)": 0.05, "WG / B (Water glass)": 0.45, "NaOH / B": 0.05, "W / B": 0.1, "SS / B (Silica sand)": 1, "SP / B": 0.02,
       "PE length (mm)": 18, "PE diameter (µm)": 12, "PE tensile strength (MPa)": 3030, "PE elastic modulus (GPa)": 88,
       "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1560, "PVA elastic modulus (GPa)": 41,
       "Curing method": "sealed (plastic sheet) 23 C 2 d, oven 100 C 24 h, air 23 C until 7 d, then water 23 C 28 d",
       "Curing time (days)": 35, "Curing temperature (°C)": 100, "Demolding age (days)": 2, "Test age (days)": 35, "Heat curing duration (h)": 24,
       "Compressive specimen": "cube", "Compressive specimen size (mm)": 50,
       "Tensile specimen": "dumbbell (JSCE)", "Tensile gauge length (mm)": 80, "Tensile test type": "direct (uniaxial)",
       "Source table/page": "Table 1 (mix), Table 3 (fibers), Table 5 (tensile), Sect. 2.2 (curing)"}
note19 = ("B = precursors (GGBS+FA+SF = 1). WG 0.45 (28.9% SiO2, 9.1% Na2O, 62.0% H2O; its water NOT added to W/B). "
          "CS = caustic soda flakes 0.05 (paper gives 11.5 M; taken as solid mass ratio, VERIFY). Test age 35 d = 7 d + 28 d in water (Sect. 2.2: "
          "all specimens in water 28 d before mechanical tests; tension test age not restated, VERIFY). Compressive strength only in Fig. 3 (not entered). "
          "Table 5 = virgin tension tests (Table 8 = pre-cracked/healed, not used). ")
for mid, g, f, pe, pva, fcr, fts, eps in [("S-PE", .55, .40, 1.0, 0.5, 3.70, 6.64, 10.51), ("S-PVA", .55, .40, 0.5, 1.0, 3.84, 6.04, 6.79),
                                          ("F-PE", .30, .65, 1.0, 0.5, 2.70, 5.18, 11.99), ("F-PVA", .30, .65, 0.5, 1.0, 2.84, 4.60, 10.35)]:
    r = dict(A19)
    r.update({"GGBS": g, "FA (Fly ash)": f, "PE fiber (vol%)": pe, "PVA fiber (vol%)": pva, "Total fiber (vol%)": pe + pva,
              "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": fts, "Tensile strain capacity (%)": eps,
              "Conversions / notes": f"{mid}. " + note19})
    rows.append(r)

# ---------------- 022: F-ECFC Taguchi, Tables 2, 6, 7 ----------------
A22 = {"Article Name": "Optimization of fly ash-based polyethylene fiber-reinforced engineered cement-free composites with low-density and ultra-ductility using Taguchi robust design method",
       "Author": "Phương Hoàng Nguyễn, Huy Hoàng Nguyễn, Quang-Hiếu Lương, John E. Bolander, Bang Yeon Lee", "Year": 2023, "DOI / URL": "https://doi.org/10.1016/j.jobe.2023.105946",
       "FA (Fly ash)": 0.7, "NaOH / B": 0.1, "SSM / B (Na2SiO3 anhydrous)": 0.115, "W / B": 0.43,
       "PE length (mm)": 18, "PE diameter (µm)": 12, "PE tensile strength (MPa)": 2700, "PE elastic modulus (GPa)": 88,
       "Test age (days)": 7, "Compressive specimen": "cube", "Compressive specimen size (mm)": 50,
       "Tensile specimen": "dumbbell (JSCE, 30 x 13 mm section)", "Tensile gauge length (mm)": 80, "Tensile test type": "direct (uniaxial)",
       "Source table/page": "Table 2 (mix), Table 4 (fiber), Table 5 (design), Table 6 (fc), Table 7 (tensile), Sect. 3.1"}
fc22 = [0.34, 1.44, 4.48, 7.41, 5.93, 10.09, 18.23, 26.74, 20.70, 26.02, 21.94, 27.14, 32.51, 31.81, 23.67, 21.85]
ts22 = [(0.32, 0.38, 6.97), (2.10, 2.73, 14.65), (3.70, 5.44, 12.20), (3.84, 7.40, 10.27), (2.03, 4.18, 12.85), (1.67, 3.86, 4.20),
        (4.49, 8.79, 10.12), (4.20, 7.93, 10.45), (3.93, 7.87, 7.02), (5.01, 8.04, 7.99), (2.44, 3.67, 1.89), (3.67, 6.42, 6.37),
        (4.66, 8.09, 6.06), (4.98, 6.63, 4.13), (4.12, 4.80, 1.70), (1.94, 2.17, 0.74)]
ids22 = [(60, 12, .5), (60, 24, 1), (60, 36, 1.5), (60, 48, 2), (80, 12, 1), (80, 24, .5), (80, 36, 2), (80, 48, 1.5),
         (100, 12, 1.5), (100, 24, 2), (100, 36, .5), (100, 48, 1), (120, 12, 2), (120, 24, 1.5), (120, 36, 1), (120, 48, .5)]
for (T, CT, FV), fc, (fcr, fts, eps) in zip(ids22, fc22, ts22):
    r = dict(A22)
    note = (f"{T}C-{CT}H-{FV}%. B = FA 0.7 + SH 0.1 + SMP 0.2 (weight ratios of binder, activators in B as X/B). SMP 0.2 x 0.575 = 0.115 anhydrous, "
            "water 0.345 + 0.085 = 0.43. VERIFY: SH taken as solid NaOH (paper: 'SH solution', activator 7.2 M; water content of the solution not stated). "
            "Antifoaming agent 0.001 of B. All tests at 7 d of age (Sect. 3.1). ")
    if fc < 5:
        note += f"Reported fc {fc} MPa (Table 6) is below 5 MPa and left out of the fc column (outside plausible range for the model)."
        fcv = None
    else:
        fcv = fc
    r.update({"PE fiber (vol%)": FV, "Total fiber (vol%)": FV,
              "Curing method": f"air 23 C 4 d, demolded, oven {T} C for {CT} h, cooled to 23 C; tested at 7 d",
              "Curing time (days)": 7, "Curing temperature (°C)": T, "Heat curing duration (h)": CT, "Demolding age (days)": 4,
              "Compressive strength (MPa)": fcv, "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": fts,
              "Tensile strain capacity (%)": eps, "Conversions / notes": note})
    rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w7_w7b.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows")

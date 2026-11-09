# Builder for w4_mdpi_old.csv: MDPI (2012-2022) ECC / SHCC / HPFRCC / UHPC papers with DIRECT (uniaxial / dog-bone) tension data.
# Every number below was read from the cited paper's tables/text (full text via Europe PMC fullTextXML).
import csv, glob, os, re
import pandas as pd

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "additions")
NAME = "w4_mdpi_old"
with open(os.path.join(D, "TEMPLATE.csv"), encoding="utf-8-sig") as f:
    H = next(csv.reader(f))
assert len(H) == 99
rows = []


def add(base, **kw):
    r = dict(base)
    r.update({k: v for k, v in kw.items() if v is not None})
    r = {k: v for k, v in r.items() if v is not None}
    for k in r:
        assert k in H, k
    rows.append(r)


R = lambda x, n=4: round(x, n)
DIRECT = {"Tensile test type": "direct"}

# ---------------------------------------------------------------- 1 Wang et al. 2020 (SHCC repair material, tension at 1/14/28/90 d)
B = 555 + 680
b = {"Article Name": "Research on Bonding and Shrinkage Properties of SHCC-Repaired Concrete Beams",
     "Author": "Wang P., Jiao M., Hu C., Tian L., Zhao T., Lei D., Fu H.", "Year": 2020, "DOI / URL": "https://doi.org/10.3390/ma13071757",
     "OPC / Cement": R(555 / B), "FA (Fly ash)": R(680 / B), "W / B": R(420 / B), "Sand (type not stated) / B": R(490 / B),
     "SP / B": R(27.8 / B, 5), "Binder content (kg/m³)": B,
     "PVA fiber (vol%)": 2.0, "PVA length (mm)": 8, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 42,
     "Total fiber (vol%)": 2.0, "Curing method": "wet burlap 24 h, then indoor air T=25±3 °C, RH 60±5% to test age",
     "Curing temperature (°C)": 25, "Curing RH (%)": 60, "Demolding age (days)": 1,
     "Tensile specimen": "dumbbell", **DIRECT}
for age, fcr, ft, eps in [(1, 2.050, 2.945, 4.247), (14, 2.893, 3.750, 4.336), (28, 2.950, 3.824, 4.331), (90, 3.073, 3.950, 3.545)]:
    add(b, **{"Test age (days)": age, "Curing time (days)": age, "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft,
              "Tensile strain capacity (%)": eps,
              "Compressive strength (MPa)": 48.49 if age == 28 else None,
              "Compressive specimen": "cube" if age == 28 else None, "Compressive specimen size (mm)": "100" if age == 28 else None,
              "Source table/page": "Table 2 (mix, kg/m3), Table 4 (PVA), Table 6 (uniaxial tension)" + ("; Sec. 2.1 text (fc 28 d)" if age == 28 else ""),
              "Conversions / notes": f"Table 2 kg/m3: cement 555, FA 680, sand 490, water 420, SP 27.8, PVA 26 (26/1300 = 2.0 vol%). Binder = cement+FA = {B}. "
                                     "P.O 42.5 cement; sand type not stated. Strains in Table 6 already in %. Elastic modulus in tension Et given in Table 6."
                                     + (" fc 48.49 MPa (100 mm cube, 28 d, indoor curing) from text." if age == 28 else "")})

# ---------------------------------------------------------------- 2 Yin et al. 2018 (SHCC freeze-thaw; basic 28-d properties)
B = 745 + 319
add({"Article Name": "Freeze-Thaw Durability of Strain-Hardening Cement-Based Composites under Combined Flexural Load and Chloride Environment",
     "Author": "Yin L., Yan C., Liu S.", "Year": 2018, "DOI / URL": "https://doi.org/10.3390/ma11091721",
     "OPC / Cement": R(745 / B), "FA (Fly ash)": R(319 / B), "W / B": R(319 / B), "SS / B (Silica sand)": R(639 / B),
     "SP / B": R(30 / B, 5), "Binder content (kg/m³)": B, "PVA fiber (vol%)": 2.0, "Total fiber (vol%)": 2.0,
     "Curing method": "demoulded 24 h, standard curing room 20±2 °C, RH 95±5%", "Curing time (days)": 28, "Curing temperature (°C)": 20,
     "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
     "Compressive specimen": "cube", "Compressive specimen size (mm)": "100", "Tensile specimen": "dumbbell 600x330x15 mm (as printed)", **DIRECT,
     "Compressive strength (MPa)": 56, "Tensile strength (MPa)": 5.2, "Tensile strain capacity (%)": 3.4,
     "Source table/page": "Table 1 (mix kg/m3 + 28-d properties), Sec. 2 text",
     "Conversions / notes": f"Table 1 kg/m3: cement 745, FA 319, water 319, silica sand 639, water-reducing agent ('Water-RAE') 30, PVA 26 (text: 2 vol%). "
                            f"Binder = cement+FA = {B}. Tensile strain 0.034 -> 3.4%. Flexural strength 13.05 MPa. PVA fibre properties not given."})

# ---------------------------------------------------------------- 3 Hauch et al. 2022 (UHPFRC, uniaxial tension, 3 specimens)
B = 825 + 175
add({"Article Name": "Predicting the Tensile Behaviour of Ultra-High Performance Fibre-Reinforced Concrete from Single-Fibre Pull-Out Tests",
     "Author": "Hauch K., Maryamh K., Redenbach C., Schnell J.", "Year": 2022, "DOI / URL": "https://doi.org/10.3390/ma15145085",
     "OPC / Cement": R(825 / B), "SF (Silica fume)": R(175 / B), "W / B": R(179 / B), "SS / B (Silica sand)": R(975 / B), "Sand max size (µm)": 500,
     "QP / B (Quartz powder)": R(200 / B), "SP / B": R(30.25 / B, 5), "Binder content (kg/m³)": B,
     "Steel fiber (vol%)": 2.0, "Steel length (mm)": 12.5, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2800, "Steel elastic modulus (GPa)": 200,
     "Total fiber (vol%)": 2.0, "Curing method": "climate chamber 28 d", "Curing time (days)": 28, "Test age (days)": 28, **DIRECT,
     "Tensile specimen": "uniaxial tension specimen (3 tested)",
     "Compressive strength (MPa)": 150.2, "Tensile strength (MPa)": 11.51, "Tensile strain capacity (%)": 0.70,
     "Source table/page": "Table 1 (mix g/L, fc, matrix ft), Table 4 (uniaxial tension), Sec. 2 text (fibre)",
     "Conversions / notes": "Table 1 g/L = kg/m3: CEM I 52.5 R 825, quartz sand 0.125/0.5 975, quartz flour 200, silica fume 175, water 179, PCE 30.25. "
                            "Binder = cement+SF = 1000. Table 4 mean of 3: sigma_ult 11.51 MPa, eps_ult 0.0070 (-> 0.70%; specimen 2 strain printed 0.0010). "
                            "Table 1 also lists 'uniaxial tensile strength 6.4 MPa' at strain 0.00087 (matrix/crack-initiation strength, not put in a column); "
                            "bending tensile strength 13.77 MPa."})

# ---------------------------------------------------------------- 4 Kalthoff et al. 2021 (plain UHPC 1, centric tension, 12 curing regimes x ages)
B = 832 + 135
b = {"Article Name": "Influence of High Temperature Curing and Surface Humidity on the Tensile Strength of UHPC",
     "Author": "Kalthoff M., Raupach M., Matschei T.", "Year": 2021, "DOI / URL": "https://doi.org/10.3390/ma14154260",
     "OPC / Cement": R(832 / B), "SF (Silica fume)": R(135 / B), "W / B": R(189 / B), "River sand / B": R(1030 / B), "Sand max size (µm)": 500,
     "QP / B (Quartz powder)": R(219 / B), "SP / B": R(0.0353 * 832 / B, 5), "Binder content (kg/m³)": B, "Total fiber (vol%)": 0,
     "Demolding age (days)": 2, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100",
     "Tensile specimen": "briquette (ASTM C307 x3 scale), 228.6 mm long, neck 76.5x76.5 mm", **DIRECT}
TS = {  # (treatment, storage, days of storage) -> {age: ft}
    ("heat", "water", 2): {7: 8.3, 14: 5.9, 28: 6.5, 56: 5.9, 90: 5.7, 180: 6.6},
    ("heat", "water", 9): {14: 8.0, 28: 6.2, 56: 5.1, 90: 5.8, 180: 6.7},
    ("heat", "water", 23): {28: 9.3, 56: 4.9, 90: 5.6, 180: 5.9},
    ("heat", "sealed", 2): {7: 8.6, 14: 7.0, 28: 5.0, 56: 4.3, 90: 5.5, 180: 5.8},
    ("heat", "sealed", 9): {14: 9.2, 28: 6.2, 56: 4.9, 90: 5.1, 180: 6.3},
    ("heat", "sealed", 23): {28: 8.7, 56: 6.2, 90: 5.4, 180: 6.3},
    ("autoclave", "water", 2): {7: 7.2, 14: 7.6, 28: 5.7, 56: 5.8, 90: 5.6, 180: 5.6},
    ("autoclave", "water", 9): {14: 10.2, 28: 6.9, 56: 6.2, 90: 5.6, 180: 6.2},
    ("autoclave", "water", 23): {28: 9.5, 56: 5.8, 90: 6.8, 180: 5.1},
    ("autoclave", "sealed", 2): {7: 7.4, 14: 7.9, 28: 6.9, 56: 6.8, 90: 6.4, 180: 8.0},
    ("autoclave", "sealed", 9): {14: 6.9, 28: 7.4, 56: 7.2, 90: 7.6, 180: 6.9},
    ("autoclave", "sealed", 23): {28: 7.7, 56: 7.4, 90: 7.1, 180: 8.0}}
CS = {
    ("heat", "water", 2): {7: 186.2, 14: 181.4, 28: 177.7, 56: 147.3, 90: 179.1, 180: 165.4},
    ("heat", "water", 9): {14: 180.8, 28: 179.0, 56: 163.9, 90: 172.9, 180: 175.0},
    ("heat", "water", 23): {28: 184.1, 56: 173.1, 90: 167.5, 180: 192.4},
    ("heat", "sealed", 2): {7: 179.7, 14: 178.2, 28: 169.9, 56: 141.9, 90: 154.6, 180: 198.6},
    ("heat", "sealed", 9): {14: 177.7, 28: 176.6, 56: 179.7, 90: 162.7, 180: 161.5},
    ("heat", "sealed", 23): {28: 178.6, 56: 172.4, 90: 167.3, 180: 168.6},
    ("autoclave", "water", 2): {7: 189.1, 14: 186.0, 28: 185.9, 56: 177.5, 90: 192.9, 180: 177.8},
    ("autoclave", "water", 9): {14: 178.7, 28: 197.5, 56: 192.9, 90: 179.9, 180: 188.7},
    ("autoclave", "water", 23): {28: 176.9, 56: 186.0, 90: 205.4, 180: 201.0},
    ("autoclave", "sealed", 2): {7: 190.6, 14: 213.5, 28: 220.2, 56: 205.4, 90: 179.0, 180: 177.4},
    ("autoclave", "sealed", 9): {14: 208.0, 28: 218.9, 56: 186.9, 90: 214.1, 180: 214.3},
    ("autoclave", "sealed", 23): {28: 221.0, 56: 170.7, 90: 199.0, 180: 177.4}}
TAB = {k: i + 1 for i, k in enumerate(TS)}
for k, ages in TS.items():
    trt, sto, n = k
    for age, ft in ages.items():
        heat = trt == "heat"
        add(b, **{"Curing method": ("demould 48 h; 48 h in water at 90 °C (heat treatment)" if heat else
                                    "demould 48 h; autoclave ~190 °C / 12.5 bar (9 h heating, 15 h hold, ~30 h cooling)")
                                   + f"; then {n} d {'under water' if sto == 'water' else 'sealed in foil'} at 20 °C; then 20 °C / 65% RH until test",
                  "Curing temperature (°C)": 90 if heat else 190, "Heat curing duration (h)": 48 if heat else 15,
                  "Curing time (days)": 5 + n, "Test age (days)": age,
                  "Tensile strength (MPa)": ft, "Compressive strength (MPa)": CS[k].get(age),
                  "Source table/page": f"Table 1 (mix), Table A{TAB[k]} (ft), Table A{TAB[k] + 12} (fc)",
                  "Conversions / notes": "UHPC 1 (no fibres), kg/m3: CEM III/A 52.5 R (slag cement) 832, water 189, quartz powder 0-0.063 219, river sand 0.1-0.5 mm 1030 "
                                         "(printed '1.030'), silica fume 135, SP 3.53 M.-% of cement. Binder = cement+SF = 967 (w/b 0.195; paper 0.19). "
                                         "Curing time = 2 d formwork + 3 d treatment + storage days. Heat curing duration for autoclave = hold time. "
                                         "Mean of 5-7 bone specimens. Some ages marked '(1) according to [19]' (earlier study by the authors). "
                                         "UHPC 2 series (Tables A25-A29) not used: curing variants only defined in Fig. 2."})

# ---------------------------------------------------------------- 5 Kim M.K. & Kim D.J. 2018 (HPFRCC with milled glass fibre, steel 2 vol%)
B = 1.15
b = {"Article Name": "Electromechanical Response of High-Performance Fiber-Reinforced Cementitious Composites Containing Milled Glass Fibers under Tension",
     "Author": "Kim M.K., Kim D.J.", "Year": 2018, "DOI / URL": "https://doi.org/10.3390/ma11071115",
     "FA (Fly ash)": R(0.15 / B), "W / B": R(0.35 / B), "SS / B (Silica sand)": R(1.0 / B),
     "Steel fiber (vol%)": 2.0, "Steel elastic modulus (GPa)": 200, "Total fiber (vol%)": 2.0,
     "Curing method": "covered 1 d at 25 °C / 60% RH, demoulded, water-cured at 24 °C for 14 d, then stored 25 °C / 60% RH",
     "Curing time (days)": 14, "Curing temperature (°C)": 24, "Demolding age (days)": 1,
     "Tensile specimen": "dog-bone (50 mm wide), steel mesh at ends", **DIRECT}
for s, c, mgf, sp, fcm, ecc, epc, scc, spc in [("M0.00", 1.0, 0.0, 0.0055, 95, 0.025, 0.68, 5.6, 12.2), ("M0.05", 0.95, 0.05, 0.0055, 89, 0.028, 0.72, 6.0, 12.5),
                                               ("M0.10", 0.90, 0.10, 0.006, 83, 0.023, 0.69, 5.3, 10.7)]:
    add(b, **{"OPC / Cement": R(c / B), "Other binder": R(mgf / B) if mgf else 0, "SP / B": R(sp / B, 5),
              "First-cracking strength (MPa)": scc, "Tensile strength (MPa)": spc, "Tensile strain capacity (%)": epc,
              "Source table/page": "Table 1 (mix by weight), Table 2 (fibres), Table 4 (tension, averages), Sec. 2 text",
              "Conversions / notes": f"{s}: weight ratios cement {c}, milled glass fibre (MGF, 0.3 mm long, replaces cement) {mgf}, silica sand 1.0 (avg 0.43 mm), FA 0.15, "
                                     f"SP {sp} (liquid, 25% solids), water 0.35; binder B = cement+MGF+FA = 1.15 (MGF -> 'Other binder'). "
                                     "Fibres: 1 vol% long smooth steel (30 mm, 0.3 mm, 2447 MPa) + 1 vol% medium smooth steel (19.5 mm, 0.2 mm, 2942 MPa). "
                                     f"Matrix (no steel fibre) compressive strength {fcm} MPa - not entered as composite fc. First-crack strain {ecc}%. "
                                     "Test age not stated (after 14 d water curing)."})

# ---------------------------------------------------------------- 6 Kim D.J. et al. 2014 (HPSFRC, hooked/twisted steel 2%, 2 sands)
B = 0.80 + 0.20 + 0.07
b = {"Article Name": "Mechanical Characterization of High-Performance Steel-Fiber Reinforced Cement Composites with Self-Healing Effect",
     "Author": "Kim D.J., Kang S.H., Ahn T.H.", "Year": 2014, "DOI / URL": "https://doi.org/10.3390/ma7010508",
     "OPC / Cement": R(0.80 / B), "FA (Fly ash)": R(0.20 / B), "SF (Silica fume)": R(0.07 / B), "W / B": R(0.26 / B),
     "Steel fiber (vol%)": 2.0, "Steel length (mm)": 30, "Steel elastic modulus (GPa)": 200, "Total fiber (vol%)": 2.0,
     "Tensile specimen": "dog-bone (direct tensile test)", **DIRECT}
for mat, fib, scc, spc, epc in [("A", "H", 7.814, 10.738, 0.451), ("A", "T", 8.779, 12.876, 0.450), ("B", "H", 7.879, 12.595, 0.546), ("B", "T", 9.707, 15.361, 0.519)]:
    sp = 0.02 if mat == "A" else 0.04
    sand = {"M-sand / B": R(1.0 / B)} if mat == "A" else {"SS / B (Silica sand)": R(1.0 / B)}
    add(b, **sand, **{"SP / B": R(sp / B, 5),
                      "Steel diameter (µm)": 375 if fib == "H" else 300, "Steel tensile strength (MPa)": 2311 if fib == "H" else 2428,
                      "First-cracking strength (MPa)": scc, "Tensile strength (MPa)": spc, "Tensile strain capacity (%)": epc,
                      "Source table/page": "Table 1 (matrix by weight), Table 2 (fibres), Table 3 (tension)",
                      "Conversions / notes": f"Matrix {mat}: cement (Type III) 0.80, FA 0.20, SF 0.07, SP {sp}, water 0.26, sand 1.00 "
                                             + ("(type 1 normal crushed sand -> M-sand)" if mat == "A" else "(type 3 very fine silica sand)")
                                             + f"; B = cement+FA+SF = 1.07. {'Hooked' if fib == 'H' else 'Twisted (equivalent diameter 0.3 mm)'} steel fibre 2 vol%. "
                                             + f"Matrix compressive strength {81 if mat == 'A' else 113} MPa (mortar, no fibres) - not entered as composite fc. "
                                             "Curing regime and test age not stated (pre-cracking done at 28 d)."})

# ---------------------------------------------------------------- 7 Li et al. 2019 (ECC matrix with PVA / KEVLAR / PE fibres, quasi-static uniaxial tension; steel-grid specimens skipped)
B = 1.11
b = {"Article Name": "Experimental Investigation on the Quasi-Static Tensile Capacity of Engineered Cementitious Composites Reinforced with Steel Grid and Fibers",
     "Author": "Li L., Liu W., Wu J., Wu W., Wu M.", "Year": 2019, "DOI / URL": "https://doi.org/10.3390/ma12172666",
     "OPC / Cement": R(1 / B), "FA (Fly ash)": R(0.11 / B), "W / B": R(0.3 / B), "SP / B": R(0.013 / B, 5),
     "Curing method": "demoulded 24 h, curing room 20±0.5 °C, RH 95±5%", "Curing time (days)": 28, "Curing temperature (°C)": 20,
     "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28, "Tensile specimen": "plate, steel tabs bonded at ends", **DIRECT}
MIXN = ("Matrix by mass: P.O 42.5 cement 1.0, siliceous fly ash 0.11, water 0.3, SP 0.013; no sand; B = cement+FA = 1.11. "
        "Note: companion paper (10.3390/ma14227042) lists the same 0.11 as silica fume. Only specimens without steel grid (S0) used.")
TT = {"M": [("M", 0, 0.98, 0.98, 0.01)],
      "A": [("A0.5", 0.5, 1.39, 1.39, 0.05), ("A1", 1.0, 1.77, 1.92, 0.35), ("A1.5", 1.5, 1.78, 2.00, 0.23), ("A2", 2.0, 2.63, 2.80, 0.39)],
      "K": [("K0.5", 0.5, 1.79, 1.79, 0.06), ("K1", 1.0, 1.6, 1.6, 0.12), ("K1.5", 1.5, 2.21, 2.21, 0.26), ("K2", 2.0, 2.93, 2.93, 0.24)],
      "E": [("E0.5", 0.5, 1.21, 1.21, 0.24), ("E1", 1.0, 1.01, 1.40, 1.98), ("E1.5", 1.5, 1.64, 1.94, 4.87), ("E2", 2.0, 1.8, 2.18, 5.18)]}
TABN = {"M": "Table 6", "A": "Table 6", "K": "Table 7", "E": "Table 8"}
for fam, lst in TT.items():
    for sid, vf, fcr, ft, eps in lst:
        fib = {}
        if fam == "A":
            fib = {"PVA fiber (vol%)": vf, "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1560, "PVA elastic modulus (GPa)": 41}
        elif fam == "E":
            fib = {"PE fiber (vol%)": vf, "PE length (mm)": 12, "PE tensile strength (MPa)": 2180, "PE elastic modulus (GPa)": 66}
        note = {"M": "plain matrix.", "A": "PVA fibre.", "E": "PE fibre (Table 4: 2.18 GPa, 66 GPa, 12 mm; diameter not given).",
                "K": "KEVLAR (aramid) fibre 12 mm, 2920 MPa, 70.5 GPa, 1.44 g/cm3 - no aramid column, counted in Total fiber only."}[fam]
        add(b, **fib, **{"Total fiber (vol%)": vf, "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
                         "Source table/page": f"Table 2-4 (fibres), Table 5 (matrix), {TABN[fam]} (tension)",
                         "Conversions / notes": f"{sid}: {vf} vol% {note} " + MIXN})

# ---------------------------------------------------------------- 8 Chen et al. 2022 (lightweight PE-ECC matrix of TR-LECC)
B = 874 + 391.5 + 39
add({"Article Name": "Tensile Experiments and Numerical Analysis of Textile-Reinforced Lightweight Engineered Cementitious Composites",
     "Author": "Chen M., Deng X., Guo R., Fu C., Zhang J.", "Year": 2022, "DOI / URL": "https://doi.org/10.3390/ma15165494",
     "OPC / Cement": R(874 / B), "FA (Fly ash)": R(391.5 / B), "Nano-SiO2": R(39 / B), "W / B": R(238.7 / B), "FA cenosphere / B": R(195.8 / B),
     "SP / B": R(91.7 / B, 5), "Binder content (kg/m³)": B, "PE fiber (vol%)": R(20 / 970, 3), "Total fiber (vol%)": R(20 / 970, 3),
     "Curing method": "24 h in mould at room temperature, then 20±2 °C / 95% RH for 27 d", "Curing time (days)": 28, "Curing temperature (°C)": 20,
     "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28, "Tensile specimen": "dog-bone (JSCE)", **DIRECT,
     "First-cracking strength (MPa)": 5.5, "Tensile strength (MPa)": 8.8, "Tensile strain capacity (%)": 7.8,
     "Source table/page": "Table 3 (LECC tension), Table 4 (mix kg/m3), Sec. 2 text",
     "Conversions / notes": f"Table 4 kg/m3: cement 874, FA 391.5, nanosilica 39, FA cenospheres (fine aggregate, 0.01-0.5 mm) 195.8, water 238.7, SP 91.7 (as printed), "
                            f"PE fibre 20 -> 20/970 = 2.06 vol% (density assumed 970). Binder = cement+FA+NS = {B}. Test age assumed 28 d (1 d + 27 d curing). "
                            "PE fibre geometry not given. fc not reported."})

# ---------------------------------------------------------------- 9 dos Santos et al. 2020 (HPC mortar + SAP + steel micro-fibre 1.28%, direct tension with DIC)
b = {"Article Name": "Effect of the Combination of Superabsorbent Polymers for Autogenous Shrinkage Control with Steel Fibers of High-Performance Concrete under Uniaxial Tension Using DIC",
     "Author": "dos Santos K.F., Ribeiro A.C.B.S., da Silva E.F., Manzano M.A.R., Motta L.A.C., Toledo Filho R.D.", "Year": 2020,
     "DOI / URL": "https://doi.org/10.3390/ma13204638", "Curing method": "moist room 22±1 °C, RH 100%", "Curing temperature (°C)": 22, "Curing RH (%)": 100,
     "Curing time (days)": 28, "Test age (days)": 28, "Tensile specimen": "dog-bone (Fig. 4)", **DIRECT}
for m, c, s, sand, sap, fib, sp, wb, wt, fc, ft3, t4 in [
        ("REF-035", 675.8, 67.6, 1306.5, 0, 0, 11.15, 0.35, 0.35, 82.80, 5.39, None), ("REF-040", 654.2, 65.4, 1264.5, 0, 0, 8.50, 0.40, 0.40, 72.32, 4.92, None),
        ("SAP-0.2", 675.8, 67.6, 1306.5, 1.35, 0, 12.50, 0.35, 0.38, 71.36, 5.04, None), ("SAP-0.3", 675.8, 67.6, 1306.5, 2.03, 0, 12.50, 0.35, 0.40, 68.24, 5.07, None),
        ("REF-035F", 675.8, 67.6, 1306.5, 0, 100, 13.50, 0.35, 0.35, 86.20, 6.01, (5.87, 3.86)), ("SAP-0.2F", 675.8, 67.6, 1306.5, 1.35, 100, 13.50, 0.35, 0.38, 77.09, 4.59, (4.29, 2.31)),
        ("SAP-0.3F", 675.8, 67.6, 1306.5, 2.03, 100, 13.50, 0.35, 0.40, 72.78, 5.92, (5.62, 5.35)), ("SAP-0.6F", 675.8, 67.6, 1306.5, 4.06, 100, 13.50, 0.35, 0.46, 63.60, 3.23, (4.50, 3.31))]:
    B = c + s
    extra = R((wt - wb) * c / B) if wt > wb else None
    fibcols = {"Steel fiber (vol%)": 1.28, "Steel length (mm)": 13, "Steel diameter (µm)": 160, "Total fiber (vol%)": 1.28} if fib else {"Total fiber (vol%)": 0}
    if t4:
        tens = {"First-cracking strength (MPa)": t4[0], "Tensile strength (MPa)": max(t4)}
        tnote = f" Table 4: sigma_cc {t4[0]}, sigma_pc {t4[1]} MPa (ft = max); Table 3 lists first-cracking stress {ft3} MPa (differs slightly)."
    else:
        tens = {"Tensile strength (MPa)": ft3}
        tnote = f" Plain mortar: ft = Table 3 first-cracking (= failure) stress {ft3} MPa."
    add(b, **fibcols, **tens, **{"OPC / Cement": R(c / B), "SF (Silica fume)": R(s / B), "W / B": R(wb * c / B), "Extra water / B": extra,
                                 "Sand (type not stated) / B": R(sand / B), "SP / B": R(sp / B, 5), "Binder content (kg/m³)": R(B, 1),
                                 "Compressive strength (MPa)": fc,
                                 "Source table/page": "Table 2 (mix kg/m3), Table 3 (fc, ft), Table 4 (tension of SFRC)",
                                 "Conversions / notes": f"{m}: kg/m3 cement {c}, silica fume {s}, sand {sand}, SAP {sap}, steel fibre {fib}, SP {sp}; "
                                                        f"w/c basic {wb}, total {wt} (incl. SAP-absorbed water -> Extra water/B). Binder = cement+SF. "
                                                        "Water derived as w/c x cement. Dramix OL 13/.16 straight steel micro-fibre, 1.28 vol%. No coarse aggregate." + tnote})

# ---------------------------------------------------------------- 10/11 Yuan et al. 2020 and Lee et al. 2021 (NSHSDC / HSDC, same mix, Yoon group)
B = 1.25
hs = {"OPC / Cement": R(1 / B), "SF (Silica fume)": R(0.25 / B), "W / B": 0.172, "SS / B (Silica sand)": R(1.10 / B), "Sand max size (µm)": 300,
      "QP / B (Quartz powder)": R(0.30 / B),
      "Steel fiber (vol%)": 1.0, "Steel length (mm)": 19.5, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2650, "Steel elastic modulus (GPa)": 200,
      "PE fiber (vol%)": 0.5, "PE length (mm)": 12, "PE diameter (µm)": 31, "PE tensile strength (MPa)": 2900, "PE elastic modulus (GPa)": 100,
      "Total fiber (vol%)": 1.5, "Curing method": "room 20±1 °C, RH 60±5% until test", "Curing temperature (°C)": 20, "Curing RH (%)": 60,
      "Test age (days)": 28, **DIRECT}
hsn = ("Mix by weight: water 0.215, Type I cement 1.00, silica fume 0.25, silica filler 0.30 (-> QP), silica sand 0.08-0.30 mm 1.10, "
       "steel 1.0 vol% + PE 0.5 vol%, SP 3.0% (basis not stated, not converted). B = cement+SF = 1.25; w/b 0.172 as printed.")
add(hs, **{"Article Name": "Bond Strength and Flexural Capacity of Normal Concrete Beams Strengthened with No-Slump High-Strength, High-Ductility Concrete",
           "Author": "Yuan T.F., Hong S.H., Shin H.O., Yoon Y.S.", "Year": 2020, "DOI / URL": "https://doi.org/10.3390/ma13194218",
           "Compressive strength (MPa)": 123.4, "Tensile strength (MPa)": 9.7, "Compressive specimen": "cylinder (ASTM C39)",
           "Source table/page": "Table 2 (mix), Table 4 (fibres), Table 5 (28-d strengths)",
           "Conversions / notes": "NSHSDC. " + hsn + " Flexural strength 21.9 MPa."})
add(hs, **{"Article Name": "Shielding Effectiveness and Impact Resistance of Concrete Walls Strengthened by High-Strength High-Ductility Concrete",
           "Author": "Lee J.H., Choi J.S., Yuan T.F., Yoon Y.S.", "Year": 2021, "DOI / URL": "https://doi.org/10.3390/ma14247773",
           "Compressive strength (MPa)": 122.3, "Tensile strength (MPa)": 9.7,
           "Source table/page": "Table 1 (mix), Table 3 (steel fibre), Sec. 2 text (PE fibre), Table 4 (28-d strengths)",
           "Conversions / notes": "HSDC. " + hsn + " Flexural strength 22.9 MPa. Same mix and group as Yuan et al. 2020 (10.3390/ma13194218), separate batch."})

# ---------------------------------------------------------------- 12 Hakeem et al. 2022 (UHPC, dog-bone direct tension)
B = 900 + 220
add({"Article Name": "Experimental Investigation of Hybrid Beams Utilizing Ultra-High Performance Concrete (UHPC) as Tension Reinforcement",
     "Author": "Hakeem I.Y., Rahman M.K., Althoey F.", "Year": 2022, "DOI / URL": "https://doi.org/10.3390/ma15165619",
     "OPC / Cement": R(900 / B), "SF (Silica fume)": R(220 / B), "W / B": R(168 / B), "Sand (type not stated) / B": R(990 / B),
     "SP / B": R(42 / B, 5), "Binder content (kg/m³)": B, "Steel fiber (vol%)": R(157 / 7850, 3), "Steel length (mm)": 13, "Steel diameter (µm)": 200,
     "Steel tensile strength (MPa)": 2500, "Total fiber (vol%)": R(157 / 7850, 3),
     "Curing method": "heat curing 90 °C for 2 d", "Curing time (days)": 2, "Curing temperature (°C)": 90, "Heat curing duration (h)": 48,
     "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Tensile specimen": "dog-bone (ASTM D638)", **DIRECT,
     "Compressive strength (MPa)": 172, "Tensile strength (MPa)": 10,
     "Source table/page": "Table 2 (fibre), Table 3 (mix kg/m3), Table 5 (results), Sec. 2 text",
     "Conversions / notes": f"Table 3 kg/m3: OPC 900, micro-silica 220, fine aggregate 990 (FM 2.22, ~600 um), copper-coated steel fibre 157 (/7850 = 2.0 vol%), "
                            f"SP 42, water 168. Binder = OPC+MS = {B}. Cylinder fc 160 MPa; text gives cube 170 MPa and split 26 MPa vs Table 5 172 / 15 MPa "
                            "(Table 5 used). Test age not stated (UHPC heat-cured 2 d)."})

# ---------------------------------------------------------------- 13 Bae & Choi 2022 (UHPFRC 120/180 MPa grades, direct tension)
b = {"Article Name": "Experimental Study on the Flexural Behavior of Lap-Spliced Ultra-High-Performance Fiber-Reinforced Concrete Beams",
     "Author": "Bae B.I., Choi H.K.", "Year": 2022, "DOI / URL": "https://doi.org/10.3390/polym14112138", **DIRECT,
     "Tensile specimen": "direct tension (stress-CMOD)"}
for m, w, c, bfs, sf, fil, sand, sra, sp, f13, f195, f163, vf, fc, ft in [
        ("120-0", 204, 781.5, 136.8, 58.6, 234.4, 859.6, 7.8, 18, 0, 0, 0, 0, 140.8, 2.4),
        ("120-V1.5", 204, 781.5, 136.8, 58.6, 234.4, 859.6, 7.8, 18, 0, 78, 39, 1.5, 142.2, 10.6),
        ("180-0", 170, 799.5, 0, 199.9, 239.9, 879.5, 8, 18.4, 0, 0, 0, 0, 173.3, 3.0),
        ("180-V1.0", 170, 799.5, 0, 199.9, 239.9, 879.5, 8, 18.4, 78, 0, 0, 1.0, 174.0, 7.6),
        ("180-V2.0", 170, 799.5, 0, 199.9, 239.9, 879.5, 8, 18.4, 156, 0, 0, 2.0, 178.5, 11.6),
        ("180-V1.5", 170, 799.5, 0, 199.9, 239.9, 879.5, 8, 18.4, 0, 78, 39, 1.5, 175.9, 12.4)]:
    B = c + bfs + sf
    fibc = {"Total fiber (vol%)": vf}
    if vf:
        fibc.update({"Steel fiber (vol%)": vf, "Steel length (mm)": 13 if f13 else 19.5, "Steel diameter (µm)": 200,
                     "Steel tensile strength (MPa)": 2600, "Steel elastic modulus (GPa)": 200})
    add(b, **fibc, **{"OPC / Cement": R(c / B), "GGBS": R(bfs / B), "SF (Silica fume)": R(sf / B), "W / B": R(w / B),
                      "Sand (type not stated) / B": R(sand / B), "QP / B (Quartz powder)": R(fil / B), "SP / B": R(sp / B, 5), "Binder content (kg/m³)": R(B, 1),
                      "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft,
                      "Source table/page": "Table 1 (Vf, fibre), Table 2 (mix kg/m3), Table 3 (fc, ft)",
                      "Conversions / notes": f"{m}: kg/m3 water {w}, cement {c}, blast furnace slag {bfs} (printed 'Basalt Furnace'), SF {sf}, filler {fil} (-> QP), sand {sand}, "
                                             f"shrinkage-reducing agent {sra}, SP {sp}, steel fibre 13/0.2 {f13}, 19.5/0.2 {f195}, 16.3/0.2 {f163}. Binder = cement+slag+SF. "
                                             + ("Vf 1.5 from Table 1 and (78+39)/7850; Table 3 prints 2.0 for 120-V1.5. Fibre length: mix of 19.5 and 16.3 mm. " if f195 else "")
                                             + "Direct tensile strength obtained via stress-CMOD (specimen details not given). Curing regime and test age not stated."})

# ---------------------------------------------------------------- 14 Zhang et al. 2021 (UHPC with premixed binder, uniaxial tension)
B = 913.96
add({"Article Name": "Flexural Behavior of T-Shaped UHPC Beams with Varying Longitudinal Reinforcement Ratios",
     "Author": "Zhang R., Hu P., Chen K., Li X., Yang X.", "Year": 2021, "DOI / URL": "https://doi.org/10.3390/ma14195706",
     "Other binder": 1.0, "W / B": R(164.51 / B), "SS / B (Silica sand)": R(1096.75 / B), "SP / B": R(4.57 / B, 5), "Binder content (kg/m³)": B,
     "Steel fiber (vol%)": 2.0, "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Total fiber (vol%)": 2.0,
     "Curing method": "20±2 °C, RH >90%, 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 90, "Test age (days)": 28,
     "Compressive specimen": "cube", "Compressive specimen size (mm)": "100", "Tensile specimen": "uniaxial tension specimen (Fig. 3a), LVDTs over gauge length", **DIRECT,
     "Compressive strength (MPa)": 166.0, "First-cracking strength (MPa)": 4.14, "Tensile strength (MPa)": 8.42, "Tensile strain capacity (%)": 0.7,
     "Source table/page": "Table 1 (fibre), Table 2 (mix kg/m3), Table 4 (tension), Sec. 2 text (fc)",
     "Conversions / notes": "Table 2 kg/m3: water 164.51, premixed binder 913.96 (composition not given -> 'Other binder' = 1), quartz sand 1096.75, "
                            "steel fibre 158 (2 vol%), PCE SP 4.57; W/B 18%. Steel fibre 13 mm x 0.2 mm, strength >2850 MPa. "
                            "Strain at ultimate 0.007 -> 0.7%. Prism (100x100x300) compressive strength 141.8 MPa."})

# ---------------------------------------------------------------- 15 Hanifehzadeh et al. 2021 (UHPC for column jackets)
B = 1.25
add({"Article Name": "Structural Response of Steel Jacket-UHPC Retrofitted Reinforced Concrete Columns under Blast Loading",
     "Author": "Hanifehzadeh M., Aryan H., Gencturk B., Akyniyazov D.", "Year": 2021, "DOI / URL": "https://doi.org/10.3390/ma14061521",
     "OPC / Cement": R(1 / B), "SF (Silica fume)": R(0.25 / B), "W / B": R(0.27 / B), "SS / B (Silica sand)": R(1.0 / B), "Sand max size (µm)": 2000,
     "QP / B (Quartz powder)": R(0.25 / B),
     "Steel fiber (vol%)": 2.5, "Steel length (mm)": 13, "Steel diameter (µm)": 210, "Steel tensile strength (MPa)": 2750, "Steel elastic modulus (GPa)": 200,
     "Total fiber (vol%)": 2.5, "Compressive specimen": "cylinder (ASTM C39)", **DIRECT,
     "Compressive strength (MPa)": 146.2, "Tensile strength (MPa)": 10.2,
     "Source table/page": "Table 2 (mix weight ratios), Table 3 (properties), Sec. 2 text (fibre)",
     "Conversions / notes": "Weight ratios: Type I/II cement 1.00, densified SF 0.25, silica powder SCS40 0.25 (-> QP), fine sand L60 0.40 (max 0.6 mm) + "
                            "coarse sand GS#22 0.60 (max 2 mm) (both US Silica -> SS), water 0.27. B = cement+SF = 1.25. Dramix straight steel 13 mm x 0.21 mm, 2.5 vol%. "
                            "Split tensile 15.1 MPa, MOR 17.6 MPa, E 41 GPa. SP not listed. Curing and test age not stated; direct tension specimen not described."})

# ---------------------------------------------------------------- write
df = pd.DataFrame(rows).reindex(columns=H)
norm = lambda s: re.sub(r"^https?://(dx\.)?doi\.org/", "", str(s).strip().lower())
taken = set()
with open(os.path.join(D, "existing_papers.txt"), encoding="utf-8") as f:
    for l in f:
        if l.strip() and not l.startswith("#"):
            taken.add(norm(l))
for fn in glob.glob(os.path.join(D, "*.csv")):
    if os.path.basename(fn) in ("TEMPLATE.csv", NAME + ".csv"):
        continue
    try:
        taken |= {norm(x) for x in pd.read_csv(fn, encoding="utf-8-sig")["DOI / URL"].dropna().unique()}
    except Exception:
        pass
dup = sorted({d for d in df["DOI / URL"] if norm(d) in taken})
if dup:
    print("DROPPING already-collected DOIs:", dup)
    df = df[~df["DOI / URL"].isin(dup)]
df.to_csv(os.path.join(D, NAME + ".csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows,", df["DOI / URL"].nunique(), "papers")

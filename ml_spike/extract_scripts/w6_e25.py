"""Wave 6, agent e25: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e25.csv (99-column TEMPLATE header).
Papers: conbuildmat.2018.11.260, 2019.07.284, 2019.117031, 2019.117963, 2020.120347
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


# ---------- 1) Ahmad et al.: UHPC, control M0 only (natural pozzolan mixes skipped)
P = {"Article Name": "Influence of admixing natural pozzolan as partial replacement of cement and microsilica in UHPC mixtures",
     "Author": "Shamsad Ahmad, Khaled Own Mohaisen, Saheed Kolawole Adekunle, Salah U. Al-Dulaijan, Mohammed Maslehuddin",
     "Year": 2018, "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2018.11.260"}
B = 900 + 220
for age, fc in [(7, 124.1), (14, 132.9), (28, 143.0), (90, 161.6)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(900 / B), "SF (Silica fume)": r4(220 / B), "W / B": r4(163 / B), "Dune sand / B": r4(1005 / B),
              "SP / B": r4(40 / B), "Binder content (kg/m³)": B, "Steel fiber (vol%)": 2.0, "Steel length (mm)": 13,
              "Steel diameter (µm)": 220, "Steel tensile strength (MPa)": 2500, "Total fiber (vol%)": 2.0,
              "Curing method": "demoulded 6 h after casting; water-soaked burlap moist curing 14 d, then laboratory air",
              "Curing time (days)": 14, "Demolding age (days)": 0.25, "Test age (days)": age, "Compressive specimen": "cube",
              "Compressive specimen size (mm)": "100", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 7 (mix, kg/m3), Table 9 (fc), sect. 2.3 (curing)",
              "Conversions / notes": "Control mix M0 only (mixes with natural pozzolan skipped). kg/m3 / B (cement + microsilica = 1120); stated w/b 0.145. "
                                     "Steel fibre 157 kg/m3 = 2.0 vol% (density 7850), copper-coated 13 mm x 0.22 mm. "
                                     "Splitting tensile strength 18.0 MPa at 28 d (very high for splitting; not entered). No direct tension test. "
                                     "SP kg/m3 as dosed (liquid, SG 1.08). Year from DOI. Laboratory temperature not stated."})
    rows.append(r)

# ---------- 2) Nguyen Amanjean et al.: UHPFRC with SF or MK, characteristic fc at 28 d
P = {"Article Name": "Effect of design parameters on the properties of ultra-high performance fibre-reinforced concrete in the fresh state",
     "Author": "E. Nguyen Amanjean, M. Mouret, T. Vidal", "Year": 2019,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2019.07.284"}
# id, SF, MK, sand, SP, fibre vol%, w/b effective, fc char.
for mid, sf, mk, sa, sp, fv, wb, fc in [("UHPFRC-1", .25, 0, 1.02, .045, 2.0, .205, 150), ("UHPFRC-2", 0, .30, 1.02, .050, 2.0, .175, 152),
                                         ("UHPFRC-3", 0, .30, 1.09, .048, 1.5, .163, 132), ("UHPFRC-4", 0, .30, 1.62, .060, 2.0, .226, 132)]:
    B = 1 + sf + mk
    r = dict(P)
    r.update({"OPC / Cement": r4(1 / B), "SF (Silica fume)": r4(sf / B), "Metakaolin": r4(mk / B), "W / B": wb,
              "Sand (type not stated) / B": r4(sa / B), "SP / B": sp, "Steel fiber (vol%)": fv, "Total fiber (vol%)": fv,
              "Curing method": "20 C, 95 % RH room from demoulding until test", "Curing temperature (°C)": 20, "Curing RH (%)": 95,
              "Test age (days)": 28, "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "110x220",
              "Compressive strength (MPa)": fc, "Source table/page": "Table 3 (mix, fc), sect. 3.1",
              "Conversions / notes": f"{mid}. Proportions by cement weight; binder = cement + SF/MK; sand 0/2 mm. "
                                     "VERIFY: fc is the CHARACTERISTIC value (mean minus Student factor x s, 6 cylinders), not the mean; "
                                     "SP given as 'weight percentage of binder' with values 0.045-0.060, taken as fraction of binder; "
                                     "W/B is the 'effective' water/binder of Table 3; fibre type = steel (dimensions not given); curing time not stated. "
                                     + ("For UHPFRC-4 the components are percentages of its own cement content." if mid == "UHPFRC-4" else "")})
    rows.append(r)

# ---------- 3) Karim et al.: non-proprietary UHPC (NP1-NP4, NP-HSF), 7 d fc
P = {"Article Name": "Assessment of transport properties, volume stability, and frost resistance of non-proprietary ultra-high performance concrete",
     "Author": "Rizwan Karim, Meysam Najimi, Behrouz Shafei", "Year": 2019,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2019.117031"}
# id, sand+masonry sand, SF, w/c, HRWR, fc
for mid, sa, sf, wc, hr, fc in [("NP1", 1.40, .07, .20, .090, 97.2), ("NP2", 1.20, .07, .20, .110, 97.9), ("NP3", 1.20, .07, .25, .047, 86.9),
                                 ("NP4", 1.40, .07, .25, .034, 77.2), ("NP-HSF", 1.40, .25, .25, .060, 71.7)]:
    B = 1 + sf
    r = dict(P)
    r.update({"OPC / Cement": r4(1 / B), "SF (Silica fume)": r4(sf / B), "W / B": r4(wc / B), "Sand (type not stated) / B": r4(sa / B),
              "SP / B": r4(hr / B), "Steel fiber (vol%)": 2.0, "Total fiber (vol%)": 2.0,
              "Curing method": "demoulded after 1 d, then stored in curing room until test (temperature/RH not stated)",
              "Demolding age (days)": 1, "Test age (days)": 7, "Compressive specimen": "cylinder", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 2 (mix, ratios by weight), Table 3 (7-d fc), sect. 2.4",
              "Conversions / notes": f"{mid}. Ratios by weight of cement; B = cement + SF; sand = fine aggregate + masonry sand (sum). "
                                     "Mixes NP-GMS (unexplained footnote) and proprietary P1, P2 skipped. Steel fibre 2 % of concrete volume (type/dimensions not stated). "
                                     "VERIFY: HRWR ratios 0.034-0.110 (to cement, as dosed) look high; cylinder size not stated. "
                                     "Split tensile strength (Table 3) not entered. Year from DOI."})
    rows.append(r)

# ---------- 4) Yu et al.: UHDCC (PE fibre), size effect; tension of 10/20/40 mm dog-bones + cylinder fc
P = {"Article Name": "Experimental study on the size effect of ultra-high ductile cementitious composites",
     "Author": "Jiangtao Yu, Fangyuan Dong, Junhong Ye", "Year": 2019,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2019.117963"}
B = 711.6 + 853.9
for th, fcr, ft, et in [(10, 2.86, 4.28, 8.01), (20, 2.57, 4.25, 7.24), (40, 3.23, 3.78, 9.66)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(711.6 / B), "FA (Fly ash)": r4(853.9 / B), "W / B": r4(394.5 / B), "Sand (type not stated) / B": r4(569.3 / B),
              "SP / B": r4(4.8 / B), "Binder content (kg/m³)": round(B, 1), "PE fiber (vol%)": 2.0, "PE diameter (µm)": 24,
              "PE tensile strength (MPa)": 2900, "PE elastic modulus (GPa)": 116, "Total fiber (vol%)": 2.0,
              "Curing method": "sealed in mould (plastic film) and demoulded after 2 d, then laboratory air 28 d", "Curing time (days)": 30,
              "Demolding age (days)": 2, "Test age (days)": 30, "Compressive specimen": "cylinder",
              "Compressive specimen size (mm)": "100x200", "Tensile specimen": f"dog-bone, thickness {th} mm", "Tensile gauge length (mm)": 80,
              "Tensile test type": DIRECT, "Compressive strength (MPa)": 26.20, "First-cracking strength (MPa)": fcr,
              "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": et,
              "Source table/page": "Table 1 (mix, g/L), Table 2 (PE), Table 5 (tension), Table 7 (cylinder fc), sect. 2.2",
              "Conversions / notes": f"Dog-bone thickness {th} mm (10, 15, 20, 30, 40, 60 mm tested; 10/20/40 entered). Mix in g/L (B = cement + FA = 1565.5); "
                                     "fibre 19.4 g/L / 0.97 = 2.0 vol%. fc = phi100x200 cylinder without end-friction reduction (also 25.17 / 25.65 for phi50 / phi75; cubes 31-37 MPa), "
                                     "same value on all three rows. First cracking = sigma_tc, strength = sigma_tp, strain = eps_tu (last stress drop). "
                                     "VERIFY: test age 30 d derived from '2 d in mould + 28 d in air'; sand type and PE length not stated."})
    rows.append(r)

# ---------- 5) Si et al.: PVA-FRCC, 28 fibre mixes (control M without fibre skipped)
P = {"Article Name": "Establishment of fiber factor for rheological and mechanical performance of polyvinyl alcohol (PVA) fiber reinforced mortar",
     "Author": "Wen Si, Mingli Cao, Li Li", "Year": 2020, "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2020.120347"}
fib = {"CS": (6, 40, 1500, 36.7), "CL": (12, 40, 1500, 36.7), "JL": (12, 31, 1600, 39)}
fc = {"CS": [73.00, 76.88, 70.94, 77.69, 75.63, 77.75, 70.31, 75.88, 68.50, 70.95],
      "CL": [72.63, 73.13, 71.81, 75.88, 72.38, 72.75, 71.38, 69.31, 68.13],
      "JL": [69.94, 78.50, 79.63, 80.00, 82.56, 80.44, 77.94, 77.88, 78.63]}
vf = {"CS": [.1, .3, .5, .8, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5], "CL": [.1, .3, .5, .8, 1.0, 1.5, 2.0, 2.5, 3.0],
      "JL": [.1, .3, .5, .8, 1.0, 1.5, 2.0, 2.5, 3.0]}
for k in ["CS", "CL", "JL"]:
    L, d, ts, E = fib[k]
    for v, f in zip(vf[k], fc[k]):
        r = dict(P)
        r.update({"OPC / Cement": 1.0, "W / B": 0.3, "SS / B (Silica sand)": 0.5, "SP / B": 0.0035, "PVA fiber (vol%)": v,
                  "PVA length (mm)": L, "PVA diameter (µm)": d, "PVA tensile strength (MPa)": ts, "PVA elastic modulus (GPa)": E,
                  "Total fiber (vol%)": v, "Curing method": "20 C room 24 h, demoulded, water tank at constant temperature to 28 d",
                  "Curing time (days)": 28, "Demolding age (days)": 1, "Test age (days)": 28, "Compressive strength (MPa)": f,
                  "Source table/page": "Table 2 (fibres), Table 3 (mix), Table 4 (fc), sect. 3.1-3.2",
                  "Conversions / notes": f"{k}{v}. W/C 0.3, S/C 0.5 (by mass), SP 0.35 % of cement, defoamer 0.1 % of volume (allowed). "
                                         "Control without fibre skipped. No tension test (flexural only). Water tank temperature not stated; fc specimen size not given in the text read."})
        rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e25.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows;", df["DOI / URL"].nunique(), "papers")

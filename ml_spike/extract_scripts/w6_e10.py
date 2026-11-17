"""Wave 6, agent e10: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e10.csv (99-column TEMPLATE header).
Papers: compstruct.2019.111198, compstruct.2020.112191, conbuildmat.2012.04.030, 2013.02.021, 2014.02.005,
        2017.01.060, 2017.10.040, 2017.11.072, 2017.12.175
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


# ---------------------------------------------- 1) hybrid PVA/steel SHCC, 7 d (compstruct 111198)
P = {"Article Name": "Mechanical performance of Strain-Hardening Cementitious Composites (SHCC) with hybrid polyvinyl alcohol and steel fibers",
     "Author": "Jing Yu, Yixin Chen, Christopher K.Y. Leung", "Year": 2019,
     "DOI / URL": "https://doi.org/10.1016/j.compstruct.2019.111198"}
t1 = [("P25S00", 2.5, 0.0, .0041, 32.73, 3.51, 5.85, 5.48), ("P20S05", 2.0, .5, .0040, 34.19, 3.95, 5.13, 5.08),
      ("P15S10", 1.5, 1.0, .0039, 35.53, 4.37, 5.74, 0.48), ("P00S25", 0.0, 2.5, .0031, 37.13, 4.51, 6.06, 0.19)]
for mid, pv, sv, sp, fc, fcr, ft, eps in t1:
    r = dict(P)
    r.update({"OPC / Cement": .18, "FA (Fly ash)": .80, "SF (Silica fume)": .02, "W / B": .20,
              "Sand (type not stated) / B": .20, "SP / B": sp, "Total fiber (vol%)": pv + sv,
              "Curing method": "covered, demolded 24 h, then fog room 23 C RH 95 % for 6 d", "Curing time (days)": 6,
              "Curing temperature (°C)": 23, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 7,
              "Tensile specimen": "coupon 175x50x15 mm", "Tensile gauge length (mm)": 50, "Tensile test type": DIRECT,
              "Compressive strength (MPa)": fc, "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft,
              "Tensile strain capacity (%)": eps, "Source table/page": "Table 1 (mix), Table 3 (fibers), Table 4 (7-d properties), sect. 2.1/2.2",
              "Conversions / notes": f"{mid}. Matrix by weight of binder (C 0.18, FA 0.80, SF 0.02). SP = solution with 30 % solids, as dosed. "
                                     "Test age 7 d (1 d + 6 d fog room, stated in Table 4 caption)."})
    if pv:
        r.update({"PVA fiber (vol%)": pv, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 42})
    if sv:
        r.update({"Steel fiber (vol%)": sv, "Steel length (mm)": 13, "Steel diameter (µm)": 160, "Steel tensile strength (MPa)": 2500, "Steel elastic modulus (GPa)": 210})
    rows.append(r)

# ---------------------------------------------- 2) ECC unconfined cylinders (compstruct 112191)
P = {"Article Name": "Axial compressive behavior of engineered cementitious composite confined by fiber-reinforced polymer",
     "Author": "Zheng Dang, Peng Feng, Jia-Qi Yang, Qian Zhang", "Year": 2020,
     "DOI / URL": "https://doi.org/10.1016/j.compstruct.2020.112191"}
r = dict(P)
r.update({"OPC / Cement": .5, "FA (Fly ash)": .5, "W / B": .27, "Sand (type not stated) / B": .36, "SP / B": .005,
          "PVA fiber (vol%)": 2, "PVA length (mm)": 12, "PVA diameter (µm)": 40,
          "PVA tensile strength (MPa)": 1560, "PVA elastic modulus (GPa)": 41, "Total fiber (vol%)": 2,
          "Curing method": "molds covered 24 h at 20 C, then standard curing 20 C RH > 95 % for 28 d", "Curing time (days)": 28,
          "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
          "Compressive specimen": "cylinder", "Compressive strength (MPa)": 64.6,
          "Source table/page": "Table 2 (mix, weight ratios to cement), Table 3 (fiber), Table 5 (E-U-M average)",
          "Conversions / notes": "ECC, matrix ratios by weight (C 1, FA 1, quartz sand 0.72, water 0.54, SP 0.01) divided by B = 2; water/cementitious 0.27 stated. "
                                 "Quartz sand (max 0.42 mm) taken as sand. Monotonic unconfined cylinders E-U-M average (cyclic E-U-C 66.0 not used). "
                                 "VERIFY: test age 28 d from the 28 d standard curing statement (unconfined cylinder test age not stated explicitly); cylinder size not stated. No tensile data in text."})
rows.append(r)

# ---------------------------------------------- 3) UHPFRC steel 2 vol%, 7/14/28 d (conbuildmat 2012.04.030)
P = {"Article Name": "Experimental test methods to determine the uniaxial tensile and compressive behaviour of ultra high performance fibre reinforced concrete (UHPFRC)",
     "Author": "A.M.T. Hassan, S.W. Jones, G.H. Mahmud", "Year": 2012,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2012.04.030"}
B = 657 + 418 + 119
for age, ft, eps, fc in ((7, 8.97, 2781, 145.96), (14, 8.92, 1499, 149.05), (28, 9.07, 2749, 150.56)):
    r = dict(P)
    r.update({"OPC / Cement": r4(657 / B), "GGBS": r4(418 / B), "SF (Silica fume)": r4(119 / B), "W / B": r4(185 / B),
              "SS / B (Silica sand)": r4(1051 / B), "SP / B": r4(40 / B), "Binder content (kg/m³)": B,
              "Steel fiber (vol%)": 2, "Steel length (mm)": 13, "Total fiber (vol%)": 2, "Test age (days)": age,
              "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "50x100",
              "Tensile specimen": "dog-bone, reduced section 26x50 mm", "Tensile test type": DIRECT,
              "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": r4(eps / 1e4),
              "Source table/page": "Table 1 (mix), Table 2 (tensile and compressive vs age), sect. 3",
              "Conversions / notes": f"UHPFRC {age} d; UHPC (no fiber) skipped. kg/m3 / B (cement+GGBS+SF = 1194). Silica sand 1051 kg/m3 (avg 0.27 mm). "
                                     "Strain = strain corresponding to max tensile stress (microstrain / 1e4 = %). Curing regime not stated. Steel fiber 157 kg/m3 = 2 vol% as stated; length 13 mm from text."})
    rows.append(r)

# ---------------------------------------------- 4) hybrid PVA+steel ECC, fc 28 d (conbuildmat 2013.02.021)
P = {"Article Name": "Material properties of a new hybrid fibre-reinforced engineered cementitious composite",
     "Author": "Khin T. Soe, Y.X. Zhang, L.C. Zhang", "Year": 2013,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2013.02.021"}
for mid, pv, sv, fc in (("ECC_M1", 1.5, .5, 67), ("ECC_M2", 1.75, .58, 69)):
    r = dict(P)
    r.update({"OPC / Cement": r4(1 / 2.2), "FA (Fly ash)": r4(1.2 / 2.2), "W / B": r4(.56 / 2.2), "Sand (type not stated) / B": r4(.8 / 2.2),
              "HRWR / B": r4(.012 / 2.2), "PVA fiber (vol%)": pv, "PVA length (mm)": 8, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600,
              "PVA elastic modulus (GPa)": 66, "Steel fiber (vol%)": sv, "Steel length (mm)": 12, "Steel diameter (µm)": 200,
              "Steel tensile strength (MPa)": 2600, "Steel elastic modulus (GPa)": 200, "Total fiber (vol%)": pv + sv,
              "Curing method": "covered 24 h, demolded, curing chamber 23 C RH 100 % until test", "Curing time (days)": 28,
              "Curing temperature (°C)": 23, "Curing RH (%)": 100, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 1 (fibers), Table 2 (mix, weight ratios), Table 4 / sect. 3.2 (fc)",
              "Conversions / notes": f"{mid}. Ratios by weight to cement, B = 2.2. Direct tension data only at strain rates 1e-5 to 1e-1 /s with test age not stated, so not entered. "
                                     "Strength values are rounded integers (Table 4)."})
    rows.append(r)

# ---------------------------------------------- 5) fly ash geopolymer + PVA, three curing regimes (conbuildmat 2014.02.005)
P = {"Article Name": "A feasibility study of strain hardening fiber reinforced fly ash-based geopolymer composites",
     "Author": "Motohiro Ohno, Victor C. Li", "Year": 2014,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2014.02.005"}
for mid, cm, hh, fc, ft, eps in (("R", "air at room temperature 23 C until 28 d", None, 17.4, 2.9, 2.7),
                                 ("T60-4", "oven 60 C for 4 h, then air at room temperature until 28 d", 4, 20.9, 3.2, 3.8),
                                 ("T60-8", "oven 60 C for 8 h, then air at room temperature until 28 d", 8, 27.6, 3.4, 4.3)):
    r = dict(P)
    r.update({"FA (Fly ash)": 1.0, "WG / B (Water glass)": .256, "NaOH / B": .056, "W / B": r4(.039 + .12),
              "SS / B (Silica sand)": .3, "PVA fiber (vol%)": 2, "PVA length (mm)": 12, "PVA diameter (µm)": 39,
              "PVA tensile strength (MPa)": 1620, "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": 2,
              "Curing method": cm, "Curing time (days)": 28, "Curing temperature (°C)": 60 if hh else 23, "Demolding age (days)": 1,
              "Test age (days)": 28, "Heat curing duration (h)": hh, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50.8",
              "Tensile specimen": "dog-bone (JSCE)", "Tensile gauge length (mm)": 100, "Tensile test type": DIRECT,
              "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix), Table 3 (fiber), Table 4 (28 d properties), sect. 2.2/2.3",
              "Conversions / notes": f"{mid}. Class F fly ash A 0.8 + B 0.2 (= B, 1.0). Na2SiO3 0.256 is a sodium silicate solution (water glass as dosed, solids not given). "
                                     "W/B = pre-mix water 0.039 + mix water 0.12 (water in the silicate solution not added). Fine silica sand 110 um."})
    rows.append(r)

# ---------------------------------------------- 6) UHDCC (conbuildmat 2017.01.060)
P = {"Article Name": "A strain-hardening cementitious composites with the tensile capacity up to 8%",
     "Author": "Kequan Yu, Yichao Wang, Jiangtao Yu, Shilang Xu", "Year": 2017,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2017.01.060"}
mixes = {"UHDCC-1": dict(c=593.0, fa=711.6, g=0, sf=0, sand=474.4, w=313.1, hr=4.0, fc_cyl=23.67, fc_cube=52.60, ft=6.52, fcr=2.24, eps=7.98),
         "UHDCC-2": dict(c=936.7, fa=201.4, g=0, sf=0, sand=601.1, w=361.3, hr=4.2, fc_cyl=19.20, fc_cube=45.86, ft=6.07, fcr=3.20, eps=11.98),
         "UHDCC-3": dict(c=500.0, fa=0, g=650, sf=150, sand=700.0, w=230.0, hr=25.0, fc_cyl=95.55, fc_cube=121.50, ft=17.84, fcr=9.86, eps=8.49)}
for mid, m in mixes.items():
    B = m["c"] + m["fa"] + m["g"] + m["sf"]
    base = dict(P)
    base.update({"OPC / Cement": r4(m["c"] / B), "FA (Fly ash)": r4(m["fa"] / B) or None, "GGBS": r4(m["g"] / B) or None,
                 "SF (Silica fume)": r4(m["sf"] / B) or None, "W / B": r4(m["w"] / B), "Sand (type not stated) / B": r4(m["sand"] / B),
                 "HRWR / B": r4(m["hr"] / B), "Binder content (kg/m³)": round(B, 1), "PE fiber (vol%)": 2, "Total fiber (vol%)": 2,
                 "Demolding age (days)": 1})
    r = dict(base)
    r.update({"Curing method": "demolded after 1 d, cured in air for 6 months before testing", "Curing time (days)": 180, "Test age (days)": 180,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Compressive strength (MPa)": m["fc_cube"],
              "Tensile specimen": "dog-bone (JSCE)", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
              "Tensile strength (MPa)": m["ft"], "First-cracking strength (MPa)": m["fcr"], "Tensile strain capacity (%)": m["eps"],
              "Source table/page": "Table 2 (mix kg/m3), Table 7 (tensile), Table 8 (fc), sect. 2.2",
              "Conversions / notes": f"{mid}. kg/m3 / B (cement+FA+GGBFS+SF). PE fiber 19 kg/m3 = 1.96 vol% (2 vol% implied by text). Fiber 1 or 2 (Table 4) not assigned to mixes, so PE geometry left empty. "
                                     "VERIFY: test age 6 months taken as 180 d (derived). Tensile strain = Table 7 strain capacity (averaged). "
                                     + ("VERIFY: text gives peak tensile strength 18.17 MPa, Table 7 gives 17.84 (Table used). " if mid == "UHDCC-3" else "")})
    rows.append(r)
    r = dict(base)
    r.update({"Curing method": "demolded after 1 d, air curing, 28 d", "Curing time (days)": 28, "Test age (days)": 28,
              "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "50x100", "Compressive strength (MPa)": m["fc_cyl"],
              "Source table/page": "Table 2 (mix), Table 8 (cylinder fc), sect. 2.3",
              "Conversions / notes": f"{mid}. Cylinders compressed after 28 d curing (text). kg/m3 / B. Curing medium of the 28 d cylinders assumed same as the other specimens (air); VERIFY."})
    rows.append(r)

# ---------------------------------------------- 7) UHP-ECC with PE fibers (conbuildmat 2017.10.040)
P = {"Article Name": "Development of ultra-high performance engineered cementitious composites using polyethylene (PE) fibers",
     "Author": "Ke-Quan Yu, Jiang-Tao Yu, Jian-Guo Dai, Zhou-Dao Lu, Surendra P. Shah", "Year": 2017,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2017.10.040"}
B = 800 + 150 + 750
r = dict(P)
r.update({"OPC / Cement": r4(800 / B), "GGBS": r4(750 / B), "SF (Silica fume)": r4(150 / B), "W / B": r4(230 / B),
          "SS / B (Silica sand)": r4(500 / B), "HRWR / B": r4(25 / B), "Binder content (kg/m³)": B,
          "PE fiber (vol%)": 2, "PE length (mm)": 18, "PE diameter (µm)": 20, "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 100,
          "Total fiber (vol%)": 2, "Curing time (days)": 28, "Test age (days)": 28, "Compressive specimen": "cube",
          "Compressive specimen size (mm)": "100", "Compressive strength (MPa)": 112.69,
          "Tensile specimen": "dumbbell (JSCE 2008)", "Tensile gauge length (mm)": 100, "Tensile test type": DIRECT,
          "Tensile strength (MPa)": 17.42, "First-cracking strength (MPa)": 10.3, "Tensile strain capacity (%)": 8.17,
          "Source table/page": "Table 3 (mix), Table 4 (PE), Table 5 (fc), sect. 3.2 and Conclusions (tensile)",
          "Conversions / notes": "kg/m3 / B (C+SF+GGBFS = 1700). W/B 0.135 stated (excl. HRWRA water). 100 mm cube fc 112.69 (70.7 mm cube 121.50 not used). "
                                 "Tensile strength, first-cracking and rupture strain from text (conclusions). Curing regime (medium) not stated; "
                                 "VERIFY: dumbbells 'tested after 28 days curing', compression age not stated (28 d assumed same series)."})
rows.append(r)

# ---------------------------------------------- 8) ECC with low-cost PVA, tensile only (conbuildmat 2017.11.072)
P = {"Article Name": "Matrix tailoring of Engineered Cementitious Composites (ECC) with non-oil-coated, low tensile strength PVA fiber",
     "Author": "Zhigang Zhang, Qian Zhang", "Year": 2017,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2017.11.072"}
# id: (fa ratio, sand, CR, water, hrwr, vma, fiber type, E, fcr, ft, eps)
t8 = [("M2.2-K", 2.2, 1.16, 0, .8, .013, 0, "K", 18.0, 3.83, 6.49, 3.8), ("M2.2-C", 2.2, 1.16, 0, .8, .013, 0, "C", 17.0, 3.77, 4.49, 1.2),
      ("M2.2VMA-C", 2.2, 1.16, 0, .8, .013, .0005, "C", 18.4, 3.91, 5.56, 2.1), ("M4.0-C", 4.0, 1.8, 0, 1.24, .018, 0, "C", 14.8, 2.83, 4.41, 2.4),
      ("M2.2CR-C", 2.2, .87, .14, .8, .013, 0, "C", 13.1, 2.88, 5.07, 5.2)]
for mid, fa, sand, cr, w, hr, vma, ft_, E, fcr, ft, eps in t8:
    B = 1 + fa
    r = dict(P)
    r.update({"OPC / Cement": r4(1 / B), "FA (Fly ash)": r4(fa / B), "W / B": r4(w / B), "Sand (type not stated) / B": r4(sand / B),
              "Crumb rubber / B": r4(cr / B) if cr else None, "HRWR / B": r4(hr / B), "VMA / B": r4(vma / B) if vma else None,
              "PVA fiber (vol%)": 2, "PVA length (mm)": 12, "PVA diameter (µm)": 39,
              "PVA tensile strength (MPa)": 1600 if ft_ == "K" else 1300, "PVA elastic modulus (GPa)": 42 if ft_ == "K" else 22, "Total fiber (vol%)": 2,
              "Curing method": "demolded after 1 d, air 20 C RH 40 %", "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 40,
              "Demolding age (days)": 1, "Test age (days)": 28, "Tensile specimen": "dog-bone (JSCE)", "Tensile test type": DIRECT,
              "Tensile strength (MPa)": ft, "First-cracking strength (MPa)": fcr, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (fiber), Table 2 (mix, weight ratios to cement), Table 3 (tensile), sect. 3.1",
              "Conversions / notes": f"{mid}. Ratios by weight to cement; B = cement + FA = {B}. Type-{ft_} PVA. VMA 0.05 % of cement. "
                                     "Crumb rubber replaces 25 vol% of silica sand. Compressive strengths only in Fig. 4 (text: ~45 MPa for M2.2 mixes), not entered. "
                                     "M2.2FAC-C (fly ash cenosphere) skipped."})
    rows.append(r)

# ---------------------------------------------- 9) PE fibre cement paste composites, fc (conbuildmat 2017.12.175)
P = {"Article Name": "Comparative strain and deflection hardening behaviour of polyethylene fibre reinforced ambient air and heat cured geopolymer composites",
     "Author": "Faiz Uddin Ahmed Shaikh, Anthony Fairchild, Ronnie Zammar", "Year": 2017,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2017.12.175"}
for v, fc in ((0.5, 59.1), (0.75, 59.0), (1.0, 47.0), (1.5, 33.0)):
    r = dict(P)
    r.update({"OPC / Cement": 1.0, "W / B": .4, "PE fiber (vol%)": v, "PE length (mm)": 12, "PE diameter (µm)": 12, "PE tensile strength (MPa)": 3500,
              "PE elastic modulus (GPa)": 123, "Total fiber (vol%)": v,
              "Curing method": "covered 24 h, demolded, wet cured in water 28 d", "Curing time (days)": 28, "Demolding age (days)": 1,
              "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 2 (mix), Table 3 (PE), Table 4 (fc), sect. 2.1",
              "Conversions / notes": f"CC-{v}%PE cement paste (no sand). Geopolymer series skipped (activator quantities unclear in table). "
                                     "VERIFY: SP content garbled in Table 2 (only '3.5 %' shown for CC-1.5%PE), left empty; test age 28 d derived from the 28 d wet curing statement. "
                                     "Tensile strain only in a figure, not entered."})
    rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e10.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows ->", os.path.join(out_dir, "w6_e10.csv"))

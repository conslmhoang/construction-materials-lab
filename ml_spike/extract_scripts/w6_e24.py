"""Wave 6, agent e24: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e24.csv (99-column TEMPLATE header).
Papers: conbuildmat.2014.08.089, 2008.02.018, 2017.07.158
"""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
add = os.path.join(here, "..", "additions")
out_dir = os.path.join(here, "..", "additions_v2")
cols = list(pd.read_csv(os.path.join(add, "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
rows = []


def r4(x):
    return round(x, 4)


# ---------- 1) Keskin et al.: PVA ECC with FA or GGBFS, 4 mixes x 4 ages
P = {"Article Name": "Correlation between the viscoelastic properties and cracking potential of engineered cementitious composites",
     "Author": "Suleyman Bahadir Keskin, Mustafa Sahmaran, Ismail Ozgur Yaman, Mohamed Lachemi", "Year": 2014,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2014.08.089"}
mixes = {"F 1.2": ("FA", 1.2, {7: (40.1, 4.26), 14: (51.3, 4.54), 28: (69.3, 4.59), 90: (75.8, 4.62)}),
         "F 2.2": ("FA", 2.2, {7: (30.2, 3.13), 14: (35.9, 3.49), 28: (46.1, 3.49), 90: (54.7, 3.51)}),
         "S 1.2": ("GGBS", 1.2, {7: (59.9, 4.57), 14: (72.4, 4.91), 28: (88.5, 5.91), 90: (91.2, 5.94)}),
         "S 2.2": ("GGBS", 2.2, {7: (51.8, 3.84), 14: (64.2, 4.20), 28: (76.3, 4.50), 90: (80.3, 4.59)})}
for mid, (ma, ratio, d) in mixes.items():
    B = 1 + ratio
    for age, (fc, ft) in d.items():
        r = dict(P)
        r.update({"OPC / Cement": r4(1 / B), ("FA (Fly ash)" if ma == "FA" else "GGBS"): r4(ratio / B),
                  "W / B": 0.27, "SS / B (Silica sand)": 0.36, "PVA fiber (vol%)": 2.0, "Total fiber (vol%)": 2.0,
                  "Curing method": "demolded 24 h, 7 d at 95 % RH 23 C in plastic bags, then 50 % RH 23 C until test",
                  "Curing time (days)": age, "Curing temperature (°C)": 23, "Curing RH (%)": 50, "Demolding age (days)": 1,
                  "Test age (days)": age, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
                  "Tensile specimen": "briquet", "Tensile test type": "direct (uniaxial)",
                  "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft,
                  "Source table/page": "Table 2 (mix), Table 3 (fc, tensile strength), sect. 2.2",
                  "Conversions / notes": f"{mid}. Ratios by mass to PC / CM as given (MA/PC = {ratio}, W/CM 0.27, S/CM 0.36). "
                                         "HRWR given only in kg/m3 (no mix density), SP/B left empty. Tensile strain capacity not reported. "
                                         "VERIFY: tensile strength measured on briquet specimens (direct tension assumed); the 90 d tensile value is in Table 3 but the text only describes tests at 7, 14, 28 d. "
                                         "Curing time = test age (same environment until test)."})
        rows.append(r)

# ---------- 2) Tafraoui et al.: UHPC SF vs MK, fibre mixes SFF and MKF (quartz mixes skipped)
P = {"Article Name": "Metakaolin in the formulation of UHPC",
     "Author": "Ahmed Tafraoui, Gilles Escadeillas, Soltane Lebaili, Thierry Vidal", "Year": 2009,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2008.02.018"}
mk = {"SFF": dict(c=818, sa=899, sf=204, fi=164, sp=26.0, w=221.8, sfk="SF (Silica fume)", fc=(192.0, 204.0, 234.0)),
      "MKF": dict(c=824, sa=906, sf=206, fi=165, sp=26.2, w=223.4, sfk="Metakaolin", fc=(161.0, 195.0, 212.0))}
for mid, m in mk.items():
    B = m["c"] + m["sf"]
    for i in range(3):
        r = dict(P)
        r.update({"OPC / Cement": r4(m["c"] / B), m["sfk"]: r4(m["sf"] / B), "W / B": r4(m["w"] / B),
                  "SS / B (Silica sand)": r4(m["sa"] / B), "SP / B": r4(m["sp"] / B), "Binder content (kg/m³)": B,
                  "Steel fiber (vol%)": r4(m["fi"] / 7850 * 100), "Steel length (mm)": 13, "Steel diameter (µm)": 160,
                  "Total fiber (vol%)": r4(m["fi"] / 7850 * 100), "Demolding age (days)": 1,
                  "Compressive specimen": "prism halves", "Compressive specimen size (mm)": "40x40x160 (half prisms)",
                  "Compressive strength (MPa)": m["fc"][i],
                  "Source table/page": "Table 3 (mix, kg/m3), Table 6 (fc), sect. 2.3.2-2.3.3",
                  "Conversions / notes": f"{mid}. kg/m3 / B (cement + {'SF' if mid == 'SFF' else 'MK'} = {B}); W/B from total water in Table 3 (stated 0.22). "
                                         "Fibre vol% = kg/m3 / 7850 (VERIFY, density not given). Mixes with crushed quartz (SFQ, SFQF, MKQ, MKQF) and fibre-free SF, MK skipped. "
                                         "Flexural strength not entered. SP: acrylic copolymer."})
        if i == 0:
            r.update({"Curing method": "24 h at 20 C sealed, demoulded, water 20 C until 28 d", "Curing time (days)": 28,
                      "Curing temperature (°C)": 20, "Test age (days)": 28})
        else:
            t = 90 if i == 1 else 150
            r.update({"Curing method": f"24 h at 20 C sealed, demoulded, 4 d water 20 C, then thermal treatment {t} C (cycle in Fig. 2)",
                      "Curing time (days)": 5, "Curing temperature (°C)": t, "Test age (days)": 6})
            r["Conversions / notes"] += (" VERIFY: test age 6 d derived (1 d in mould + 5 d after demoulding, tested after cooling of heat cycle); "
                                         "heat treatment duration only in Fig. 2, left empty.")
        rows.append(r)

# ---------- 3) Alsalman et al.: UHPC with steel fibres, groups A-C (river sand); group D (fly ash as aggregate) skipped
P = {"Article Name": "Evaluation of modulus of elasticity of ultra-high performance concrete",
     "Author": "Ali Alsalman, Canh N. Dang, Gary S. Prinz, W. Micah Hale", "Year": 2017,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2017.07.158"}
grp = {"A": (1365, 30.26, 647, [2, 3, 4], [137.9, 140.8, 155.3]),
       "B": (1600, 38.22, 310, [6, 7, 8], [135.9, 143.2, 145.7]),
       "C": (1600, 77.22, 310, [10, 11, 12], [128.3, 127.6, 144.1])}
for g, (B, hr, sa, ids, fcs) in grp.items():
    for vf, uid, fc in zip([2, 4, 6], ids, fcs):
        r = dict(P)
        r.update({"OPC / Cement": 0.8, "SF (Silica fume)": 0.2, "W / B": 0.2, "River sand / B": r4(sa / B), "SP / B": r4(hr / B),
                  "Binder content (kg/m³)": B, "Steel fiber (vol%)": vf, "Steel length (mm)": 12.7, "Steel diameter (µm)": 200,
                  "Total fiber (vol%)": vf,
                  "Curing method": "demolded 1 d, then heat 100 % RH: 2 d at 60 C and 3 d at 90 C, then environmental chamber until 28 d",
                  "Curing time (days)": 5, "Curing temperature (°C)": 90, "Curing RH (%)": 100, "Demolding age (days)": 1,
                  "Test age (days)": 28, "Heat curing duration (h)": 120, "Compressive specimen": "cylinder",
                  "Compressive specimen size (mm)": "75x150", "Compressive strength (MPa)": fc,
                  "Source table/page": "Table 3 (mix), Table 5 (fc at 28 d), sect. 3.5 (curing)",
                  "Conversions / notes": f"UHPC-{uid}, group {g}, fibre {vf} vol%. Binder = cement 80 % + SF 20 % (B in Table 3). kg/m3 / B. Fine-1 = Arkansas river sand. "
                                         "Fibre-free mixes and group D (class C fly ash as fine aggregate) skipped. W/B 0.2 as stated; HRWRA kg/m3 as dosed. "
                                         "Heat curing 5 d: duration of 120 h = 2 d + 3 d."})
        rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e24.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows;", df["DOI / URL"].nunique(), "papers")

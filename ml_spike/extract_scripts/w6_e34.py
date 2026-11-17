"""Wave 6, agent e34: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e34.csv (99-column TEMPLATE header).
Papers: compositesb.2011.10.005, compositesb.2018.12.083, compstruct.2023.117570,
        conbuildmat.2012.05.031, conbuildmat.2016.02.102
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


def paper(name, author, year, doi):
    return {"Article Name": name, "Author": author, "Year": year, "DOI / URL": "https://doi.org/" + doi}


# ---------- 1) Cavdar 2012: PVA fibre mortars at 21 C (reference condition of the high-temperature study)
P = paper("A study on the effects of high temperature on mechanical properties of fiber reinforced cementitious composites",
          "Ahmet Cavdar", 2012, "10.1016/j.compositesb.2011.10.005")
for pva, fc in [(0.5, 47.8), (1.0, 39.19), (1.5, 41.9), (2.0, 46.99)]:
    r = dict(P)
    r.update({"OPC / Cement": 1.0, "W / B": 0.5, "Sand (type not stated) / B": 3.0, "PVA fiber (vol%)": pva, "PVA length (mm)": 12,
              "PVA diameter (µm)": 660, "PVA tensile strength (MPa)": 900, "PVA elastic modulus (GPa)": 23, "Total fiber (vol%)": pva,
              "Curing method": "moist room 21 C 24 h, demoulded, tap water 30 d (tested at 21 C, surface-dry)",
              "Curing time (days)": 30, "Curing temperature (°C)": 21, "Demolding age (days)": 1, "Test age (days)": 31,
              "Compressive specimen": "prism half (EN 196)", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 3 (mix), Table 1 (fibre), Table 7 (fc, 21 C rows), sect. 2",
              "Conversions / notes": f"PVA {pva} vol%. Mortar by weight 450 g cement : 1350 g standard sand : 225 g water (EN 196), no admixture. "
                                     "Only the 21 C (unheated) compressive result kept; 100/450/650 C rows and no-fibre control skipped. "
                                     "VERIFY: test age 31 d = 24 h mould + 30 d water (paper says 30 days in water). "
                                     "VERIFY: PVA diameter 660 um as printed in Table 1 (looks odd for a PVA fibre). Fibre vol% from the Table 3 row heading."})
    rows.append(r)

# ---------- 2) Ahmad et al. 2019: steel-fibre UHPC, room-temperature control specimens
P = paper("Mechanical properties of steel fiber-reinforced UHPC mixtures exposed to elevated temperature: Effects of exposure duration and fiber content",
          "Shamsad Ahmad, Mehboob Rasul, Saheed Kolawole Adekunle, Salah U. Al-Dulaijan, Mohammed Maslehuddin, Syed Imran Ali",
          2019, "10.1016/j.compositesb.2018.12.083")
B = 900 + 220
for nm, sand, st, fc in [("MFC2", 1040, 50, 143), ("MFC4", 1024, 100, 143), ("MFC6", 1005, 157, 148), ("MFC8", 991, 200, 157)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(900 / B), "SF (Silica fume)": r4(220 / B), "W / B": r4(162 / B), "Dune sand / B": r4(sand / B),
              "SP / B": r4(40 / B), "Binder content (kg/m³)": B, "Steel fiber (vol%)": r4(st / 7850 * 100),
              "Total fiber (vol%)": r4(st / 7850 * 100),
              "Curing method": "covered 24 h, demoulded, 28 d moist curing in indoor tank at room temperature, then 15 d air drying",
              "Curing time (days)": 28, "Demolding age (days)": 1, "Test age (days)": 43,
              "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "75 x 150", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 4 (mix, kg/m3), Table 6 (room-temperature control fc), sect. 2.2-2.3",
              "Conversions / notes": f"{nm}: steel fibre {st} kg/m3 (paper names it {nm[-1]} % by mass). Binder = cement + microsilica = {B}; W/B 162/{B} matches stated 0.145. "
                                     "VERIFY: fibre vol% = kg/m3 / 7850 (steel density not given). "
                                     "VERIFY: SP 40 kg/m3 in Table 4 but text says 50 kg/m3. "
                                     "VERIFY: test age 43 d = 28 d moist + 15 d air drying (control specimens not explicitly said to be air dried). "
                                     "Dune sand. Specimens heated to 300 C skipped; flexural data not used."})
    rows.append(r)

# ---------- 3) Zhao et al. 2023: UHPC with steel fibre 2 vol% (SF01), 28 d static fc
P = paper("Comparative study on the effect of steel and plastic synthetic fibers on the dynamic compression properties and microstructure of ultra-high-performance concrete (UHPC)",
          "Shuo Zhao, Runqing Liu, Jun Liu, Lihai Yang", 2023, "10.1016/j.compstruct.2023.117570")
B = 778 + 165
r = dict(P)
r.update({"OPC / Cement": r4(778 / B), "SF (Silica fume)": r4(165 / B), "W / B": r4(179 / B), "SS / B (Silica sand)": r4((226 + 1010) / B),
          "SP / B": r4(21 / B), "Binder content (kg/m³)": B, "Steel fiber (vol%)": 2.0, "Steel length (mm)": 30, "Steel diameter (µm)": 900,
          "Steel tensile strength (MPa)": 1200, "Steel elastic modulus (GPa)": 108, "Total fiber (vol%)": 2.0,
          "Curing method": "curing room 20 +/- 2 C, RH > 95 % for 24 h, demoulded, curing room 28 d", "Curing time (days)": 28,
          "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
          "Compressive specimen": "cube", "Compressive specimen size (mm)": "40", "Compressive strength (MPa)": 139.1,
          "Source table/page": "Table 3 (mix, kg/m3), Table 2 (fibre), Table 4 (static fc 28 d)",
          "Conversions / notes": "Mix SF01 only (2 vol% hooked steel fibre). PS (plastic synthetic) fibre mixes and no-fibre S0P0 skipped. "
                                 f"kg/m3 / B (cement + silica fume = {B}). Silica sand 1 (226) + sand 2 (1010) summed. "
                                 "fc = static compressive strength in Table 4 (40 mm cubes cut from broken prisms, GB/T 17671). Dynamic SHPB data not used. "
                                 "VERIFY: age stated '28 d' (24 h in curing room, then 28 d curing room)."})
rows.append(r)

# ---------- 4) Zheng et al. 2012: steel fibre RPC (SRPC1-3), 20 C reference compressive (prism)
P = paper("Compressive stress-strain relationship of steel fiber-reinforced reactive powder concrete after exposure to elevated temperatures",
          "Wenzhong Zheng, Haiyan Li, Ying Wang", 2012, "10.1016/j.conbuildmat.2012.05.031")
for nm, c, sf, sl, qs, wr, w, vf, fc in [("SRPC1", 808.70, 242.61, 121.31, 970.44, 46.90, 234.52, 1, 142.92),
                                         ("SRPC2", 800.53, 240.16, 120.08, 960.64, 46.43, 232.15, 2, 155.59),
                                         ("SRPC3", 792.37, 237.71, 118.85, 950.84, 45.96, 229.79, 3, 159.21)]:
    B = c + sf + sl
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), "SF (Silica fume)": r4(sf / B), "GGBS": r4(sl / B), "W / B": r4(w / B),
              "SS / B (Silica sand)": r4(qs / B), "SP / B": r4(wr / B), "Binder content (kg/m³)": r4(B),
              "Steel fiber (vol%)": vf, "Total fiber (vol%)": vf,
              "Curing method": "24 h standard conditions, demoulded, 3 d at 90 C in accelerated curing box, standard curing room 60 d, then air 2 months; tested at 20 C",
              "Curing time (days)": 64, "Curing temperature (°C)": 90, "Heat curing duration (h)": 72, "Demolding age (days)": 1, "Test age (days)": 124,
              "Compressive specimen": "prism", "Compressive specimen size (mm)": "70.7 x 70.7 x 228", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 1 (mix, kg/m3; fc = prismatic strength at room temperature), sect. 2.2",
              "Conversions / notes": f"{nm}: steel fibre {vf} vol% (Table 1 'volume dosage' 0.0{vf}). Binder = cement + silica fume + slag = {r4(B)}. "
                                     "Quartz sand used as sand. Water reducer entered as SP / B. Table 1 columns read as printed: WR about 4 % of binder, W/B 0.20. "
                                     "VERIFY: test age 124 d = 1 + 3 + 60 d + about 2 months air exposure. fc is PRISMATIC strength (70.7 x 70.7 x 228 mm), not cube. "
                                     "Rows at 120-900 C skipped. Steel fibre dimensions not given."})
    rows.append(r)

# ---------- 5) Sobuz et al. 2016: UHPC without coarse aggregate, mixes 1-18 (FM 2.13 / 2.34 / 2.79), 7/28/56/90 d
P = paper("Manufacturing ultra-high performance concrete utilising conventional materials and production methods",
          "H.R. Sobuz, P. Visintin, M.S. Mohamed Ali, M. Singh, M.C. Griffith, A.H. Sheikh", 2016, "10.1016/j.conbuildmat.2016.02.102")
tab2 = {1: (2.13, .1775, .045), 2: (2.13, .17, .0565), 3: (2.13, .165, .0642), 4: (2.13, .1775, .0192), 5: (2.13, .17, .0307), 6: (2.13, .165, .0384),
        7: (2.34, .1775, .045), 8: (2.34, .17, .0565), 9: (2.34, .165, .0642), 10: (2.34, .1775, .0192), 11: (2.34, .17, .0307), 12: (2.34, .165, .0384),
        13: (2.79, .1775, .045), 14: (2.79, .17, .0565), 15: (2.79, .165, .0642), 16: (2.79, .1775, .0192), 17: (2.79, .17, .0307), 18: (2.79, .165, .0384)}
tab5 = {1: (117, 139, 149, 141), 2: (117, 145, 152, 147), 3: (112, 147, 143, 146), 4: (123, 150, 153, 150), 5: (120, 149, 148, 146), 6: (128, 153, 153, 155),
        7: (107, 136, 138, 144), 8: (102, 141, 150, 138), 9: (107, 141, 153, 141), 10: (131, 146, 148, 139), 11: (130, 143, 157, 150), 12: (123, 137, 162, 158),
        13: (112, 138, 149, 153), 14: (110, 141, 151, 154), 15: (110, 138, 153, 143), 16: (121, 150, 134, 154), 17: (119, 148, 151, 151), 18: (124, 148, 155, 151)}
B = 1.266  # cement 1 + silica fume 0.266
for m, (fm, wc, spc) in tab2.items():
    # fibre volume per unit cement mass (assumed densities: cement 3.15, sand 2.65, SF 2.2, water 1, SP liquid 1.1, steel 7.85)
    vol = 1 / 3.15 + 1 / 2.65 + 0.266 / 2.2 + wc + spc / 1.1 + 0.233 / 7.85
    vf = r4(0.233 / 7.85 / vol * 100)
    for i, age in enumerate((7, 28, 56, 90)):
        r = dict(P)
        r.update({"OPC / Cement": r4(1 / B), "SF (Silica fume)": r4(0.266 / B), "W / B": r4(wc / B), "SP / B": r4(spc / B),
                  "Steel fiber (vol%)": vf, "Total fiber (vol%)": vf,
                  "Curing method": "fog room until test", "Curing time (days)": age, "Test age (days)": age,
                  "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100 x 200", "Compressive strength (MPa)": tab5[m][i],
                  "Source table/page": "Table 2 (w:c, sp:c, FM), Table 5 (fc 7/28/56/90 d), note under Table 2 (1:1:0.266:0.233)",
                  "Conversions / notes": f"Mix {m}-FA, sand FM {fm}. Weight ratio cement : aggregate : silica fume : steel fibre = 1 : 1 : 0.266 : 0.233; "
                                         f"B = cement + SF = 1.266; W/B = added water w:c {wc} / B (free water in SP not added; paper's total w:c includes it); SP = sp:c {spc} / B. "
                                         "VERIFY: steel fibre vol% DERIVED from the mass ratio with assumed densities (cement 3.15, sand 2.65, SF 2.2, steel 7.85), not stated in paper; "
                                         "fibre dimensions not given. Sulphate-resisting Portland cement. "
                                         + ("Washed river sand FM 2.34. " if fm == 2.34 else "Sand source for this FM not specified (mined / manufactured / river). ")
                                         + "Mixes 19-24 (FM 4.01 granulated lead slag) and the coarse-aggregate mixes skipped."})
        if fm == 2.34:
            r["River sand / B"] = r4(1 / B)
        else:
            r["Sand (type not stated) / B"] = r4(1 / B)
        rows.append(r)

df = pd.DataFrame(rows)
for c in cols:
    if c not in df.columns:
        df[c] = None
df = df[cols]
df.to_csv(os.path.join(out_dir, "w6_e34.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows", df["DOI / URL"].nunique(), "papers")

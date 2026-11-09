import csv
D=r"C:/Users/A/AppData/Local/Temp/claude/b2f7628fb08bc050/a3efc949-de1b-43db-a003-74458f673bb7/scratchpad/additions"
with open(D+"/TEMPLATE.csv",encoding="utf-8-sig") as f: H=next(csv.reader(f))
assert len(H)==99
rows=[]
def add(base,**kw):
    r=dict(base); r.update(kw)
    for k in r: assert k in H, k
    rows.append(r)
R=lambda x,n=4: round(x,n)

# 1 Jin et al 2019
b={"Article Name":"Mechanical Properties of High-Volume Fly Ash Strain Hardening Cementitious Composite (HVFA-SHCC) for Structural Application",
 "Author":"Jin C., Wu C., Feng C., Zhang Q., Shangguan Z., Pan Z., Meng S.","Year":2019,"DOI / URL":"https://doi.org/10.3390/ma12162607",
 "W / B":0.25,"SS / B (Silica sand)":0.36,"Sand max size (µm)":300,"PVA fiber (vol%)":2,"PVA length (mm)":12,"PVA diameter (µm)":39,
 "PVA tensile strength (MPa)":1620,"PVA elastic modulus (GPa)":42.8,"Total fiber (vol%)":2,"Curing method":"standard curing room 23±2°C, RH 95±5%",
 "Curing time (days)":28,"Curing temperature (°C)":23,"Curing RH (%)":95,"Demolding age (days)":1,"Test age (days)":28,
 "Compressive specimen":"prism","Compressive specimen size (mm)":"100x100x300","Tensile specimen":"dog-bone (30x30 mm mid-section)",
 "Tensile gauge length (mm)":80,"Tensile test type":"direct"}
for r,sp,efc,sfc,etu,stp in [(2.4,0.0082,0.019,3.67,1.92,3.97),(3.2,0.0071,0.020,3.34,3.42,4.10),(4.4,0.0042,0.022,3.26,3.07,3.99)]:
    add(b,**{"OPC / Cement":R(1/(1+r)),"FA (Fly ash)":R(r/(1+r)),"SP / B":R(sp/(1+r),5),"Tensile strength (MPa)":stp,
     "First-cracking strength (MPa)":sfc,"Tensile strain capacity (%)":etu,"Source table/page":"Table 2 (mix), Table 4 (fibre), Table 5 (tension)",
     "Conversions / notes":f"Mix FA{r}: Table 2 gives cement=1, FA/C={r}; binder fractions = 1/(1+r), r/(1+r). S/B and W/B given directly. SP (Table 2 'SP (kg)'={sp}) assumed per unit cement, divided by (1+r). Fibre modulus listed as 42.8 in Table 4 (units printed MPa, taken as GPa); model table uses 22 GPa. Silica sand avg 110 µm, max 300 µm. P.II 42.5 cement, Grade I FA. Compressive strength per mix only in Fig. 8 (text: all >30 MPa) - left blank. First-crack strain {efc}%."})

# 2 Atmajayanti et al 2021
b={"Article Name":"Influences of Sodium Lignosulfonate and High-Volume Fly Ash on Setting Time and Hardened State Properties of Engineered Cementitious Composites",
 "Author":"Atmajayanti A.T., Hung C.-C., Yuen T.Y.P., Shih R.-C.","Year":2021,"DOI / URL":"https://doi.org/10.3390/ma14174779",
 "W / B":0.35,"Sand max size (µm)":210,"PVA length (mm)":12,"PVA diameter (µm)":39,"PVA tensile strength (MPa)":1600,"PVA elastic modulus (GPa)":41,
 "Curing method":"water 20±2°C until 1 day before test, then air 20±2°C","Curing temperature (°C)":20,"Demolding age (days)":1,
 "Compressive specimen":"cylinder","Compressive specimen size (mm)":"100x200","Tensile specimen":"dog-bone (JSCE HPFRCC)","Tensile gauge length (mm)":80,"Tensile test type":"direct"}
def atm(r,vf,nls,age,fc=None,ft=None,eps=None,note=""):
    B=1+r
    d={"OPC / Cement":R(1/B),"FA (Fly ash)":R(r/B),"SS / B (Silica sand)":R(0.8/B),"PVA fiber (vol%)":vf,"Total fiber (vol%)":vf,"Test age (days)":age,"Curing time (days)":age-1,
       "Compressive strength (MPa)":fc,"Tensile strength (MPa)":ft,"Tensile strain capacity (%)":eps,
       "Source table/page":"Table 1 (mix), Sec. 3.4-3.5 text (fc, ft, strain; values rounded in text, curves in Figs. 11-15)",
       "Conversions / notes":f"Mix FA{r}-{vf}%-{nls*100:g}%NLS. Table 1 by weight: OPC 1, FA {r}, silica sand 0.8 (0.105-0.210 mm); fractions divided by binder (1+{r}). Cement 382 kg/m3 for all mixes per footnote. NLS (sodium lignosulfonate) = {nls} of cement mass = {nls/B:.5f} of binder (no column). PCE SP used, dosage not reported. Curing time ~ age-1 d in water. "+note}
    if r==1.2: d["Binder content (kg/m³)"]=R(382*B,1)
    if not vf: d["Total fiber (vol%)"]=0
    add(b,**{k:v for k,v in d.items() if v is not None})
atm(1.2,2,0,28,fc=62,ft=3.0,eps=1.5,note="fc 62 MPa from FA-series text; fibre-series text gives 66 MPa for Vf 2% (conclusions say 62) - conflict in paper.")
atm(2.2,2,0,28,fc=27,ft=2.0,eps=7.0,note="Binder content not filled: footnote cement 382 kg/m3 for all mixes would give 1222 kg/m3 binder, suspicious.")
atm(1.2,0,0,28,fc=35,ft=1.4,note="Plain matrix (no fibre).")
atm(1.2,2,0.005,28,eps=5.0,note="Only strain capacity given in text; ft 'not significantly affected' by NLS.")
atm(1.2,2,0.02,28,eps=1.8,note="Only strain capacity given in text.")
atm(1.2,2,0,7,fc=20,note="7-day fc of NLS 0% mix from NLS-series text.")
atm(1.2,2,0.02,7,fc=24,note="7-day fc from NLS-series text.")

# 3 Liu et al 2026 tuff powder
b={"Article Name":"Effects of Waste Powders of Tuff Manufactured Sand on Characteristics of Highly Ductile Polyvinyl Alcohol Fiber Engineered Cementitious Composite",
 "Author":"Liu T., Wang Y., Yu B., Ji S., Wang K., Wang F.","Year":2026,"DOI / URL":"https://doi.org/10.3390/ma19020296",
 "OPC / Cement":R(455.5/910.9),"FA (Fly ash)":R(364.4/910.9),"SF (Silica fume)":R(91/910.9),"W / B":0.4,"Binder content (kg/m³)":910.9,
 "PVA fiber (vol%)":2.5,"PVA length (mm)":12,"PVA diameter (µm)":40,"PVA tensile strength (MPa)":1560,"PVA elastic modulus (GPa)":41,"Total fiber (vol%)":2.5,
 "Curing method":"standard curing room (conditions not stated)","Curing time (days)":28,"Demolding age (days)":1,"Test age (days)":28,
 "Compressive specimen":"prism","Compressive specimen size (mm)":"40x40x80","Tensile specimen":"dog-bone 80x30x13 mm (JC/T 2461-2018)","Tensile test type":"direct"}
for p,sp,fc,eps,ft in [(0,6.59,48.4,4.0,4.2),(20,6.80,52.6,4.3,4.3),(40,6.97,53.6,4.6,4.4),(60,7.11,50.2,4.4,3.7),(80,7.22,49.5,4.3,3.3),(100,7.32,48.9,2.8,3.2)]:
    add(b,**{"SS / B (Silica sand)":R(0.65*(100-p)/100),"Stone sludge powder / B":R(0.65*p/100),"SP / B":R(sp/1000,5),"Compressive strength (MPa)":fc,
     "Tensile strength (MPa)":ft,"Tensile strain capacity (%)":eps,"Source table/page":"Table 8 (mix), Sec. 3.1-3.2 text (fc, ft, strain)",
     "Conversions / notes":f"TP{p}: tuff stone powder (waste powder of tuff manufactured sand) replaces {p}% of quartz sand (60 mesh) by mass; total sand/B = 0.65 (text) -> recorded under Stone sludge powder/B. Binder kg/m3 from Table 8 (455.5+364.4+91=910.9). SP {sp} wt‰ of binder. Tensile = peak tensile stress; gauge length not stated. Compressive specimen size 40x40x80 as printed in paper."})

# 4 Han et al 2024 coral sand (splitting)
B=1.43
b={"Article Name":"Effect of PVA Fiber on the Mechanical Properties of Seawater Coral Sand Engineered Cementitious Composites",
 "Author":"Han H., Gao G., Li Y., Hou D., Han Y.","Year":2024,"DOI / URL":"https://doi.org/10.3390/ma17061446",
 "OPC / Cement":R(1/B),"FA (Fly ash)":R(0.43/B),"W / B":R(0.5/B),"Sea sand / B":R(0.5/B),"Sand max size (µm)":2500,"SP / B":R(0.00123/B,6),
 "PVA length (mm)":12,"PVA diameter (µm)":39,"PVA tensile strength (MPa)":1620,"PVA elastic modulus (GPa)":42.8,
 "Curing method":"standard curing box 20°C, RH 95%","Curing time (days)":28,"Curing temperature (°C)":20,"Curing RH (%)":95,"Demolding age (days)":1,"Test age (days)":28,
 "Compressive specimen":"cube","Compressive specimen size (mm)":"70.7","Tensile specimen":"cylinder disc 50 dia x 25 mm","Tensile test type":"splitting"}
for vf,fc,fcr,ft in [(0,None,1.15,1.15),(0.575,None,1.33,1.48),(1.15,44.21,1.38,2.07),(1.725,None,1.48,2.65),(2.3,45.88,1.50,3.03)]:
    d={"PVA fiber (vol%)":vf,"Total fiber (vol%)":vf,"Compressive strength (MPa)":fc,"Tensile strength (MPa)":ft,"First-cracking strength (MPa)":fcr,
       "Source table/page":"Table 1 (mix), Table 6 (splitting), Sec. 3 text (fc)",
       "Conversions / notes":f"P-{vf}: Table 1 mass ratios C 1 : FA 0.43 : coral sand 0.5 : seawater 0.5 : SP 0.00123, divided by binder 1.43. Coral sand (FM 2.1, max 2.5 mm) recorded as Sea sand; mixing water = simulated seawater. SPLITTING tensile test (not direct); first-crack = splitting first-crack strength. fc for other mixes only in Fig. 7."}
    add(b,**{k:v for k,v in d.items() if v is not None})

# 5 Qiu et al 2026 hybrid local fibres (HBSAC)
b={"Article Name":"Hybrid Local Fibers for Enhancing the Mechanical Properties of Engineered Cementitious Composites",
 "Author":"Qiu X., Tang L., Shi Y., Li H., Wang T.","Year":2026,"DOI / URL":"https://doi.org/10.3390/ma19132908",
 "SS / B (Silica sand)":0.58,"Sand max size (µm)":150,"W / B":0.30,"SP / B":0.002,
 "Curing method":"20±2°C, RH >95%","Curing time (days)":27,"Curing temperature (°C)":20,"Curing RH (%)":95,"Demolding age (days)":1,"Test age (days)":28,
 "Compressive specimen":"cube","Compressive specimen size (mm)":"70.7","Tensile specimen":"dog-bone (JC/T 2461-2018)","Tensile test type":"direct"}
fcq={("30",0,0):31.6,("50",0,0):20.6,("50",1.0,1.0):23.8}
tab={("30",0,0):(4.0,0.017),("30",2.0,0):(5.2,1.1),("30",1.5,0.5):(5.4,2.9),("30",1.0,1.0):(6.2,3.2),("30",0,2.0):(5.8,1.8),
     ("50",0,0):(3.4,0.014),("50",2.0,0):(3.9,2.3),("50",1.5,0.5):(4.2,5.0),("50",1.0,1.0):(4.5,5.3),("50",0,2.0):(3.9,2.3)}
for fa in ["30","50"]:
    for a,e in [(0,0),(2.0,0),(1.5,0.5),(1.0,1.0),(0,2.0)]:
        ft,eps=tab[(fa,a,e)]
        d={"SAC (Calcium sulfoaluminate cement)":0.68 if fa=="30" else 0.48,"FA (Fly ash)":0.30 if fa=="30" else 0.50,"SF (Silica fume)":0.02,
           "PVA fiber (vol%)":a,"PE fiber (vol%)":e,"Total fiber (vol%)":a+e,"Tensile strength (MPa)":ft,"Tensile strain capacity (%)":eps,
           "Compressive strength (MPa)":fcq.get((fa,a,e)),"Source table/page":"Table 3 (mix), Table 5 (tension), Sec. 3.3 text (fc)",
           "Conversions / notes":f"FA{fa}-A{a:g}-E{e:g}. Binder = high-belite sulphoaluminate cement (HBSAC, recorded as SAC) + FA + SF (%). Common components in Table 3 given as (%) - taken as % of binder mass: SS 58, W 30, SP 0.20; also redispersible powder 0.77, thixotropic agent 0.20, boric acid 0.21, air-entrainer 0.02 (no columns). Silica sand 100-200 mesh (max ~150 µm). Test age implied (1 d mould + 27 d curing). Fibres from local (Chinese) manufacturers. fc for other mixes only in Fig. 11."+(" Plain matrix: tensile value is matrix cracking/peak strength." if a+e==0 else "")}
        if a: d.update({"PVA length (mm)":12,"PVA diameter (µm)":39,"PVA tensile strength (MPa)":1300,"PVA elastic modulus (GPa)":35})
        if e: d.update({"PE length (mm)":12,"PE diameter (µm)":24,"PE tensile strength (MPa)":3000,"PE elastic modulus (GPa)":110})
        add(b,**{k:v for k,v in d.items() if v is not None})

# 6 Zhao et al 2025 ANN constitutive
B=555.3+666.4
b={"Article Name":"An Experimental Study on the Mechanical Properties and ANN-Based Prediction of a Tensile Constitutive Model of ECCs",
 "Author":"Zhao Q., Yang Z., Zhang X., Xia Z., Xiong K., Yan J.","Year":2025,"DOI / URL":"https://doi.org/10.3390/polym17233183",
 "OPC / Cement":R(555.3/B),"FA (Fly ash)":R(666.4/B),"W / B":R(329.9/B),"River sand / B":R(439.8/B),"SP / B":R(8.6/B,5),"Binder content (kg/m³)":R(B,1),
 "Curing method":"20±5°C, RH 95%","Curing time (days)":28,"Curing temperature (°C)":20,"Curing RH (%)":95,"Demolding age (days)":1,"Test age (days)":28,
 "Compressive specimen":"cube","Compressive specimen size (mm)":"70.7","Tensile specimen":"dog-bone 330x60x13 mm","Tensile gauge length (mm)":80,"Tensile test type":"direct"}
fib={"PE":{"PE length (mm)":12,"PE diameter (µm)":21.6,"PE tensile strength (MPa)":3120,"PE elastic modulus (GPa)":126},
     "K-PVA":{"PVA length (mm)":12,"PVA diameter (µm)":31,"PVA tensile strength (MPa)":1600,"PVA elastic modulus (GPa)":41},
     "N-PVA":{"PVA length (mm)":12,"PVA diameter (µm)":31,"PVA tensile strength (MPa)":1450,"PVA elastic modulus (GPa)":37.5}}
data=[("PE",1.3,49.70,4.15,5.06,3.36),("PE",1.5,None,4.3,5.26,3.39),("PE",1.7,54.30,4.45,5.64,3.55),
      ("K-PVA",1.3,49.90,3.11,4.19,3.03),("K-PVA",1.5,52.05,3.72,4.73,3.19),("K-PVA",1.7,47.23,4.15,5.01,3.33),
      ("N-PVA",1.3,46.70,2.11,2.61,2.56),("N-PVA",1.5,51.65,3.13,3.57,3.11),("N-PVA",1.7,45.57,2.21,2.96,2.96)]
for t,v,fc,scr,spk,eps in data:
    lab={"K-PVA":"K-PVA = Kuraray RECS-15","N-PVA":"N-PVA = domestic Chinese PVA (Tai'an)","PE":"PE fibre"}[t]
    d=dict(fib[t]); d.update({("PE fiber (vol%)" if t=="PE" else "PVA fiber (vol%)"):v,"Total fiber (vol%)":v,"Compressive strength (MPa)":fc,
      "First-cracking strength (MPa)":scr,"Tensile strength (MPa)":spk,"Tensile strain capacity (%)":eps,
      "Source table/page":"Table 2 (fibre), Table 3 (mix, kg/m3), Table 4 (tension), Sec. 3.1 text (fc)",
      "Conversions / notes":f"{t}{v}: kg/m3 divided by binder {B:.1f} (cement 555.3 + FA 666.4). River sand avg 150 µm. {lab}."+(" fc for PE1.5 not stated in text (figure only)." if fc is None else "")})
    add(b,**{k:v for k,v in d.items() if v is not None})

# 7 Cheng et al 2021 recycled brick fine aggregate
B=1185
b={"Article Name":"Effect of Fiber Content on the Mechanical Properties of Engineered Cementitious Composites with Recycled Fine Aggregate from Clay Brick",
 "Author":"Cheng Z., Yan W., Sui Z., Tang J., Yuan C., Chu L., Feng H.","Year":2021,"DOI / URL":"https://doi.org/10.3390/ma14123272",
 "OPC / Cement":R(770/B),"FA (Fly ash)":R(415/B),"W / B":R(415/B),"SP / B":R(0.6/B,5),"VMA / B":R(1.8/B,5),"Binder content (kg/m³)":B,"Sand max size (µm)":300,
 "PVA length (mm)":12,"PVA diameter (µm)":40,"PVA tensile strength (MPa)":1560,"PVA elastic modulus (GPa)":41,
 "Curing method":"20±2°C, RH 95%","Curing time (days)":28,"Curing temperature (°C)":20,"Curing RH (%)":95,"Demolding age (days)":1,"Test age (days)":28,
 "Compressive specimen":"cube","Tensile specimen":"rectangular plate 280x40x15 mm","Tensile gauge length (mm)":120,"Tensile test type":"direct"}
for name,qs,rfa,fc,ect,sct,eut,sut in [("ECC-QS",415,0,37.4,0.067,2.271,2.131,3.548),("ECC-RFA25",311.25,103.75,36.3,0.099,2.188,2.352,2.936),
    ("ECC-RFA50",207.5,207.5,36.7,0.066,1.887,1.381,1.935),("ECC-RFA75",103.75,311.25,34.3,0.158,1.833,2.374,2.252),("ECC-RFA100",0,415,33.7,0.235,1.792,3.301,2.168)]:
    add(b,**{"SS / B (Silica sand)":R(qs/B),"PVA fiber (vol%)":1.75,"Total fiber (vol%)":1.75,"Compressive strength (MPa)":fc,"Compressive specimen size (mm)":"not stated (cube)",
     "First-cracking strength (MPa)":sct,"Tensile strength (MPa)":sut,"Tensile strain capacity (%)":eut,"Source table/page":"Table 3 (fibre), Table 5 (mix), Table 7 (fc), Table 9 (tension)",
     "Conversions / notes":f"{name}: kg/m3 / binder 1185 (cement 770 + FA 415). Recycled clay-brick fine aggregate RFA/B = {rfa/B:.4f} (no column; <300 µm) replacing quartz sand. PVA 22.75 kg/m3 / 1300 kg/m3 = 1.75 vol%. Thickener recorded as VMA. Cube size for Table 7 not stated (sizes 40-100 mm used in paper). Ultimate strain taken as strain capacity; cracking strain {ect}%."})
for vf,kg,fc,ect,sct,eut,sut in [(1.25,16.25,31.5,0.189,1.112,1.31,1.752),(1.5,19.5,35.8,0.207,1.792,2.04,2.036),(1.75,22.75,38.2,0.235,1.892,3.00,3.368),(2.0,26,32.9,0.264,2.336,4.19,3.456)]:
    add(b,**{"SS / B (Silica sand)":0,"PVA fiber (vol%)":vf,"Total fiber (vol%)":vf,"Compressive strength (MPa)":fc,"Compressive specimen size (mm)":"100",
     "First-cracking strength (MPa)":sct,"Tensile strength (MPa)":sut,"Tensile strain capacity (%)":eut,"Source table/page":"Table 6 (mix), Table 11 (fc, 100 mm cube), Table 15 (tension)",
     "Conversions / notes":f"ECO-ECC-{vf}%: 100% RFA, RFA/B = {415/B:.4f} (no column; recycled clay-brick fine aggregate <300 µm). PVA {kg} kg/m3. fc from 100 mm cubes; Table 11 also gives 40/50/70.7 mm cube values. Cracking strain {ect}%."})

# 8 Zhao et al 2022 damage constitutive model
B=1+2+0.073
b={"Article Name":"An Experimental and Analytical Study on a Damage Constitutive Model of Engineered Cementitious Composites under Uniaxial Tension",
 "Author":"Zhao D., Wang C., Li K., Zhang P., Cong L., Chen D.","Year":2022,"DOI / URL":"https://doi.org/10.3390/ma15176063",
 "OPC / Cement":R(1/B),"FA (Fly ash)":R(2/B),"SF (Silica fume)":R(0.073/B),"SS / B (Silica sand)":R(1.5/B),"SP / B":R(0.041/B,5),
 "PVA length (mm)":12,"PVA diameter (µm)":40,"PVA tensile strength (MPa)":1560,"PVA elastic modulus (GPa)":41,
 "Curing method":"saturated lime water, then dried","Curing time (days)":28,"Test age (days)":28,
 "Tensile specimen":"thin plate 280x40x13 mm","Tensile gauge length (mm)":120,"Tensile test type":"direct"}
for g,vf,w,sk,spk,ep,eu,ek in [("V1R3",1,0.860,1.976,3.104,0.511,1.895,0.025),("V2R3",1.5,0.860,2.020,2.959,0.796,2.539,0.048),("V3R1",2,0.738,3.440,4.572,0.503,2.230,0.041),
                     ("V3R2",2,0.768,2.665,3.787,1.071,2.975,0.067),("V3R3",2,0.860,2.447,3.234,2.000,4.077,0.069)]:
    add(b,**{"W / B":R(w/B,3),"PVA fiber (vol%)":vf,"Total fiber (vol%)":vf,"First-cracking strength (MPa)":sk,"Tensile strength (MPa)":spk,"Tensile strain capacity (%)":ep,
     "Source table/page":"Table 1 (mix), Table 2 (fibre), Table 3 (averages)",
     "Conversions / notes":f"{g}: Table 1 mass ratios cement 1 : sand 1.5 : FA 2 : micro-silica 0.073 : water {w} (no units printed; W/B matches stated 0.24/0.25/0.28) divided by binder 3.073. Strain capacity = strain at peak stress εp; ultimate (post-peak) strain εu = {eu}%. First-crack strain {ek}%. Test age assumed 28 d (cured 28 d in lime water then dried). No fc reported. Cement 'ordinary silicate cement'."})

# 9 Yang et al 2024 CNC
b={"Article Name":"A preliminary investigation of incorporating cellulose nanocrystals into engineered cementitious composites",
 "Author":"Yang X., Ren J.-G., Li L.-X., Wang Z., Zhang Q.-H., Liu Q.-L.","Year":2024,"DOI / URL":"https://doi.org/10.3389/fmats.2024.1443517",
 "SS / B (Silica sand)":0.35,"Sand max size (µm)":212,"W / B":0.3,"PVA fiber (vol%)":2,"Total fiber (vol%)":2,"PVA length (mm)":12,"PVA diameter (µm)":40,
 "Curing method":"air curing room 20±2°C, RH >60%","Curing time (days)":28,"Curing temperature (°C)":20,"Curing RH (%)":60,"Demolding age (days)":1,"Test age (days)":28,
 "Compressive specimen":"cube","Compressive specimen size (mm)":"70.7","Tensile specimen":"dog-bone","Tensile gauge length (mm)":100,"Tensile test type":"direct"}
for m,c,cnc,hr,fc,eps,fcr,ft in [("ECC2-C1",0.3,0.1,0.09,47,3.2,3.5,5.0),("ECC2",0.3,0,0.06,None,4.1,3.2,4.6),("ECC1",0.4,0,0.07,49.6,1.6,3.6,5.1),
                          ("ECC1-C1",0.4,0.1,0.14,59.3,0.9,4.6,6.0),("ECC1-C2",0.4,0.2,0.19,62.8,0.8,4.9,5.7),("ECC1-C4",0.4,0.4,0.31,66.0,0.5,5.1,5.5)]:
    d={"OPC / Cement":c,"FA (Fly ash)":R(1-c,2),"HRWR / B":R(hr/100,5),"Compressive strength (MPa)":fc,"Tensile strain capacity (%)":eps,"First-cracking strength (MPa)":fcr,"Tensile strength (MPa)":ft,
       "Source table/page":"Table 2 (mix), Table 4 (tension), Sec. 3 text (fc)",
       "Conversions / notes":f"{m}: Table 2 cement {c}, FA {1-c:.1f}, sand 0.35, water 0.3 (no units; binder sums to 1). Quartz sand 120-212 µm. CNC {cnc} wt% (cellulose nanocrystals, no column). HRWR {hr}% assumed of binder mass. PVA KURALON K-II; strength/modulus not reported."+(" fc of ECC2 only in Fig. 8." if fc is None else "")}
    add(b,**{k:v for k,v in d.items() if v is not None})

with open(D+"/pvaecc.csv","w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=H); w.writeheader()
    for r in rows: w.writerow(r)
print(len(rows), len(set(r["DOI / URL"] for r in rows)))
bcols=H[H.index("OPC / Cement"):H.index("CKD (Cement kiln dust)")+1]
for r in rows:
    s=sum(float(r.get(c) or 0) for c in bcols)
    if abs(s-1)>0.002: print("SUM",r["Article Name"][:30],s)

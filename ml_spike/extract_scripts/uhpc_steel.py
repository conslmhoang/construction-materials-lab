import csv
D=r"C:/Users/A/AppData/Local/Temp/claude/b2f7628fb08bc050/a3efc949-de1b-43db-a003-74458f673bb7/scratchpad/additions"
with open(D+"/TEMPLATE.csv",encoding="utf-8-sig") as f: H=next(csv.reader(f))
rows=[]
def r4(x): return round(x,4) if isinstance(x,float) else x
def add(base,**kw):
    d=dict(base); d.update(kw)
    for k in d: assert k in H, k
    bf=["OPC / Cement","GGBS","FA (Fly ash)","SF (Silica fume)","Limestone powder"]
    s=sum(d.get(k,0) or 0 for k in bf)
    assert abs(s-1)<0.002,(d["Article Name"],s)
    rows.append({k:r4(v) for k,v in d.items()})

# ---------- P1 Mina 2021
B=1100.
p1={"Article Name":"Optimizing the Mechanical Properties of Ultra-High-Performance Fibre-Reinforced Concrete to Increase Its Resistance to Projectile Impact",
 "Author":"Mina A.L.; Trezos K.G.; Petrou M.F.","Year":2021,"DOI / URL":"https://doi.org/10.3390/ma14175098",
 "OPC / Cement":880/B,"SF (Silica fume)":220/B,"Local sand / B":(475+358)/B,"Sand max size (µm)":500,"Binder content (kg/m³)":1100,
 "Steel diameter (µm)":160,"Steel tensile strength (MPa)":3000,
 "Curing method":"Demoulded 24 h, water tank; water heated from 20 C to 90 C on day 3, held 90 C for 11 days, back to 20 C by day 14, then 20 C water until testing",
 "Curing temperature (°C)":90,"Demolding age (days)":1,"Heat curing duration (h)":264,
 "Compressive specimen":"cube","Compressive specimen size (mm)":"100x100x100","Tensile specimen":"prism 100x50x500 (direct tension)","Tensile test type":"direct",
 "Source table/page":"Tables 1-2 (mix, kg/m3), Table 5 (fc cube, direct tension)"}
mix1=[("0/16/4.5",0,0,176,50,131.6,4.2,""),("0/16/6.1",0,0,176,67,124.0,4.4,""),("0/20/6.1",0,0,220,67,104.4,3.7,""),
 ("2(0-2)/16/6.1",0,160,176,67,155.8,9.2,""),("2(0-2)/20/6.1",0,160,220,67,127.7,6.3,""),
 ("6(5-1)/16/4.5",400,80,176,50,163.8,6.1,""),("6(5-1)/16/6.1",400,80,176,67,176.7,9.5,""),("6(3-3)/16/6.1",240,240,176,67,187.6,6.5,"; dogbone direct tension of this mix = 10.6 MPa (Table 5)")]
for n,f6,f13,w,sp,fc,ft,ex in mix1:
    vf=(f6+f13)/7850*100
    L = 13 if (f13>0 and f6==0) else ""
    note=f"Mix {n}. kg/m3 / binder (cement 880 + SF 220 = 1100). Steel fibre vol% = kg/7850 (density given) ({f6} kg 6 mm + {f13} kg 13 mm). SP {sp} kg/m3. Test age not reported. ft = direct tension on 100x50x500 prisms"+ex
    if f6>0 and f13>0: note+="; hybrid 6 mm + 13 mm straight steel fibres, length left blank"
    kw={"W / B":w/B,"SP / B":sp/B,"Steel fiber (vol%)":vf,"Steel length (mm)":L,"Total fiber (vol%)":vf,
      "Compressive strength (MPa)":fc,"Tensile strength (MPa)":ft,"Conversions / notes":note}
    if vf==0: kw.update({"Steel diameter (µm)":"","Steel tensile strength (MPa)":""})
    add(p1,**kw)

# ---------- P2 Fang 2022
B=829+216+35.
p2={"Article Name":"Effects of Steel Fiber and Specimen Geometric Dimensions on the Mechanical Properties of Ultra-High-Performance Concrete",
 "Author":"Fang H.; Gu M.; Zhang S.; Jiang H.; Fang Z.; Hu J.","Year":2022,"DOI / URL":"https://doi.org/10.3390/ma15093027",
 "OPC / Cement":829/B,"SF (Silica fume)":216/B,"Limestone powder":35/B,"W / B":194/B,"SS / B (Silica sand)":1079/B,"SP / B":29/B,"Binder content (kg/m³)":B,
 "Steel elastic modulus (GPa)":200,"Curing method":"Demoulded ~24 h, moist cured 7 days, then natural outdoor curing until test",
 "Curing time (days)":7,"Demolding age (days)":1,"Compressive specimen":"cylinder","Compressive specimen size (mm)":"100x200",
 "Tensile specimen":"dog-bone","Tensile gauge length (mm)":80,"Tensile test type":"direct",
 "Source table/page":"Table 1 (fibres), Table 2 (mix), Table 4 (fc), Table 6 (dog-bone ft, peak strain)"}
ftyp={"I":(0.22,13,2600,"hooked-end"),"II":(0.22,16,2500,"hooked-end"),"III":(0.25,16,2600,"hooked-end"),"IV":(0.20,13,2800,"straight")}
mix2=[("I",0,"I",28,129.01,3.64,58),("II",1,"I",28,131.46,7.13,1834),("III",2,"I",28,135.07,10.73,2576),("IV",3,"I",28,138.45,11.66,3357),
 ("V",2,"II",28,135.09,10.47,2503),("VI",2,"III",28,134.86,10.77,2564),("VII",2,"IV",28,135.74,7.82,698),
 ("III",2,"I",3,90.46,8.13,701),("III",2,"I",7,111.77,9.19,1130)]
for n,vf,t,age,fc,ftv,eps in mix2:
    d,L,s,typ=ftyp[t]
    note=f"Mix {n}, fibre Type {t} ({typ}). kg/m3 / binder; binder taken as cement 829 + SF 216 + nano-CaCO3 35 = 1080 kg/m3 (nano-CaCO3 put under Limestone powder; paper does not define binder). Water reducer 29 kg/m3 put in SP/B. Strain capacity = peak strain {eps} microstrain (Table 6) converted to %."
    kw={"Steel fiber (vol%)":vf,"Total fiber (vol%)":vf,"Test age (days)":age,"Compressive strength (MPa)":fc,"Tensile strength (MPa)":ftv,"Tensile strain capacity (%)":eps/1e4,"Conversions / notes":note}
    if vf>0: kw.update({"Steel length (mm)":L,"Steel diameter (µm)":d*1000,"Steel tensile strength (MPa)":s})
    else: kw.update({"Steel elastic modulus (GPa)":""})
    add(p2,**kw)

# ---------- P3 Yuan 2022
B=1300.
p3={"Article Name":"Influence and Mechanism of Curing Methods on Mechanical Properties of Manufactured Sand UHPC",
 "Author":"Yuan C.; Xu S.; Raza A.; Wang C.; Wang D.","Year":2022,"DOI / URL":"https://doi.org/10.3390/ma15186183",
 "OPC / Cement":1000/B,"FA (Fly ash)":100/B,"SF (Silica fume)":200/B,"W / B":221/B,"SP / B":40.2/B,"Binder content (kg/m³)":B,
 "Steel fiber (vol%)":235.5/7800*100,"Steel length (mm)":13,"Steel diameter (µm)":200,"Steel tensile strength (MPa)":2850,"Total fiber (vol%)":235.5/7800*100,
 "Demolding age (days)":2,"Compressive specimen":"cube","Compressive specimen size (mm)":"100x100x100","Tensile specimen":"dog-bone","Tensile test type":"direct"}
cur={"SM":"steam curing (temperature/duration not reported)","SD":"standard curing (details not reported)","SP":"sprinkler curing (details not reported)","CH":"saturated Ca(OH)2 solution curing (details not reported)"}
base_note="kg/m3 / binder (cement P.O52.5 1000 + FA 100 + SF 200 = 1300). Steel fibre 235.5 kg/m3 / 7800 kg/m3 (density 7.8 g/cm3 given, Table 2) = 3.02 vol%. Fibre strength >=2850 MPa. Demoulded after 48 h."
for c,fc in [("SM",149.7),("SD",80.9),("SP",107.0),("CH",105.0)]:
    add(p3,**{"M-sand / B":1200/B,"Curing method":cur[c],"Test age (days)":3,"Compressive strength (MPa)":fc,"Tensile test type":"","Tensile specimen":"",
      "Source table/page":"Table 5 (mix), text Sec. 3.1 (3-d fc)","Conversions / notes":f"MS-{c}, manufactured sand. "+base_note+" 28/56-d fc only given as % of SM in text (not recorded)."})
for sand,c,fte,ftu in [("RS","SM",7.44,8.54),("MS","SM",7.75,8.72),("MS","SD",6.15,6.72),("MS","SP",6.10,6.60),("MS","CH",6.23,7.03)]:
    kw={"Curing method":cur[c],"Test age (days)":28,"First-cracking strength (MPa)":fte,"Tensile strength (MPa)":ftu,"Compressive specimen":"","Compressive specimen size (mm)":"",
      "Source table/page":"Table 5 (mix), Table 6 (uniaxial tension)","Conversions / notes":f"{sand}-{c}. "+base_note+" F_te = initial crack strength, F_cu = tensile strength (Table 6). Dog-bone dimensions not given. No absolute 28-d fc given."}
    kw["M-sand / B" if sand=="MS" else "River sand / B"]=1200/B
    add(p3,**kw)

# ---------- P4 Zuo 2022
p4={"Article Name":"Effect of Curing Regime on the Mechanical Strength, Hydration, and Microstructure of Ecological Ultrahigh-Performance Concrete (EUHPC)",
 "Author":"Zuo Z.; Zhang J.; Li B.; Shen C.; Xin G.; Chen X.","Year":2022,"DOI / URL":"https://doi.org/10.3390/ma15051668",
 "W / B":0.16,"SS / B (Silica sand)":1.0,"Sand max size (µm)":1200,
 "Steel fiber (vol%)":2,"Steel length (mm)":13,"Steel diameter (µm)":200,"Steel tensile strength (MPa)":2200,"Total fiber (vol%)":2,"Demolding age (days)":1,
 "Compressive specimen":"prism halves (40x40 loaded area)","Compressive specimen size (mm)":"40x40x40","Tensile specimen":"prism 40x40x160, four-point bending","Tensile test type":"flexural",
 "Source table/page":"Table 2 (mix, mass ratios), Table 3 (standard curing), Table 4 (steam curing)"}
mix4=[("S20F0G0",.8,.2,0,0,(127.1,42.0,149.1,45.5),(157.3,47.3,155.1,40.1)),
("S20F10G0",.7,.2,.1,0,(122.9,40.7,143.4,44.3),(155.1,47.8,156.3,42.5)),
("S20F10G10",.6,.2,.1,.1,(118.6,38.0,138.2,39.2),(162.9,48.8,152.6,44.5)),
("S20F0G20",.6,.2,0,.2,(124.1,40.1,148.6,45.3),(172.5,50.9,161.5,44.9)),
("S15F15G15",.55,.15,.15,.15,(117.8,36.1,140.8,39.5),(161.3,44.2,151.8,42.1)),
("S17.5F10G17.5",.55,.175,.1,.175,(120.5,37.8,144.3,40.4),(168.1,46.3,158.6,46.5)),
("S20F10G20",.5,.2,.1,.2,(116.1,32.7,137.3,35.3),(163.8,45.6,155.2,43.8))]
for n,c,sf,fa,gg,std,stm in mix4:
    for cname,vals,temp,hh,cm in [("standard",std,20,"", "Standard curing 20+/-2 C, 95% RH after demoulding at 24 h"),
                                  ("steam",stm,70,72,"24 h at ~20 C, steam 70 C for 72 h, then standard room 20 C")]:
        for age,fc,fb in [(7,vals[0],vals[1]),(28,vals[2],vals[3])]:
            add(p4,**{"OPC / Cement":c,"SF (Silica fume)":sf,"FA (Fly ash)":fa,"GGBS":gg,"Curing method":cm,"Curing temperature (°C)":temp,
              "Curing RH (%)":95 if cname=="standard" else "","Heat curing duration (h)":hh,"Test age (days)":age,
              "Compressive strength (MPa)":fc,"Tensile strength (MPa)":fb,
              "Conversions / notes":f"Mix {n}, {cname} curing. Mix given as mass fractions of cementitious = 1; quartz sand (0.5-1.2 mm) / binder = 1.0 put in SS/B; defoamer 0.1% of binder. SP dosage not reported. Fibre tensile strength given as >2200 MPa. Tensile strength column = FLEXURAL strength (four-point, 40x40x160)."})

# ---------- P5 Guo LK 2024
B=1+0.214+0.214
p5={"Article Name":"Enhancing UHPC Tensile Performance Using Polystyrene Beads: Significant Improvements and Mechanisms",
 "Author":"Guo L.-K.; Chen L.-B.; Chen Z.-W.; Wang J.-Y.","Year":2024,"DOI / URL":"https://doi.org/10.3390/ma17112479",
 "OPC / Cement":1/B,"SF (Silica fume)":0.214/B,"GGBS":0.214/B,"W / B":0.251/B,"SS / B (Silica sand)":1.064/B,"SP / B":0.012/B,
 "Steel fiber (vol%)":2,"Steel length (mm)":16,"Steel diameter (µm)":200,"Steel tensile strength (MPa)":2500,
 "Curing method":"24 h in moulds under plastic, then water immersion at 25 C","Curing time (days)":28,"Curing temperature (°C)":25,"Demolding age (days)":1,"Test age (days)":28,
 "Compressive specimen":"cube","Compressive specimen size (mm)":"100x100x100","Tensile specimen":"dog-bone (MCS-EPFL), 50x30 section","Tensile gauge length (mm)":200,"Tensile test type":"direct",
 "Source table/page":"Table 1 (mix, mass ratio to cement), Table 2 (fibre), Table 3 (tension), text Sec. 3 (fc)"}
for n,ps,fte,ftu,eps,fc in [("F2.0",0,6.53,8.68,1390,""),("PS1",1,6.74,10.17,2017,""),("PS2",2,6.89,11.58,3820,133.87),("PS4",4,6.35,9.37,2418,"")]:
    note=f"Mix {n}. Hooked steel fibres. Ratios to cement converted to binder = cement + SF + 'mineral powder' (taken as GGBS) = 1.428. Quartz sand put in SS/B. Polystyrene beads {ps} vol% (no column; mass ratio not given). Strain capacity = ultimate tensile strain {eps} microstrain -> %."
    if n!="PS2": note+=" fc: text gives only relative values (PS1 +5%, PS2 +4.6%, PS4 +0.2% vs control) - left blank."
    add(p5,**{"Total fiber (vol%)":2,"Compressive strength (MPa)":fc,"First-cracking strength (MPa)":fte,"Tensile strength (MPa)":ftu,"Tensile strain capacity (%)":eps/1e4,"Conversions / notes":note})

# ---------- P6 Park 2021
p6={"Article Name":"Residual Tensile Properties and Explosive Spalling of High-Performance Fiber-Reinforced Cementitious Composites Exposed to Thermal Damage",
 "Author":"Park G.-K.; Park G.-J.; Park J.-J.; Lee N.; Kim S.-W.","Year":2021,"DOI / URL":"https://doi.org/10.3390/ma14071608",
 "Steel fiber (vol%)":2,"Steel length (mm)":19.5,"Steel diameter (µm)":200,"Steel tensile strength (MPa)":2500,"Steel elastic modulus (GPa)":200,
 "Curing method":"1 day room temperature, then 2 days in 90 C water, then room temperature until testing","Curing temperature (°C)":90,"Heat curing duration (h)":48,"Demolding age (days)":1,
 "Tensile specimen":"dog-bone","Tensile test type":"direct","Source table/page":"Table 1 (mix), Table 3 (fibres), Table 4 (fibre dosages), Table 5 (ft before fire)"}
mats={"100":(704.4,70.5,140.9,0,140.9,845.3,11.1,4.6,0.28),"140":(739.2,73.9,0,147.8,221.8,813.2,24.3,4.8,0.25),"180":(783.6,195.9,0,0,235.1,861.9,47.0,4.9,0.2)}
res={"100":[("",0,0,13.41),("PP0.2",.2,0,11.79),("PP0.4",.4,0,12.40),("PP0.6",.6,0,12.72),("PN0.2",.1,.1,12.73),("PN0.4",.2,.2,12.27),("PN0.6",.3,.3,12.79)],
     "140":[("",0,0,15.53),("PP0.2",.2,0,13.74),("PP0.4",.4,0,13.83),("PP0.6",.6,0,13.37),("PN0.2",.1,.1,13.18),("PN0.4",.2,.2,12.73),("PN0.6",.3,.3,13.14)],
     "180":[("",0,0,18.78),("PP0.2",.2,0,15.73),("PP0.4",.4,0,16.66),("PP0.6",.6,0,17.29),("PN0.2",.1,.1,16.33),("PN0.4",.2,.2,15.48),("PN0.6",.3,.3,16.72)]}
for m,(c,sf,fa,gg,qp,ss,sp,sra,wb) in mats.items():
    B=c+sf+fa+gg
    for suf,pp,ny,ftv in res[m]:
        n=m+("-"+suf if suf else "")
        note=f"Mix {n}, unheated (before fire) values only. kg/m3 / binder (cement+SF+FA/GGBS = {B:.1f}). Silica flour put in QP/B. W/B = paper value (consistent with total water incl. 70% of SP / binder). SRA {sra} kg/m3 not in a column. Design fc label {m} MPa is a target class, not a measured value - fc left blank. Test age not reported."
        if ny: note+=f" Nylon fibre {ny} vol% (9 mm, 16-28 um) has no column; included in Total fiber."
        kw={"OPC / Cement":c/B,"SF (Silica fume)":sf/B,"FA (Fly ash)":fa/B,"GGBS":gg/B,"W / B":wb,"QP / B (Quartz powder)":qp/B,"SS / B (Silica sand)":ss/B,"SP / B":sp/B,"Binder content (kg/m³)":B,
            "Total fiber (vol%)":2+pp+ny,"Tensile strength (MPa)":ftv,"Conversions / notes":note}
        if pp: kw.update({"PP fiber (vol%)":pp,"PP length (mm)":19,"PP diameter (µm)":30})
        add(p6,**kw)

# ---------- P7 Yu 2019
B=1080.
p7={"Article Name":"Rheological and Mechanical Properties of Ultra-High-Performance Concrete Containing Fine Recycled Concrete Aggregates",
 "Author":"Yu L.; Huang L.; Ding H.","Year":2019,"DOI / URL":"https://doi.org/10.3390/ma12223717",
 "OPC / Cement":648/B,"FA (Fly ash)":324/B,"SF (Silica fume)":108/B,"W / B":194.4/B,"Binder content (kg/m³)":B,
 "Steel fiber (vol%)":2.5,"Steel length (mm)":13,"Steel diameter (µm)":200,"Steel tensile strength (MPa)":3000,"Total fiber (vol%)":2.5,
 "Curing method":"48 h under plastic at room temperature, then standard room 20+/-2 C, >95% RH","Curing time (days)":28,"Curing temperature (°C)":20,"Curing RH (%)":95,"Demolding age (days)":2,"Test age (days)":28,
 "Compressive specimen":"cube","Compressive specimen size (mm)":"100x100x100","Tensile specimen":"dog-bone","Tensile test type":"direct",
 "Source table/page":"Table 2 (mix, kg/m3), Sec. 3.3 text / Figs. 5-6 (fc, direct ft values stated in text)"}
for n,nrs,rca,sp,fc,ftv,fl in [("N100R0",1188,0,21.6,177.13,8.42,17.70),("N80R20",950.4,237.6,21.6,179.78,8.70,18.66),("N60R40",712.8,475.2,21.7,184.26,9.13,19.26),
                               ("N40R60",475.2,712.8,21.9,180.32,8.94,19.97),("N20R80",237.6,950.4,22.0,177.30,8.28,17.31),("N0R100",0,1188,22.3,173.05,7.14,16.46)]:
    add(p7,**{"River sand / B":nrs/B,"SP / B":sp/B,"Compressive strength (MPa)":fc,"Tensile strength (MPa)":ftv,
      "Conversions / notes":f"Mix {n}. kg/m3 / binder (cement 648 + FA 324 + SF 108 = 1080). Natural river sand in River sand/B; fine recycled concrete aggregate RCA/B = {rca/B:.3f} (no column). Steel fibre 196 kg/m3 = 2.5 vol% (paper). Fibre strength >3000 MPa. Four-point flexural strength = {fl} MPa (not recorded as row)."})

# ---------- P8 Gu 2021
B=1.3
add({},**{"Article Name":"Cyclic Behavior of Reinforced High Strain-Hardening UHPC under Axial Tension","Author":"Gu J.-B.; Wang J.-Y.; Guo Y.-Q.","Year":2021,"DOI / URL":"https://doi.org/10.3390/ma14133602",
 "OPC / Cement":1/B,"SF (Silica fume)":0.3/B,"W / B":0.2/B,"Sand (type not stated) / B":1.34/B,"SP / B":0.005/B,
 "Steel fiber (vol%)":1.8,"Steel length (mm)":16,"Steel diameter (µm)":200,"Steel tensile strength (MPa)":2500,"Steel elastic modulus (GPa)":200,"Total fiber (vol%)":1.8,
 "Curing method":"non-steam cured (no further details)","Test age (days)":28,"Compressive specimen":"cube","Compressive specimen size (mm)":"100x100x100","Tensile specimen":"dog-bone (plain HSHUHPC)","Tensile test type":"direct",
 "Compressive strength (MPa)":154.1,"Tensile strength (MPa)":9.77,"Tensile strain capacity (%)":0.3,
 "Source table/page":"Table 2 (mix, mass ratio to cement), Table 3 (fibre), Sec. 2 text (fc, ft)",
 "Conversions / notes":"Ratios to cement converted to binder = cement + SF = 1.3. 'Fine filler' 0.3 per cement (= 0.231 of binder), type not specified - not placed in a column. Tensile values stated as 'around 9.77 MPa' and 'around 3000 microstrain'. Test age 28 d stated for fc; tension age not stated."})

# ---------- P9 Guo YQ 2022 (fc only)
B=1.23
p9={"Article Name":"Nonlinear Inverse Analysis for Predicting the Tensile Properties of Strain-Softening and Strain-Hardening UHPFRC","Author":"Guo Y.-Q.; Wang J.-Y.; Gu J.-B.","Year":2022,"DOI / URL":"https://doi.org/10.3390/ma15093067",
 "OPC / Cement":1/B,"SF (Silica fume)":0.23/B,"W / B":0.24/B,"Sand (type not stated) / B":1.08/B,"SP / B":0.034/B,"Coarse aggregate / B":1.24/B,
 "Steel length (mm)":16,"Steel diameter (µm)":200,"Steel tensile strength (MPa)":2500,"Steel elastic modulus (GPa)":200,
 "Curing method":"24 h under plastic at room temperature, then water curing at 20 C","Curing time (days)":28,"Curing temperature (°C)":20,"Demolding age (days)":1,
 "Compressive specimen":"cylinder","Compressive specimen size (mm)":"100x200","Source table/page":"Table 1 (mix), Table 2 (fibre), Table 3 (fc)"}
for vf,fc in [(0.5,139.9),(0.75,135.2),(1.0,134.2),(1.25,140.6),(1.5,147.3)]:
    add(p9,**{"Steel fiber (vol%)":vf,"Total fiber (vol%)":vf,"Compressive strength (MPa)":fc,
      "Conversions / notes":f"Vf={vf}%. Mass ratios to cement converted to binder (cement+SF=1.23). Basalt coarse aggregate max 8 mm. Straight brass-coated fibres. Only notched 3-point bending (no direct tension) - tensile fields blank. Test age not stated explicitly (after 28 d water curing)."})

# ---------- P10 Guo M 2021
B=1090.
p10={"Article Name":"Relationships among the Characteristic Tensile Strain, Curing Age, and Strength of Reactive Powder Concrete","Author":"Guo M.; Gao R.","Year":2021,"DOI / URL":"https://doi.org/10.3390/ma14102660",
 "OPC / Cement":920/B,"SF (Silica fume)":170/B,"W / B":174/B,"SS / B (Silica sand)":(460+340+280)/B,"SP / B":22/B,"Binder content (kg/m³)":B,
 "Steel fiber (vol%)":2,"Steel diameter (µm)":220,"Steel tensile strength (MPa)":2800,"Total fiber (vol%)":2,
 "Curing method":"24 h in standard curing room, demoulded, standard curing room until test (GB/T 50081-2019)","Demolding age (days)":1,
 "Tensile specimen":"dumbbell","Tensile test type":"direct","Source table/page":"Table 1 (mix), Table 3 (fc, axial tension)"}
for age,fc,ftv,eps in [(3,46.8,5.14,142.76),(7,67.8,5.68,166.10),(14,70.2,5.72,175.62),(28,101.2,6.2,196.44),(56,113.1,6.84,200.85)]:
    add(p10,**{"Test age (days)":age,"Curing time (days)":age,"Compressive strength (MPa)":fc,"Tensile strength (MPa)":ftv,"Tensile strain capacity (%)":eps/1e4,
      "Conversions / notes":"kg/m3 / binder (cement 920 + SF 170). Quartz sand (coarse 460 + medium 340 + fine 280) in SS/B. Steel fibre 120 kg/m3 stated as Vf=2% by the paper (120/7850 would give 1.53%) - paper value used. Fibre length 12-15 mm (left blank). Strain capacity = ultimate (peak) tensile strain from Table 3, microstrain -> %. Compressive specimen size not stated. Table 3 compressive column header mislabelled ft in source."})

# ---------- P11 Kim MJ 2018
B=788.5+197.1
p11={"Article Name":"Hybrid Effect of Twisted Steel and Polyethylene Fibers on the Tensile Performance of Ultra-High-Performance Cementitious Composites","Author":"Kim M.-J.; Kim S.; Yoo D.-Y.","Year":2018,"DOI / URL":"https://doi.org/10.3390/polym10080879",
 "OPC / Cement":788.5/B,"SF (Silica fume)":197.1/B,"W / B":0.2,"SS / B (Silica sand)":867.4/B,"QP / B (Quartz powder)":236.6/B,"SP / B":52.6/B,"Binder content (kg/m³)":B,
 "Curing method":"24 h at 20 C/60% RH under plastic, steam curing 90 C for 72 h, then room conditions","Curing temperature (°C)":90,"Heat curing duration (h)":72,"Demolding age (days)":1,"Test age (days)":7,
 "Compressive specimen":"cylinder","Compressive specimen size (mm)":"100x200","Tensile specimen":"dog-bone, 30x13 section","Tensile gauge length (mm)":80,"Tensile test type":"direct",
 "Source table/page":"Table 1 (mix), Table 4 (fibres), Sec. 3 text (fc, ft, strain capacity)"}
plen={"SPE":12,"MPE":18,"LPE":27,"LLPE":36}
for n,t,pe,pt,fc,ftv,sc,ex in [("T2.0",2,0,None,204.4,15.5,0.52,""),("T1.5-LLPE0.5",1.5,.5,"LLPE","",10.4,0.83,""),
  ("T1.0-SPE1.0",1.0,1.0,"SPE","",14.3,"","; ft 14.3 inferred from text 'series decreased from 14.3 MPa (SPE) to 10.5 MPa (LLPE)' - doubtful"),
  ("T1.0-LPE1.0",1.0,1.0,"LPE","",11.6,0.84,""),("T1.0-LLPE1.0",1.0,1.0,"LLPE","",10.5,1.01,""),("T0.5-SPE1.5",.5,1.5,"SPE",139.3,11.9,1.66,""),
  ("T0.5-MPE1.5",.5,1.5,"MPE","",11.5,1.16,""),("SPE2.0",0,2,"SPE","",7.8,0.94,""),("MPE2.0",0,2,"MPE","",9.7,0.79,""),("LLPE2.0",0,2,"LLPE","",12.2,1.35,"")]:
    kw={"Steel fiber (vol%)":t,"Total fiber (vol%)":t+pe,"Compressive strength (MPa)":fc,"Tensile strength (MPa)":ftv,"Tensile strain capacity (%)":sc,
        "Conversions / notes":f"Mix {n}. kg/m3 / binder (cement+SF = 985.6). W/B 0.2 per paper (total water incl. SP water / binder; free water/B = 0.163). Silica flour in QP/B. SP/B from Table 1 (52.6 kg/m3 liquid, 30% solids); Table 3 lists varying batch SP (470-740 g) per mix. Twisted fibre strength 2428 MPa (Table 4; text says 2788). Other per-mix fc only in figure."+ex}
    if t: kw.update({"Steel length (mm)":30,"Steel diameter (µm)":300,"Steel tensile strength (MPa)":2428,"Steel elastic modulus (GPa)":200})
    if pe: kw.update({"PE fiber (vol%)":pe,"PE length (mm)":plen[pt],"PE diameter (µm)":30,"PE tensile strength (MPa)":3030,"PE elastic modulus (GPa)":88})
    add(p11,**kw)

# ---------- P12 Choi MS 2016
B=771+193.
p12={"Article Name":"Improvement in Predicting the Post-Cracking Tensile Behavior of Ultra-High Performance Cementitious Composites Based on Fiber Orientation Distribution","Author":"Choi M.S.; Kang S.-T.; Lee B.Y.; Koh K.-T.; Ryu G.-S.","Year":2016,"DOI / URL":"https://doi.org/10.3390/ma9100829",
 "OPC / Cement":771/B,"SF (Silica fume)":193/B,"W / B":160/B,"Sand (type not stated) / B":848/B,"QP / B (Quartz powder)":231/B,"SP / B":46.3/B,"Binder content (kg/m³)":B,
 "Steel fiber (vol%)":2,"Steel diameter (µm)":200,"Steel tensile strength (MPa)":2500,"Steel elastic modulus (GPa)":200,"Total fiber (vol%)":2,
 "Curing method":"2 days room temperature, demoulded, steam curing 90+/-3 C for 3 days, then 20 C water until testing","Curing temperature (°C)":90,"Heat curing duration (h)":72,"Demolding age (days)":2,
 "Tensile specimen":"notched dog-bone (10 mm notch each side)","Tensile test type":"direct","Source table/page":"Table 2 (mix), Table 3 (direct tension)"}
for m,fte,ftu,desc in [("A",6.68,7.59,"cast to induce random fibre distribution"),("B",7.55,14.92,"cast to align fibres along flow direction")]:
    add(p12,**{"First-cracking strength (MPa)":fte,"Tensile strength (MPa)":ftu,
      "Conversions / notes":f"Casting Method {m} ({desc}); same mix. kg/m3 / binder (cement+SF=964). Siliceous filler (4 um, SiO2>98%) put in QP/B. Text says W/B 0.2 (table water 160 gives 0.166). Steel fibres 156 kg/m3 = 2 vol% (paper, density 7.5 g/cm3); hybrid of 16.3 mm and 19.5 mm straight fibres (length blank). Notched specimen: strain capacity not reported (CMOD only). fc and test age not reported."})

# ---------- P13 Kim MK 2021
B=1.15
p13={"Article Name":"Electromechanical Response of Smart Ultra-High Performance Concrete under External Loads Corresponding to Different Electrical Measurements","Author":"Kim M.K.; Le H.V.; Kim D.J.","Year":2021,"DOI / URL":"https://doi.org/10.3390/s21041281",
 "OPC / Cement":1/B,"SF (Silica fume)":0.15/B,"W / B":0.2/B,"QP / B (Quartz powder)":0.25/B,"SP / B":0.042/B,
 "Steel fiber (vol%)":2,"Steel length (mm)":30,"Steel diameter (µm)":300,"Steel tensile strength (MPa)":2447,"Steel elastic modulus (GPa)":200,"Total fiber (vol%)":2,
 "Curing method":"48 h under plastic at 25 C/60% RH, demoulded, then 90 C water curing for 3 days","Curing temperature (°C)":90,"Heat curing duration (h)":72,"Demolding age (days)":2,
 "Compressive specimen":"cube","Compressive specimen size (mm)":"50x50x50","Tensile specimen":"dumbbell, 25x50 section","Tensile gauge length (mm)":100,"Tensile test type":"direct",
 "Source table/page":"Table 1 (mix), Table 2 (fibres), Table 3 (tension), Table 4 (compression)"}
for m,meas,ss,fcs,ecc,epc,scc,spc,fc in [("Ma","DC",1.0,0,0.032,0.66,10.16,17.54,145.07),("Mb","DC",0.5,0.5,0.029,0.69,7.49,16.52,171.95),
                                      ("Ma","AC",1.0,0,0.027,0.73,9.94,17.74,140.20),("Mb","AC",0.5,0.5,0.029,0.61,6.75,17.66,167.40)]:
    add(p13,**{"SS / B (Silica sand)":ss/B,"Compressive strength (MPa)":fc,"First-cracking strength (MPa)":scc,"Tensile strength (MPa)":spc,"Tensile strain capacity (%)":epc,
      "Conversions / notes":f"Mix {m}, specimens tested with {meas} electrical measurement. Weight ratios to cement converted to binder (cement+SF=1.15). Silica powder in QP/B. W/B = water/binder (SP 30% solids; its water excluded). Fine steel slag aggregate FSSA/B = {fcs/B:.3f} (no column). Fibre data = 30 mm smooth fibres used in tensile specimens; compressive cubes used 6 mm/200 um smooth fibres (2 vol%). fc from Table 4 (Table 1 lists f'ck {178 if m=='Ma' else 179} MPa). Strain capacity = post-cracking strain at peak (Table 3). Test age not reported."})

with open(D+"/uhpc_steel.csv","w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=H); w.writeheader()
    for r in rows: w.writerow({k:r.get(k,"") for k in H})
print(len(rows), len(set(r["DOI / URL"] for r in rows)))

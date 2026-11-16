"""Load "04 Dataset_web.xlsx" and turn each row into the 33 model inputs with EXACTLY the
rules the web page uses (index.html: ROLES, calcMix, buildFeatures). Training and the web
therefore see the same numbers for the same mix.

    from web_data import load
    X, Y, groups = load()     # X: DataFrame of FEATURES, Y: {"fc","eps"} Series, groups: paper
"""
import os, re, json
import numpy as np, pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
DATA = os.path.join(root, "04 Dataset_web.xlsx")

FEATURES = ["OPC", "GGBS", "FA", "SF", "MK", "LP",
            "WG_B", "NaOH_B", "CaOH2_B", "Na2SO4_B", "SSM_B",
            "W_B", "Sand_B", "QP_B", "Light_B", "SP_B", "VMA_B",
            "V_PE", "V_PVA", "V_Steel", "V_PBO", "V_total",
            "Cure_T", "Cure_days", "Cure_RH", "Age_days", "Cure_water", "Cure_sealed", "Cure_heat",
            "W_C", "Activator_tot", "Paste_vol", "Binder_kgm3"]
OUTPUTS = {"fc": "Compressive strength (MPa)",
           "eps": "Tensile strain capacity (%)"}
CONDS = ["Curing method", "Curing temperature (°C)", "Relative humidity (%)", "Curing duration (days)", "Test age (days)"]

# same table as ROLES in index.html (first match wins)
ROLES = [
    (r"(?i)^OPC\b", "B:OPC"), (r"(?i)^GGBS\b", "B:GGBS"), (r"(?i)^FA \(fly", "B:FA"), (r"(?i)^SF \(", "B:SF"),
    (r"(?i)metakaolin", "B:MK"), (r"(?i)^limestone powder", "B:LP"),
    (r"(?i)^SAC\b|^CAC\b|^RHA\b|recycled powder|reactive mgo|^CKD\b|diatomite|dolomite powder|pond ash|nano-sio2|^EAFD$|calcined zeolite", "B:other"),
    (r"^WG\b", "WG_B"), (r"^NaOH$", "NaOH_B"), (r"^Ca\(OH\)2$", "CaOH2_B"), (r"^Na2SO4$", "Na2SO4_B"),
    (r"^SSM\b", "SSM_B"), (r"^Na2CO3$", "Na2CO3_B"),
    (r"(?i)^water$", "W_B"),
    (r"(?i)sand|stone sludge|^RCF$", "Sand_B"), (r"(?i)quartz powder", "QP_B"),
    (r"(?i)crumb rubber|cenosphere|^HGM$|EPS beads|vermiculite|^EGGA$|^GPA$", "Light_B"),
    (r"^SP$|^HRWR$", "SP_B"), (r"^VMA$|^HPMC\b", "VMA_B"),
    (r"(?i)coarse aggregate", "coarse"),
    (r"(?i)selvage pe|^PE fiber", "F:PE"), (r"(?i)^PVA fiber", "F:PVA"), (r"(?i)^steel fiber", "F:Steel"),
    (r"(?i)^PBO fiber", "F:PBO"), (r"(?i)fib(er|re)", "F:other"),
]
PASTE_RHO = {"OPC": 3.15, "GGBS": 2.9, "FA": 2.3, "SF": 2.2, "MK": 2.5, "LP": 2.7}


def role_of(name):
    # JS regexes without the i flag are case-sensitive; (?i) marks the ones that have it
    for pat, r in ROLES:
        if re.search(pat, name):
            return r
    return "other"


def densities():
    html = open(os.path.join(root, "index.html"), encoding="utf-8").read()
    block = html.split("const DEFAULT_MATERIALS = [")[1].split("];")[0]
    mats = [json.loads(l.strip().rstrip(",")) for l in block.splitlines() if l.strip().startswith("{")]
    return {m["name"]: float(m["density"]) for m in mats}


def features(D, rho):
    mats = [c for c in D.columns if c in rho]
    role = {n: role_of(n) for n in mats}
    fib = [n for n in mats if role[n].startswith("F:")]
    mix = [n for n in mats if n not in fib]                         # everything entered in the binder table
    V = D[mats].fillna(0).astype(float)
    W = D["Water"].astype(float)                                     # NaN when the paper gave no W/B
    V["Water"] = W.fillna(0)

    Bn = [n for n in mix if role[n].startswith("B:")]
    B = V[Bn].sum(axis=1).replace(0, np.nan)
    X = pd.DataFrame(index=D.index)
    for k in ["OPC", "GGBS", "FA", "SF", "MK", "LP"]:
        X[k] = V[[n for n in Bn if role[n] == "B:" + k]].sum(axis=1) / B
    tot = lambda r: V[[n for n in mix if role[n] == r]].sum(axis=1)
    for k in ["WG_B", "NaOH_B", "CaOH2_B", "Na2SO4_B", "SSM_B", "Sand_B", "QP_B", "Light_B", "SP_B", "VMA_B"]:
        X[k] = tot(k) / B
    X["W_B"] = (W / B).where(W > 0)
    for k in ["PE", "PVA", "Steel", "PBO"]:
        X["V_" + k] = V[[n for n in fib if role[n] == "F:" + k]].sum(axis=1)
    X["V_total"] = V[fib].sum(axis=1)

    # calcMix: 1 m3 = fibers (vol%) + the rest split by the mass ratios and particle densities
    denom = sum(V[n] / rho[n] for n in mix)
    base = (1 - X["V_total"] / 100) / denom.replace(0, np.nan)
    bkg = B * base
    vb = sum((V[n] / B) / (PASTE_RHO.get(role[n][2:]) or rho[n] / 1000) for n in Bn)

    X["Cure_T"] = D["Curing temperature (°C)"].astype(float)
    X["Cure_days"] = D["Curing duration (days)"].astype(float)
    X["Cure_RH"] = D["Relative humidity (%)"].astype(float)
    X["Age_days"] = D["Test age (days)"].astype(float)
    m = D["Curing method"].astype(str)
    X["Cure_water"] = (m == "Water curing").astype(int)
    X["Cure_sealed"] = (m == "Sealed / wrapped").astype(int)
    X["Cure_heat"] = ((m == "Heat / steam curing") & (X["Cure_T"] > 40)).astype(int)
    X["W_C"] = X["W_B"] / X["OPC"].where(X["OPC"] > 0)
    X["Activator_tot"] = X[["WG_B", "NaOH_B", "CaOH2_B", "Na2SO4_B", "SSM_B"]].sum(axis=1) + tot("Na2CO3_B") / B
    X["Paste_vol"] = (vb + X["W_B"].fillna(0.3)) / 1000 * bkg
    X["Binder_kgm3"] = bkg
    return X[FEATURES]


def load(path=DATA):
    D = pd.read_excel(path, sheet_name="Data")
    X = features(D, densities())
    Y = {k: pd.to_numeric(D[c], errors="coerce") for k, c in OUTPUTS.items()}
    return X, Y, D["Paper"].astype(str)

"""Load "excel/04 Dataset_web.xlsx" and turn each row into the model inputs with EXACTLY the rules
of the web page (index.html: calcMix + buildFeatures). Training and the web see the same numbers.

Inputs = the 21 materials (materials21.json) + curing method / temperature / duration + test age,
plus 5 values computed from them (total fiber, water/cement, activator total, binder kg/m3, paste volume).

    from web_data import load
    X, Y, groups = load()     # X: DataFrame of FEATURES, Y: {"fc","eps"} Series, groups: paper
"""
import os, json
import numpy as np, pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
DATA = os.path.join(root, "excel", "04 Dataset_web.xlsx")
M21 = json.load(open(os.path.join(root, "materials21.json"), encoding="utf-8"))["materials"]
KEYS = [m["key"] for m in M21]
BINDER = [m["key"] for m in M21 if m["group"] == "binder"]
FIBERS = [m["key"] for m in M21 if m["group"] == "fiber"]
ACTIVATORS = ["NaOH", "Na2SO4", "Na2SiO3", "WG", "CaOH2"]
CONDS = ["Cure_T", "Cure_days", "Age_days", "Cure_water", "Cure_sealed", "Cure_heat", "Cure_air"]
DERIVED = ["V_total", "W_C", "Activator_tot", "Binder_kgm3", "Paste_vol"]
FEATURES = KEYS + CONDS + DERIVED
OUTPUTS = {"fc": "Compressive strength (MPa)", "eps": "Tensile strain capacity (%)"}
METHOD_FLAG = {"Water curing": "Cure_water", "Sealed / wrapped": "Cure_sealed",
               "Heat / steam curing": "Cure_heat", "Air (lab ambient)": "Cure_air"}


def densities():
    """kg/m3 of the 21 materials, from the material list embedded in index.html."""
    html = open(os.path.join(root, "index.html"), encoding="utf-8").read()
    block = html.split("const DEFAULT_MATERIALS = [")[1].split("];")[0]
    mats = {json.loads(l.strip().rstrip(","))["name"]: json.loads(l.strip().rstrip(",")) for l in block.splitlines() if l.strip().startswith("{")}
    return {m["key"]: float(mats[m["name"]]["density"]) for m in M21}


def features(D, rho):
    V = pd.DataFrame({m["key"]: pd.to_numeric(D[m["name"]], errors="coerce").fillna(0) for m in M21})
    B = V[BINDER].sum(axis=1).replace(0, np.nan)
    X = pd.DataFrame(index=D.index)
    for k in KEYS:
        X[k] = V[k] if k in FIBERS else V[k] / B           # shares / ratios per (cement + FA + GGBS)
    X["Cure_T"] = pd.to_numeric(D["Curing temperature (°C)"], errors="coerce")
    X["Cure_days"] = pd.to_numeric(D["Curing duration (days)"], errors="coerce")
    X["Age_days"] = pd.to_numeric(D["Test age (days)"], errors="coerce")
    m = D["Curing method"].astype(str)
    for name, flag in METHOD_FLAG.items():
        X[flag] = (m == name).astype(int)
    X["V_total"] = V[FIBERS].sum(axis=1)
    X["W_C"] = X["Water"] / X["Cement"].where(X["Cement"] > 0)
    X["Activator_tot"] = X[ACTIVATORS].sum(axis=1)
    # calcMix: fibers take their vol%, the rest of 1 m3 is split by mass ratio / density
    nonfib = [k for k in KEYS if k not in FIBERS]
    denom = sum(X[k] / rho[k] for k in nonfib)
    X["Binder_kgm3"] = (1 - X["V_total"] / 100) / denom.replace(0, np.nan)      # binder shares add up to 1
    vb = sum(X[k] / (rho[k] / 1000) for k in BINDER)                               # litres per kg binder
    X["Paste_vol"] = (vb + X["Water"]) / 1000 * X["Binder_kgm3"]
    return X[FEATURES]


def load(path=DATA):
    D = pd.read_excel(path, sheet_name="Data")
    X = features(D, densities())
    Y = {k: pd.to_numeric(D[c], errors="coerce") for k, c in OUTPUTS.items()}
    return X, Y, D["Paper"].astype(str)

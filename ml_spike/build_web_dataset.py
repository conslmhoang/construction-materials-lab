"""Build the training file "04 Dataset_web.xlsx": one row per mix x test age, and ONLY the columns
the web calculator has:

  Paper, DOI | the 69 web materials | curing method, temperature, RH, duration, test age |
  compressive strength, direct tensile strength, tensile strain capacity

Units are the web's units: binder materials = mass fraction of the binder (they sum to 1),
other materials = mass ratio to the binder, fibers = vol%.
Only rows that pass the cleaning (clean/dataset_clean.csv: use_fc / use_ft / use_eps) are kept,
and an output cell is left blank when that value is not used.

Usage:  python build_web_dataset.py
"""
import os, re, json
import numpy as np, pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
SRC = os.path.join(root, "03 Dataset_ratio.xlsx")
OUT = os.path.join(root, "04 Dataset_web.xlsx")

# ---- the 69 web materials, in the web's order
html = open(os.path.join(root, "index.html"), encoding="utf-8").read()
block = html.split("const DEFAULT_MATERIALS = [")[1].split("];")[0]
WEB = [json.loads(l.strip().rstrip(","))["name"] for l in block.splitlines() if l.strip().startswith("{")]
assert len(WEB) == 69, len(WEB)

# ---- 03 Dataset_ratio.xlsx, read the same way as before (spike.py)
raw = pd.read_excel(SRC, "Dataset", header=None)
d = raw.iloc[2:].reset_index(drop=True)
d.columns = range(raw.shape[1])
d[0] = d[0].ffill()
d = d[d.iloc[:, 4:].notna().any(axis=1)].reset_index(drop=True)
F = pd.read_csv(os.path.join(here, "clean", "dataset_clean.csv"), encoding="utf-8-sig")
assert len(F) == len(d), (len(F), len(d))
N = lambda i: pd.to_numeric(d[i], errors="coerce")

# ---- which source columns go into which web material (values are added up)
SRC_COLS = {
    # binders (fraction of binder)
    "OPC (Ordinary Portland Cement)": [4], "SAC (calcium sulfoaluminate cement)": [5],
    "CAC (calcium aluminate cement)": [6], "GGBS (Ground-granulated blast furnace slag)": [7],
    "FA (Fly ash)": [8], "SF (Silica fume)": [9], "Metakaolin": [10], "Limestone Powder": [11],
    "Diatomite": [12], "Nano-SiO2": [13], "Recycled powder (construction & demolition waste powder)": [14],
    "Dolomite powder": [15], "Pond ash": [16], "RHA (rice husk ash)": [18], "EAFD": [19],
    "Reactive MgO": [37], "CKD (cement kiln dust)": [55],
    # activators (ratio to binder)
    "WG (Water glass)": [67], "NaOH": [68], "Ca(OH)2": [69], "Na2SO4": [70],
    "SSM - Na2SiO3 (Anhydrous sodium metasilicate)": [71], "Na2CO3": [72],
    # aggregates / fillers (ratio to binder); sand of unstated or "fine" type -> silica sand,
    # "local" sand and SSD aggregate -> river sand
    "SS (Silica sand)": [86, 87, 97], "River sand": [94, 90, 181], "Dune sand": [91], "M-sand": [92],
    "Sea sand": [93], "Stone sludge powder": [95], "RCF": [161], "GPA": [174], "Quartz powder": [104],
    "Calcined zeolite": [88], "FA cenosphere": [102], "Vermiculite": [103], "HGM": [105],
    "Crumb rubber": [106], "EPS beads": [107], "EGGA": [139], "Coarse aggregate": [148],
    # admixtures (ratio to binder)
    "SP": [110], "HRWR": [116], "VMA": [117], "HPMC (hydroxypropyl methyl cellulose)": [118],
    "CNT": [108], "CNF": [109], "Water repellent": [111], "Ca(NO3)2": [119],
    "Anti-foamer / defoamer": [120, 126], "Expansive admixture (CSA / CaO-type expansive agent)": [124],
    "SRA": [125], "SHMP": [138], "AE agent": [156],
    "Borax (Na2B4O7·10H2O, sodium tetraborate decahydrate)": [173],
    # fibers (vol%)
    "PE fiber": [182], "PVA fiber": [189], "Steel fiber": [199, 206, 207, 281, 282, 289], "PBO fiber": [211],
    "PP fiber": [217], "Glass fiber": [227], "PET fiber": [235], "Basalt fiber": [242], "Carbon fiber": [295],
    "RTP fiber": [241], "CaCO3 whisker fiber": [271], "Sisal fiber": [303], "PA fiber": [313],
}
unknown = [k for k in SRC_COLS if k not in WEB]
assert not unknown, unknown

D = pd.DataFrame(index=d.index)
D["Paper"] = F["paper"].values
D["DOI"] = F["doi"].fillna("").values
for name in WEB:
    if name == "Water":
        D[name] = N(83).fillna(N(134)).fillna(N(85))           # W/B, else total water / B, else mixing liquid / B
    elif name in SRC_COLS:
        vals = sum(N(i).fillna(0) for i in SRC_COLS[name])
        if name == "SP":
            vals = vals.where(vals > 0, N(172).fillna(0))         # water reducer of unstated type
        D[name] = vals
    else:
        D[name] = 0.0                                            # material on the web, not in any paper

# ---- curing and test conditions, as the web asks for them
cm = d[327].astype(str).str.lower().where(d[327].notna(), "")
T = N(329)
method = np.select(
    [cm.str.contains("heat|steam|oven|°c") & (T.fillna(20) > 40),
     cm.str.contains("water"), cm.str.contains("seal|wrap|plastic"), cm.str.contains(r"\bair\b|ambient")],
    ["Heat / steam curing", "Water curing", "Sealed / wrapped", "Air (lab ambient)"],
    "Standard moist room")
D["Curing method"] = method
D["Curing temperature (°C)"] = T
D["Relative humidity (%)"] = N(330)
D["Curing duration (days)"] = N(328)
D["Test age (days)"] = N(341).fillna(N(328))

# ---- outputs: only the values the cleaning kept
use = {k: F[f"use_{k}"].astype(bool).values for k in ("fc", "ft", "eps")}
D["Compressive strength (MPa)"] = N(389).where(use["fc"])
D["Direct tensile strength (MPa)"] = N(404).where(use["ft"])
D["Tensile strain capacity (%)"] = N(418).where(use["eps"])

keep = use["fc"] | use["ft"] | use["eps"]
D = D[keep].reset_index(drop=True)

# fibers with only a "total fiber" value and no type cannot be entered on the web
fib = [n for n in WEB if re.search(r"fib(er|re)", n, re.I)]
no_type = D[fib].sum(axis=1) == 0
print("rows kept:", len(D), "| dropped, fiber type not given:", int(no_type.sum()))
D = D[~no_type].reset_index(drop=True)
# a mix must have at least one binder the web knows (rows with only "other binder" cannot be entered)
from web_data import role_of
binder_cols = [n for n in WEB if role_of(n).startswith("B:")]
no_binder = D[binder_cols].sum(axis=1) == 0
print("dropped, no web binder:", int(no_binder.sum()))
D = D[~no_binder].reset_index(drop=True)

# drop material columns that are 0 in every row? No: keep all 69 so the file matches the web 1:1.
guide = pd.DataFrame({"Item": [
    "One row", "Paper / DOI", "Binder materials", "Other materials", "Fibers", "Curing method",
    "Curing duration", "Outputs", "Source", "Rebuild"], "Meaning": [
    "One mix at one test age.",
    "Source paper (used to group rows and list sources on data.html).",
    "OPC, GGBS, FA, SF, metakaolin, limestone powder, SAC, CAC, RHA ...: mass fraction of the binder (they add up to 1).",
    "Water, sand, quartz powder, activators, admixtures ...: mass ratio to the binder.",
    "Volume % of the mix.",
    "Standard moist room / Water curing / Sealed / wrapped / Air (lab ambient) / Heat / steam curing (same list as the web).",
    "For heat curing: days at high temperature; otherwise days of curing before the test.",
    "Blank when the paper did not report it or the value was excluded during cleaning (see data.html).",
    "Built from 03 Dataset_ratio.xlsx (full extraction, 773 columns) with ml_spike/build_web_dataset.py.",
    "python ml_spike/build_web_dataset.py, then python ml_spike/train_export.py"]})
with pd.ExcelWriter(OUT, engine="openpyxl") as w:
    D.to_excel(w, sheet_name="Data", index=False)
    guide.to_excel(w, sheet_name="Guide", index=False)
print("wrote", OUT, D.shape)
print({k: int(D[c].notna().sum()) for k, c in [("fc", "Compressive strength (MPa)"), ("ft", "Direct tensile strength (MPa)"), ("eps", "Tensile strain capacity (%)")]})

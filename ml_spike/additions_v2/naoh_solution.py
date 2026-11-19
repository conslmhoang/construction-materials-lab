"""NaOH solution given by molarity -> NaOH solids and water (the user allowed this conversion, 2026-11-19).

Source of the table (ml_spike/reference/naoh_solution_table.csv): OxyChem Caustic Soda Handbook, Table 1 "Density and NaOH Content of
Membrane Grade Caustic Soda solutions at 60 °F", p. 30
(https://www.oxychem.com/siteassets/documents/chlor-alkali/caustic-soda-handbook.pdf).
Molarity = (g NaOH per L) / 40.00 g/mol. Values between rows: linear interpolation. Cross-check: 50 wt% = 19.1 M,
same as OpenStax Chemistry 2e, Appendix F.

    from naoh_solution import naoh_split
    s = naoh_split(molarity=10, solution_mass=0.15)       # solution mass as a ratio to binder (or kg/m3)
    s -> {"NaOH": 0.0450, "water": 0.1050, "wt_pct": 30.03, "note": "..."}
    s = naoh_split(molarity=12, solution_volume_L=1.0)    # a volume in litres -> mass from the specific gravity
"""
import os
import numpy as np
import pandas as pd

_T = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reference", "naoh_solution_table.csv"))
SOURCE = "OxyChem Caustic Soda Handbook, Table 1 (p. 30), 60 °F; molarity = (g NaOH/L)/40.00, linear interpolation"


def naoh_split(molarity, solution_mass=None, solution_volume_L=None):
    gpl = float(molarity) * 40.00
    if not (_T.NaOH_g_per_L.min() <= gpl <= _T.NaOH_g_per_L.max()):
        raise ValueError(f"{molarity} M is outside the table (1-52 wt%)")
    wt = float(np.interp(gpl, _T.NaOH_g_per_L, _T.wt_pct_NaOH))
    sg = float(np.interp(gpl, _T.NaOH_g_per_L, _T.specific_gravity))
    if solution_mass is None:
        if solution_volume_L is None:
            raise ValueError("give solution_mass or solution_volume_L")
        solution_mass = solution_volume_L * sg          # kg per litre of solution
    naoh = solution_mass * wt / 100
    return {"NaOH": round(naoh, 6), "water": round(solution_mass - naoh, 6), "wt_pct": round(wt, 2), "sg": round(sg, 4),
            "note": f"{molarity} M NaOH solution = {wt:.2f} wt% NaOH (SG {sg:.4f}); {SOURCE}"}


if __name__ == "__main__":
    for M in (8, 10, 12, 14, 16):
        print(M, naoh_split(M, solution_mass=1.0))

"""
embed_materials.py
------------------
Injects the material database from "01 Datamix.xlsx" into the standalone
index.html calculator, so the web page works without any Python backend.

Usage
-----
    python embed_materials.py
    python embed_materials.py "01 Datamix.xlsx" index.html

Run this again whenever you update the Excel database, then commit and push:

    git add .
    git commit -m "Update material database"
    git push

The script rewrites only the block between these two markers in index.html:

    // >>> MATERIALS BEGIN
    const DEFAULT_MATERIALS = [ ... ];
    // <<< MATERIALS END
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pandas as pd

DEFAULT_EXCEL = "01 Datamix.xlsx"
DEFAULT_HTML = "index.html"

BEGIN_MARK = "// >>> MATERIALS BEGIN"
END_MARK = "// <<< MATERIALS END"

PROPERTY_ALIASES = {
    "density": ["Density (kg/m3)", "Density (kg/m³)", "Density"],
    "energy": ["Energy (MJ/kg)", "Energy"],
    "co2": ["CO2 (kg/kg)", "CO₂ (kg/kg)", "CO2", "CO₂"],
    "cost": ["Cost ($/kg)", "Cost"],
}


def _clean_text(value) -> str:
    """Normalizes a cell: removes non-breaking spaces, newlines and extra whitespace."""
    if pd.isna(value):
        return ""
    text = str(value).replace("\xa0", " ").replace("\n", " ")
    return re.sub(r"\s+", " ", text).strip()


def _find_property_row(df: pd.DataFrame, property_name: str):
    """Finds the row index holding a given material property."""
    aliases = PROPERTY_ALIASES[property_name]
    first_col = df.iloc[:, 0].apply(_clean_text)

    for alias in aliases:
        matches = first_col.str.casefold() == alias.casefold()
        if matches.any():
            return int(matches[matches].index[0])

    for alias in aliases:
        alias_norm = alias.replace(" ", "").replace("³", "3").casefold()
        for idx, value in first_col.items():
            value_norm = value.replace(" ", "").replace("³", "3").casefold()
            if alias_norm in value_norm:
                return int(idx)
    return None


def extract_materials(excel_path: str | Path, sheet_name: int | str = 0) -> list[dict]:
    """Reads the Excel database and returns a list of material dicts."""
    excel_path = Path(excel_path)
    if not excel_path.exists():
        raise FileNotFoundError(f"Excel file not found: {excel_path.resolve()}")

    df = pd.read_excel(excel_path, sheet_name=sheet_name, header=None)
    if df.empty or df.shape[1] < 2:
        raise ValueError("The sheet is empty or has an unexpected layout.")

    names = [_clean_text(v) for v in df.iloc[0, 1:]]
    rows = {prop: _find_property_row(df, prop) for prop in PROPERTY_ALIASES}
    if rows["density"] is None:
        raise ValueError("Could not find the 'Density' row in the first column.")

    materials: list[dict] = []
    skipped: list[str] = []

    for col, name in enumerate(names, start=1):
        if not name or name.lower().startswith("unnamed"):
            continue

        def value(prop: str) -> float:
            idx = rows.get(prop)
            if idx is None:
                return 0.0
            num = pd.to_numeric(df.iloc[idx, col], errors="coerce")
            return 0.0 if pd.isna(num) else round(float(num), 6)

        density = pd.to_numeric(df.iloc[rows["density"], col], errors="coerce")
        if pd.isna(density) or density <= 0:
            skipped.append(name)
            continue

        materials.append({
            "name": name,
            "density": round(float(density), 6),
            "energy": value("energy"),
            "co2": value("co2"),
            "cost": value("cost"),
        })

    if not materials:
        raise ValueError("No material with a valid density was found.")

    if skipped:
        print(f"  Skipped (no density): {', '.join(skipped)}")

    return materials


def inject(materials: list[dict], html_path: str | Path) -> Path:
    """Replaces the DEFAULT_MATERIALS block inside index.html."""
    html_path = Path(html_path)
    if not html_path.exists():
        raise FileNotFoundError(f"HTML file not found: {html_path.resolve()}")

    html = html_path.read_text(encoding="utf-8")
    if BEGIN_MARK not in html or END_MARK not in html:
        raise ValueError(
            f"Markers not found in {html_path.name}. "
            f"Expected '{BEGIN_MARK}' and '{END_MARK}'."
        )

    lines = ",\n".join(
        "  " + json.dumps(m, ensure_ascii=False, separators=(",", ":"))
        for m in materials
    )
    block = f"{BEGIN_MARK}\nconst DEFAULT_MATERIALS = [\n{lines}\n];\n{END_MARK}"

    pattern = re.compile(
        re.escape(BEGIN_MARK) + r".*?" + re.escape(END_MARK),
        re.DOTALL,
    )
    html_path.write_text(pattern.sub(lambda _: block, html, count=1), encoding="utf-8")
    return html_path


def main() -> int:
    excel = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_EXCEL
    html = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_HTML

    print(f"Reading  : {excel}")
    materials = extract_materials(excel)
    print(f"  Found  : {len(materials)} materials")

    out = inject(materials, html)
    print(f"Updated  : {out}")
    print("\nNext:  git add .  &&  git commit -m \"Update material database\"  &&  git push")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

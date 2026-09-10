"""
mix_log.py
----------
Logs every mix design run to an Excel file, one row per run.

Log file layout (sheet "MixLog"):
    - First column : "Timestamp"   -> date and time of the run (YYYY-MM-DD HH:MM:SS)
    - Next columns : material names -> the ratio / proportion values entered by the user
    - Each run      : appended as a new row at the bottom of the table

A material used for the first time in a later run is automatically added as a new
column; earlier rows are filled with 0 (or left blank if FILL_MISSING_WITH_ZERO is False).

Quick start:
    from mix_log import save_mix_log

    binder = {"OPC": 1.0, "GGBFS": 0.5, "Sand": 2.0, "Water": 0.35}
    fiber  = {"PVA fiber": 2.0}

    save_mix_log(binder, fiber)                      # writes to "02 MixLog.xlsx"
    save_mix_log(binder, fiber, note="Mix M1 - 28d") # with a note
"""

from __future__ import annotations

import os
import re
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping, Optional

import pandas as pd

# ------------------------------------------------------------- settings ----

LOG_EXCEL_FILE = "02 MixLog.xlsx"   # default log file name
LOG_SHEET_NAME = "MixLog"           # sheet name
TIME_COLUMN = "Timestamp"           # name of the date/time column
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"   # date/time format written into the cell

# Suffix appended to fiber names so they are distinguishable from binder ratios
# (fibers are entered as % of volume, binders as mass ratios).
# Set to "" to keep plain material names for publication-ready tables.
FIBER_COLUMN_SUFFIX = " (%vol)"

# Auxiliary columns that are always pushed to the far right of the table
NOTE_COLUMN = "Mix ID"
TRAILING_COLUMNS = (NOTE_COLUMN,)

# Materials unused in a given run -> write 0 (True) or leave blank (False)
FILL_MISSING_WITH_ZERO = True


# -------------------------------------------------------------- helpers ----

def _clean_name(value: Any) -> str:
    """
    Normalizes a material name into a single-line column header.

    Names in the Excel database contain line breaks, e.g.
    "OPC\\n(Ordinary Portland Cement)". Collapsing them keeps the log headers
    on one line and identical to the ones used by the standalone HTML version.
    """
    text = str(value).replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip()


def build_log_row(
    binder_ratios: Optional[Mapping[str, float]] = None,
    fiber_ratios_percent: Optional[Mapping[str, float]] = None,
    timestamp: Optional[datetime] = None,
    note: str = "",
    extra: Optional[Mapping[str, Any]] = None,
) -> dict:
    """Builds one log row as {column name: value} from the user's input ratios."""
    ts = timestamp or datetime.now()
    row: dict[str, Any] = {TIME_COLUMN: ts.strftime(TIME_FORMAT)}

    for name, ratio in (binder_ratios or {}).items():
        row[_clean_name(name)] = float(ratio)

    for name, percent in (fiber_ratios_percent or {}).items():
        row[f"{_clean_name(name)}{FIBER_COLUMN_SUFFIX}"] = float(percent)

    for key, value in (extra or {}).items():
        row[_clean_name(key)] = value

    if note:
        row[NOTE_COLUMN] = str(note)

    return row


def _order_columns(old_columns, new_row: Mapping[str, Any]) -> list[str]:
    """Keeps the existing column order, appends new materials, pushes aux columns last."""
    ordered = [TIME_COLUMN]
    ordered += [c for c in old_columns if c not in ordered and c not in TRAILING_COLUMNS]
    ordered += [c for c in new_row if c not in ordered and c not in TRAILING_COLUMNS]
    ordered += [c for c in TRAILING_COLUMNS
                if c in old_columns or c in new_row]
    return ordered


def _format_sheet(path: Path, sheet_name: str) -> None:
    """Styles the sheet: bold header, frozen header row, sensible column widths."""
    try:
        from openpyxl import load_workbook
        from openpyxl.styles import Alignment, Font, PatternFill
    except ImportError:
        return

    wb = load_workbook(path)
    if sheet_name not in wb.sheetnames:
        return
    ws = wb[sheet_name]

    header_font = Font(bold=True)
    header_fill = PatternFill("solid", fgColor="DDEBF7")
    for cell in ws[1]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    ws.freeze_panes = "B2"

    for col_idx, column_cells in enumerate(ws.columns, start=1):
        letter = column_cells[0].column_letter
        max_len = max((len(str(c.value)) for c in column_cells if c.value is not None),
                      default=8)
        ws.column_dimensions[letter].width = min(max(10, max_len + 2), 24)
        if col_idx > 1:
            for cell in column_cells[1:]:
                if isinstance(cell.value, (int, float)):
                    cell.number_format = "0.###"
                    cell.alignment = Alignment(horizontal="center")

    wb.save(path)


# --------------------------------------------------------- main functions ----

def read_mix_log(
    log_path: str | Path = LOG_EXCEL_FILE,
    sheet_name: str = LOG_SHEET_NAME,
) -> pd.DataFrame:
    """Reads the whole mix design history. Returns an empty DataFrame if no log exists."""
    path = Path(log_path)
    if not path.exists():
        return pd.DataFrame(columns=[TIME_COLUMN])
    try:
        return pd.read_excel(path, sheet_name=sheet_name)
    except (ValueError, KeyError):
        return pd.DataFrame(columns=[TIME_COLUMN])


def save_mix_log(
    binder_ratios: Optional[Mapping[str, float]] = None,
    fiber_ratios_percent: Optional[Mapping[str, float]] = None,
    log_path: str | Path = LOG_EXCEL_FILE,
    sheet_name: str = LOG_SHEET_NAME,
    timestamp: Optional[datetime] = None,
    note: str = "",
    extra: Optional[Mapping[str, Any]] = None,
) -> Path:
    """
    Appends one mix design row to the Excel log file.

    binder_ratios        : dict {material name: ratio} - exactly the calculation input
    fiber_ratios_percent : dict {fiber name: volume percent}
    log_path             : path to the Excel log (created if missing)
    timestamp            : run time (defaults to the moment this function is called)
    note                 : short label identifying this mix in the log (e.g. "GP-FA30")
    extra                : additional columns to record (e.g. {"Actual volume (m3)": 0.05})

    Returns the path to the log file.
    """
    if not binder_ratios and not fiber_ratios_percent:
        raise ValueError("Nothing to log: at least one material is required.")

    row = build_log_row(
        binder_ratios=binder_ratios,
        fiber_ratios_percent=fiber_ratios_percent,
        timestamp=timestamp,
        note=note,
        extra=extra,
    )

    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    old_df = read_mix_log(path, sheet_name)
    new_df = pd.concat([old_df, pd.DataFrame([row])], ignore_index=True)
    new_df = new_df.reindex(columns=_order_columns(list(old_df.columns), row))

    if FILL_MISSING_WITH_ZERO:
        for col in new_df.columns:
            if col == TIME_COLUMN or col in TRAILING_COLUMNS:
                continue
            new_df[col] = pd.to_numeric(new_df[col], errors="coerce").fillna(0.0)

    if NOTE_COLUMN in new_df.columns:
        new_df[NOTE_COLUMN] = new_df[NOTE_COLUMN].fillna("")

    # Write to a temporary file first, then replace -> the existing log is never
    # corrupted if something fails halfway through.
    tmp_fd, tmp_name = tempfile.mkstemp(suffix=".xlsx", dir=str(path.parent))
    os.close(tmp_fd)
    tmp_path = Path(tmp_name)
    try:
        with pd.ExcelWriter(tmp_path, engine="openpyxl") as writer:
            new_df.to_excel(writer, sheet_name=sheet_name, index=False)
        _format_sheet(tmp_path, sheet_name)
        shutil.move(str(tmp_path), str(path))
    except PermissionError as exc:
        tmp_path.unlink(missing_ok=True)
        raise PermissionError(
            f"Cannot write to '{path}'. Please close the file in Excel and try again."
        ) from exc
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise

    return path


def save_mix_log_from_result(
    binder_ratios: Optional[Mapping[str, float]] = None,
    fiber_ratios_percent: Optional[Mapping[str, float]] = None,
    mix_result: Optional[dict] = None,
    actual_volume_m3: Optional[float] = None,
    log_path: str | Path = LOG_EXCEL_FILE,
    note: str = "",
    include_totals: bool = False,
    **kwargs,
) -> Path:
    """
    Extended version: logs the input ratios plus optional summary columns from the result.

    include_totals=True adds:
        Total mass (kg/m3), Cost ($/m3), Energy (MJ/m3), CO2 (kg/m3)
    actual_volume_m3, if given, is recorded in the "Actual volume (m3)" column.
    """
    extra: dict[str, Any] = dict(kwargs.pop("extra", {}) or {})

    if actual_volume_m3 is not None:
        extra["Actual volume (m3)"] = float(actual_volume_m3)

    if include_totals and mix_result:
        totals = mix_result.get("totals_per_m3", {})
        extra["Total mass (kg/m3)"] = totals.get("total_material_mass_kg_m3", 0.0)
        extra["Cost ($/m3)"] = totals.get("cost_per_m3", 0.0)
        extra["Energy (MJ/m3)"] = totals.get("energy_mj_per_m3", 0.0)
        extra["CO2 (kg/m3)"] = totals.get("co2_kg_per_m3", 0.0)

    return save_mix_log(
        binder_ratios=binder_ratios,
        fiber_ratios_percent=fiber_ratios_percent,
        log_path=log_path,
        note=note,
        extra=extra,
        **kwargs,
    )


if __name__ == "__main__":
    demo_binder = {"OPC": 1.0, "GGBFS": 0.5, "Silica sand": 2.0, "Water": 0.35}
    demo_fiber = {"PVA fiber": 2.0}
    out = save_mix_log(demo_binder, demo_fiber, note="Demo batch")
    print(f"Log written to: {out.resolve()}")
    print(read_mix_log(out).tail())

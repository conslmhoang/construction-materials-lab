from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Mapping, Optional
import pandas as pd

DEFAULT_EXCEL_FILE = "01 Datamix.xlsx"

PROPERTY_ALIASES = {
    "density": ["Density (kg/m3)", "Density (kg/m³)", "Density"],
    "energy": ["Energy (MJ/kg)", "Energy"],
    "co2": ["CO2 (kg/kg)", "CO₂ (kg/kg)", "CO2", "CO₂"],
    "cost": ["Cost ($/kg)", "Cost"],
}

@dataclass
class Material:
    """Represents a material loaded from the Excel database."""
    name: str
    density: float
    energy: float = 0.0
    co2: float = 0.0
    cost: float = 0.0

def _clean_text(value) -> str:
    """Cleans text data from Excel, removing non-breaking spaces and extra whitespaces."""
    if pd.isna(value):
        return ""
    return str(value).replace("\xa0", " ").strip()

def _find_property_row(df: pd.DataFrame, property_name: str) -> Optional[int]:
    """Finds the row index corresponding to a specific material property."""
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

def load_material_database(
    excel_path: str | Path = DEFAULT_EXCEL_FILE,
    sheet_name: int | str = 0,
) -> Dict[str, Material]:
    """Loads material database from the Excel file."""
    excel_path = Path(excel_path)
    if not excel_path.exists():
        raise FileNotFoundError(f"Excel file not found: {excel_path.resolve()}")

    df = pd.read_excel(excel_path, sheet_name=sheet_name, header=None)

    if df.empty or df.shape[1] < 2:
        raise ValueError("Excel file is empty or formatted incorrectly.")

    material_names = [_clean_text(v) for v in df.iloc[0, 1:].tolist()]
    property_rows = {prop: _find_property_row(df, prop) for prop in PROPERTY_ALIASES}

    if property_rows["density"] is None:
        raise ValueError("Could not find 'Density' row in the Excel file.")

    materials: Dict[str, Material] = {}

    for col_idx, material_name in enumerate(material_names, start=1):
        if not material_name or material_name.lower().startswith("unnamed"):
            continue

        def get_value(prop: str, default: float = 0.0) -> float:
            row_idx = property_rows.get(prop)
            if row_idx is None:
                return default
            try:
                val = df.iloc[row_idx, col_idx]
                value = pd.to_numeric(val, errors="coerce")
                return default if pd.isna(value) else float(value)
            except Exception:
                return default

        density = get_value("density", float("nan"))
        if pd.isna(density) or density <= 0:
            continue

        materials[material_name] = Material(
            name=material_name,
            density=density,
            energy=get_value("energy"),
            co2=get_value("co2"),
            cost=get_value("cost"),
        )

    if not materials:
        raise ValueError("No valid materials loaded from the Excel database.")

    return materials

def calculate_mix_design(
    binder_ratios: Mapping[str, float],
    fiber_ratios_percent: Mapping[str, float],
    materials: Mapping[str, Material],
) -> dict:
    """Calculates material mass and volumes for 1 m3 mix design without strict ratio constraints."""
    if not binder_ratios and not fiber_ratios_percent:
        raise ValueError("Please select at least one material for the mix design.")

    ratio_sum = sum(float(r) for r in binder_ratios.values())

    # Calculate Fibers
    fiber_results = {}
    total_fiber_volume = 0.0
    total_fiber_mass = 0.0
    total_fiber_cost = 0.0
    total_fiber_energy = 0.0
    total_fiber_co2 = 0.0

    for name, ratio_percent in fiber_ratios_percent.items():
        if name not in materials:
            raise KeyError(f"Fiber material '{name}' not found in database.")
        material = materials[name]
        volume = float(ratio_percent) / 100.0  
        mass = volume * material.density 

        cost = mass * material.cost
        energy = mass * material.energy
        co2 = mass * material.co2

        fiber_results[name] = {
            "name": name,
            "ratio_percent": float(ratio_percent),
            "volume_m3": volume,
            "density_kg_m3": material.density,
            "mass_kg_m3": mass,
            "cost_per_m3": cost,
            "energy_mj_per_m3": energy,
            "co2_kg_per_m3": co2,
        }

        total_fiber_volume += volume
        total_fiber_mass += mass
        total_fiber_cost += cost
        total_fiber_energy += energy
        total_fiber_co2 += co2

    if total_fiber_volume >= 1.0:
        raise ValueError(f"Total fiber volume must be less than 1.0 m³ (current = {total_fiber_volume:.4f} m³).")

    # Calculate Binders / Aggregates / Activators
    remaining_volume = max(0.0, 1.0 - total_fiber_volume)
    
    binder_results = {}
    total_binder_mass = 0.0
    total_binder_cost = 0.0
    total_binder_energy = 0.0
    total_binder_co2 = 0.0
    total_binder_volume = 0.0

    if binder_ratios:
        # Nếu nhập hệ số tỷ lệ
        denominator = sum(
            float(ratio) / materials[name].density
            for name, ratio in binder_ratios.items()
        )
        if denominator > 0:
            binder_base_mass = remaining_volume / denominator
        else:
            binder_base_mass = 0.0

        for name, ratio in binder_ratios.items():
            if name not in materials:
                raise KeyError(f"Material '{name}' not found in database.")
            material = materials[name]

            mass = float(ratio) * binder_base_mass
            volume = mass / material.density
            cost = mass * material.cost
            energy = mass * material.energy
            co2 = mass * material.co2

            binder_results[name] = {
                "name": name,
                "ratio": float(ratio),
                "volume_m3": volume,
                "density_kg_m3": material.density,
                "mass_kg_m3": mass,
                "cost_per_m3": cost,
                "energy_mj_per_m3": energy,
                "co2_kg_per_m3": co2,
            }

            total_binder_mass += mass
            total_binder_volume += volume
            total_binder_cost += cost
            total_binder_energy += energy
            total_binder_co2 += co2

    return {
        "remaining_binder_volume_m3": remaining_volume,
        "binder_ratio_sum": ratio_sum,
        "binder": binder_results,
        "fiber": fiber_results,
        "totals_per_m3": {
            "binder_mass_kg_m3": total_binder_mass,
            "fiber_mass_kg_m3": total_fiber_mass,
            "total_material_mass_kg_m3": total_binder_mass + total_fiber_mass,
            "binder_volume_m3": total_binder_volume,
            "fiber_volume_m3": total_fiber_volume,
            "total_volume_m3": total_binder_volume + total_fiber_volume,
            "cost_per_m3": total_binder_cost + total_fiber_cost,
            "energy_mj_per_m3": total_binder_energy + total_fiber_energy,
            "co2_kg_per_m3": total_binder_co2 + total_fiber_co2,
        },
    }

def calculate_actual_volume(mix_result: dict, actual_volume_m3: float) -> dict:
    """Scales 1 m³ proportions to the actual required casting volume."""
    if actual_volume_m3 <= 0:
        raise ValueError("Actual volume must be greater than 0.")

    actual_binder = {
        name: {
            "name": item["name"],
            "mass_kg": item["mass_kg_m3"] * actual_volume_m3,
            "volume_m3": item["volume_m3"] * actual_volume_m3,
            "cost": item["cost_per_m3"] * actual_volume_m3,
            "energy_mj": item["energy_mj_per_m3"] * actual_volume_m3,
            "co2_kg": item["co2_kg_per_m3"] * actual_volume_m3,
        }
        for name, item in mix_result["binder"].items()
    }

    actual_fiber = {
        name: {
            "name": item["name"],
            "mass_kg": item["mass_kg_m3"] * actual_volume_m3,
            "volume_m3": item["volume_m3"] * actual_volume_m3,
            "cost": item["cost_per_m3"] * actual_volume_m3,
            "energy_mj": item["energy_mj_per_m3"] * actual_volume_m3,
            "co2_kg": item["co2_kg_per_m3"] * actual_volume_m3,
        }
        for name, item in mix_result["fiber"].items()
    }

    per_m3 = mix_result["totals_per_m3"]

    return {
        "actual_volume_m3": float(actual_volume_m3),
        "binder": actual_binder,
        "fiber": actual_fiber,
        "totals": {
            "binder_mass_kg": per_m3["binder_mass_kg_m3"] * actual_volume_m3,
            "fiber_mass_kg": per_m3["fiber_mass_kg_m3"] * actual_volume_m3,
            "total_material_mass_kg": per_m3["total_material_mass_kg_m3"] * actual_volume_m3,
            "cost": per_m3["cost_per_m3"] * actual_volume_m3,
            "energy_mj": per_m3["energy_mj_per_m3"] * actual_volume_m3,
            "co2_kg": per_m3["co2_kg_per_m3"] * actual_volume_m3,
        },
    }
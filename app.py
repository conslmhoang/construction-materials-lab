import streamlit as st
import pandas as pd
from pathlib import Path

from mix_design import (
    load_material_database,
    calculate_mix_design,
    calculate_actual_volume,
)
from mix_log import (
    LOG_EXCEL_FILE,
    read_mix_log,
    save_mix_log_from_result,
)

st.set_page_config(
    page_title="Construction Materials Lab",
    page_icon="🧱",
    layout="wide"
)

# --- CUSTOM CSS: SOFT GREEN & LIGHT BLUE THEME ---
st.markdown("""
    <style>
    /* Overall page background */
    .main {
        background-color: #f4fbf7;
    }

    /* Component containers (cards) */
    .stContainer {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e2f0e8;
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.04);
        margin-bottom: 20px;
    }

    h1, h2, h3 {
        color: #1b4332;
    }

    /* Buttons: blue-to-green gradient that brightens on hover */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        height: 45px;
        background: linear-gradient(135deg, #38bdf8 0%, #4ade80 100%);
        color: #0f172a;
        border: none;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }

    /* Hover: brighten and lift */
    .stButton>button:hover {
        background: linear-gradient(135deg, #0ea5e9 0%, #22c55e 100%);
        color: #ffffff;
        box-shadow: 0 6px 16px rgba(34, 197, 94, 0.3);
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_db():
    try:
        return load_material_database("01 Datamix.xlsx")
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return None


materials_db = load_db()

st.title("🧱 Construction Materials Lab")
st.markdown("##### *Mix-Design Calculation & Optimization Tool*")
st.caption(
    "Le Minh Hoang - MS student, Architecture and Civil Engineering, Chonnam National University  \n"
    "Construction Materials Lab, founded by Prof. Bang Yeon Lee"
)
st.divider()

if materials_db:
    material_names = list(materials_db.keys())

    non_fiber_materials = [
        name for name in material_names
        if "fiber" not in name.lower() and "fibre" not in name.lower()
    ]
    fiber_materials = [
        name for name in material_names
        if "fiber" in name.lower() or "fibre" in name.lower()
    ]

    # --- SECTION 1: MIX-DESIGN CONFIGURATION ---
    st.subheader("1. Mix-Design Configuration")

    col_binder, col_fiber = st.columns(2, gap="large")
    binder_ratios = {}
    fiber_ratios = {}

    with col_binder:
        with st.container():
            st.markdown("### 🏛️ Binder + Aggregates + Activators")

            selected_binders = st.multiselect("Select materials:", non_fiber_materials, key="binders")

            for b in selected_binders:
                mat = materials_db[b]
                ratio = st.number_input(
                    f"Proportion for **{b}** (Density: {mat.density:g} kg/m³)",
                    min_value=0.0, value=0.0, step=0.0001, format="%.4f", key=f"ratio_{b}"
                )
                if ratio > 0:
                    binder_ratios[b] = ratio

    with col_fiber:
        with st.container():
            st.markdown("### 🧵 Fiber Types")

            selected_fibers = st.multiselect("Select fiber materials:", fiber_materials, key="fibers")

            for f in selected_fibers:
                mat = materials_db[f]
                ratio = st.number_input(
                    f"Volume % for **{f}** (Density: {mat.density:g} kg/m³)",
                    min_value=0.0, value=0.0, step=0.0001, format="%.4f", key=f"ratio_{f}"
                )
                if ratio > 0:
                    fiber_ratios[f] = ratio

    # Short label identifying this mix, stored alongside the ratios in the log
    mix_note = st.text_input(
        "Mix ID (optional) - the name this mix carries in the history table",
        value="",
        placeholder="e.g. GP-FA30, M1, Trial 05",
        key="mix_note",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Calculate for 1 m³ Mix Design", type="primary"):
        try:
            mix_result = calculate_mix_design(binder_ratios, fiber_ratios, materials_db)
            st.session_state["mix_result"] = mix_result
            st.session_state["mix_inputs"] = (dict(binder_ratios), dict(fiber_ratios))
            st.success("✅ Calculation completed successfully!")

            # --- LOG: every successful run appends one row to 02 MixLog.xlsx ---
            try:
                save_mix_log_from_result(
                    binder_ratios=binder_ratios,
                    fiber_ratios_percent=fiber_ratios,
                    mix_result=mix_result,
                    include_totals=True,
                    note=mix_note,
                )
                st.caption(f"📝 Saved to `{LOG_EXCEL_FILE}`")
            except Exception as log_err:
                st.warning(f"Calculation is fine, but the log could not be saved: {log_err}")

        except Exception as e:
            st.error(f"Error: {e}")

    # --- SECTION 2: RESULTS FOR 1 m3 ---
    if "mix_result" in st.session_state:
        st.divider()
        res_1m3 = st.session_state["mix_result"]

        st.subheader("📊 Results for 1 m³")

        df_1m3 = []
        for v in res_1m3["binder"].values():
            df_1m3.append({
                "Category": "Binder / Aggregate / Activator",
                "Material": v["name"],
                "Mass (kg)": round(v["mass_kg_m3"], 1),
                "Volume (m³)": round(v["volume_m3"], 4),
                "Cost ($)": round(v["cost_per_m3"], 1),
                "Energy (MJ)": round(v["energy_mj_per_m3"], 1),
                "CO2 (kg)": round(v["co2_kg_per_m3"], 1)
            })
        for v in res_1m3["fiber"].values():
            df_1m3.append({
                "Category": "Fiber",
                "Material": v["name"],
                "Mass (kg)": round(v["mass_kg_m3"], 1),
                "Volume (m³)": round(v["volume_m3"], 4),
                "Cost ($)": round(v["cost_per_m3"], 1),
                "Energy (MJ)": round(v["energy_mj_per_m3"], 1),
                "CO2 (kg)": round(v["co2_kg_per_m3"], 1)
            })

        st.dataframe(pd.DataFrame(df_1m3), use_container_width=True, hide_index=True)

        t = res_1m3["totals_per_m3"]
        st.markdown(f"""
            📦 **TOTALS (1 m³):**
            ⚖️ **Mass:** `{t['total_material_mass_kg_m3']:.1f} kg` |
            💰 **Cost:** `${t['cost_per_m3']:.1f}` |
            ⚡ **Energy:** `{t['energy_mj_per_m3']:.1f} MJ` |
            🌱 **CO2:** `{t['co2_kg_per_m3']:.1f} kg`
        """)

        # --- SECTION 3: ACTUAL BATCH VOLUME ---
        st.divider()
        st.subheader("2. Actual Batch Volume Calculation")

        col_vol, col_btn = st.columns([1, 2], gap="medium")
        with col_vol:
            actual_vol = st.number_input("Enter target volume (m³)", min_value=0.001, value=1.000, step=0.001, format="%.4f")

        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            calculate_actual = st.button("📦 Compute Actual Batch", type="secondary")

        if calculate_actual:
            try:
                actual_res = calculate_actual_volume(res_1m3, actual_vol)

                st.markdown(f"### 📋 Batch Breakdown ({actual_vol} m³)")
                df_actual = []
                for v in actual_res["binder"].values():
                    df_actual.append({
                        "Category": "Binder / Aggregate / Activator",
                        "Material": v["name"],
                        "Mass (kg)": round(v["mass_kg"], 1),
                        "Volume (m³)": round(v["volume_m3"], 4),
                        "Cost ($)": round(v["cost"], 1),
                        "Energy (MJ)": round(v["energy_mj"], 1),
                        "CO2 (kg)": round(v["co2_kg"], 1)
                    })
                for v in actual_res["fiber"].values():
                    df_actual.append({
                        "Category": "Fiber",
                        "Material": v["name"],
                        "Mass (kg)": round(v["mass_kg"], 1),
                        "Volume (m³)": round(v["volume_m3"], 4),
                        "Cost ($)": round(v["cost"], 1),
                        "Energy (MJ)": round(v["energy_mj"], 1),
                        "CO2 (kg)": round(v["co2_kg"], 1)
                    })

                st.dataframe(pd.DataFrame(df_actual), use_container_width=True, hide_index=True)

                t_act = actual_res["totals"]
                st.success(f"""
                    🎯 **BATCH TOTALS ({actual_vol} m³):**
                    ⚖️ **Mass:** `{t_act['total_material_mass_kg']:.1f} kg` |
                    💰 **Cost:** `${t_act['cost']:.1f}` |
                    ⚡ **Energy:** `{t_act['energy_mj']:.1f} MJ` |
                    🌱 **CO2:** `{t_act['co2_kg']:.1f} kg`
                """)

                # Log a second row recording the actual batch volume
                binder_in, fiber_in = st.session_state.get("mix_inputs", ({}, {}))
                try:
                    save_mix_log_from_result(
                        binder_ratios=binder_in,
                        fiber_ratios_percent=fiber_in,
                        mix_result=res_1m3,
                        actual_volume_m3=actual_vol,
                        include_totals=True,
                        note=st.session_state.get("mix_note", ""),
                    )
                    st.caption(f"📝 Batch saved to `{LOG_EXCEL_FILE}`")
                except Exception as log_err:
                    st.warning(f"Batch computed, but the log could not be saved: {log_err}")

            except Exception as e:
                st.error(f"Error: {e}")

    # --- SECTION 4: MIX DESIGN HISTORY (LOG) ---
    st.divider()
    st.subheader("3. Mix Design History")
    st.caption(
        "Every successful calculation is appended as one row: timestamp + the ratios you entered. "
        "On Streamlit Cloud the file is wiped whenever the app restarts — download it to keep your data."
    )

    log_df = read_mix_log()
    if log_df.empty:
        st.info("No runs logged yet. Run a calculation to create the first row.")
    else:
        st.dataframe(log_df.iloc[::-1], use_container_width=True, hide_index=True)

        col_dl1, col_dl2, col_dl3 = st.columns([1, 1, 2], gap="small")

        log_path = Path(LOG_EXCEL_FILE)
        if log_path.exists():
            with col_dl1:
                st.download_button(
                    "⬇️ Download Excel",
                    data=log_path.read_bytes(),
                    file_name=LOG_EXCEL_FILE,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

        with col_dl2:
            st.download_button(
                "⬇️ Download CSV",
                data=log_df.to_csv(index=False).encode("utf-8-sig"),
                file_name="MixLog.csv",
                mime="text/csv",
            )

        with col_dl3:
            if st.button("🗑️ Clear log", type="secondary"):
                if log_path.exists():
                    log_path.unlink()
                st.rerun()

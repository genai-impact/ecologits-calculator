import streamlit as st
from src.utils import (
    format_energy_eq_electric_vehicle,
    format_energy_eq_electricity_consumption_ireland,
    format_energy_eq_electricity_production,
    format_energy_eq_physical_activity,
    format_gwp_eq_airplane_paris_nyc,
    format_gwp_eq_streaming,
    PhysicalActivity,
    EnergyProduction,
)

############################################################################################################


def get_impacts(model, active_params, total_params, mix_ghg, mix_adpe, mix_pe):
    return 1


############################################################################################################


def display_impacts(impacts):
    st.divider()

    col_energy, col_ghg, col_adpe, col_pe, col_water = st.columns(5)

    with col_energy:
        st.markdown('<h4 align="center">⚡️ Energy</h4>', unsafe_allow_html=True)
        st.latex(
            f"\Large {impacts.energy.magnitude:.3g} \ \large {impacts.energy.units}"
        )
        st.markdown(
            '<p align="center"><i>Evaluates the electricity consumption<i></p>',
            unsafe_allow_html=True,
        )

    with col_ghg:
        st.markdown('<h4 align="center">🌍️ GHG Emissions</h4>', unsafe_allow_html=True)
        st.latex(f"\Large {impacts.gwp.magnitude:.3g} \ \large {impacts.gwp.units}")
        st.markdown(
            '<p align="center"><i>Evaluates the effect on global warming<i></p>',
            unsafe_allow_html=True,
        )

    with col_adpe:
        st.markdown(
            '<h4 align="center">🪨 Abiotic Resources</h4>', unsafe_allow_html=True
        )
        st.latex(f"\Large {impacts.adpe.magnitude:.3g} \ \large {impacts.adpe.units}")
        st.markdown(
            '<p align="center"><i>Evaluates the use of metals and minerals<i></p>',
            unsafe_allow_html=True,
        )

    with col_pe:
        st.markdown('<h4 align="center">⛽️ Primary Energy</h4>', unsafe_allow_html=True)
        st.latex(f"\Large {impacts.pe.magnitude:.3g} \ \large {impacts.pe.units}")
        st.markdown(
            '<p align="center"><i>Evaluates the use of energy resources<i></p>',
            unsafe_allow_html=True,
        )

    with col_water:
        st.markdown('<h4 align="center">🚰 Water</h4>', unsafe_allow_html=True)
        st.latex("\Large Upcoming...")
        st.markdown(
            '<p align="center"><i>Evaluates the use of water<i></p>',
            unsafe_allow_html=True,
        )


############################################################################################################


def display_equivalent(impacts):
    st.divider()

    ev_eq = format_energy_eq_electric_vehicle(impacts.energy)

    streaming_eq = format_gwp_eq_streaming(impacts.gwp)

    col1, col2, col3 = st.columns(3)

    with col1:
        physical_activity, distance = format_energy_eq_physical_activity(impacts.energy)
        if physical_activity == PhysicalActivity.WALKING:
            physical_activity = "🚶 " + physical_activity.capitalize()
        if physical_activity == PhysicalActivity.RUNNING:
            physical_activity = "🏃 " + physical_activity.capitalize()

        st.markdown(
            f'<h4 align="center">{physical_activity}</h4>', unsafe_allow_html=True
        )
        st.latex(f"\Large {distance.magnitude:.3g} \ \large {distance.units}")
        st.markdown(
            '<p align="center"><i>Based on energy consumption<i></p>',
            unsafe_allow_html=True,
        )

    with col2:
        ev_eq = format_energy_eq_electric_vehicle(impacts.energy)
        st.markdown(
            '<h4 align="center">🔋 Electric Vehicle</h4>', unsafe_allow_html=True
        )
        st.latex(f"\Large {ev_eq.magnitude:.3g} \ \large {ev_eq.units}")
        st.markdown(
            '<p align="center"><i>Based on energy consumption<i></p>',
            unsafe_allow_html=True,
        )

    with col3:
        streaming_eq = format_gwp_eq_streaming(impacts.gwp)
        st.markdown('<h4 align="center">⏯️ Streaming</h4>', unsafe_allow_html=True)
        st.latex(f"\Large {streaming_eq.magnitude:.3g} \ \large {streaming_eq.units}")
        st.markdown(
            '<p align="center"><i>Based on GHG emissions<i></p>',
            unsafe_allow_html=True,
        )

    st.divider()

    st.markdown(
        '<h3 align="center">What if 1% of the planet does this request everyday for 1 year ?</h3>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p align="center">If this use case is largely deployed around the world, the equivalent impacts would be the impacts of this request x 1% of 8 billion people x 365 days in a year.</p>',
        unsafe_allow_html=True,
    )

    col4, col5, col6 = st.columns(3)

    with col4:
        electricity_production, count = format_energy_eq_electricity_production(
            impacts.energy
        )
        if electricity_production == EnergyProduction.NUCLEAR:
            emoji = "☢️"
            name = "Nuclear power plants"
        if electricity_production == EnergyProduction.WIND:
            emoji = "💨️ "
            name = "Wind turbines"
        st.markdown(
            f'<h4 align="center">{emoji} {count.magnitude:.0f} {name} (yearly)</h4>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p align="center"><i>Based on energy consumption<i></p>',
            unsafe_allow_html=True,
        )

    with col5:
        ireland_count = format_energy_eq_electricity_consumption_ireland(impacts.energy)
        st.markdown(
            f'<h4 align="center">🇮🇪 {ireland_count.magnitude:.3f} x Ireland <span style="font-size: 12px">(yearly ⚡️ cons.)</span></h2></h4>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p align="center"><i>Based on energy consumption<i></p>',
            unsafe_allow_html=True,
        )

    with col6:
        paris_nyc_airplane = format_gwp_eq_airplane_paris_nyc(impacts.gwp)
        st.markdown(
            f'<h4 align="center">✈️ {round(paris_nyc_airplane.magnitude):,} Paris ↔ NYC</h4>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p align="center"><i>Based on GHG emissions<i></p>',
            unsafe_allow_html=True,
        )

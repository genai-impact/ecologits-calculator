import streamlit as st
from ecologits.impacts.llm import compute_llm_impacts
from ecologits.tracers.utils import DATACENTER_PUE, DATACENTER_WUE

from src.utils import format_impacts, average_range_impacts, range_percent_impact_one_sided
from src.impacts import display_impacts
from src.electricity_mix import (
    COUNTRY_CODES,
    find_electricity_mix,
    dataframe_electricity_mix,
)
from src.models import load_models
from src.constants import PROMPTS

import plotly.express as px


def reset_model():
    model = "CUSTOM"


def expert_mode():
    st.markdown("### 🤓 Expert mode")

    with st.container(border=True):
        ########## Model info ##########

        col1, col2, col3 = st.columns(3)

        df = load_models(filter_main=True)

        with col1:
            provider_exp = st.selectbox(
                label="Provider",
                options=[x for x in df["provider_clean"].unique()],
                index=7,
                key=1,
            )

        with col2:
            model_exp = st.selectbox(
                label="Model",
                options=[
                    x
                    for x in df["name_clean"].unique()
                    if x
                    in df[df["provider_clean"] == provider_exp]["name_clean"].unique()
                ],
                key=2,
            )

        with col3:
            output_tokens_exp = st.selectbox(
                label="Example prompt", options=[x[0] for x in PROMPTS], key=3
            )

        df_filtered = df[
            (df["provider_clean"] == provider_exp) & (df["name_clean"] == model_exp)
        ]

        try:
            total_params = int(df_filtered["total_parameters"].iloc[0])
        except:
            total_params = int(
                (
                    df_filtered["total_parameters"].values[0]["min"]
                    + df_filtered["total_parameters"].values[0]["max"]
                )
                / 2
            )

        try:
            active_params = int(df_filtered["active_parameters"].iloc[0])
        except:
            active_params = int(
                (
                    df_filtered["active_parameters"].values[0]["min"]
                    + df_filtered["active_parameters"].values[0]["max"]
                )
                / 2
            )

        ########## Model parameters ##########

        col11, col22, col33 = st.columns(3)

        with col11:
            active_params = st.number_input(
                "Active parameters (B)", 0, None, active_params
            )

        with col22:
            total_params = st.number_input(
                "Total parameters (B)", 0, None, total_params
            )

        with col33:
            output_tokens = st.number_input(
                label="Output completion tokens",
                min_value=0,
                value=[x[1] for x in PROMPTS if x[0] == output_tokens_exp][0],
            )

        ########## Electricity mix ##########

        location = st.selectbox("Location", [x[0] for x in COUNTRY_CODES])

        col4, col5 = st.columns(2)

        with col4:
            mix_gwp = st.number_input(
                "Electricity mix - GHG emissions [kgCO2eq / kWh]",
                find_electricity_mix(
                    [x[1] for x in COUNTRY_CODES if x[0] == location][0]
                )[2],
                format="%0.6f",
            )
            # disp_ranges = st.toggle('Display impact ranges', False)
        with col5:
            mix_adpe = st.number_input(
                "Electricity mix - Abiotic resources [kgSbeq / kWh]",
                find_electricity_mix(
                    [x[1] for x in COUNTRY_CODES if x[0] == location][0]
                )[0],
                format="%0.13f",
            )

        col6, col7 = st.columns(2)    
        with col6:
            mix_pe = st.number_input(
                "Electricity mix - Primary energy [MJ / kWh]",
                find_electricity_mix(
                    [x[1] for x in COUNTRY_CODES if x[0] == location][0]
                )[1],
                format="%0.3f",
            )
        with col7:
            mix_wue = st.number_input(
                "Electricity mix - Off-site Water Usage Efficiency [L / kWh]",
                find_electricity_mix(
                    [x[1] for x in COUNTRY_CODES if x[0] == location][0]
                )[4],
                format="%0.3f",
            )

    datacenter_pue = DATACENTER_PUE[provider_exp.lower()]
    datacenter_wue = DATACENTER_WUE[provider_exp.lower()]

    impacts = compute_llm_impacts(
        model_active_parameter_count=active_params,
        model_total_parameter_count=total_params,
        output_token_count=output_tokens,
        request_latency=100000,
        if_electricity_mix_gwp=mix_gwp,
        if_electricity_mix_adpe=mix_adpe,
        if_electricity_mix_pe=mix_pe,
        if_electricity_mix_wue=mix_wue,
        datacenter_pue=datacenter_pue,
        datacenter_wue=datacenter_wue,
    )

    range_percent_impact_one_sided_calculated = range_percent_impact_one_sided(impacts)

    impacts, usage, embodied = format_impacts(impacts)

    with st.container(border=True):
        st.markdown(
            '<h3 align="center">Environmental Impacts</h2>', unsafe_allow_html=True
        )

        display_impacts(impacts, range_percent_impact_one_sided_calculated)

    with st.expander("⚖️ Usage vs Embodied"):
        st.markdown(
            '<h3 align="center">Embodied vs Usage comparison</h2>',
            unsafe_allow_html=True,
        )

        st.markdown(
            "The usage impacts account for the electricity consumption of the model while the embodied impacts account for resource extraction (e.g., minerals and metals), manufacturing, and transportation of the hardware."
        )


        col_ghg_comparison, col_adpe_comparison, col_pe_comparison, col_wcf_comparison = st.columns(4)

        with col_ghg_comparison:
            fig_gwp = px.pie(
                values=[
                    average_range_impacts(usage.gwp.value),
                    average_range_impacts(embodied.gwp.value),
                ],
                names=["usage", "embodied"],
                title="GHG Emissions",
                color_discrete_sequence=["#00BF63", "#0B3B36"],
                width=100,
            )
            fig_gwp.update_layout(
                showlegend=False, 
                title_x=0.1)

            st.plotly_chart(fig_gwp)

        with col_adpe_comparison:
            fig_adpe = px.pie(
                values=[
                    average_range_impacts(usage.adpe.value),
                    average_range_impacts(embodied.adpe.value),
                ],
                names=["usage", "embodied"],
                title="Abiotic Depletion",
                color_discrete_sequence=["#0B3B36", "#00BF63"],
                width=100,
            )
            fig_adpe.update_layout(showlegend=False, title_x=0.05)
            st.plotly_chart(fig_adpe)

        with col_pe_comparison:
            fig_pe = px.pie(
                values=[
                    average_range_impacts(usage.pe.value),
                    average_range_impacts(embodied.pe.value),
                ],
                names=["usage", "embodied"],
                title="Primary Energy",
                color_discrete_sequence=["#00BF63", "#0B3B36"],
                width=100,
            )
            fig_pe.update_layout(showlegend=False, title_x=0.05)

            st.plotly_chart(fig_pe)

        with col_wcf_comparison:
            fig_wcf = px.pie(
                values = [
                    average_range_impacts(usage.wcf.value), 
                    average_range_impacts(embodied.wcf.value)],
                names = ['usage', 'embodied'],
                title='Water Consumption Footprint',
                color_discrete_sequence=["#00BF63", "#0B3B36"],
                width = 100
                )
            fig_wcf.update_layout(
                showlegend=False, 
                title={'text': 'Water Consumption<br>Footprint', 'x': 0.5, 'xanchor': 'center'}
                )

            st.plotly_chart(fig_wcf)

    with st.expander("🌍️ Location impact"):
        st.markdown(
            '<h4 align="center">How can location impact the footprint ?</h4>',
            unsafe_allow_html=True,
        )

        countries_to_compare = st.multiselect(
            label="Countries to compare",
            options=[x[0] for x in COUNTRY_CODES],
            default=["🇫🇷 France", "🇺🇸 United States", "🇨🇳 China"],
        )


        try:
            df_comp = dataframe_electricity_mix(countries_to_compare)

            impact_type = st.selectbox(
                label="Select an impact type to compare",
                options=[x for x in df_comp.columns if x != "country"],
                index=1,
            )

            df_comp.sort_values(by=impact_type, inplace=True)

            fig_2 = px.bar(
                df_comp,
                x=df_comp.index,
                y=impact_type,
                text=impact_type,
                color=impact_type,
            )

            st.plotly_chart(fig_2)

        except:
            st.warning("Can't display chart with no values.")

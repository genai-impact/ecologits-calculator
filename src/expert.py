import pandas as pd
import streamlit as st
from ecologits.electricity_mix_repository import electricity_mixes
from ecologits.impacts.llm import compute_llm_impacts

from src.latency_estimator import latency_estimator
from src.utils import format_impacts
from src.impacts import display_impacts
from src.electricity_mix import COUNTRY_CODES, format_electricity_mix_criterion, format_country_name
from src.models import load_models
from src.constants import PROMPTS
from src.constants import PROMPTS

import plotly.express as px


def expert_mode():
    st.markdown("### 🤓 Expert mode")

    with st.container(border=True):
        st.markdown("###### Configure the model")

        ########## Model info ##########

        provider_col, model_col = st.columns(2)

        df = load_models(filter_main=True)

        with provider_col:
            providers_clean = [x for x in df["provider_clean"].unique()]
            provider_exp = st.selectbox(
                label="Provider",
                options=providers_clean,
                index=providers_clean.index("OpenAI"),
                key=1,
            )

        with model_col:
            models_clean = [
                x
                for x in df["name_clean"].unique()
                if x in df[df["provider_clean"] == provider_exp]["name_clean"].unique()
            ]
            model_exp = st.selectbox(
                label="Model",
                options=models_clean,
                key=2,
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

        provider_raw = df_filtered["provider"].values[0]
        model_name_raw = df_filtered["name"].values[0]
        tps_raw = latency_estimator.get_throughput(provider_raw, model_name_raw)

        ########## Model parameters ##########

        active_params_col, total_params_col, throughput_col = st.columns(3)

        with active_params_col:
            active_params = st.number_input("Active parameters (B)", 0, None, active_params)

        with total_params_col:
            total_params = st.number_input("Total parameters (B)", 0, None, total_params)

        with throughput_col:
            throughput = st.number_input("Average TPS", 1.0, None, tps_raw)


    with st.container(border=True):
        st.markdown("###### Configure the prompt")

        prompt_col, token_col = st.columns(2)

        with prompt_col:
            output_tokens_exp = st.selectbox(
                label="Example prompt", options=[x[0] for x in PROMPTS], key=3
            )

        with token_col:
            output_tokens = st.number_input(
                label="Output completion tokens",
                min_value=0,
                value=[x[1] for x in PROMPTS if x[0] == output_tokens_exp][0],
            )


    with st.container(border=True):
        st.markdown("###### Configure the data center")

        dc_pue_col, dc_wue_col, dc_location_col = st.columns(3)
        with dc_pue_col:
            datacenter_pue = st.number_input(
                label="Data center PUE",
                value=1.2,
                min_value=1.0
            )
        with dc_wue_col:
            datacenter_wue = st.number_input(
                label="Data center WUE [L / kWh]",
                value=0.6,
                min_value=0.
            )
        with dc_location_col:
            dc_location = st.selectbox(
                label="Data center location",
                options=[c[1] for c in COUNTRY_CODES],
                format_func=format_country_name,
                index=0
            )

        em_gwp_col, em_adpe_col, em_pe_col, em_wue_col = st.columns(4)
        electricity_mix = electricity_mixes.find_electricity_mix(dc_location)
        with em_gwp_col:
            em_gwp = st.number_input(
                label="GHG emissions [kgCO2eq / kWh]",
                value=electricity_mix.gwp,
                format="%0.6f",
            )
        with em_adpe_col:
            em_adpe = st.number_input(
                label="Abiotic resources [kgSbeq / kWh]",
                value=electricity_mix.adpe,
                format="%0.13f",
            )
        with em_pe_col:
            em_pe = st.number_input(
                label="Primary energy [MJ / kWh]",
                value=electricity_mix.pe,
                format="%0.3f",
            )
        with em_wue_col:
            em_wue = st.number_input(
                label="Water consumption [L / kWh]",
                value=electricity_mix.wue,
                format="%0.3f",
            )

    estimated_latency = latency_estimator.estimate(
        provider=provider_raw,
        model_name=model_name_raw,
        output_tokens=output_tokens,
        throughput=throughput
    )

    impacts = compute_llm_impacts(
        model_active_parameter_count=active_params,
        model_total_parameter_count=total_params,
        output_token_count=output_tokens,
        request_latency=estimated_latency,
        if_electricity_mix_gwp=em_gwp,
        if_electricity_mix_adpe=em_adpe,
        if_electricity_mix_pe=em_pe,
        if_electricity_mix_wue=em_wue,
        datacenter_pue=datacenter_pue,
        datacenter_wue=datacenter_wue
    )

    impacts, usage, embodied = format_impacts(impacts)

    with st.container(border=True):
        st.markdown(
            '<h3 align="center">Environmental Impacts</h2>', unsafe_allow_html=True
        )

        display_impacts(impacts)

    with st.expander("⚖️ Usage vs Embodied"):
        st.markdown(
            '<h3 align="center">Embodied vs Usage comparison</h2>',
            unsafe_allow_html=True,
        )

        st.markdown(
            "The usage impacts account for the electricity consumption of the model while the embodied impacts account for resource extraction (e.g., minerals and metals), manufacturing, and transportation of the hardware."
        )

        col_ghg_comparison, col_adpe_comparison, col_pe_comparison = st.columns(3)

        with col_ghg_comparison:
            fig_gwp = px.pie(
                values=[
                    usage.gwp.value if isinstance(usage.gwp.value, float) else usage.gwp.value.mean,
                    embodied.gwp.value if isinstance(embodied.gwp.value, float) else embodied.gwp.value.mean,
                ],
                names=["usage", "embodied"],
                title="GHG emissions",
                color_discrete_sequence=["#00BF63", "#0B3B36"],
                width=100,
            )
            fig_gwp.update_layout(showlegend=False, title_x=0.5)

            st.plotly_chart(fig_gwp)

        with col_adpe_comparison:
            fig_adpe = px.pie(
                values=[
                    usage.adpe.value if isinstance(usage.adpe.value, float) else usage.adpe.value.mean,
                    embodied.adpe.value if isinstance(embodied.adpe.value, float) else embodied.adpe.value.mean,
                ],
                names=["usage", "embodied"],
                title="Abiotic depletion",
                color_discrete_sequence=["#0B3B36", "#00BF63"],
                width=100,
            )
            fig_adpe.update_layout(showlegend=False, title_x=0.5)

            st.plotly_chart(fig_adpe)

        with col_pe_comparison:
            fig_pe = px.pie(
                values=[
                    usage.pe.value if isinstance(usage.pe.value, float) else usage.pe.value.mean,
                    embodied.pe.value if isinstance(embodied.pe.value, float) else embodied.pe.value.mean,
                ],
                names=["usage", "embodied"],
                title="Primary energy",
                color_discrete_sequence=["#00BF63", "#0B3B36"],
                width=100,
            )
            fig_pe.update_layout(showlegend=False, title_x=0.5)

            st.plotly_chart(fig_pe)

    with st.expander("🌍️ Location impact"):
        st.markdown(
            '<h4 align="center">How can location impact the footprint ?</h4>',
            unsafe_allow_html=True,
        )

        countries_to_compare = st.multiselect(
            label="Countries to compare",
            options=[c[1] for c in COUNTRY_CODES],
            format_func=format_country_name,
            default=["FRA", "USA", "CHN"],
        )

        try:
            impact_type = st.selectbox(
                label="Select an impact type to compare",
                options=["gwp", "adpe", "pe", "wue"],
                format_func=format_electricity_mix_criterion,
                index=0,
            )

            df_comp = pd.DataFrame([em for em in electricity_mixes.list_electricity_mixes() if em.zone in countries_to_compare])
            df_comp = df_comp.sort_values(by=impact_type, ascending=True)

            fig_2 = px.bar(
                df_comp,
                x=df_comp.zone.apply(format_country_name),
                y=impact_type,
                text=impact_type,
                color=impact_type,
            )

            st.plotly_chart(fig_2)

        except:
            st.warning("Can't display chart with no values.")

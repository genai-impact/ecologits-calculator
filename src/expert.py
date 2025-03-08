import streamlit as st
import pandas as pd
from ecologits.impacts.llm import compute_llm_impacts

from src.utils import format_impacts, average_range_impacts, format_impacts_expert, model_active_params_fn, model_total_params_fn
from src.impacts import display_impacts
#from src.constants import PROVIDERS, MODELS
from src.electricity_mix import COUNTRY_CODES, find_electricity_mix, dataframe_electricity_mix
from ecologits.model_repository import models

import plotly.express as px

def reset_model():
    model = 'CUSTOM'

def expert_mode():

    st.markdown("### 🤓 Expert mode")

    with st.container(border = True):

        ########## Model info ##########

        # col1, col2, col3 = st.columns(3)

        # with col1:
        #     provider = st.selectbox(label = 'Provider expert',
        #                             options = [x[0] for x in PROVIDERS],
        #                             index = 0)
        #     provider = [x[1] for x in PROVIDERS if x[0] == provider][0]
        #     if 'huggingface_hub' in provider:
        #         provider = 'huggingface_hub'
        
        # with col2:
        #     model = st.selectbox('Model expert', [x[0] for x in MODELS if provider in x[1]])
        #     model = [x[1] for x in MODELS if x[0] == model][0].split('/', 1)[1]

        ########## Model parameters ##########   

        col11, col22, col33 = st.columns(3)

        with col11:
            # st.write(provider, model)
            # st.write(models.find_model(provider, model))
            # st.write(model_active_params_fn(provider, model, 45))
            active_params = st.number_input('Active parameters (B)', 0, None, 45)

        with col22:
            total_params = st.number_input('Total parameters (B)', 0, None, 45)

        with col33:
            output_tokens = st.number_input('Output completion tokens', 100)

        ########## Electricity mix ##########

        location = st.selectbox('Location', [x[0] for x in COUNTRY_CODES])

        col4, col5, col6 = st.columns(3)

        with col4:
            mix_gwp = st.number_input('Electricity mix - GHG emissions [kgCO2eq / kWh]', find_electricity_mix([x[1] for x in COUNTRY_CODES if x[0] ==location][0])[2], format="%0.6f")
            #disp_ranges = st.toggle('Display impact ranges', False)
        with col5:
            mix_adpe = st.number_input('Electricity mix - Abiotic resources [kgSbeq / kWh]', find_electricity_mix([x[1] for x in COUNTRY_CODES if x[0] ==location][0])[0], format="%0.13f")
        with col6:
            mix_pe = st.number_input('Electricity mix - Primary energy [MJ / kWh]', find_electricity_mix([x[1] for x in COUNTRY_CODES if x[0] ==location][0])[1], format="%0.3f")

    impacts = compute_llm_impacts(model_active_parameter_count=active_params,
                model_total_parameter_count=total_params,
                output_token_count=output_tokens,
                request_latency=100000,
                if_electricity_mix_gwp=mix_gwp,
                if_electricity_mix_adpe=mix_adpe,
                if_electricity_mix_pe=mix_pe
            )
    
    impacts, usage, embodied = format_impacts(impacts)
    
    with st.container(border = True):

        st.markdown('<h3 align="center">Environmental Impacts</h2>', unsafe_allow_html = True)

        display_impacts(impacts)

    with st.expander('⚖️ Usage vs Embodied'):

        st.markdown('<h3 align="center">Embodied vs Usage comparison</h2>', unsafe_allow_html = True)

        st.markdown('The usage impacts account for the electricity consumption of the model while the embodied impacts account for resource extraction (e.g., minerals and metals), manufacturing, and transportation of the hardware.')
        
        col_ghg_comparison, col_adpe_comparison, col_pe_comparison = st.columns(3)

        with col_ghg_comparison:
            fig_gwp = px.pie(
                values = [average_range_impacts(usage.gwp.value), average_range_impacts(embodied.gwp.value)],
                names = ['usage', 'embodied'],
                title = 'GHG emissions',
                color_discrete_sequence=["#636EFA", "#00CC96"],
                width = 100
                )
            fig_gwp.update_layout(showlegend=False, title_x=0.5)

            st.plotly_chart(fig_gwp)

        with col_adpe_comparison:
            fig_adpe = px.pie(
                values = [average_range_impacts(usage.adpe.value), average_range_impacts(embodied.adpe.value)],
                names = ['usage', 'embodied'],
                title = 'Abiotic depletion',
                color_discrete_sequence=["#00CC96","#636EFA"],
                width = 100)
            fig_adpe.update_layout(
                showlegend=True,
                legend=dict(yanchor="bottom", x = 0.35, y = -0.1),
                title_x=0.5)
            
            st.plotly_chart(fig_adpe)

        with col_pe_comparison:
            fig_pe = px.pie(
                values = [average_range_impacts(usage.pe.value), average_range_impacts(embodied.pe.value)],
                names = ['usage', 'embodied'],
                title = 'Primary energy',
                color_discrete_sequence=["#636EFA", "#00CC96"],
                width = 100)
            fig_pe.update_layout(showlegend=False, title_x=0.5)

            st.plotly_chart(fig_pe)

    with st.expander('🌍️ Location impact'):

        st.markdown('<h4 align="center">How can location impact the footprint ?</h4>', unsafe_allow_html = True)

        countries_to_compare = st.multiselect(
            label = 'Countries to compare',
            options = [x[0] for x in COUNTRY_CODES],
            default = ["🇫🇷 France", "🇺🇸 United States", "🇨🇳 China"]
            )

        try:

            df = dataframe_electricity_mix(countries_to_compare)

            impact_type = st.selectbox(
                label='Select an impact type to compare',
                options=[x for x in df.columns if x!='country'],
                index=1)

            df.sort_values(by = impact_type, inplace = True)

            fig_2 = px.bar(df, x = df.index, y = impact_type, text = impact_type, color = impact_type)
            st.plotly_chart(fig_2)

        except:

            st.warning("Can't display chart with no values.")
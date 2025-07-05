import streamlit as st
from ecologits.impacts.llm import compute_llm_impacts

from src.utils import format_impacts, average_range_impacts
from src.impacts import display_impacts
from src.electricity_mix import COUNTRY_CODES, find_electricity_mix, dataframe_electricity_mix
from src.models import load_models
from src.constants import PROMPTS

import plotly.express as px

def reset_model():
    model = 'CUSTOM'

def expert_mode():

    st.markdown("### 🤓 Expert mode")

    with st.container(border = True):

        ########## Model info ##########

        col1, col2, col3 = st.columns(3)
        
        df = load_models(filter_main=True)

        with col1:
            provider_exp = st.selectbox(
                label = 'Provider',
                options = [x for x in df['provider_clean'].unique()],
                index = 7,
                key = 1
            )

        with col2:
            model_exp = st.selectbox(
                label = 'Model',
                options = [x for x in df['name_clean'].unique() if x in df[df['provider_clean'] == provider_exp]['name_clean'].unique()],
                key = 2
            )

        with col3:
            output_tokens_exp = st.selectbox(
                label = 'Example prompt',
                options = [x[0] for x in PROMPTS],
                key = 3
            )
        
        df_filtered = df[(df['provider_clean'] == provider_exp) & (df['name_clean'] == model_exp)]

        try:
            total_params = int(df_filtered['total_parameters'].iloc[0])
        except:
            total_params = int((df_filtered['total_parameters'].values[0]['min'] + df_filtered['total_parameters'].values[0]['max'])/2)
            
        try:
            active_params = int(df_filtered['active_parameters'].iloc[0])
        except:
            active_params = int((df_filtered['active_parameters'].values[0]['min'] + df_filtered['active_parameters'].values[0]['max'])/2)

        ########## Model parameters ##########   

        col11, col22, col33 = st.columns(3)

        with col11:
            active_params = st.number_input('Active parameters (B)', 0, None, active_params)

        with col22:
            total_params = st.number_input('Total parameters (B)', 0, None, total_params)

        with col33:
            output_tokens = st.number_input(
                label = 'Output completion tokens',
                min_value = 0,
                value = [x[1] for x in PROMPTS if x[0] == output_tokens_exp][0]
            )

        ########## Electricity mix ##########

        location = st.selectbox('Location', [x[0] for x in COUNTRY_CODES])

        col4, col5, col6 = st.columns(3)

        with col4:
            try:
                mix_gwp = st.number_input('Electricity mix - GHG emissions [kgCO2eq / kWh]', float(find_electricity_mix([x[1] for x in COUNTRY_CODES if x[0] ==location][0])[2]), format="%0.6f")
            #disp_ranges = st.toggle('Display impact ranges', False)

            except: 
                mix_gwp = st.number_input('Electricity mix - GHG emissions [kgCO2eq / kWh]', float(find_electricity_mix(["WOR"][0])[2]), format="%0.6f")
                st.warning(f"Lacking data on {location}, showing global average data.")

        with col5:
            try:
                mix_adpe = st.number_input('Electricity mix - Abiotic resources [kgSbeq / kWh]', float(find_electricity_mix([x[1] for x in COUNTRY_CODES if x[0] ==location][0])[0]), format="%0.13f")
            except:
                mix_adpe = st.number_input('Electricity mix - Abiotic resources [kgSbeq / kWh]', float(find_electricity_mix(["WOR"][0])[0]), format="%0.13f")
                st.warning(f"Lacking data on {location}, showing global average data.")

        with col6:
            try: 
                mix_pe = st.number_input('Electricity mix - Primary energy [MJ / kWh]', float(find_electricity_mix([x[1] for x in COUNTRY_CODES if x[0] ==location][0])[1]), format="%0.3f")
            except: 
                mix_pe = st.number_input('Electricity mix - Primary energy [MJ / kWh]', float(find_electricity_mix(["WOR"][0])[1]), format="%0.3f")
                st.warning(f"Lacking data on {location}, showing global average data.")


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

        display_impacts(impacts, provider_exp, location)

    with st.expander('⚖️ Usage vs Embodied'):

        st.markdown('<h3 align="center">Embodied vs Usage comparison</h2>', unsafe_allow_html = True)

        st.markdown('The usage impacts account for the electricity consumption of the model while the embodied impacts account for resource extraction (e.g., minerals and metals), manufacturing, and transportation of the hardware.')
        
        col_ghg_comparison, col_adpe_comparison, col_pe_comparison = st.columns(3)
        
        with col_ghg_comparison:

            fig_gwp = px.pie(
            values = [average_range_impacts(usage.gwp.value), average_range_impacts(embodied.gwp.value)],
            names = ['usage', 'embodied'],
            title = 'GHG emissions',
            color_discrete_sequence=["#00BF63", "#0B3B36"],
            width = 400
            )
            fig_gwp.update_layout(
                showlegend=False, 
                title_x=0.25)

            st.plotly_chart(fig_gwp)

        with col_adpe_comparison:
            fig_adpe = px.pie(
                values = [average_range_impacts(usage.adpe.value), average_range_impacts(embodied.adpe.value)],
                names = ['usage', 'embodied'],
                title = 'Abiotic depletion',
                color_discrete_sequence=["#0B3B36","#00BF63"],
                width = 400
                )
            fig_adpe.update_layout(
                showlegend=False,
                title_x=0.25)
            
            st.plotly_chart(fig_adpe)

        with col_pe_comparison:
            fig_pe = px.pie(
                values = [average_range_impacts(usage.pe.value), average_range_impacts(embodied.pe.value)],
                names = ['usage', 'embodied'],
                title = 'Primary energy',
                color_discrete_sequence=["#00BF63", "#0B3B36"],
                width = 400
                )
            fig_pe.update_layout(
                showlegend=False, 
                title_x=0.25)

            st.plotly_chart(fig_pe)

    with st.expander('🌍️ Location impact'):

        st.markdown('<h4 align="center">How can location impact the footprint ?</h4>', unsafe_allow_html = True)

        countries_to_compare = st.multiselect(
            label = 'Countries to compare',
            options = [x[0] for x in COUNTRY_CODES],
            default = ["🇫🇷 France", "🇺🇸 United States", "🇨🇳 China"]
            )

        try:

            df_comp = dataframe_electricity_mix(countries_to_compare)


            impact_metrices = [
                "Abiotic Depletion Potential for Elements (Kilograms of antimony equivalent)",
                "Primary energy demand (Megajoules)",
                "Global Warming Potential (Kilograms of CO2 equivalent)",
                "Water Withdrawal Factor (Liters/Kilowatt-hour)",
                "Water Consumption Factor (Liters/Kilowatt-hour)"
            ]

            impact_labels = {
                impact_metrices[0] : "adpe (kg eq. Sb)",
                impact_metrices[1]  : "pe (MJ)",
                impact_metrices[2]  : "gwp (kg eq. CO2)",
                impact_metrices[3] :  "water_wwf (L/kWh)",
                impact_metrices[4] : "water_wcf (L/kWh)" 
            }

            impact_type = st.selectbox(
                label='Select an impact type to compare',
                options=[x for x in impact_labels],  # les noms affichés à l'utilisateur
                index=1
            )

            impact_type_used = impact_labels[impact_type]

            df_comp.sort_values(by = impact_type_used, inplace = True)
            
            fig_2 = px.bar(
                df_comp,
                x = df_comp.index,
                y = impact_type_used,
                text = impact_type_used,
                color = impact_type_used
            )
            
            st.plotly_chart(fig_2)

            impact_explanations = {
                impact_metrices[0]:
                    "Measures the depletion of non-renewable resources (metals, minerals), expressed in kg of antimony equivalent (Sb). \
                    The enviornmental impact equates to that amount of antimony being extracted.",
                impact_metrices[1]:
                    "Total amount of primary energy used (both renewable and non-renewable), expressed in megajoules (MJ).",
                impact_metrices[2]:
                    "Potential contribution to climate change over a 100-year time horizon, expressed in kilograms of CO₂ equivalent.",
                impact_metrices[3]:
                    "Total volume of water withdrawn throughout the process, expressed in liters (L).",
                impact_metrices[4]:
                    "Volume of water actually consumed (not returned to the source), expressed in liters (L)."
            }

            st.info(impact_explanations[impact_type])

        except:

            st.warning("Can't display chart with no values.")
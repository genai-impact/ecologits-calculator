import streamlit as st

from ecologits.tracers.utils import llm_impacts
from src.impacts import get_impacts, display_impacts, display_equivalent_energy, display_equivalent_ghg, display_equivalent_wcf
from src.utils import format_impacts, range_percent_impact_one_sided
from src.content import WARNING_CLOSED_SOURCE, WARNING_MULTI_MODAL, WARNING_BOTH, HOW_TO_TEXT_COMPANY
from src.models import load_models

from src.constants import PROMPTS

def company_mode():

    st.expander("How to use this calculator?", expanded = False).markdown(HOW_TO_TEXT_COMPANY)


    st.markdown("### 👩🏻‍💻 Calculator for companies")

    with st.container(border=True):
        
        df = load_models(filter_main=True)
        
        col1, col2, col3 = st.columns(3)

        with col1:
            provider = st.selectbox(
                label = 'Provider',
                options = [x for x in df['provider_clean'].unique()],
                index = 7,
                key = 61
            ) 

        with col2:
            model = st.selectbox(
                label = 'Model',
                options = [x for x in df['name_clean'].unique() if x in df[df['provider_clean'] == provider]['name_clean'].unique()],
                key = 62
            )

        with col3:
            output_tokens = st.selectbox(
                'Example prompt', 
                [x[0] for x in PROMPTS],
                key = 63     
            )
            
        # WARNING DISPLAY
        provider_raw = df[(df['provider_clean'] == provider) & (df['name_clean'] == model)]['provider'].values[0]
        model_raw = df[(df['provider_clean'] == provider) & (df['name_clean'] == model)]['name'].values[0]

        df_filtered = df[(df['provider_clean'] == provider) & (df['name_clean'] == model)]

        if df_filtered['warning_arch'].values[0] and not df_filtered['warning_multi_modal'].values[0]:
            st.warning(WARNING_CLOSED_SOURCE)
        if df_filtered['warning_multi_modal'].values[0] and not df_filtered['warning_arch'].values[0]:
            st.warning(WARNING_MULTI_MODAL)
        if df_filtered['warning_arch'].values[0] and df_filtered['warning_multi_modal'].values[0]:
            st.warning(WARNING_BOTH)
            
        col4, col5, col6 = st.columns(3)

        with col4:
            company_size = st.number_input(
                label="Company size (in number of employees)",
                min_value=1,
                value=10,   
                step=1,
                key = 64
            ) 
        
        #TODO : lire la literature pour comprendre des chiffres en moyen pour remplisser comme defaut
        #par example, entre 400 - 800 > entreprise taille moyenne, frequence correspondant : ...
        with col5:
            use_percentage = st.number_input(
                label = 'What percentage of employees use LLM daily (in %)?',
                min_value=10,
                max_value=100,
                value=80,   
                step=10,
                key = 65
            )

        #TODO : lire la literature pour comprendre des chiffres en moyen pour remplisser comme defaut
        #par example, entre 400 - 800 > entreprise taille moyenne, frequence correspondant : ...
        with col6:
            request_frequency = st.number_input(
                label = 'How frequently do the employees use LLM (requests per day)?',
                min_value=1,
                value=20,   # valeur par défaut
                step=5,
                key = 66
            )

    company_multiplier = company_size * use_percentage/100 * request_frequency

    #try:

    impacts = llm_impacts(
                    provider=provider_raw,
                    model_name=model_raw,
                    output_token_count=[x[1] for x in PROMPTS if x[0] == output_tokens][0],
                    request_latency=100000
                )

    range_percent_impact_one_sided_calculated = range_percent_impact_one_sided(impacts)
    impacts, _, _ = format_impacts(impacts)

    display_company = True
    
    with st.container(border=True):

        st.markdown('<h3 align = "center">Environmental impacts</h3>', unsafe_allow_html=True)
        st.markdown('<p align = "center">To understand how the impacts are computed, visit the 📖 Methodology tab. ' \
        'Over the course of a day, the enviornmental impacts from the LLM usage of this company is estimated to be:</p>', unsafe_allow_html=True)
        display_impacts(impacts, range_percent_impact_one_sided_calculated, company_multiplier)
    
    with st.container(border=False):
            st.markdown('<h3 align = "center">Equivalences</h3>', unsafe_allow_html=True)
            if display_company == True:
                st.markdown('<p align = "center">The company making these requests to the LLM over a day is equivalent to the following actions:</p>', unsafe_allow_html=True)            
            else:
                st.markdown('<p align = "center">Making this request to the LLM is equivalent to the following actions:</p>', unsafe_allow_html=True)
            page = st.radio(' ', ['Energy', 'GHG', 'Water'], horizontal=True, key='company_page_radio')

        
    with st.container(border=True):                                            
        if page == 'Energy' :
            display_equivalent_energy(impacts, company_multiplier, display_company)
        elif page == 'GHG' :  
            display_equivalent_ghg(impacts, company_multiplier,display_company)    
        else :  
            display_equivalent_wcf(impacts, company_multiplier,display_company)
        
    # except Exception as e:
    #    st.error('Could not find the model in the repository. Please try another model.')
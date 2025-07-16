import streamlit as st

from ecologits.tracers.utils import llm_impacts
from src.impacts import get_impacts, display_impacts_company, display_equivalent_company
from src.utils import format_impacts
from src.content import WARNING_CLOSED_SOURCE, WARNING_MULTI_MODAL, WARNING_BOTH
from src.models import load_models

from src.constants import PROMPTS

def company_mode():

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
                value=10,   # valeur par défaut
                step=1,
                key = 64
            ) 
        
        #TODO : lire la literature pour comprendre des chiffres en moyen pour remplisser comme defaut
        #par example, entre 400 - 800 > entreprise taille moyenne, frequence correspondant : ...
        with col5:
            use_percentage = st.number_input(
                label = 'What percentage of employees use LLM daily (in %)?',
                min_value=0,
                max_value=100,
                value=75,   # valeur par défaut
                step=5,
                key = 65
            )

        #TODO : lire la literature pour comprendre des chiffres en moyen pour remplisser comme defaut
        #par example, entre 400 - 800 > entreprise taille moyenne, frequence correspondant : ...
        with col6:
            request_frequency = st.number_input(
                label = 'How frequently do the employees use LLM (times per day)?',
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

    impacts, _, _ = format_impacts(impacts)

    #down here

    
    with st.container(border=True):

        st.markdown('<h3 align = "center">Environmental impacts</h3>', unsafe_allow_html=True)
        st.markdown('<p align = "center">To understand how the environmental impacts are computed go to the 📖 Methodology tab.</p>', unsafe_allow_html=True)
        display_impacts_company(impacts, provider, company_multiplier, location="🌎 World")
    
    with st.container(border=True):
        #TODO : corriger ça 
        st.markdown('<h3 align = "center">That\'s equivalent to ...</h3>', unsafe_allow_html=True)
        st.markdown('<p align = "center">On the scale of the company, making this request to the LLM over a day is equivalent to the following actions :</p>', unsafe_allow_html=True)
        display_equivalent_company(impacts, provider, company_multiplier, location="🌎 World")
            
    #except Exception as e:
    #    st.error('Could not find the model in the repository. Please try another model.')
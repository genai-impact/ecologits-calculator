import streamlit as st

from ecologits.tracers.utils import llm_impacts
from src.impacts import get_impacts, display_impacts, display_equivalent_ghg, display_equivalent_energy
from src.utils import format_impacts
from src.content import WARNING_CLOSED_SOURCE, WARNING_MULTI_MODAL, WARNING_BOTH, HOW_TO_TEXT
from src.models import load_models

from src.constants import PROMPTS


def calculator_mode():

    st.expander("How to use this calculator?", expanded = False).markdown(HOW_TO_TEXT)

    with st.container(border=True):
        df = load_models(filter_main=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            provider = st.selectbox(
                label="Provider",
                options=[x for x in df["provider_clean"].unique()],
                index=7,
            )

        with col2:
            model = st.selectbox(
                label="Model",
                options=[
                    x
                    for x in df["name_clean"].unique()
                    if x in df[df["provider_clean"] == provider]["name_clean"].unique()
                ],
            )

        with col3:
            output_tokens = st.selectbox("Example prompt", [x[0] for x in PROMPTS])

        # WARNING DISPLAY
        provider_raw = df[
            (df["provider_clean"] == provider) & (df["name_clean"] == model)
        ]["provider"].values[0]
        model_raw = df[
            (df["provider_clean"] == provider) & (df["name_clean"] == model)
        ]["name"].values[0]

        df_filtered = df[
            (df["provider_clean"] == provider) & (df["name_clean"] == model)
        ]

        if (
            df_filtered["warning_arch"].values[0]
            and not df_filtered["warning_multi_modal"].values[0]
        ):
            st.warning(WARNING_CLOSED_SOURCE)
        if (
            df_filtered["warning_multi_modal"].values[0]
            and not df_filtered["warning_arch"].values[0]
        ):
            st.warning(WARNING_MULTI_MODAL)
        if (
            df_filtered["warning_arch"].values[0]
            and df_filtered["warning_multi_modal"].values[0]
        ):
            st.warning(WARNING_BOTH)

    try:
        impacts = llm_impacts(
            provider=provider_raw,
            model_name=model_raw,
            output_token_count=[x[1] for x in PROMPTS if x[0] == output_tokens][0],
            request_latency=100000,
        )

        impacts, _, _ = format_impacts(impacts)

        with st.container(border=True):

            st.markdown('<h3 align = "center">Environmental impacts</h3>', unsafe_allow_html=True)
            #st.markdown('<p align = "center">To understand how the environmental impacts are computed go to the 📖 Methodology tab.</p>', unsafe_allow_html=True)
            display_impacts(impacts)                 
        
        with st.container(border=False):
            st.markdown('<h3 align = "center">Equivalences</h3>', unsafe_allow_html=True)
            st.markdown('<p align = "center">Making this request to the LLM is equivalent to the following actions :</p>', unsafe_allow_html=True)
            page = st.radio(' ', ['Energy' , 'GHG'], horizontal=True)
        
        with st.container(border=True):                                            
             if page == 'Energy' :
                display_equivalent_energy(impacts)
             else :  
                display_equivalent_ghg(impacts)
        
            
    except Exception as e:
        st.error('Could not find the model in the repository. Please try another model.')
import streamlit as st

from src.content import (
    HERO_TEXT,
    ABOUT_TEXT,
    CITATION_LABEL,
    CITATION_TEXT,
    LICENCE_TEXT,
    INTRO_TEXT,
    METHODOLOGY_TEXT,
    SUPPORT_TEXT,
)

from src.expert import expert_mode
from src.calculator import calculator_mode
from src.token_estimator import token_estimator

st.set_page_config(layout="wide", page_title="ECOLOGITS", page_icon="💬")

with open("src/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

st.html(HERO_TEXT)

st.success(INTRO_TEXT, icon="🌱")

tab_calculator, tab_expert, tab_token, tab_method, tab_about, tab_support = st.tabs(
    [
        "🧮 Calculator",
        "🤓 Expert Mode",
        "🪙 Tokens estimator",
        "📖 Methodology",
        "ℹ️ About",
        "🩷 Support us",
    ]
)

with tab_calculator:
    calculator_mode()

with tab_expert:
    expert_mode()

with tab_token:
    token_estimator()

with tab_method:
    st.write(METHODOLOGY_TEXT)

with tab_about:
    st.markdown(ABOUT_TEXT, unsafe_allow_html=True)

with tab_support:
    st.markdown(SUPPORT_TEXT, unsafe_allow_html=True)


with st.expander("📚 Citation"):
    st.html(CITATION_LABEL)
    st.code(CITATION_TEXT, language="bibtex")

st.html(LICENCE_TEXT)

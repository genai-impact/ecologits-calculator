import streamlit as st
import tiktoken
from .content import TOKEN_ESTIMATOR_TEXT

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def token_estimator():
    
    st.markdown("### 🪙 Tokens estimator")
    
    st.markdown("As our methodology deeply relies on the number of tokens processed by the model *(and as no-one is token-fluent)*, we provide you with a tool to estimate the number of tokens in a given text.")
    
    st.expander("ℹ️ What is a token anyway ?", expanded = False).markdown(TOKEN_ESTIMATOR_TEXT)
    
    user_text_input = st.text_area("Type or paste some text to estimate the amount of tokens.", "EcoLogits is a great project!")
    
    _, col2, _ = st.columns([2, 1, 2])
    
    with col2:
    
        st.metric(
            label = 'tokens estimated amount',
            #label_visibility = 'hidden',
            value = num_tokens_from_string(user_text_input, "cl100k_base"),
            border = True
        )
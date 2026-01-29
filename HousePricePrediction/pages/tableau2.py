import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.9rem; 
        padding-bottom: 0rem;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
        max-width: 98% !important;
    }

    .centered-title {
        text-align: center;
        font-size: 30px;
        font-weight: 650;
        color: white;
        margin-bottom: 18px;
    }

    iframe {
        width: 100% !important;
        height: 115vh !important;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="centered-title">Property Characteristics</div>',
    unsafe_allow_html=True
)

tableau_url = (
    "https://public.tableau.com/views/PropertyCharacteristics_17695050634760/PropertyCharacteristics"
    "?:embed=y"
    "&:showVizHome=no"
    "&:toolbar=no"
)

components.iframe(
    tableau_url,
    scrolling=True
)


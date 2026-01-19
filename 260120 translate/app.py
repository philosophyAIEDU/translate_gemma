import streamlit as st
from streamlit_option_menu import option_menu
import os
import json

# Import components and modules
from src.translator import TranslateGemmaWrapper
import src.utils as utils
from components.text_tab import render_text_tab
from components.image_tab import render_image_tab
from components.pdf_tab import render_pdf_tab
from components.glossary_tab import render_glossary_tab
from components.history_tab import render_history_tab

# Page Configuration
st.set_page_config(
    page_title="TranslateGemma Educator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
LANGUAGES_FILE = os.path.join(DATA_DIR, 'languages.json')
GLOSSARY_FILE = os.path.join(DATA_DIR, 'glossary.json')
HISTORY_FILE = os.path.join(DATA_DIR, 'history.json')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Load Resources
languages = utils.load_languages(LANGUAGES_FILE)

# Initialize Translator
# We initialize it once, but the internal loading is cached via @st.cache_resource in the class
translator = TranslateGemmaWrapper()

# Sidebar
with st.sidebar:
    st.image("https://github.com/google/gemma_pytorch/raw/main/assets/gemma_logo.png", width=200) # Placeholder or actual logo
    st.title("Educator Translator")
    
    selected_tab = option_menu(
        "Navigation",
        ["Text Translation", "Image Translation", "PDF Translation", "Glossary", "History"],
        icons=['translate', 'image', 'file-pdf', 'book', 'clock-history'],
        menu_icon="cast",
        default_index=0,
    )
    
    st.info("Using google/translategemma-4b-it")

# Main Content
if selected_tab == "Text Translation":
    render_text_tab(translator, languages, HISTORY_FILE)
elif selected_tab == "Image Translation":
    render_image_tab(translator, languages, HISTORY_FILE)
elif selected_tab == "PDF Translation":
    render_pdf_tab(translator, languages, HISTORY_FILE)
elif selected_tab == "Glossary":
    render_glossary_tab(GLOSSARY_FILE)
elif selected_tab == "History":
    render_history_tab(HISTORY_FILE)

# Footer
st.markdown("---")
st.markdown("Built with TranslateGemma | For Educators")

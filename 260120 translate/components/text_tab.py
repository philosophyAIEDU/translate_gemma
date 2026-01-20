import streamlit as st
from datetime import datetime
import src.utils as utils

def render_text_tab(translator, languages, history_file):
    st.header("Text Translation")

    if not languages:
        st.error("No languages available. Please check the languages.json file.")
        return

    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.selectbox("Source Language", options=list(languages.keys()), format_func=lambda x: f"{languages[x]} ({x})", key="text_source")
    with col2:
        target_lang = st.selectbox("Target Language", options=list(languages.keys()), format_func=lambda x: f"{languages[x]} ({x})", index=1, key="text_target")

    input_text = st.text_area("Enter text to translate", height=200)
    
    if st.button("Translate Text", key="btn_translate_text"):
        if not input_text:
            st.warning("Please enter some text.")
            return

        with st.spinner("Translating..."):
            try:
                # Optional: Apply Glossary here
                # if apply_glossary:
                #     input_text = apply_glossary_func(input_text)
                
                translation = translator.translate_text(input_text, source_lang, target_lang)
                st.success("Translation Complete!")
                st.text_area("Translation", value=translation, height=200)

                # Save to history
                record = {
                    "timestamp": datetime.now().isoformat(),
                    "type": "text",
                    "source_lang": source_lang,
                    "target_lang": target_lang,
                    "original": input_text,
                    "translated": translation
                }
                utils.save_history(record, history_file)
                
            except Exception as e:
                import traceback
                error_msg = traceback.format_exc()
                st.error(f"An error occurred: {error_msg}")

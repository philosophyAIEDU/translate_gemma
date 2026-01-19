import streamlit as st
import pandas as pd
from datetime import datetime
import src.utils as utils

def render_pdf_tab(translator, languages, history_file):
    st.header("PDF Translation")
    
    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.selectbox("Source Language", options=list(languages.keys()), format_func=lambda x: f"{languages[x]} ({x})", key="pdf_source")
    with col2:
        target_lang = st.selectbox("Target Language", options=list(languages.keys()), format_func=lambda x: f"{languages[x]} ({x})", index=1, key="pdf_target")

    uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])
    
    if uploaded_file is not None:
        if st.button("Translate PDF", key="btn_translate_pdf"):
            with st.spinner("Processing PDF (converting to images)..."):
                try:
                    # Note: This returns a list of dicts {page: int, translated_text: str}
                    results = translator.translate_pdf(uploaded_file, source_lang, target_lang)
                    
                    st.success("PDF Translation Complete!")
                    
                    full_text = ""
                    for res in results:
                        st.subheader(f"Page {res['page']}")
                        st.write(res['translated_text'])
                        st.divider()
                        full_text += f"\n--- Page {res['page']} ---\n{res['translated_text']}\n"
                    
                    # Save to history
                    record = {
                        "timestamp": datetime.now().isoformat(),
                        "type": "pdf",
                        "source_lang": source_lang,
                        "target_lang": target_lang,
                        "original": f"[PDF: {uploaded_file.name}]",
                        "translated": full_text
                    }
                    utils.save_history(record, history_file)
                    
                    st.download_button("Download Translation", data=full_text, file_name=f"translated_{uploaded_file.name}.txt")

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

import streamlit as st
from datetime import datetime
import src.utils as utils
import src.pdf_processor as pdf_proc

def render_pdf_tab(translator, languages, history_file):
    st.header("PDF Translation")

    if not languages:
        st.error("No languages available. Please check the languages.json file.")
        return

    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.selectbox("Source Language", options=list(languages.keys()), format_func=lambda x: f"{languages[x]} ({x})", key="pdf_source")
    with col2:
        target_lang = st.selectbox("Target Language", options=list(languages.keys()), format_func=lambda x: f"{languages[x]} ({x})", index=1, key="pdf_target")

    uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])

    if uploaded_file is not None:
        if st.button("Translate PDF", key="btn_translate_pdf"):
            try:
                # Convert PDF to images first
                with st.spinner("Converting PDF to images..."):
                    images = pdf_proc.convert_pdf_to_images(uploaded_file)

                total_pages = len(images)
                st.info(f"Found {total_pages} page(s) to translate.")

                # Progress bar for translation
                progress_bar = st.progress(0)
                status_text = st.empty()

                results = []
                full_text = ""

                for i, img in enumerate(images):
                    status_text.text(f"Translating page {i + 1} of {total_pages}...")
                    translated_text = translator.translate_image(img, source_lang, target_lang)
                    results.append({
                        "page": i + 1,
                        "translated_text": translated_text
                    })
                    full_text += f"\n--- Page {i + 1} ---\n{translated_text}\n"
                    progress_bar.progress((i + 1) / total_pages)

                status_text.empty()
                progress_bar.empty()

                st.success("PDF Translation Complete!")

                for res in results:
                    st.subheader(f"Page {res['page']}")
                    st.write(res['translated_text'])
                    st.divider()

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
                import traceback
                error_msg = traceback.format_exc()
                st.error(f"An error occurred: {error_msg}")

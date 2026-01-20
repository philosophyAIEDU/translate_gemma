import streamlit as st
from PIL import Image
from datetime import datetime
import src.utils as utils

def render_image_tab(translator, languages, history_file):
    st.header("Image Translation")

    if not languages:
        st.error("No languages available. Please check the languages.json file.")
        return

    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.selectbox("Source Language", options=list(languages.keys()), format_func=lambda x: f"{languages[x]} ({x})", key="img_source")
    with col2:
        target_lang = st.selectbox("Target Language", options=list(languages.keys()), format_func=lambda x: f"{languages[x]} ({x})", index=1, key="img_target")

    uploaded_file = st.file_uploader("Upload an Image", type=['png', 'jpg', 'jpeg', 'webp'])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        # Convert to RGB mode to ensure compatibility with the model
        if image.mode != 'RGB':
            image = image.convert('RGB')
        st.image(image, caption="Uploaded Image", width=400)
        
        if st.button("Translate Image", key="btn_translate_img"):
            with st.spinner("Analyzing and Translating..."):
                try:
                    translation = translator.translate_image(image, source_lang, target_lang)
                    st.success("Translation Complete!")
                    
                    st.divider()
                    st.subheader("Translated Text")
                    st.write(translation)
                    
                    # Save to history
                    record = {
                        "timestamp": datetime.now().isoformat(),
                        "type": "image",
                        "source_lang": source_lang,
                        "target_lang": target_lang,
                        "original": f"[Image: {uploaded_file.name}]",
                        "translated": translation
                    }
                    utils.save_history(record, history_file)

                except Exception as e:
                    import traceback
                    error_msg = traceback.format_exc()
                    st.error(f"An error occurred: {error_msg}")

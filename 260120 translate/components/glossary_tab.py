import streamlit as st
import pandas as pd
import src.utils as utils

def render_glossary_tab(glossary_file):
    st.header("Glossary Management")
    
    glossary_data = utils.load_glossary(glossary_file)
    
    # Simple UI to add terms
    with st.expander("Add New Term"):
        c1, c2 = st.columns(2)
        with c1:
            term = st.text_input("Source Term")
        with c2:
            translation = st.text_input("Target Translation")
        
        if st.button("Add Term"):
            if term and translation:
                glossary_data.append({"term": term, "translation": translation})
                utils.save_glossary(glossary_data, glossary_file)
                st.success(f"Added {term} -> {translation}")
                st.rerun()
            else:
                st.warning("Both fields are required.")

    # Display current glossary
    if glossary_data:
        st.subheader("Current Terms")
        df = pd.DataFrame(glossary_data)
        st.dataframe(df, use_container_width=True)
        
        # Simple deletion (optional, maybe just by index or clear all)
        if st.button("Clear Glossary"):
            utils.save_glossary([], glossary_file)
            st.rerun()
    else:
        st.info("Glossary is empty.")

import streamlit as st
import pandas as pd
import src.utils as utils

def render_history_tab(history_file):
    st.header("Translation History")
    
    history_data = utils.load_history(history_file)
    
    if history_data:
        # Convert to DataFrame for easier display
        df = pd.DataFrame(history_data)
        # Reorder columns if needed
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            
            # Export
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Download History (CSV)",
                csv,
                "history.csv",
                "text/csv",
                key='download-csv'
            )
    else:
        st.info("No translation history found.")

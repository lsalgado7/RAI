import streamlit as st
import pandas as pd
import json
import os
from dotenv import load_dotenv
from src.crew import FinancialCrew

# --- 1. Environment Setup ---
load_dotenv()

# --- 2. Streamlit Page Configuration ---
st.set_page_config(page_title="RAI", layout="wide")
st.title("🔎 Research Assistant Agent")
st.markdown(
    "Welcome to RAI, a agent to help researchers find good data for their projects."
)

# --- 3. Sidebar UI ---
with st.sidebar:
    st.header("⚙️ Configuration")
    st.info("Agents will scour Kaggle, HuggingFace, and Academic Repos.")

# --- 4. Main User Input ---
topic = st.text_input("I am looking for datasets about...", "Alzheimer's MRI Imagery")

# --- 5. Execution Logic ---
if st.button("🚀 Find Datasets"):
    
    # Check for API Key
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("Missing API Key!")
        st.stop()
    
    # Run the Agent Crew
    with st.spinner('Scouting data repositories... (This may take 1-2 minutes)'):
        crew = FinancialCrew(topic)
        result = crew.run()
        
        st.success("Discovery Complete!")
        
        # --- 6. Display Results ---
        tab1, tab2 = st.tabs(["📝 Research Guide", "📋 Found Datasets"])
        
        # Tab 1: Executive Summary Report
        with tab1:
            try:
                with open('reports/summary.md', 'r') as f:
                    st.markdown(f.read())
            except:
                st.warning("Report file not found.")

        # Tab 2: Structured Data Table
        with tab2:
            try:
                with open('data/metrics.json', 'r') as f:
                    data = json.load(f)
                
                df = pd.DataFrame(data['datasets'])
                
                st.data_editor(
                    df,
                    column_config={
                        "url": st.column_config.LinkColumn("Download Link")
                    },
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error parsing data: {e}")
import streamlit as st
import pandas as pd
import os

# --- Configuration & Styling ---
st.set_page_config(page_title="Rivora | AI Intelligence", layout="wide")

st.markdown("""
    <style>
    /* Global Styles */
    :root { --accent-gradient: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); }
    .main { background-color: #f8fafc; }
    
    /* Hero Gradient Section */
    .hero-container {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 3rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 2rem;
    }
    
    /* Modern Metric Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    
    /* Typography */
    h1, h2, h3 { font-family: 'Inter', sans-serif !important; font-weight: 700; }
    
    /* Skill Tags */
    .skill-tag {
        display: inline-block;
        background: #eef2ff;
        color: #4f46e5;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    
    /* Button Styling */
    .stButton>button {
        background: #4f46e5 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### 💠 Rivora Engine")
    st.caption("AI-Powered Talent Discovery")
    st.write("---")
    st.write("### Methodology")
    st.write("Ranking engine utilizes multi-factor analysis: behavior, IR, and technical skill weights[cite: 97, 107].")
    st.write("### Dataset Stats")
    st.metric("Total Candidates", "100K")
    st.metric("Active Model", "v1.0.4-prod")

# --- Hero Section ---
st.markdown("""
    <div class="hero-container">
        <h1>Rivora</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">AI-Powered Candidate Intelligence Engine</p>
    </div>
""", unsafe_allow_html=True)

# --- Metric Cards ---
col1, col2, col3 = st.columns(3)
col1.metric("Candidates Processed", "100,000")
col2.metric("Top Recommendations", "100")
col3.metric("System Status", "Operational")

st.markdown("<br>", unsafe_allow_html=True)

# --- Ranking Display ---
if st.button('Initialize Ranking Engine'):
    if os.path.exists('output/top100.csv'):
        df = pd.read_csv('output/top100.csv')
        st.subheader("Top Ranked Candidates")
        
        for i, row in df.head(10).iterrows():
            match_pct = min(int(row['score']), 100)
            
            with st.expander(f"Rank {row['rank']} | ID: {row['candidate_id']} • {match_pct}% Match"):
                c1, c2 = st.columns([1, 3])
                c1.metric("Match Score", f"{match_pct}%")
                c2.progress(match_pct / 100)
                
                st.markdown("**Reasoning:**")
                st.info(row['reasoning'])
                
                st.markdown("**Core Competencies:**")
                # Simulated skill visualization
                st.markdown('<span class="skill-tag">Production ML</span> <span class="skill-tag">Retrieval Systems</span>', unsafe_allow_html=True)
    else:
        st.error("Ranking data not found. Execute the ingestion pipeline first.")
else:
    st.info("Click the button to scan the candidate database and generate the top 100 ranked matches.")
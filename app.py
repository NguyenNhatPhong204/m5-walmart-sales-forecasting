import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(page_title="M5 Sales Forecasting", layout="wide", initial_sidebar_state="expanded")

# 2. Inject Editorial Custom CSS
st.markdown("""
    <style>
        /* Import Google Fonts: Playfair Display (Serif) and Inter (Sans-serif) */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500&display=swap');

        /* Overall App Background (Ivory/Off-white from the reference image) */
        [data-testid="stAppViewContainer"] {
            background-color: #FAF9F6;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #F3F2EF;
            border-right: 1px solid #EAE8E4;
        }

        /* Remove default header background */
        [data-testid="stHeader"] {
            background: transparent;
        }

        /* Global Font Settings */
        html, body, p, span, label, div {
            font-family: 'Inter', sans-serif !important;
            color: #1A1A1A;
        }

        /* Custom Editorial Typography */
        .hero-title {
            font-family: 'Playfair Display', serif !important;
            font-size: 56px;
            font-weight: 600;
            color: #111111;
            line-height: 1.1;
            letter-spacing: -0.02em;
            margin-top: 10px;
            margin-bottom: 10px;
        }
        
        .hero-subtitle {
            font-family: 'Inter', sans-serif !important;
            font-size: 18px;
            color: #555555;
            font-weight: 300;
            margin-bottom: 40px;
        }

        .section-header {
            font-family: 'Inter', sans-serif !important;
            font-size: 16px;
            font-weight: 600;
            color: #333333;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        
        /* Chart Container Styling */
        .chart-container {
            background-color: #FFFFFF;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.04);
            border: 1px solid #F0F0F0;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Load Data with Cache
@st.cache_data
def load_data():
    return pd.read_parquet('data_processed/dashboard_data.parquet')

with st.spinner("Loading forecasting data..."):
    df = load_data()

# 4. Sidebar Configuration
st.sidebar.markdown("<div class='section-header'>Product Filters</div>", unsafe_allow_html=True)

store_list = df['store_id'].unique()
selected_store = st.sidebar.selectbox("Select Store", store_list)

store_data = df[df['store_id'] == selected_store]

item_list = store_data['item_id'].unique()
selected_item = st.sidebar.selectbox("Select Item", item_list)

final_data = store_data[store_data['item_id'] == selected_item].sort_values('date')

# 5. Main Content Area (Editorial Header)
st.markdown("""
    <div class="hero-title">RETAIL SALES<br>FORECASTING DASHBOARD</div>
    <div class="hero-subtitle">AI Project: Supply Chain Optimization using the LightGBM Algorithm • DEVELOPER - NGUYEN NHAT PHONG</div>
""", unsafe_allow_html=True)

st.markdown(f"<div class='section-header'>28-Day Forecast vs Actual : {selected_item} @ {selected_store}</div>", unsafe_allow_html=True)

# 6. High-End Plotly Figure Setup
fig = go.Figure()

# Observed Line (Sharp, Dark Charcoal - represents grounded reality)
fig.add_trace(go.Scatter(
    x=final_data['date'], 
    y=final_data['sold'],
    mode='lines+markers', 
    name='Observed (Actual)',
    line=dict(color='#2B2B2B', width=2),
    marker=dict(size=8, color='#2B2B2B', symbol='circle')
))

# Predicted Line (Smooth, Vibrant Indigo with Gradient Fill - represents AI probability)
fig.add_trace(go.Scatter(
    x=final_data['date'], 
    y=final_data['prediction'],
    mode='lines', 
    name='Predicted (Forecast)',
    line=dict(color='#6366F1', width=3, shape='spline'), # Spline makes the curve smooth and continuous
    fill='tozeroy', # Fills the area down to the X-axis
    fillcolor='rgba(99, 102, 241, 0.1)', # Subtle indigo shadow
))

# Clean, minimalist grid layout
fig.update_layout(
    xaxis_title="",
    yaxis_title="Sales Volume",
    hovermode="x unified",
    legend=dict(
        orientation="h", 
        yanchor="bottom", 
        y=1.02, 
        xanchor="right", 
        x=1,
        font=dict(family="Inter", size=12, color="#333")
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=True, gridcolor='#EAE8E4', tickfont=dict(family='Inter', color='#555')),
    yaxis=dict(showgrid=True, gridcolor='#EAE8E4', tickfont=dict(family='Inter', color='#555')),
    margin=dict(l=0, r=0, t=10, b=0)
)

# Render Chart inside a styled white container for pop
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# 7. Data Expander
st.markdown("<br>", unsafe_allow_html=True)
if st.checkbox("Show Detailed Dataset"):
    display_df = final_data[['date', 'sold', 'prediction']].rename(
        columns={
            'date': 'Date', 
            'sold': 'Observed (Actual)', 
            'prediction': 'Predicted (Forecast)'
        }
    )
    display_df.reset_index(drop=True, inplace=True)
    st.dataframe(display_df, use_container_width=True)
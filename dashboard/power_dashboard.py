import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import math
import time
from datetime import datetime

# Page setup
st.set_page_config(
    page_title="Power System Dashboard",
    page_icon="⚡",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.8rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .section-title {
        font-size: 1.8rem;
        color: #2563EB;
        border-left: 5px solid #3B82F6;
        padding-left: 1rem;
        margin-top: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-title">⚡ LIVE POWER SYSTEM MONITOR</h1>', unsafe_allow_html=True)
st.markdown("### Generation (410V) → Step-up (11kV) → 5 Lines → Distribution Areas")

# Load data
@st.cache_data(ttl=5)  # Cache for 5 seconds for live updates
def load_data(use_live_data=False):
    try:
        if use_live_data:
            system_df = pd.read_csv('data/power_system_live.csv')
            loss_df = pd.read_csv('data/loss_calculations_live.csv')
            data_source = "🔄 LIVE DATA"
        else:
            system_df = pd.read_csv('data/power_system.csv')
            loss_df = pd.read_csv('data/loss_calculations.csv')
            data_source = "📁 STATIC DATA"
    except FileNotFoundError:
        # Fallback to static data if live data doesn't exist
        system_df = pd.read_csv('data/power_system.csv')
        loss_df = pd.read_csv('data/loss_calculations.csv')
        data_source = "📁 STATIC DATA (Fallback)"
    
    return system_df, loss_df, data_source

# SIDEBAR
st.sidebar.image("https://img.icons8.com/color/96/000000/electricity.png", width=80)
st.sidebar.header("⚙️ System Controls")

# Data settings in sidebar
use_live_data = st.sidebar.toggle("Use Live Data", value=False)
refresh_rate = st.sidebar.slider("Auto-refresh (seconds)", 5, 60, 10)
selected_line = st.sidebar.selectbox(
    "Select Line for Details",
    ["LINE_001", "LINE_002", "LINE_003", "LINE_004", "LINE_005"]
)

refresh = st.sidebar.button("🔄 Refresh Data", type="primary")

st.sidebar.markdown("---")
st.sidebar.info("""
**System Configuration:**
- Generation: 410V
- Transmission: 11kV
- 5 Independent Lines
- 5 Distribution Areas
""")

# Load appropriate data
try:
    system_df, loss_df, data_source = load_data(use_live_data)
    
    # Display data source
    st.sidebar.info(f"Data Source: {data_source}")
    
    # Auto-refresh if live data is enabled
    if use_live_data:
        time.sleep(refresh_rate)
        st.rerun()
    
    # Merge data
    combined_df = pd.merge(system_df, loss_df, on=['line_id', 'area_name'])
    
    # Live indicator
    if use_live_data:
        st.markdown("""
        <div style="background: linear-gradient(90deg, #00b09b, #96c93d); 
                    padding: 10px; border-radius: 10px; margin-bottom: 20px;">
            <h3 style="color: white; text-align: center; margin: 0;">
            🔄 LIVE DATA STREAMING • Auto-refresh every """ + str(refresh_rate) + """ seconds
            </h3>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: #3B82F6; padding: 10px; border-radius: 10px; margin-bottom: 20px;">
            <h3 style="color: white; text-align: center; margin: 0;">
            📊 STATIC DATA MODE • Toggle 'Use Live Data' for real-time simulation
            </h3>
        </div>
        """, unsafe_allow_html=True)
    
    # Last update time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.caption(f"Last updated: {current_time}")
    
    # MAIN DASHBOARD
    # Row 1: System Overview Metrics
    st.markdown('<h2 class="section-title">System Overview</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_load = combined_df['load_kw'].sum()
        st.metric("Total Load", f"{total_load:,.0f} kW")
    
    with col2:
        total_loss = combined_df['total_losses_kw'].sum()
        st.metric("Total Losses", f"{total_loss:,.1f} kW")
    
    with col3:
        avg_efficiency = combined_df['efficiency'].mean()
        st.metric("Avg Efficiency", f"{avg_efficiency:.1f}%")
    
    with col4:
        total_current = combined_df['current_amps'].sum()
        st.metric("Total Current", f"{total_current:,.0f} A")
    
    # Row 2: Loss Distribution Chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Losses by Line")
        fig1 = px.bar(
            combined_df,
            x='line_id',
            y=['line_losses_kw', 'transformer_losses_kw'],
            title="Line vs Transformer Losses",
            labels={'value': 'Losses (kW)', 'variable': 'Loss Type'},
            color_discrete_map={'line_losses_kw': '#3B82F6', 'transformer_losses_kw': '#10B981'}
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Efficiency by Area")
        fig2 = px.pie(
            combined_df,
            names='area_name',
            values='efficiency',
            title="Distribution Efficiency",
            hole=0.4,
            color='area_name'
        )
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Row 3: Line Details Table
    st.markdown('<h2 class="section-title">Line Details</h2>', unsafe_allow_html=True)
    
    # Create detailed table
    display_df = combined_df[['line_id', 'area_name', 'line_length_km', 'conductor_type', 
                            'load_kw', 'current_amps', 'line_losses_kw', 
                            'transformer_losses_kw', 'total_losses_kw', 
                            'loss_percentage', 'efficiency', 'voltage_drop_v']]
    
    # Format the table
    display_df.columns = ['Line ID', 'Area', 'Length (km)', 'Conductor', 'Load (kW)', 
                         'Current (A)', 'Line Loss (kW)', 'XFMR Loss (kW)', 
                         'Total Loss (kW)', 'Loss %', 'Efficiency %', 'Voltage Drop (V)']
    
    st.dataframe(
        display_df.style.format({
            'Load (kW)': '{:.0f}',
            'Current (A)': '{:.1f}',
            'Line Loss (kW)': '{:.2f}',
            'XFMR Loss (kW)': '{:.2f}',
            'Total Loss (kW)': '{:.2f}',
            'Loss %': '{:.2f}',
            'Efficiency %': '{:.2f}',
            'Voltage Drop (V)': '{:.1f}'
        }).background_gradient(subset=['Loss %'], cmap='RdYlGn_r'),
        use_container_width=True,
        height=300
    )
    
    # Row 4: Selected Line Details
    st.markdown('<h2 class="section-title">Line Details: ' + selected_line + '</h2>', unsafe_allow_html=True)
    
    line_data = combined_df[combined_df['line_id'] == selected_line].iloc[0]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📏 Line Parameters")
        st.write(f"**Area:** {line_data['area_name']}")
        st.write(f"**Length:** {line_data['line_length_km']} km")
        st.write(f"**Conductor:** {line_data['conductor_type']}")
        st.write(f"**Resistance:** {line_data['resistance_ohm_km']} Ω/km")
    
    with col2:
        st.markdown("### 🔌 Electrical Parameters")
        st.write(f"**Load:** {line_data['load_kw']} kW")
        st.write(f"**Current:** {line_data['current_amps']} A")
        st.write(f"**Power Factor:** {line_data['power_factor']}")
        st.write(f"**Voltage Drop:** {line_data['voltage_drop_v']} V")
    
    with col3:
        st.markdown("### 📊 Loss Analysis")
        st.write(f"**Line Losses:** {line_data['line_losses_kw']} kW")
        st.write(f"**Transformer Losses:** {line_data['transformer_losses_kw']} kW")
        st.write(f"**Total Losses:** {line_data['total_losses_kw']} kW")
        st.write(f"**Efficiency:** {line_data['efficiency']}%")
    
    # Row 5: System Diagram
    st.markdown('<h2 class="section-title">System Diagram</h2>', unsafe_allow_html=True)
    
    # Create a simple ASCII diagram
    diagram = f"""
    ```
    ╔═══════════════════════════════════════════════════════════════╗
    ║                    POWER SYSTEM DIAGRAM                       ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║                                                                ║
    ║  [Power House]                                                ║
    ║       ↓ 410V                                                  ║
    ║  [Step-up Transformer] 410V → 11kV                            ║
    ║       ↓ 11kV                                                  ║
    ║                                                                ║
    ║  ┌─────────┬─────────┬─────────┬─────────┬─────────┐          ║
    ║  │ LINE_001│ LINE_002│ LINE_003│ LINE_004│ LINE_005│          ║
    ║  │ 8.5 km  │ 12.3 km │ 6.8 km  │ 15.2 km │ 9.7 km  │          ║
    ║  │ 850 kW  │ 1200 kW │ 650 kW  │ 1500 kW │ 950 kW  │          ║
    ║  └─────────┴─────────┴─────────┴─────────┴─────────┘          ║
    ║         ↓         ↓         ↓         ↓         ↓             ║
    ║     [Area A]   [Area B]   [Area C]   [Area D]   [Area E]      ║
    ║                                                                ║
    ╚═══════════════════════════════════════════════════════════════╝
    ```
    """
    st.markdown(diagram)
    
    # Row 6: Download Report
    st.markdown('<h2 class="section-title">Reports</h2>', unsafe_allow_html=True)
    
    # Convert DataFrame to CSV for download
    csv = combined_df.to_csv(index=False).encode('utf-8')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="📥 Download Loss Report (CSV)",
            data=csv,
            file_name="power_system_loss_report.csv",
            mime="text/csv"
        )
    
    with col2:
        if st.button("📄 Generate Summary Report"):
            report = f"""
            POWER SYSTEM LOSS REPORT
            ========================
            
            System Configuration:
            - Generation Voltage: 410V
            - Transmission Voltage: 11kV
            - Number of Lines: 5
            
            Summary Statistics:
            - Total Load: {total_load:,.0f} kW
            - Total Losses: {total_loss:,.1f} kW
            - Overall Efficiency: {100 - (total_loss/total_load*100):.2f}%
            - Average Loss Percentage: {combined_df['loss_percentage'].mean():.2f}%
            
            Highest Loss Line: {combined_df.loc[combined_df['total_losses_kw'].idxmax(), 'line_id']}
            Most Efficient Line: {combined_df.loc[combined_df['efficiency'].idxmax(), 'line_id']}
            
            Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            st.text_area("System Report", report, height=200)

except FileNotFoundError:
    st.error("⚠️ Data files not found. Please run the calculation script first.")
    st.info("Run this command in terminal: `python scripts/calculate_losses.py`")
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.info("Make sure all data files exist in the 'data' folder")
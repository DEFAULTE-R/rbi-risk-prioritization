import streamlit as st
import pandas as pd
from risk_calculator import calculate_risk

# -------------------------------------------------
# Page Configuration (DO THIS FIRST)
# -------------------------------------------------
st.set_page_config(
    page_title="RBI Risk Prioritization Tool",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# Custom CSS for Better Visual Urgency
# -------------------------------------------------
st.markdown("""
<style>
    /* Risk category styling with clear urgency */
    .high-risk {
        color: #FF0000 !important;
        font-weight: 900 !important;
        background-color: #FFE5E5 !important;
        padding: 6px 12px !important;
        border-radius: 6px !important;
        border: 2px solid #FF0000 !important;
        text-align: center !important;
    }
    
    .medium-risk {
        color: #FF8C00 !important;
        font-weight: 900 !important;
        background-color: #FFF0E0 !important;
        padding: 6px 12px !important;
        border-radius: 6px !important;
        border: 2px solid #FF8C00 !important;
        text-align: center !important;
    }
    
    .low-risk {
        color: #008000 !important;
        font-weight: 900 !important;
        background-color: #E5FFE5 !important;
        padding: 6px 12px !important;
        border-radius: 6px !important;
        border: 2px solid #008000 !important;
        text-align: center !important;
    }
    
    /* Legend styling */
    .risk-legend {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
        border: 1px solid #dee2e6;
    }
    
    .legend-item {
        display: inline-block;
        margin-right: 20px;
        padding: 8px 15px;
        border-radius: 6px;
        font-weight: bold;
    }
    
    /* Highlight high risk rows in table */
    .high-row {
        background-color: #FFF5F5 !important;
        border-left: 4px solid #FF0000 !important;
    }
    
    .medium-row {
        background-color: #FFF9F0 !important;
        border-left: 4px solid #FF8C00 !important;
    }
    
    /* Gradient for RiskScore cells */
    .risk-score-high {
        background: linear-gradient(90deg, #FFE5E5, #FFB3B3) !important;
        font-weight: 900 !important;
        color: #B22222 !important;
        text-align: center !important;
    }
    
    .risk-score-medium {
        background: linear-gradient(90deg, #FFF0E0, #FFD9B3) !important;
        font-weight: 900 !important;
        color: #D2691E !important;
        text-align: center !important;
    }
    
    .risk-score-low {
        background: linear-gradient(90deg, #E5FFE5, #B3FFB3) !important;
        font-weight: 900 !important;
        color: #006400 !important;
        text-align: center !important;
    }
    
    /* Emergency banner */
    .emergency-banner {
        background: linear-gradient(90deg, #FF0000, #FF6666);
        color: white !important;
        padding: 15px;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        border: 3px solid #B22222;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Title & Description
# -------------------------------------------------
st.title("RBI Risk Prioritization Tool")
st.caption(
    "Indian Refinery RBI decision-support tool using transparent, engineer-verifiable logic."
)

# -------------------------------------------------
# RISK LEGEND (VISUAL URGENCY)
# -------------------------------------------------
st.markdown("""
<div class="risk-legend">
    <strong>⚠️ RISK LEVEL LEGEND:</strong><br><br>
    <span class="legend-item" style="background-color: #FFE5E5; color: #FF0000; border: 2px solid #FF0000;">
        🔴 HIGH RISK - IMMEDIATE ATTENTION REQUIRED
    </span>
    <span class="legend-item" style="background-color: #FFF0E0; color: #FF8C00; border: 2px solid #FF8C00;">
        🟠 MEDIUM RISK - SCHEDULE INSPECTION
    </span>
    <span class="legend-item" style="background-color: #E5FFE5; color: #008000; border: 2px solid #008000;">
        🟢 LOW RISK - ROUTINE MONITORING
    </span>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SAFETY BANNER (EMERGENCY STYLE)
# -------------------------------------------------
st.markdown("""
<div class="emergency-banner">
    ⚠️ SAFETY-CRITICAL ENGINEERING TOOL ⚠️<br>
    INDIAN REFINERY RBI COMPLIANCE | ENGINEER VERIFICATION MANDATORY<br>
    <small>This system provides inspection-prioritization support only. 
    All decisions must be reviewed and approved by a qualified engineer.</small>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# -------------------------------------------------
# Sidebar – Data Input
# -------------------------------------------------
st.sidebar.header("Data Input")
uploaded_file = st.sidebar.file_uploader(
    "Upload Vessels CSV",
    type=["csv"]
)

# -------------------------------------------------
# Load Data
# -------------------------------------------------
df = None

if uploaded_file is None:
    st.sidebar.info("Using sample vessel data.")
    try:
        df = pd.read_csv("data/vessels.csv")
    except FileNotFoundError:
        st.error("Sample data not found. Please upload a CSV file.")
else:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error reading uploaded file: {e}")

# Normalize column names defensively
if df is not None:
    df.columns = [c.strip() for c in df.columns]

# -------------------------------------------------
# Main Processing
# -------------------------------------------------
if df is not None:

    required_columns = ["VesselID", "CorrosionRate", "Age", "OperatingPressure"]
    missing_columns = [c for c in required_columns if c not in df.columns]

    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}")
    else:
        # Calculate Risk
        df[['RiskScore', 'RiskCategory']] = df.apply(
            lambda row: calculate_risk(
                row["CorrosionRate"],
                row["Age"],
                row["OperatingPressure"]
            ),
            axis=1,
            result_type="expand"
        )

        df_sorted = df.sort_values(by="RiskScore", ascending=False).reset_index(drop=True)

        # -------------------------------------------------
        # Executive Summary with Visual Indicators
        # -------------------------------------------------
        st.subheader("📊 Executive Summary")
        
        high_risk_count = len(df_sorted[df_sorted["RiskCategory"] == "HIGH"])
        total_assets = len(df_sorted)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Assets", total_assets)
        
        with col2:
            if high_risk_count > 0:
                st.markdown(f"""
                <div style="background-color: #FFE5E5; padding: 15px; border-radius: 8px; border: 3px solid #FF0000;">
                    <h3 style="color: #FF0000; margin: 0;">{high_risk_count}</h3>
                    <p style="color: #FF0000; margin: 0; font-weight: bold;">HIGH-RISK ASSETS</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.metric("High-Risk Assets", high_risk_count)
        
        with col3:
            avg_score = df_sorted['RiskScore'].mean()
            if avg_score > 10:
                color = "#FF0000"
            elif avg_score > 5:
                color = "#FF8C00"
            else:
                color = "#008000"
            
            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border: 2px solid {color};">
                <h3 style="color: {color}; margin: 0;">{avg_score:.2f}</h3>
                <p style="color: {color}; margin: 0; font-weight: bold;">AVERAGE RISK SCORE</p>
            </div>
            """, unsafe_allow_html=True)

        st.caption("🔺 Higher scores indicate higher inspection priority.")
        st.markdown("---")

        # -------------------------------------------------
        # Inspection Risk Distribution
        # -------------------------------------------------
        st.subheader("📈 Inspection Risk Distribution")

        risk_counts = (
            df_sorted["RiskCategory"]
            .value_counts()
            .reindex(["HIGH", "MEDIUM", "LOW"], fill_value=0)
        )
        
        # Color the chart
        chart_data = pd.DataFrame({
            'Risk Level': risk_counts.index,
            'Count': risk_counts.values,
            'Color': ['#FF0000', '#FF8C00', '#008000']
        })
        
        st.bar_chart(risk_counts)

        # -------------------------------------------------
        # Asset Prioritization Table with Enhanced Styling
        # -------------------------------------------------
        st.subheader("🎯 Asset Prioritization Table")
        
        # Function to apply CSS classes based on risk category
        def format_risk_category(val):
            if val == "HIGH":
                return f'<div class="high-risk">🔴 {val}</div>'
            elif val == "MEDIUM":
                return f'<div class="medium-risk">🟠 {val}</div>'
            else:
                return f'<div class="low-risk">🟢 {val}</div>'
        
        def format_risk_score(val):
            if val >= 10:
                return f'<div class="risk-score-high">{val:.2f}</div>'
            elif val >= 5:
                return f'<div class="risk-score-medium">{val:.2f}</div>'
            else:
                return f'<div class="risk-score-low">{val:.2f}</div>'
        
        # Create a styled DataFrame with HTML formatting
        display_df = df_sorted.copy()
        
        # Apply formatting to RiskCategory column
        display_df['RiskCategory'] = display_df['RiskCategory'].apply(format_risk_category)
        display_df['RiskScore'] = display_df['RiskScore'].apply(format_risk_score)
        
        # Display as HTML for full styling control
        st.markdown(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)
        
        st.caption("⚠️ **IMMEDIATE INSPECTION REQUIRED** for all HIGH RISK assets")

        # -------------------------------------------------
        # Inspection Priority List (URGENT ACTION LIST)
        # -------------------------------------------------
        st.subheader("🚨 CRITICAL INSPECTION PRIORITY LIST")
        
        if high_risk_count > 0:
            st.markdown(f"""
            <div style="background-color: #FFF5F5; padding: 15px; border-radius: 8px; border-left: 6px solid #FF0000; margin-bottom: 20px;">
                <h4 style="color: #FF0000; margin: 0;">⚠️ ALERT: {high_risk_count} HIGH-RISK VESSELS IDENTIFIED</h4>
                <p style="margin: 5px 0 0 0;">Immediate inspection required for these critical assets.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.caption("Supports inspection planning only and does not override statutory inspection requirements.")

        # Get top 5 or all high risk if more than 5
        if high_risk_count > 0:
            priority_df = df_sorted[df_sorted["RiskCategory"] == "HIGH"].head(5).copy()
        else:
            priority_df = df_sorted.head(5).copy()
        
        priority_df = priority_df[["VesselID", "RiskScore", "RiskCategory"]].copy()
        
        # Add urgent action column
        def get_urgent_action(row):
            if row["RiskCategory"] == "HIGH":
                return "🚨 INSPECT WITHIN 7 DAYS - CRITICAL"
            elif row["RiskCategory"] == "MEDIUM":
                return "⚠️ INSPECT WITHIN 30 DAYS"
            else:
                return "✅ ROUTINE INSPECTION"
        
        priority_df["Recommended Action"] = priority_df.apply(get_urgent_action, axis=1)
        
        # Style the priority list
        def style_priority_df(df):
            styles = []
            for i in range(len(df)):
                if df.iloc[i]["RiskCategory"] == "HIGH":
                    styles.append(['background-color: #FFE5E5', 'background-color: #FFE5E5', 
                                  'background-color: #FFE5E5', 'background-color: #FFCCCC; font-weight: bold'])
                elif df.iloc[i]["RiskCategory"] == "MEDIUM":
                    styles.append(['background-color: #FFF0E0', 'background-color: #FFF0E0', 
                                  'background-color: #FFF0E0', 'background-color: #FFE5B3; font-weight: bold'])
                else:
                    styles.append(['background-color: #E5FFE5', 'background-color: #E5FFE5', 
                                  'background-color: #E5FFE5', 'background-color: #CCFFCC; font-weight: bold'])
            return styles
        
        # Apply styling
        styled_priority = priority_df.style.apply(style_priority_df, axis=None)
        st.dataframe(styled_priority, use_container_width=True)

        # -------------------------------------------------
        # Download Button
        # -------------------------------------------------
        csv_data = df_sorted.to_csv(index=False)

        st.download_button(
            label="📥 DOWNLOAD PRIORITIZED INSPECTION REPORT",
            data=csv_data,
            file_name="RBI_Prioritized_Inspection_Report.csv",
            mime="text/csv"
        )

        # -------------------------------------------------
        # Final Emergency Disclaimer
        # -------------------------------------------------
        st.markdown("""
        <div style="background-color: #FFF3CD; padding: 15px; border-radius: 8px; border: 3px solid #FFC107; margin-top: 30px;">
            <h4 style="color: #856404; margin: 0 0 10px 0;">⚠️ EMERGENCY ACTION DISCLAIMER</h4>
            <p style="color: #856404; margin: 0;">
                <strong>THIS APPLICATION PROVIDES DECISION SUPPORT ONLY.</strong><br>
                Inspection scheduling and certification remain the responsibility of qualified personnel.<br>
                <strong>ALL HIGH-RISK ASSETS REQUIRE IMMEDIATE ENGINEER VERIFICATION.</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.caption(
    f"Submission-ready demo • Deterministic RBI logic • "
    f"Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}"
)

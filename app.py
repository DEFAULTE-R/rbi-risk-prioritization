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
# Title & Description (NO CUSTOM COLORS)
# -------------------------------------------------
st.title("RBI Risk Prioritization Tool")
st.caption(
    "Indian Refinery RBI decision-support tool using transparent, engineer-verifiable logic."
)

# -------------------------------------------------
# SAFETY BANNER (STREAMLIT-NATIVE, THEME-SAFE)
# -------------------------------------------------
st.error(
    "⚠️ **SAFETY-CRITICAL ENGINEERING TOOL**\n\n"
    "**INDIAN REFINERY RBI COMPLIANCE | ENGINEER VERIFICATION MANDATORY**\n\n"
    "This system provides inspection-prioritization support only. "
    "All decisions must be reviewed and approved by a qualified engineer."
)

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

        df_sorted = df.sort_values(by="RiskScore", ascending=False)

        # -------------------------------------------------
        # Executive Summary
        # -------------------------------------------------
        st.subheader("Executive Summary")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Assets", len(df_sorted))
        col2.metric(
            "High-Risk Assets",
            len(df_sorted[df_sorted["RiskCategory"] == "HIGH"])
        )
        col3.metric(
            "Average Risk Score",
            f"{df_sorted['RiskScore'].mean():.2f}"
        )

        st.caption("Higher scores indicate higher inspection priority.")
        st.markdown("---")

        # -------------------------------------------------
        # Inspection Risk Distribution
        # -------------------------------------------------
        st.subheader("Inspection Risk Distribution")

        risk_counts = (
            df_sorted["RiskCategory"]
            .value_counts()
            .reindex(["HIGH", "MEDIUM", "LOW"], fill_value=0)
        )

        st.bar_chart(risk_counts)

        # -------------------------------------------------
        # Asset Prioritization Table
        # -------------------------------------------------
        st.subheader("Asset Prioritization Table")

def color_risk(val):
    if val == "HIGH":
        return (
            "background-color: #c62828; "
            "color: white; "
            "font-weight: 700;"
        )
    elif val == "MEDIUM":
        return (
            "background-color: #f9a825; "
            "color: black; "
            "font-weight: 700;"
        )
    else:  # LOW
        return (
            "background-color: #2e7d32; "
            "color: white; "
            "font-weight: 700;"
        )

        st.dataframe(
            df_sorted.style.map(color_risk, subset=["RiskCategory"]),
            use_container_width=True
        )

        # -------------------------------------------------
        # Inspection Priority List
        # -------------------------------------------------
        st.subheader("📋 Inspection Priority List")
        st.caption(
            "Supports inspection planning only and does not override statutory inspection requirements."
        )

        priority_df = df_sorted[
            ["VesselID", "RiskScore", "RiskCategory"]
        ].head(5).copy()

        priority_df["Recommended Action"] = priority_df["RiskCategory"].apply(
            lambda x: "INSPECT WITHIN 7 DAYS" if x == "HIGH"
            else "INSPECT WITHIN 30 DAYS" if x == "MEDIUM"
            else "ROUTINE INSPECTION"
        )

        st.dataframe(priority_df, use_container_width=True)

        # -------------------------------------------------
        # Download Button
        # -------------------------------------------------
        csv_data = df_sorted.to_csv(index=False)

        st.download_button(
            label="📥 Download Prioritized Inspection Report",
            data=csv_data,
            file_name="RBI_Prioritized_Inspection_Report.csv",
            mime="text/csv"
        )

        # -------------------------------------------------
        # Final Disclaimer
        # -------------------------------------------------
        st.warning(
            "DISCLAIMER: This application provides decision support only. "
            "Inspection scheduling and certification remain the responsibility of qualified personnel."
        )
st.markdown("---")
st.caption(
    f"Submission-ready demo • Deterministic RBI logic • "
    f"Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}"
)

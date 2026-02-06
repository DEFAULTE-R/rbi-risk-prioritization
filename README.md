# rbi-risk-prioritization
# RBI Risk Prioritization Tool

A decision-support tool for prioritizing vessel inspection based on risk score.

## Risk Logic
(Defined in `risk_calculator.py`)

**Score Formula:**  
`Risk = (CorrosionRate * 2.0) + (Age * 0.3 IF Age > 15) + (Pressure * 0.01)`

**Thresholds:**
- **HIGH**: Score > 7.5
- **MEDIUM**: Score > 4.0
- **LOW**: Otherwise

## How to Run
# 🏭 RBI Risk Prioritization Tool
**GRASP Hackathon Submission - Indian Refinery Safety Focus**

## 🚀 Quick Start (30 seconds)
```bash
pip install -r requirements.txt
streamlit run app.py

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run Application:**
    ```bash
    streamlit run app.py
    ```

3.  **Usage:**
    - Upload a CSV having columns: `VesselID`, `CorrosionRate`, `Age`, `OperatingPressure`
    - Or view the embedded sample data.
    
## Why No Machine Learning?
RBI inspection decisions require deterministic, auditable logic.
Black-box models are unsuitable for safety-critical refinery environments.

"""
Calculate RBI risk score using transparent, auditable logic.
Inputs:
- corrosion_rate: mm/year
- age: years
- pressure: bar
Engineer verification required.
"""

*Engineer verification required for all outputs.*
## 🏆 GRASP Hackathon Compliance
- **No Machine Learning**: Deterministic calculations only
- **Transparent Logic**: Every risk score is reproducible
- **Safety-First**: Engineer verification mandatory
- **Constraint Adherence**: Streamlit + Pandas only
- **Real-World Ready**: CSV I/O for refinery integration

## ⚠️ Safety-Critical Design Philosophy
This tool follows the engineering principle: **"Trust, but verify."** 
While calculations are transparent, human judgment remains irreplaceable for safety-critical decisions.

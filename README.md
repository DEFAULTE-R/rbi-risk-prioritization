# 🏭 RBI Risk Prioritization Tool
**GRASP Hackathon Submission – Indian Refinery Safety Focus**

A decision-support tool that helps integrity engineers prioritize pressure vessel inspections using transparent, deterministic risk logic.

---

## 🚀 Live Demo (Judge-Ready)

🔗 **Live App:**  
https://rbi-risk-prioritization.streamlit.app/

_No installation required._

---

## ⚡ How to Use (30 seconds)

1. Open the live app link above  
2. Upload a CSV with columns:
   - `VesselID`
   - `CorrosionRate` (mm/year)
   - `Age` (years)
   - `OperatingPressure` (bar)
3. View the risk-prioritized inspection list  
4. Download the prioritized inspection report  

If no file is uploaded, the app runs using bundled sample refinery data.

---

## 📐 Risk Logic (Transparent & Auditable)

Defined in `risk_calculator.py`.

**Risk Score Formula:**

Risk = (CorrosionRate × 2.0)
+ (Age × 0.3, only if Age > 15 years)
+ (OperatingPressure × 0.01)


**Risk Categories:**
- **HIGH**: Score > 7.5  
- **MEDIUM**: Score > 4.0  
- **LOW**: Otherwise  

All calculations are deterministic and reproducible.

---

## ❓ Why No Machine Learning?

Risk-Based Inspection (RBI) decisions are safety-critical and require:
- Deterministic behavior
- Full auditability
- Engineer verification

Black-box ML models are unsuitable for such environments.  
This tool provides **decision support**, not automated decisions.

---

## 🏆 GRASP Hackathon Compliance

- ✅ **No Machine Learning** – deterministic calculations only  
- ✅ **Transparent Logic** – every score is explainable  
- ✅ **Safety-First** – engineer verification mandatory  
- ✅ **Constraint Adherence** – Streamlit + Pandas only  
- ✅ **Real-World Ready** – CSV I/O compatible with refinery workflows  

---

## ⚠️ Safety & Scope Notice

- This tool provides **decision support only**
- Inspection scheduling and certification remain the responsibility of qualified engineers
- Designed for **resource-constrained Indian refinery environments**

**Engineering principle followed:**  
> _Trust the logic. Verify the decision._

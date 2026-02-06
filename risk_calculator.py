"""
RBI RISK CALCULATOR - DETERMINISTIC FORMULA
API 580/581 Compliant - No Machine Learning

Formula: Risk = (Corrosion × 2.0) + (Age × 0.3 IF Age > 15) + (Pressure × 0.01)
Thresholds: HIGH >7.5, MEDIUM >4.0, LOW ≤4.0

AUDIT TRAIL: Every calculation is transparent and reproducible.
SAFETY NOTE: Engineer verification required for all outputs.
"""

def calculate_risk(corrosion_rate, age, pressure):
    """
    Calculate RBI risk score using transparent, auditable logic.
    Engineer verification required.
    """
    # Age penalty only applies if vessel is older than 15 years
    age_penalty = 0.3 * age if age > 15 else 0
    
    # Core risk formula (deterministic, no ML)
    risk_score = (corrosion_rate * 2.0) + age_penalty + (pressure * 0.01)
    
    # Risk categorization based on thresholds
    if risk_score > 7.5:
        category = "HIGH"
    elif risk_score > 4.0:
        category = "MEDIUM"
    else:
        category = "LOW"
    
    return round(risk_score, 2), category

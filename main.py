from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ml_engine import RiskCreditAgent

app = FastAPI(title="Sanjeevani AI API", version="1.0")

# Initialize Agents
risk_agent = RiskCreditAgent()

class UserData(BaseModel):
    annual_income: int
    existing_debt: int
    payment_history_score: int
    mobile_payment_volume: float
    transaction_regularity: float
    crop_yield_index: float
    renewable_energy_usage: int
    waste_management_score: int
    water_efficiency_score: int

@app.get("/")
def home():
    return {"message": "Sanjeevani AI System Operational"}

@app.post("/assess_credit")
def assess_credit(data: UserData):
    try:
        # 1. Risk Analysis
        assessment = risk_agent.predict(data.dict())
        
        # 2. Recommendation Agent Logic (Rule-based for stability)
        score = assessment['credit_score']
        sdg = assessment['sdg_score']
        recommendations = []
        
        # Loan Eligibility
        if score > 750:
            recommendations.append("Tier 1 Micro-Loan: ₹50,000 @ 8% interest")
        elif score > 600:
            recommendations.append("Tier 2 Micro-Loan: ₹25,000 @ 12% interest")
        else:
            recommendations.append("Credit Builder Loan: ₹5,000 (Secured)")
            
        # Green Financing
        if sdg > 70:
            recommendations.append("Green Subsidy: Eligible for 20% Solar Pump Rebate")
            recommendations.append("Government Scheme: PM-KUSUM Yojana Priority")
            
        return {
            "analysis": assessment,
            "recommendations": recommendations,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
import pandas as pd
import numpy as np
import xgboost as xgb
import shap
import joblib
import json

class FeatureEngineeringAgent:
    def process(self, df):
        """Creates rich features from raw inputs."""
        df_processed = df.copy()
        
        # Feature 1: Debt-to-Income Ratio
        df_processed['dti_ratio'] = df_processed['existing_debt'] / (df_processed['annual_income'] + 1)
        
        # Feature 2: Sustainability Index (SDG Score Proxy)
        df_processed['sdg_index'] = (
            (df_processed['renewable_energy_usage'] * 20) + 
            (df_processed['waste_management_score'] * 10) + 
            (df_processed['water_efficiency_score'] * 7)
        )
        
        # Feature 3: Digital Reliability
        df_processed['digital_trust'] = df_processed['mobile_payment_volume'] * df_processed['transaction_regularity']
        
        return df_processed

class RiskCreditAgent:
    def __init__(self):
        self.model = None
        self.explainer = None
        self.feature_cols = [
            'annual_income', 'existing_debt', 'payment_history_score', 
            'mobile_payment_volume', 'crop_yield_index', 'sdg_index', 
            'dti_ratio', 'digital_trust', 'water_efficiency_score'
        ]

    def train(self, data_path):
        print("🔄 Training Risk Model...")
        df = pd.read_csv(data_path)
        fe_agent = FeatureEngineeringAgent()
        df = fe_agent.process(df)
        
        X = df[self.feature_cols]
        y = df['is_default']
        
        self.model = xgb.XGBClassifier(
            n_estimators=100, 
            max_depth=4, 
            learning_rate=0.1, 
            eval_metric='logloss'
        )
        self.model.fit(X, y)
        
        # Initialize SHAP explainer
        self.explainer = shap.TreeExplainer(self.model)
        
        joblib.dump(self.model, "sanjeevani_xgb.pkl")
        print("✅ Model Trained and Saved.")

    def predict(self, input_data: dict):
        """
        Input: Dictionary of raw user data
        Output: Credit Score (300-900), Default Prob, SDG Score, Explanations
        """
        # Load Model if needed
        if not self.model:
            self.model = joblib.load("sanjeevani_xgb.pkl")
            self.explainer = shap.TreeExplainer(self.model)
            
        # Convert dict to DF
        df_input = pd.DataFrame([input_data])
        fe_agent = FeatureEngineeringAgent()
        df_feat = fe_agent.process(df_input)
        
        X_input = df_feat[self.feature_cols]
        
        # 1. Probability of Default
        prob_default = self.model.predict_proba(X_input)[0][1]
        
        # 2. Calculate Credit Score (Inverse to risk, scaled 300-900)
        credit_score = int(300 + (1 - prob_default) * 600)
        
        # 3. SDG Score (0-100)
        sdg_score = int(min(df_feat['sdg_index'].values[0], 100))
        
        # 4. SHAP Explanation
        shap_values = self.explainer.shap_values(X_input)
        
        # Top 3 factors contributing to the score
        feature_importance = list(zip(self.feature_cols, shap_values[0]))
        feature_importance.sort(key=lambda x: abs(x[1]), reverse=True)
        top_factors = [{"feature": f, "impact": float(v)} for f, v in feature_importance[:3]]

        return {
            "credit_score": credit_score,
            "default_probability": float(prob_default),
            "sdg_score": sdg_score,
            "risk_factors": top_factors
        }

# Train the model on first run
if __name__ == "__main__":
    agent = RiskCreditAgent()
    agent.train("sanjeevani_synthetic_data.csv")
import pandas as pd
import numpy as np
import random

def generate_sanjeevani_data(num_samples=1000):
    np.random.seed(42)
    
    data = {
        # --- Identity & Demographics ---
        'user_id': [f'UID_{i}' for i in range(num_samples)],
        'age': np.random.randint(18, 70, num_samples),
        'location_rural_tier': np.random.choice([1, 2, 3], num_samples), # 3 is most remote
        
        # --- Traditional Financial Indicators ---
        'annual_income': np.random.normal(150000, 50000, num_samples).astype(int),
        'existing_debt': np.random.normal(20000, 10000, num_samples).astype(int),
        'payment_history_score': np.random.randint(0, 10, num_samples), # 0=Bad, 10=Perfect
        
        # --- Non-Traditional Data (Digital Footprint) ---
        'mobile_payment_volume': np.random.normal(5000, 2000, num_samples),
        'transaction_regularity': np.random.uniform(0.1, 1.0, num_samples), # Consistency of UPI usage
        'shop_footfall_index': np.random.randint(10, 100, num_samples), # Proxy for business activity
        
        # --- Agricultural / Seasonal Data ---
        'crop_yield_index': np.random.uniform(0.5, 1.5, num_samples),
        'monsoon_impact_factor': np.random.uniform(0, 1, num_samples), # 1 = High Risk
        
        # --- ESG / SDG Metrics ---
        'renewable_energy_usage': np.random.choice([0, 1], num_samples, p=[0.7, 0.3]), # Solar pumps etc.
        'waste_management_score': np.random.randint(1, 5, num_samples),
        'water_efficiency_score': np.random.randint(1, 10, num_samples),
        'social_community_participation': np.random.randint(1, 10, num_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Ensure no negative values
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].clip(lower=0)
    
    # --- Target Variable Simulation (Logic) ---
    # We create a "True Score" to simulate Default. 
    # Default is likely if debts are high, income low, and payment history bad.
    
    df['financial_health'] = (
        (df['annual_income'] * 0.4) + 
        (df['mobile_payment_volume'] * 2) + 
        (df['payment_history_score'] * 1000) - 
        (df['existing_debt'])
    )
    
    # Probability of Default (Sigmoid-ish logic)
    df['default_prob'] = 1 / (1 + np.exp(df['financial_health'] / 50000))
    df['is_default'] = (df['default_prob'] > np.random.uniform(0.3, 0.7, num_samples)).astype(int)
    
    return df

if __name__ == "__main__":
    df = generate_sanjeevani_data()
    df.to_csv("sanjeevani_synthetic_data.csv", index=False)
    print("✅ Dataset Generated: sanjeevani_synthetic_data.csv")
"""
Simple test to debug the ML analysis issue
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_simple():
    print("🧪 SIMPLE ML TEST")
    print("=" * 30)
    
    # Simple test resume
    test_resume = "Python developer with web development experience"
    
    try:
        print("Testing /analyze-all endpoint...")
        response = requests.post(f"{BASE_URL}/analyze-all", json={
            "resume_text": test_resume
        })
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(f"Companies analyzed: {result.get('total_companies', 0)}")
            
            if result.get('company_analysis'):
                first_company = result['company_analysis'][0]
                print(f"First company: {first_company['company']}")
                
                if 'ml_analysis' in first_company:
                    ml = first_company['ml_analysis']
                    print(f"ML Score: {ml.get('ml_eligibility_score', 'N/A')}%")
                    print(f"Level: {ml.get('eligibility_level', 'N/A')}")
                    
                    if 'learning_recommendations' in ml:
                        print(f"Recommendations: {len(ml['learning_recommendations'])} skills")
                    
                    if 'learning_roadmap' in ml:
                        print(f"Roadmap: {len(ml['learning_roadmap'].get('learning_path', []))} phases")
                else:
                    print("❌ No ml_analysis in response")
            else:
                print("❌ No company_analysis in response")
                
        else:
            print(f"❌ Error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error message: {error_data.get('message', 'Unknown error')}")
            except:
                print(f"Raw response: {response.text}")
                
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_simple()
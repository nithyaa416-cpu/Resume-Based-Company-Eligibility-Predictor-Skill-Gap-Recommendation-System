"""
Test Web Interface - Check if the HTML is serving correctly
"""

import requests
import time

BASE_URL = "http://localhost:5000"

def test_web_interface():
    print("🌐 TESTING WEB INTERFACE")
    print("=" * 50)
    
    try:
        # Test if main page loads
        print("1. Testing main page...")
        response = requests.get(BASE_URL)
        
        if response.status_code == 200:
            print("✅ Main page loads successfully")
            
            # Check if it contains ML indicators
            html_content = response.text
            
            if "🤖 AI-Powered Resume Analyzer" in html_content:
                print("✅ ML-powered title found")
            else:
                print("❌ ML-powered title missing")
                
            if "ML Analysis" in html_content:
                print("✅ ML Analysis buttons found")
            else:
                print("❌ ML Analysis buttons missing")
                
            if "Learning Recommendations" in html_content:
                print("✅ Learning Recommendations section found")
            else:
                print("❌ Learning Recommendations section missing")
                
        else:
            print(f"❌ Main page failed to load: {response.status_code}")
            
        # Test API endpoints
        print("\n2. Testing API endpoints...")
        
        # Test companies endpoint
        response = requests.get(f"{BASE_URL}/companies")
        if response.status_code == 200:
            companies = response.json()
            print(f"✅ Companies API works: {len(companies['companies'])} companies")
        else:
            print(f"❌ Companies API failed: {response.status_code}")
            
        # Test analyze-all with sample data
        print("\n3. Testing analyze-all endpoint...")
        test_resume = "Python developer with 2 years experience in web development"
        
        response = requests.post(f"{BASE_URL}/analyze-all", json={
            "resume_text": test_resume
        })
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Analyze-all API works")
            
            # Check if ML analysis is present
            if result['company_analysis'] and 'ml_analysis' in result['company_analysis'][0]:
                print("✅ ML analysis data present")
                
                ml_analysis = result['company_analysis'][0]['ml_analysis']
                
                # Check for key ML features
                if 'learning_recommendations' in ml_analysis:
                    print(f"✅ Learning recommendations present: {len(ml_analysis['learning_recommendations'])} skills")
                else:
                    print("❌ Learning recommendations missing")
                    
                if 'learning_roadmap' in ml_analysis:
                    print("✅ Learning roadmap present")
                else:
                    print("❌ Learning roadmap missing")
                    
                if 'skill_readiness_levels' in ml_analysis:
                    print("✅ Skill readiness levels present")
                else:
                    print("❌ Skill readiness levels missing")
                    
            else:
                print("❌ ML analysis data missing")
                
        else:
            print(f"❌ Analyze-all API failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing web interface: {e}")
    
    print("\n🎯 SUMMARY:")
    print("If all tests pass, the web interface should show:")
    print("- 🤖 ML-powered analysis indicators")
    print("- Missing skills with red tags")
    print("- Learning recommendations (free/paid)")
    print("- Learning roadmaps with phases")
    print("- 'View Detailed Analysis' buttons")
    print()
    print("🌐 Open http://localhost:5000 in your browser to test manually")

if __name__ == "__main__":
    test_web_interface()
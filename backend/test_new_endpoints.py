#!/usr/bin/env python3
"""
Test script for the new company-role endpoints
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_companies_with_roles():
    """Test the new companies-with-roles endpoint"""
    print("🧪 Testing /companies-with-roles endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/companies-with-roles")
        data = response.json()
        
        if response.status_code == 200 and data['status'] == 'success':
            print("✅ Success!")
            print(f"📊 Total positions: {data['total_positions']}")
            print("\n📋 Available positions:")
            
            for position in data['companies_with_roles'][:5]:  # Show first 5
                print(f"  • {position['display_name']}")
            
            if len(data['companies_with_roles']) > 5:
                print(f"  ... and {len(data['companies_with_roles']) - 5} more")
                
            return True
        else:
            print(f"❌ Failed: {data.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_analyze_with_role():
    """Test analyzing with specific company and role"""
    print("\n🧪 Testing /analyze endpoint with role...")
    
    sample_resume = """
    John Doe
    Software Engineer
    
    Experience:
    - 3 years of Python development
    - React and JavaScript experience
    - AWS cloud services
    - Docker containerization
    
    Skills: Python, React, JavaScript, AWS, Docker, Git, SQL
    
    Education: BTech Computer Science
    """
    
    try:
        response = requests.post(f"{BASE_URL}/analyze", json={
            "resume_text": sample_resume,
            "company": "Google",
            "role": "Software Engineer"
        })
        
        data = response.json()
        
        if response.status_code == 200 and data['status'] == 'success':
            print("✅ Success!")
            print(f"🏢 Company: {data['company']}")
            if 'role' in data:
                print(f"💼 Role: {data['role']}")
            
            ml_analysis = data.get('ml_analysis', {})
            if ml_analysis:
                print(f"🤖 ML Eligibility Score: {ml_analysis.get('ml_eligibility_score', 'N/A')}%")
                print(f"📊 Eligibility Level: {ml_analysis.get('eligibility_level', 'N/A')}")
            
            return True
        else:
            print(f"❌ Failed: {data.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_analyze_all():
    """Test analyzing all companies and roles"""
    print("\n🧪 Testing /analyze-all endpoint...")
    
    sample_resume = """
    Jane Smith
    Full Stack Developer
    
    Experience:
    - 2 years of web development
    - Python, JavaScript, React
    - Node.js backend development
    - MongoDB database experience
    
    Skills: Python, JavaScript, React, Node.js, MongoDB, HTML, CSS, Git
    
    Education: MTech Computer Science
    """
    
    try:
        response = requests.post(f"{BASE_URL}/analyze-all", json={
            "resume_text": sample_resume
        })
        
        data = response.json()
        
        if response.status_code == 200 and data['status'] == 'success':
            print("✅ Success!")
            print(f"📊 Total positions analyzed: {data['total_positions']}")
            
            # Show top 3 matches
            if data.get('company_analysis'):
                print("\n🏆 Top 3 matches:")
                for i, result in enumerate(data['company_analysis'][:3]):
                    company = result['company']
                    role = result.get('role', 'N/A')
                    score = result.get('ml_analysis', {}).get('ml_eligibility_score', 0)
                    print(f"  {i+1}. {company} - {role}: {score}%")
            
            return True
        else:
            print(f"❌ Failed: {data.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Resume Analyzer Backend with Company-Role Support")
    print("=" * 60)
    
    # Test all endpoints
    tests = [
        test_companies_with_roles,
        test_analyze_with_role,
        test_analyze_all
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📈 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is ready for company-role support.")
    else:
        print("⚠️  Some tests failed. Please check the backend implementation.")
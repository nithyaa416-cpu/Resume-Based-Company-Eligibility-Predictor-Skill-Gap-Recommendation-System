"""
Simple API test script
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_analyze_endpoint():
    """Test the analyze endpoint with sample data"""
    
    sample_resume_text = """
    John Doe
    Software Developer
    
    Experience:
    - 3 years of experience in Python development
    - Worked with Django and Flask frameworks
    - Experience with MySQL and PostgreSQL databases
    - Familiar with React and JavaScript
    - Used Git for version control
    - Deployed applications on AWS
    - Experience with machine learning and TensorFlow
    
    Skills:
    Python, Java, JavaScript, React, Node.js, MySQL, PostgreSQL, 
    Git, AWS, Docker, HTML, CSS, Machine Learning, TensorFlow, NLP
    
    Education:
    Bachelor's in Computer Science
    """
    
    # Test data
    test_data = {
        "resume_text": sample_resume_text,
        "company": "Google"
    }
    
    try:
        # Make POST request
        response = requests.post(f"{BASE_URL}/analyze", json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Analyze endpoint test successful!")
            print(f"Company: {result['company']}")
            print(f"Overall Score: {result['analysis']['overall_score']}")
            print(f"Eligibility Level: {result['analysis']['eligibility_level']}")
            print(f"Skills Found: {len(result['resume_skills'])}")
            print(f"Missing Skills: {result['analysis']['skill_analysis']['missing_skills'][:3]}...")
            return True
        else:
            print(f"❌ Test failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure Flask app is running on port 5000")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

def test_analyze_all_endpoint():
    """Test the analyze-all endpoint"""
    
    sample_resume_text = """
    Jane Smith
    Full Stack Developer
    
    Experience:
    - 5 years of experience in web development
    - Expert in React, Node.js, and MongoDB
    - Experience with cloud platforms like AWS
    - Proficient in Python and Java
    
    Skills:
    Python, Java, JavaScript, React, Node.js, MongoDB, 
    AWS, Docker, Git, HTML, CSS, Express.js
    """
    
    test_data = {
        "resume_text": sample_resume_text
    }
    
    try:
        response = requests.post(f"{BASE_URL}/analyze-all", json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Analyze-all endpoint test successful!")
            print(f"Total Companies Analyzed: {result['total_companies']}")
            print(f"Top 3 Companies:")
            
            for i, company_result in enumerate(result['company_analysis'][:3]):
                print(f"  {i+1}. {company_result['company']}: {company_result['analysis']['overall_score']}% ({company_result['analysis']['eligibility_level']})")
            
            return True
        else:
            print(f"❌ Test failed with status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Resume Analysis API...\n")
    
    # Test individual endpoints
    success1 = test_analyze_endpoint()
    success2 = test_analyze_all_endpoint()
    
    if success1 and success2:
        print("\n🎉 All API tests passed successfully!")
    else:
        print("\n⚠️  Some tests failed. Check the server logs.")
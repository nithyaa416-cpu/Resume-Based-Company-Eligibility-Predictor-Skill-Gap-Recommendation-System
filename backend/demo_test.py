"""
Demo script to showcase the Resume Analysis System
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def demo_full_workflow():
    """Demonstrate the complete workflow"""
    
    print("🎯 Resume-Based Company Eligibility System Demo")
    print("=" * 50)
    
    # Sample resume for a Python developer
    sample_resume = """
    Alex Johnson
    Senior Software Developer
    
    EXPERIENCE:
    • 4 years of experience in Python development
    • Built web applications using Django and Flask
    • Worked with PostgreSQL and MongoDB databases
    • Experience with React.js and JavaScript
    • Deployed applications on AWS and Docker
    • Familiar with machine learning using TensorFlow
    • Used Git for version control
    
    SKILLS:
    Programming: Python, Java, JavaScript, SQL
    Web Technologies: React, Django, Flask, HTML, CSS, Node.js
    Databases: PostgreSQL, MongoDB, MySQL
    Cloud & DevOps: AWS, Docker, Git, Jenkins
    Data Science: TensorFlow, Pandas, NumPy, Machine Learning
    
    EDUCATION:
    Bachelor of Technology in Computer Science
    """
    
    print("📄 Sample Resume Profile:")
    print("- Name: Alex Johnson")
    print("- Role: Senior Software Developer") 
    print("- Experience: 4 years")
    print("- Key Skills: Python, Django, React, AWS, ML")
    print()
    
    # Step 1: Get all companies
    print("🏢 Step 1: Getting available companies...")
    try:
        response = requests.get(f"{BASE_URL}/companies")
        companies = response.json()['companies']
        print(f"✅ Found {len(companies)} companies: {', '.join(companies[:5])}...")
        print()
    except Exception as e:
        print(f"❌ Error getting companies: {e}")
        return
    
    # Step 2: Analyze against specific company (Google)
    print("🔍 Step 2: Analyzing eligibility for Google...")
    try:
        analyze_data = {
            "resume_text": sample_resume,
            "company": "Google"
        }
        response = requests.post(f"{BASE_URL}/analyze", json=analyze_data)
        result = response.json()
        
        analysis = result['analysis']
        print(f"✅ Analysis Complete!")
        print(f"   📊 Overall Score: {analysis['overall_score']}%")
        print(f"   🎯 Eligibility Level: {analysis['eligibility_level']}")
        print(f"   ✅ Skills Matched: {len(analysis['skill_analysis']['matched_skills'])}/{analysis['skill_analysis']['total_required']}")
        print(f"   ❌ Missing Skills: {', '.join(analysis['skill_analysis']['missing_skills'][:3])}...")
        print(f"   💼 Experience Score: {analysis['experience_analysis']['score']}%")
        print()
        
    except Exception as e:
        print(f"❌ Error analyzing for Google: {e}")
        return
    
    # Step 3: Analyze against all companies
    print("🌐 Step 3: Analyzing eligibility for ALL companies...")
    try:
        analyze_all_data = {
            "resume_text": sample_resume
        }
        response = requests.post(f"{BASE_URL}/analyze-all", json=analyze_all_data)
        result = response.json()
        
        print(f"✅ Analyzed {result['total_companies']} companies!")
        print(f"📈 Top 5 Best Matches:")
        
        for i, company_result in enumerate(result['company_analysis'][:5]):
            company = company_result['company']
            score = company_result['analysis']['overall_score']
            level = company_result['analysis']['eligibility_level']
            
            # Add emoji based on eligibility level
            emoji = "🟢" if level == "Highly Eligible" else "🟡" if level == "Eligible" else "🔴"
            
            print(f"   {i+1}. {emoji} {company}: {score}% ({level})")
        
        print()
        
    except Exception as e:
        print(f"❌ Error analyzing all companies: {e}")
        return
    
    # Step 4: Get recommendations for improvement
    print("💡 Step 4: Getting skill gap recommendations...")
    try:
        rec_data = {
            "company": "Google",
            "resume_skills": result['resume_skills']
        }
        response = requests.post(f"{BASE_URL}/recommendations", json=rec_data)
        rec_result = response.json()
        
        print(f"✅ Recommendations for Google:")
        recommendations = rec_result['recommendations']
        
        if recommendations:
            for i, rec in enumerate(recommendations[:3]):
                print(f"   {i+1}. Learn {rec['skill'].title()}")
                print(f"      📚 Resource: {rec['resource']}")
        else:
            print("   🎉 No additional skills needed - you're fully qualified!")
        
        print()
        
    except Exception as e:
        print(f"❌ Error getting recommendations: {e}")
        return
    
    print("🎉 Demo completed successfully!")
    print("💻 Your Resume Analysis System is working perfectly!")
    print()
    print("🔗 Available Endpoints:")
    print("   • GET  /companies - List all companies")
    print("   • POST /upload - Upload resume file")
    print("   • POST /analyze - Analyze for specific company")
    print("   • POST /analyze-all - Analyze for all companies")
    print("   • POST /recommendations - Get learning recommendations")

if __name__ == "__main__":
    demo_full_workflow()
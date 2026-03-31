"""
Test script for enhanced features:
1. Skill Readiness Levels
2. Human-readable Explanations  
3. Learning Roadmap Generator
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_enhanced_features():
    """Test all enhanced features"""
    
    print("🚀 Testing Enhanced Resume Analysis Features")
    print("=" * 60)
    
    # Enhanced sample resume with varying skill levels
    enhanced_resume = """
    ALEX CHEN
    Senior Full Stack Developer
    
    PROFESSIONAL SUMMARY
    Experienced software developer with 5 years of extensive experience in Python development.
    Expert in React and JavaScript with deep knowledge of modern web frameworks.
    Advanced proficiency in AWS cloud services and Docker containerization.
    
    TECHNICAL EXPERTISE
    
    Programming Languages:
    • Python - 5+ years of professional experience, expert level
    • JavaScript - Advanced proficiency, 4 years experience  
    • Java - Intermediate level, used in 3 projects
    • TypeScript - Familiar with, used in recent project
    
    Web Development:
    • React - Expert level, built 10+ production applications
    • Node.js - Advanced, extensive backend development experience
    • Django - Proficient, developed multiple REST APIs
    • HTML/CSS - Expert level, responsive design specialist
    • Express.js - Intermediate, used in several projects
    
    Databases:
    • PostgreSQL - Advanced, database design and optimization
    • MongoDB - Intermediate level, used in 5 projects  
    • MySQL - Familiar with basic operations
    
    Cloud & DevOps:
    • AWS - Advanced certification, extensive experience with EC2, S3, Lambda
    • Docker - Expert level, containerization specialist
    • Git - Advanced, team lead experience
    • Jenkins - Intermediate, CI/CD pipeline setup
    
    Data Science (Learning):
    • Machine Learning - Beginner, completed online course
    • TensorFlow - Basic familiarity, personal projects
    • Pandas - Intermediate, data analysis projects
    
    PROFESSIONAL EXPERIENCE
    
    Senior Developer | TechCorp (2021-Present)
    • Led development of 5 React applications serving 50K+ users
    • Architected microservices using Python and Docker
    • Implemented advanced AWS solutions including Lambda functions
    • Mentored junior developers in React and Python best practices
    
    Full Stack Developer | StartupXYZ (2019-2021)  
    • Developed web applications using React, Node.js, and PostgreSQL
    • Built RESTful APIs with Django and Express.js
    • Implemented CI/CD pipelines using Jenkins and Docker
    • Worked extensively with MongoDB for data storage
    
    PROJECTS
    • E-commerce Platform: React + Django + PostgreSQL (Advanced implementation)
    • Real-time Chat App: Node.js + Socket.io + MongoDB (Expert level)
    • Data Analytics Dashboard: Python + Pandas + Machine Learning (Intermediate)
    
    CERTIFICATIONS
    • AWS Certified Solutions Architect (Advanced)
    • React Advanced Patterns Certification
    • Docker Certified Associate
    """
    
    print("👤 Testing with Enhanced Resume Profile:")
    print("- Name: Alex Chen")
    print("- Experience: 5 years") 
    print("- Expertise: Python (Expert), React (Expert), AWS (Advanced)")
    print("- Learning: Machine Learning (Beginner), TensorFlow (Basic)")
    print()
    
    # Test 1: Skill Readiness Analysis
    print("🎯 Test 1: Skill Readiness Level Analysis")
    print("-" * 40)
    
    try:
        skill_data = {"resume_text": enhanced_resume}
        response = requests.post(f"{BASE_URL}/skill-analysis", json=skill_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Skill Analysis Complete!")
            print(f"📊 Total Skills Found: {result['total_skills']}")
            print()
            
            # Display skills by readiness level
            for level in ['Advanced', 'Intermediate', 'Beginner']:
                skills = result['skills_by_level'][level]
                if skills:
                    print(f"🟢 {level} Level ({len(skills)} skills):")
                    for skill_info in skills[:5]:  # Show top 5
                        print(f"   • {skill_info['skill']} ({skill_info['mentions']} mentions) - {skill_info['category']}")
                    print()
        else:
            print(f"❌ Skill analysis failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error in skill analysis: {e}")
    
    # Test 2: Enhanced Company Analysis with Explanations
    print("🏢 Test 2: Enhanced Company Analysis (Google)")
    print("-" * 40)
    
    try:
        analyze_data = {
            "resume_text": enhanced_resume,
            "company": "Google"
        }
        response = requests.post(f"{BASE_URL}/analyze", json=analyze_data)
        
        if response.status_code == 200:
            result = response.json()
            analysis = result['analysis']
            
            print("✅ Enhanced Analysis Complete!")
            print(f"🎯 Company: {result['company']}")
            print(f"📊 Overall Score: {analysis['overall_score']}%")
            print(f"🏆 Eligibility: {analysis['eligibility_level']}")
            print()
            
            # Display human-readable explanation
            print("🧠 AI Explanation:")
            explanation = analysis['explanation']
            print(f"   {explanation['summary']}")
            print("   Detailed Analysis:")
            for reason in explanation['reasons']:
                print(f"   • {reason}")
            print()
            
            if explanation['strengths']:
                print(f"💪 Your Strengths: {', '.join(explanation['strengths'])}")
            if explanation['weaknesses']:
                print(f"⚠️  Areas to Improve: {', '.join(explanation['weaknesses'])}")
            print()
            
            # Display Learning Roadmap
            if 'learning_roadmap' in analysis and analysis['learning_roadmap']['phases']:
                roadmap = analysis['learning_roadmap']
                print("🗺️  Personalized Learning Roadmap:")
                print(f"   📚 Total Skills to Learn: {roadmap['total_skills']}")
                print(f"   ⏱️  Estimated Time: {roadmap['estimated_time']}")
                print()
                
                for phase in roadmap['phases']:
                    print(f"   Phase {phase['phase']}: {phase['title']}")
                    print(f"   📖 {phase['description']}")
                    print(f"   ⏰ Duration: {phase['duration']}")
                    print(f"   🎯 Skills: {', '.join(phase['skills'])}")
                    print()
            
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error in company analysis: {e}")
    
    # Test 3: Multi-Company Analysis with Rankings
    print("🌐 Test 3: Multi-Company Analysis with Enhanced Features")
    print("-" * 40)
    
    try:
        analyze_all_data = {"resume_text": enhanced_resume}
        response = requests.post(f"{BASE_URL}/analyze-all", json=analyze_all_data)
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ Multi-Company Analysis Complete!")
            print(f"🏢 Analyzed {result['total_companies']} companies")
            print()
            print("🏆 Top 5 Company Matches:")
            
            for i, company_result in enumerate(result['company_analysis'][:5]):
                company = company_result['company']
                analysis = company_result['analysis']
                
                # Emoji based on eligibility
                emoji_map = {
                    "Highly Eligible": "🟢",
                    "Eligible": "🟡", 
                    "Not Eligible": "🔴"
                }
                emoji = emoji_map.get(analysis['eligibility_level'], "⚪")
                
                print(f"   {i+1}. {emoji} {company}")
                print(f"      📊 Score: {analysis['overall_score']}% ({analysis['eligibility_level']})")
                
                # Show brief explanation
                if 'explanation' in analysis:
                    print(f"      💭 {analysis['explanation']['summary']}")
                
                print()
                
        else:
            print(f"❌ Multi-company analysis failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error in multi-company analysis: {e}")
    
    print("🎉 Enhanced Feature Testing Complete!")
    print()
    print("🌟 UNIQUE FEATURES DEMONSTRATED:")
    print("✅ 1. Skill Readiness Levels (Beginner → Intermediate → Advanced)")
    print("✅ 2. Human-readable Eligibility Explanations")  
    print("✅ 3. Personalized Learning Roadmap Generator")
    print()
    print("🚀 Your project now stands out with intelligent, explainable AI!")

if __name__ == "__main__":
    test_enhanced_features()
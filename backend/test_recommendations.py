"""
Test Learning Recommendations Display
Verify that learning recommendations and roadmaps are showing in the web interface
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_recommendations():
    print("🎯 TESTING LEARNING RECOMMENDATIONS DISPLAY")
    print("=" * 60)
    
    # Test resume with some skills but missing key ones
    test_resume = """
    JOHN SMITH
    Junior Software Developer
    
    EXPERIENCE:
    • 2 years of experience in basic web development
    • Familiar with HTML, CSS, and JavaScript
    • Some experience with Python programming
    • Built simple web applications using basic frameworks
    
    SKILLS:
    HTML, CSS, JavaScript, Python (basic), Git (basic)
    
    EDUCATION:
    Bachelor's in Computer Science
    """
    
    print("👤 Test Profile (Junior Developer):")
    print("- Experience: 2 years basic web development")
    print("- Skills: HTML, CSS, JavaScript, Python (basic), Git")
    print("- Missing: Advanced frameworks, databases, cloud, ML")
    print()
    
    # Test multi-company analysis to see recommendations
    print("🤖 Testing Multi-Company Analysis with Recommendations")
    print("-" * 50)
    
    try:
        response = requests.post(f"{BASE_URL}/analyze-all", json={
            "resume_text": test_resume
        })
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ Multi-Company Analysis Complete!")
            print(f"🏢 Analyzed {result['total_companies']} companies")
            print()
            
            # Check first few companies for recommendations
            for i, company_result in enumerate(result['company_analysis'][:3]):
                company = company_result['company']
                ml_analysis = company_result['ml_analysis']
                
                print(f"🏢 {i+1}. {company}")
                print(f"   ML Score: {ml_analysis['ml_eligibility_score']}%")
                print(f"   Level: {ml_analysis['eligibility_level']}")
                
                # Check for missing skills
                if 'skill_readiness_levels' in ml_analysis and 'Missing' in ml_analysis['skill_readiness_levels']:
                    missing_skills = ml_analysis['skill_readiness_levels']['Missing']
                    print(f"   ❌ Missing Skills ({len(missing_skills)}): {[skill['skill'] for skill in missing_skills[:5]]}")
                
                # Check for learning recommendations
                if 'learning_recommendations' in ml_analysis and ml_analysis['learning_recommendations']:
                    recommendations = ml_analysis['learning_recommendations']
                    print(f"   💡 Learning Recommendations ({len(recommendations)} skills):")
                    
                    for skill, platforms in list(recommendations.items())[:3]:
                        print(f"      📚 {skill}:")
                        print(f"         🆓 Free: {', '.join(platforms['free'][:2])}")
                        print(f"         💰 Paid: {', '.join(platforms['paid'][:2])}")
                else:
                    print("   ⚠️ No learning recommendations found")
                
                # Check for learning roadmap
                if 'learning_roadmap' in ml_analysis and ml_analysis['learning_roadmap']['learning_path']:
                    roadmap = ml_analysis['learning_roadmap']
                    print(f"   🗺️ Learning Roadmap ({roadmap['estimated_duration']}):")
                    
                    for phase in roadmap['learning_path'][:2]:
                        print(f"      Phase {phase['phase']}: {phase['title']} ({phase['estimated_time']})")
                        print(f"         Skills: {', '.join(phase['skills'][:3])}")
                else:
                    print("   ⚠️ No learning roadmap found")
                
                print()
                
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test single company analysis for detailed recommendations
    print("🎯 Testing Single Company Analysis (Google)")
    print("-" * 50)
    
    try:
        response = requests.post(f"{BASE_URL}/ml-analyze", json={
            "resume_text": test_resume,
            "company": "Google"
        })
        
        if response.status_code == 200:
            result = response.json()
            ml_analysis = result['ml_analysis']
            
            print("✅ Single Company Analysis Complete!")
            print(f"🎯 Company: {result['company']}")
            print(f"🤖 ML Score: {ml_analysis['ml_eligibility_score']}%")
            print()
            
            # Detailed recommendations check
            if 'learning_recommendations' in ml_analysis and ml_analysis['learning_recommendations']:
                recommendations = ml_analysis['learning_recommendations']
                print(f"💡 Detailed Learning Recommendations ({len(recommendations)} skills):")
                
                for skill, platforms in recommendations.items():
                    print(f"   📚 {skill.title()}:")
                    print(f"      🆓 Free Platforms: {', '.join(platforms['free'][:3])}")
                    print(f"      💰 Paid Platforms: {', '.join(platforms['paid'][:3])}")
                    print()
            else:
                print("⚠️ No detailed learning recommendations found")
            
            # Detailed roadmap check
            if 'learning_roadmap' in ml_analysis and ml_analysis['learning_roadmap']['learning_path']:
                roadmap = ml_analysis['learning_roadmap']
                print(f"🗺️ Detailed Learning Roadmap:")
                print(f"   Total Skills: {roadmap['total_skills']}")
                print(f"   Duration: {roadmap['estimated_duration']}")
                print()
                
                for phase in roadmap['learning_path']:
                    print(f"   Phase {phase['phase']}: {phase['title']}")
                    print(f"      Description: {phase['description']}")
                    print(f"      Duration: {phase['estimated_time']}")
                    print(f"      Priority: {phase['priority']}")
                    print(f"      Skills: {', '.join(phase['skills'])}")
                    print()
            else:
                print("⚠️ No detailed learning roadmap found")
                
        else:
            print(f"❌ Single company analysis failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("🎉 RECOMMENDATIONS TESTING COMPLETE!")
    print()
    print("🌟 WHAT TO EXPECT IN WEB INTERFACE:")
    print("✅ 1. Missing Skills section with red skill tags")
    print("✅ 2. Learning Recommendations with free/paid platforms")
    print("✅ 3. Learning Roadmap with phases and timelines")
    print("✅ 4. 'View Detailed Analysis' buttons for each company")
    print("✅ 5. Comprehensive recommendations for skill gaps")
    print()
    print("🌐 Visit http://localhost:5000 to see the enhanced interface!")

if __name__ == "__main__":
    test_recommendations()
"""
Test script for the Resume-Based Company Eligibility System
"""

from utils.skill_extractor import SkillExtractor
from utils.eligibility_calculator import EligibilityCalculator
from database.db_utils import get_job_requirements, get_all_companies

def test_skill_extraction():
    """Test skill extraction functionality"""
    print("=== Testing Skill Extraction ===")
    
    # Sample resume text
    sample_resume = """
    John Doe
    Software Developer
    
    Experience:
    - 3 years of experience in Python development
    - Worked with Django and Flask frameworks
    - Experience with MySQL and PostgreSQL databases
    - Familiar with React and JavaScript
    - Used Git for version control
    - Deployed applications on AWS
    
    Skills:
    Python, Java, JavaScript, React, Node.js, MySQL, PostgreSQL, 
    Git, AWS, Docker, HTML, CSS
    
    Education:
    Bachelor's in Computer Science
    """
    
    extractor = SkillExtractor()
    
    # Extract skills
    skills = extractor.extract_all_skills_flat(sample_resume)
    categorized_skills = extractor.extract_skills_keyword_matching(sample_resume)
    experience_years = extractor.extract_experience_years(sample_resume)
    
    print(f"Skills found: {skills}")
    print(f"Categorized skills: {categorized_skills}")
    print(f"Experience years: {experience_years}")
    print()

def test_eligibility_calculation():
    """Test eligibility calculation"""
    print("=== Testing Eligibility Calculation ===")
    
    # Sample data
    resume_skills = ['python', 'django', 'mysql', 'react', 'git', 'aws']
    resume_experience = [3]
    
    # Get job requirements for a company
    companies = get_all_companies()
    if companies:
        company = companies[0]  # Test with first company
        job_requirements = get_job_requirements(company)
        
        if job_requirements:
            calculator = EligibilityCalculator()
            analysis = calculator.calculate_overall_eligibility(
                resume_skills, resume_experience, job_requirements
            )
            
            print(f"Company: {company}")
            print(f"Analysis: {analysis}")
        else:
            print(f"No job requirements found for {company}")
    else:
        print("No companies found in database")
    print()

def test_database_connection():
    """Test database connectivity"""
    print("=== Testing Database Connection ===")
    
    companies = get_all_companies()
    print(f"Companies in database: {companies}")
    
    if companies:
        # Test getting requirements for first company
        company = companies[0]
        requirements = get_job_requirements(company)
        print(f"Requirements for {company}: {requirements}")
    print()

if __name__ == "__main__":
    print("Starting System Tests...\n")
    
    try:
        test_database_connection()
        test_skill_extraction()
        test_eligibility_calculation()
        print("All tests completed successfully!")
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()
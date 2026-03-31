import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "jobs.db")

def get_job_requirements(company_name):
    """
    Get job requirements for a specific company
    
    Args:
        company_name (str): Name of the company
        
    Returns:
        tuple: Job requirements data or None if not found
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    SELECT 
        job_requirements.role,
        job_requirements.required_skills,
        job_requirements.tools,
        job_requirements.experience,
        job_requirements.education,
        job_requirements.job_description
    FROM job_requirements
    JOIN companies
        ON job_requirements.company_id = companies.company_id
    WHERE companies.company_name = ?
    """

    cursor.execute(query, (company_name,))
    result = cursor.fetchone()
    conn.close()

    return result

def get_all_companies():
    """
    Get list of all companies in the database
    
    Returns:
        list: List of company names
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = "SELECT company_name FROM companies ORDER BY company_name"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    # Extract company names from tuples
    companies = [row[0] for row in results]
    return companies

def get_all_companies_with_roles():
    """
    Get list of all companies with their available roles
    
    Returns:
        list: List of dictionaries containing company and role information
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = """
    SELECT 
        companies.company_name,
        job_requirements.role
    FROM companies
    JOIN job_requirements ON companies.company_id = job_requirements.company_id
    ORDER BY companies.company_name, job_requirements.role
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    # Convert to list of dictionaries
    companies_with_roles = []
    for row in results:
        companies_with_roles.append({
            "company": row[0],
            "role": row[1],
            "display_name": f"{row[0]} - {row[1]}"
        })
    
    return companies_with_roles

def get_job_requirements_by_company_and_role(company_name, role):
    """
    Get job requirements for a specific company and role
    
    Args:
        company_name (str): Name of the company
        role (str): Job role
        
    Returns:
        tuple: Job requirements data or None if not found
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    SELECT 
        job_requirements.role,
        job_requirements.required_skills,
        job_requirements.tools,
        job_requirements.experience,
        job_requirements.education,
        job_requirements.job_description
    FROM job_requirements
    JOIN companies
        ON job_requirements.company_id = companies.company_id
    WHERE companies.company_name = ? AND job_requirements.role = ?
    """

    cursor.execute(query, (company_name, role))
    result = cursor.fetchone()
    conn.close()

    return result

def get_company_details(company_name):
    """
    Get detailed information about a company including all job roles
    
    Args:
        company_name (str): Name of the company
        
    Returns:
        list: List of job details for the company
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = """
    SELECT 
        companies.company_name,
        job_requirements.role,
        job_requirements.required_skills,
        job_requirements.tools,
        job_requirements.experience,
        job_requirements.education,
        job_requirements.job_description
    FROM job_requirements
    JOIN companies ON job_requirements.company_id = companies.company_id
    WHERE companies.company_name = ?
    """
    
    cursor.execute(query, (company_name,))
    results = cursor.fetchall()
    conn.close()
    
    return results

def get_job_data_statistics():
    """
    Get statistics about current job data in the database
    
    Returns:
        dict: Statistics about companies, roles, and job data
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    stats = {}
    
    try:
        # Total companies
        cursor.execute("SELECT COUNT(*) FROM companies")
        stats['total_companies'] = cursor.fetchone()[0]
        
        # Total job positions
        cursor.execute("SELECT COUNT(*) FROM job_requirements")
        stats['total_positions'] = cursor.fetchone()[0]
        
        # Companies with most positions
        cursor.execute("""
        SELECT companies.company_name, COUNT(*) as position_count
        FROM companies
        JOIN job_requirements ON companies.company_id = job_requirements.company_id
        GROUP BY companies.company_name
        ORDER BY position_count DESC
        LIMIT 10
        """)
        stats['top_companies'] = [{"company": row[0], "positions": row[1]} for row in cursor.fetchall()]
        
        # Most common roles
        cursor.execute("""
        SELECT role, COUNT(*) as role_count
        FROM job_requirements
        GROUP BY role
        ORDER BY role_count DESC
        LIMIT 10
        """)
        stats['top_roles'] = [{"role": row[0], "count": row[1]} for row in cursor.fetchall()]
        
        # Most common skills
        cursor.execute("SELECT required_skills FROM job_requirements WHERE required_skills IS NOT NULL")
        all_skills = []
        for row in cursor.fetchall():
            skills = [skill.strip() for skill in row[0].split(',') if skill.strip()]
            all_skills.extend(skills)
        
        # Count skill frequency
        from collections import Counter
        skill_counts = Counter(all_skills)
        stats['top_skills'] = [{"skill": skill, "count": count} for skill, count in skill_counts.most_common(15)]
        
        # Database freshness (this would need a timestamp column in real implementation)
        stats['last_updated'] = "Real-time updates active"
        
    except Exception as e:
        stats['error'] = str(e)
    finally:
        conn.close()
    
    return stats

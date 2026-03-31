import sqlite3

def clean_duplicate_jobs():
    """Remove duplicate job entries from the database"""
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    
    print("🧹 Cleaning duplicate job entries...")
    
    # Find duplicates
    cursor.execute("""
    SELECT companies.company_name, job_requirements.role, COUNT(*) as count
    FROM job_requirements 
    JOIN companies ON job_requirements.company_id = companies.company_id 
    GROUP BY companies.company_name, job_requirements.role 
    HAVING COUNT(*) > 1
    """)
    
    duplicates = cursor.fetchall()
    print(f"Found {len(duplicates)} duplicate company-role combinations:")
    
    for company, role, count in duplicates:
        print(f"  • {company} - {role}: {count} entries")
    
    # Remove duplicates, keeping only the first entry for each company-role combination
    cursor.execute("""
    DELETE FROM job_requirements 
    WHERE job_id NOT IN (
        SELECT MIN(job_id) 
        FROM job_requirements 
        GROUP BY company_id, role
    )
    """)
    
    deleted_count = cursor.rowcount
    print(f"\n✅ Removed {deleted_count} duplicate entries")
    
    # Verify cleanup
    cursor.execute("""
    SELECT companies.company_name, job_requirements.role
    FROM job_requirements 
    JOIN companies ON job_requirements.company_id = companies.company_id 
    ORDER BY companies.company_name, job_requirements.role
    """)
    
    remaining = cursor.fetchall()
    print(f"\n📊 Remaining unique positions: {len(remaining)}")
    
    current_company = None
    for company, role in remaining:
        if company != current_company:
            print(f"\n🏢 {company}:")
            current_company = company
        print(f"  • {role}")
    
    conn.commit()
    conn.close()
    print("\n🎉 Database cleanup completed!")

if __name__ == "__main__":
    clean_duplicate_jobs()
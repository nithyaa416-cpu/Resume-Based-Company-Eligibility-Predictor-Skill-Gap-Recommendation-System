import sqlite3

# Connect to database (creates file if not exists)
conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

# Create companies table
cursor.execute("""
CREATE TABLE IF NOT EXISTS companies (
    company_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT UNIQUE
)
""")

# Create job requirements table
cursor.execute("""
CREATE TABLE IF NOT EXISTS job_requirements (
    job_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    role TEXT,
    required_skills TEXT,
    tools TEXT,
    experience TEXT,
    education TEXT,
    job_description TEXT,
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
)
""")

conn.commit()
conn.close()

print("Database & tables created successfully")

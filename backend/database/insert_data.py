import sqlite3

conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

# Insert company
cursor.execute(
    "INSERT OR IGNORE INTO companies (company_name) VALUES (?)",
    ("Google",)
)

# Get company_id
cursor.execute(
    "SELECT company_id FROM companies WHERE company_name = ?",
    ("Google",)
)
company_id = cursor.fetchone()[0]

# Insert job requirement
cursor.execute("""
INSERT INTO job_requirements
(company_id, role, required_skills, tools, experience, education, job_description)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    company_id,
    "Machine Learning Engineer",
    "Python, Machine Learning, NLP, SQL",
    "TensorFlow, PyTorch",
    "0-2 years",
    "BTech / MCA",
    "Build and deploy machine learning models."
))

conn.commit()
conn.close()

print("Job data inserted successfully")

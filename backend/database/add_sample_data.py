import sqlite3

conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

# Sample companies and roles data
companies_data = [
    {
        "company": "Google",
        "roles": [
            {
                "role": "Software Engineer",
                "required_skills": "Python, Java, JavaScript, Data Structures, Algorithms",
                "tools": "Git, Docker, Kubernetes, GCP",
                "experience": "0-3 years",
                "education": "BTech/MTech in Computer Science",
                "job_description": "Develop scalable software solutions and work on cutting-edge technologies."
            },
            {
                "role": "Machine Learning Engineer",
                "required_skills": "Python, Machine Learning, NLP, SQL, Statistics",
                "tools": "TensorFlow, PyTorch, Scikit-learn",
                "experience": "1-4 years",
                "education": "BTech/MTech in Computer Science or related field",
                "job_description": "Build and deploy machine learning models at scale."
            }
        ]
    },
    {
        "company": "Microsoft",
        "roles": [
            {
                "role": "Software Developer",
                "required_skills": "C#, .NET, JavaScript, SQL, Azure",
                "tools": "Visual Studio, Azure DevOps, Git",
                "experience": "0-2 years",
                "education": "BTech in Computer Science",
                "job_description": "Develop enterprise software solutions using Microsoft technologies."
            },
            {
                "role": "Data Scientist",
                "required_skills": "Python, R, Machine Learning, Statistics, SQL",
                "tools": "Azure ML, Power BI, Jupyter",
                "experience": "2-5 years",
                "education": "MTech/PhD in Data Science or related field",
                "job_description": "Analyze complex data to drive business insights and decisions."
            }
        ]
    },
    {
        "company": "Amazon",
        "roles": [
            {
                "role": "Backend Developer",
                "required_skills": "Java, Python, AWS, Microservices, REST APIs",
                "tools": "AWS, Docker, Jenkins, Git",
                "experience": "1-3 years",
                "education": "BTech in Computer Science",
                "job_description": "Build scalable backend systems for e-commerce platform."
            },
            {
                "role": "DevOps Engineer",
                "required_skills": "AWS, Docker, Kubernetes, CI/CD, Linux",
                "tools": "Jenkins, Terraform, CloudFormation",
                "experience": "2-4 years",
                "education": "BTech in Computer Science or related field",
                "job_description": "Manage cloud infrastructure and deployment pipelines."
            }
        ]
    },
    {
        "company": "Meta",
        "roles": [
            {
                "role": "Frontend Developer",
                "required_skills": "React, JavaScript, HTML, CSS, TypeScript",
                "tools": "React, Redux, Webpack, Git",
                "experience": "1-3 years",
                "education": "BTech in Computer Science",
                "job_description": "Build user interfaces for social media platforms."
            },
            {
                "role": "Full Stack Developer",
                "required_skills": "React, Node.js, JavaScript, Python, SQL",
                "tools": "React, Express, MongoDB, Git",
                "experience": "2-5 years",
                "education": "BTech/MTech in Computer Science",
                "job_description": "Develop end-to-end web applications for social platforms."
            }
        ]
    }
]

# Insert companies and job requirements
for company_data in companies_data:
    company_name = company_data["company"]
    
    # Insert company (ignore if exists)
    cursor.execute(
        "INSERT OR IGNORE INTO companies (company_name) VALUES (?)",
        (company_name,)
    )
    
    # Get company_id
    cursor.execute(
        "SELECT company_id FROM companies WHERE company_name = ?",
        (company_name,)
    )
    company_id = cursor.fetchone()[0]
    
    # Insert job requirements for each role
    for role_data in company_data["roles"]:
        cursor.execute("""
        INSERT OR IGNORE INTO job_requirements
        (company_id, role, required_skills, tools, experience, education, job_description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            company_id,
            role_data["role"],
            role_data["required_skills"],
            role_data["tools"],
            role_data["experience"],
            role_data["education"],
            role_data["job_description"]
        ))

conn.commit()
conn.close()

print("Sample data inserted successfully!")
print("Companies added: Google, Microsoft, Amazon, Meta")
print("Total roles added: 8")
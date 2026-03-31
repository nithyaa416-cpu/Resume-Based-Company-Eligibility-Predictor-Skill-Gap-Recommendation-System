# Resume-Based Company Eligibility System - API Documentation

## Base URL
```
http://localhost:5000
```

## Endpoints

### 1. Home - System Information
**GET** `/`

Returns basic system information and available endpoints.

**Response:**
```json
{
    "message": "Resume-Based Company Eligibility System API",
    "status": "OK",
    "version": "1.0",
    "endpoints": [...]
}
```

### 2. Get All Companies
**GET** `/companies`

Returns list of all companies in the database.

**Response:**
```json
{
    "status": "success",
    "companies": ["Amazon", "Google", "Microsoft", ...]
}
```

### 3. Upload Resume
**POST** `/upload`

Upload a resume file (PDF/DOCX) and extract skills.

**Request:**
- Content-Type: `multipart/form-data`
- Body: Form data with `resume` file field

**Response:**
```json
{
    "status": "success",
    "message": "Resume processed successfully",
    "data": {
        "filename": "resume.pdf",
        "text_length": 1250,
        "skills_found": 12,
        "skills": ["python", "java", "react", ...],
        "categorized_skills": {
            "programming_languages": ["python", "java"],
            "web_technologies": ["react", "html", "css"],
            ...
        },
        "experience_years": [3, 2],
        "resume_text": "John Doe Software Developer..."
    }
}
```

### 4. Analyze Resume Against Specific Company
**POST** `/analyze`

Analyze resume text against a specific company's requirements.

**Request:**
```json
{
    "resume_text": "John Doe Software Developer with 3 years experience...",
    "company": "Google"
}
```

**Response:**
```json
{
    "status": "success",
    "company": "Google",
    "analysis": {
        "role": "Software Engineer",
        "overall_score": 75.5,
        "eligibility_level": "Eligible",
        "skill_analysis": {
            "score": 8,
            "total_required": 12,
            "matched_skills": ["python", "java", "react", ...],
            "missing_skills": ["kubernetes", "tensorflow", ...],
            "match_percentage": 66.67
        },
        "experience_analysis": {
            "score": 90.0,
            "resume_experience": 3,
            "required_experience": 2,
            "message": "Meets requirement (3 >= 2 years)"
        },
        "recommendations": [
            {
                "skill": "kubernetes",
                "resource": "Learn Kubernetes: Official Kubernetes Tutorial"
            },
            ...
        ]
    },
    "resume_skills": ["python", "java", ...],
    "resume_experience": [3]
}
```

### 5. Analyze Resume Against All Companies
**POST** `/analyze-all`

Analyze resume against all companies and return ranked results.

**Request:**
```json
{
    "resume_text": "John Doe Software Developer with 3 years experience..."
}
```

**Response:**
```json
{
    "status": "success",
    "total_companies": 10,
    "resume_skills": ["python", "java", ...],
    "resume_experience": [3],
    "company_analysis": [
        {
            "company": "Google",
            "analysis": {
                "overall_score": 85.2,
                "eligibility_level": "Highly Eligible",
                ...
            }
        },
        {
            "company": "Amazon",
            "analysis": {
                "overall_score": 72.1,
                "eligibility_level": "Eligible",
                ...
            }
        },
        ...
    ]
}
```

### 6. Get Skill Gap Recommendations
**POST** `/recommendations`

Get detailed skill gap recommendations for a specific company.

**Request:**
```json
{
    "company": "Google",
    "resume_skills": ["python", "java", "react"]
}
```

**Response:**
```json
{
    "status": "success",
    "company": "Google",
    "role": "Software Engineer",
    "skill_gap_analysis": {
        "matched_skills": ["python", "java"],
        "missing_skills": ["kubernetes", "tensorflow", "docker"],
        "match_percentage": 40.0
    },
    "recommendations": [
        {
            "skill": "kubernetes",
            "resource": "Learn Kubernetes: Official Kubernetes Tutorial"
        },
        {
            "skill": "tensorflow",
            "resource": "Learn TensorFlow: TensorFlow Official Tutorial"
        },
        ...
    ]
}
```

## Error Responses

All endpoints return error responses in the following format:

```json
{
    "status": "error",
    "message": "Error description"
}
```

Common HTTP status codes:
- `400` - Bad Request (missing required fields)
- `404` - Not Found (company not found)
- `500` - Internal Server Error

## File Upload Requirements

### Supported Formats
- PDF (.pdf)
- Microsoft Word (.docx, .doc)

### File Size Limits
- Maximum file size: 10MB
- Recommended: Under 5MB for better performance

## Usage Examples

### Using curl

1. **Get all companies:**
```bash
curl -X GET http://localhost:5000/companies
```

2. **Upload resume:**
```bash
curl -X POST -F "resume=@resume.pdf" http://localhost:5000/upload
```

3. **Analyze resume:**
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"resume_text":"Your resume text here","company":"Google"}' \
     http://localhost:5000/analyze
```

### Using Python requests

```python
import requests

# Upload resume
with open('resume.pdf', 'rb') as f:
    response = requests.post('http://localhost:5000/upload', 
                           files={'resume': f})
    print(response.json())

# Analyze against company
data = {
    "resume_text": "Your resume text here",
    "company": "Google"
}
response = requests.post('http://localhost:5000/analyze', json=data)
print(response.json())
```
#!/usr/bin/env python3
"""
Resume Optimizer
Provides AI-powered suggestions to improve resume content and ATS compatibility
"""

import re
import logging
from typing import Dict, List, Tuple
from collections import Counter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResumeOptimizer:
    """AI-powered resume optimization and suggestions"""
    
    def __init__(self):
        # Initialize without spacy dependency
        self.nlp = None
        logger.info("Resume Optimizer initialized (basic mode)")
    
    def analyze_resume_structure(self, resume_text: str) -> Dict:
        """Analyze resume structure and provide improvement suggestions"""
        
        analysis = {
            "structure_score": 0,
            "suggestions": [],
            "sections_found": [],
            "missing_sections": [],
            "word_count": len(resume_text.split()),
            "character_count": len(resume_text)
        }
        
        # Check for essential sections
        essential_sections = {
            "contact": ["email", "phone", "linkedin", "github"],
            "summary": ["summary", "objective", "profile"],
            "experience": ["experience", "work", "employment", "career"],
            "education": ["education", "degree", "university", "college"],
            "skills": ["skills", "technical", "technologies", "tools"],
            "projects": ["projects", "portfolio", "work samples"]
        }
        
        resume_lower = resume_text.lower()
        
        for section, keywords in essential_sections.items():
            if any(keyword in resume_lower for keyword in keywords):
                analysis["sections_found"].append(section)
                analysis["structure_score"] += 15
            else:
                analysis["missing_sections"].append(section)
        
        # Generate structure suggestions
        if "contact" not in analysis["sections_found"]:
            analysis["suggestions"].append({
                "type": "critical",
                "category": "structure",
                "title": "Add Contact Information",
                "description": "Include email, phone, and LinkedIn profile at the top",
                "impact": "high"
            })
        
        if "summary" not in analysis["sections_found"]:
            analysis["suggestions"].append({
                "type": "important",
                "category": "structure", 
                "title": "Add Professional Summary",
                "description": "Include a 2-3 line summary highlighting your key strengths",
                "impact": "medium"
            })
        
        if "skills" not in analysis["sections_found"]:
            analysis["suggestions"].append({
                "type": "critical",
                "category": "structure",
                "title": "Add Skills Section",
                "description": "List your technical skills and tools prominently",
                "impact": "high"
            })
        
        # Word count analysis
        if analysis["word_count"] < 200:
            analysis["suggestions"].append({
                "type": "important",
                "category": "content",
                "title": "Expand Resume Content",
                "description": f"Resume is too short ({analysis['word_count']} words). Aim for 300-600 words.",
                "impact": "medium"
            })
        elif analysis["word_count"] > 800:
            analysis["suggestions"].append({
                "type": "warning",
                "category": "content",
                "title": "Consider Shortening Resume",
                "description": f"Resume is quite long ({analysis['word_count']} words). Consider condensing to 400-600 words.",
                "impact": "low"
            })
        
        return analysis
    
    def analyze_ats_compatibility(self, resume_text: str) -> Dict:
        """Analyze ATS (Applicant Tracking System) compatibility"""
        
        ats_score = 0
        suggestions = []
        
        # Check for ATS-friendly formatting
        issues = []
        
        # Check for problematic characters
        problematic_chars = ['•', '→', '★', '◆', '▪', '▫']
        found_chars = [char for char in problematic_chars if char in resume_text]
        
        if found_chars:
            issues.append("Special characters detected")
            suggestions.append({
                "type": "warning",
                "category": "ats",
                "title": "Replace Special Characters",
                "description": f"Replace special characters ({', '.join(found_chars)}) with standard bullets (-) or asterisks (*)",
                "impact": "medium"
            })
        else:
            ats_score += 20
        
        # Check for standard section headers
        standard_headers = ["experience", "education", "skills", "summary", "work history"]
        header_score = 0
        
        for header in standard_headers:
            if header in resume_text.lower():
                header_score += 1
        
        if header_score >= 3:
            ats_score += 25
        else:
            suggestions.append({
                "type": "important",
                "category": "ats",
                "title": "Use Standard Section Headers",
                "description": "Use clear, standard headers like 'Experience', 'Education', 'Skills'",
                "impact": "high"
            })
        
        # Check for contact information format
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        
        if re.search(email_pattern, resume_text):
            ats_score += 15
        else:
            suggestions.append({
                "type": "critical",
                "category": "ats",
                "title": "Add Email Address",
                "description": "Include a professional email address in standard format",
                "impact": "high"
            })
        
        if re.search(phone_pattern, resume_text):
            ats_score += 15
        else:
            suggestions.append({
                "type": "important",
                "category": "ats",
                "title": "Add Phone Number",
                "description": "Include phone number in standard format (XXX) XXX-XXXX",
                "impact": "medium"
            })
        
        # Check for keywords density
        word_count = len(resume_text.split())
        if word_count > 0:
            # Simple keyword density check
            tech_keywords = ['python', 'javascript', 'react', 'sql', 'aws', 'docker', 'git']
            keyword_count = sum(1 for word in resume_text.lower().split() if word in tech_keywords)
            keyword_density = (keyword_count / word_count) * 100
            
            if keyword_density < 2:
                suggestions.append({
                    "type": "important",
                    "category": "ats",
                    "title": "Increase Relevant Keywords",
                    "description": "Include more industry-specific keywords and technical terms",
                    "impact": "high"
                })
            else:
                ats_score += 25
        
        return {
            "ats_score": min(ats_score, 100),
            "suggestions": suggestions,
            "issues": issues
        }
    
    def suggest_skill_improvements(self, resume_text: str, target_role: str = None) -> Dict:
        """Suggest skill improvements based on market trends"""
        
        # Current market hot skills (2024-2025)
        hot_skills_by_role = {
            "ai engineer": ["Python", "PyTorch", "TensorFlow", "LangChain", "Vector Databases", "Transformers"],
            "ml engineer": ["Python", "MLOps", "Kubeflow", "Apache Airflow", "Docker", "Kubernetes"],
            "software engineer": ["Python", "JavaScript", "TypeScript", "System Design", "Microservices", "Cloud"],
            "frontend engineer": ["React", "TypeScript", "Next.js", "Tailwind CSS", "Vite", "Testing"],
            "backend engineer": ["Python", "Go", "Microservices", "PostgreSQL", "Redis", "Docker"],
            "full stack engineer": ["React", "Node.js", "TypeScript", "PostgreSQL", "Docker", "AWS"],
            "devops engineer": ["Kubernetes", "Terraform", "CI/CD", "AWS", "Monitoring", "Security"],
            "data scientist": ["Python", "R", "Machine Learning", "SQL", "Statistics", "Visualization"],
            "product manager": ["Analytics", "A/B Testing", "User Research", "Roadmapping", "Stakeholder Management"]
        }
        
        # Extract current skills from resume
        current_skills = self._extract_skills_from_text(resume_text)
        
        suggestions = []
        
        if target_role:
            role_key = target_role.lower()
            if role_key in hot_skills_by_role:
                recommended_skills = hot_skills_by_role[role_key]
                missing_skills = [skill for skill in recommended_skills if skill.lower() not in [s.lower() for s in current_skills]]
                
                if missing_skills:
                    suggestions.append({
                        "type": "important",
                        "category": "skills",
                        "title": f"Add {target_role} Skills",
                        "description": f"Consider adding these in-demand skills: {', '.join(missing_skills[:3])}",
                        "impact": "high",
                        "skills": missing_skills
                    })
        
        # General trending skills
        trending_2024 = ["AI/ML", "TypeScript", "Kubernetes", "Terraform", "Next.js", "GraphQL", "Rust", "Go"]
        missing_trending = [skill for skill in trending_2024 if skill.lower() not in [s.lower() for s in current_skills]]
        
        if missing_trending:
            suggestions.append({
                "type": "suggestion",
                "category": "skills",
                "title": "Consider Trending Technologies",
                "description": f"These technologies are trending in 2024: {', '.join(missing_trending[:3])}",
                "impact": "medium",
                "skills": missing_trending
            })
        
        return {
            "current_skills": current_skills,
            "suggestions": suggestions,
            "skill_count": len(current_skills)
        }
    
    def suggest_content_improvements(self, resume_text: str) -> Dict:
        """Suggest content improvements for better impact"""
        
        suggestions = []
        
        # Check for action verbs
        weak_verbs = ["responsible for", "worked on", "helped with", "assisted", "involved in"]
        strong_verbs = ["developed", "implemented", "designed", "optimized", "led", "created", "built", "improved"]
        
        resume_lower = resume_text.lower()
        weak_verb_count = sum(1 for verb in weak_verbs if verb in resume_lower)
        strong_verb_count = sum(1 for verb in strong_verbs if verb in resume_lower)
        
        if weak_verb_count > strong_verb_count:
            suggestions.append({
                "type": "important",
                "category": "content",
                "title": "Use Stronger Action Verbs",
                "description": "Replace weak phrases like 'responsible for' with strong action verbs like 'developed', 'implemented', 'led'",
                "impact": "high"
            })
        
        # Check for quantifiable achievements
        number_pattern = r'\b\d+(?:\.\d+)?(?:%|k|K|million|billion|x|times)?\b'
        numbers_found = len(re.findall(number_pattern, resume_text))
        
        if numbers_found < 3:
            suggestions.append({
                "type": "important",
                "category": "content",
                "title": "Add Quantifiable Achievements",
                "description": "Include specific numbers, percentages, or metrics to demonstrate impact (e.g., 'Improved performance by 30%')",
                "impact": "high"
            })
        
        # Check for buzzwords to avoid
        buzzwords = ["synergy", "leverage", "paradigm", "disruptive", "innovative", "cutting-edge"]
        found_buzzwords = [word for word in buzzwords if word in resume_lower]
        
        if found_buzzwords:
            suggestions.append({
                "type": "warning",
                "category": "content",
                "title": "Avoid Overused Buzzwords",
                "description": f"Consider replacing buzzwords ({', '.join(found_buzzwords)}) with specific, concrete terms",
                "impact": "low"
            })
        
        return {
            "suggestions": suggestions,
            "metrics": {
                "weak_verbs": weak_verb_count,
                "strong_verbs": strong_verb_count,
                "quantifiable_achievements": numbers_found,
                "buzzwords_found": len(found_buzzwords)
            }
        }
    
    def _extract_skills_from_text(self, text: str) -> List[str]:
        """Extract technical skills from resume text"""
        
        # Common technical skills to look for
        skill_patterns = [
            # Programming languages
            r'\b(?:Python|JavaScript|TypeScript|Java|C\+\+|C#|Go|Rust|PHP|Ruby|Swift|Kotlin|Scala|R)\b',
            # Frameworks and libraries
            r'\b(?:React|Angular|Vue|Node\.js|Django|Flask|Spring|Express|Next\.js|Nuxt\.js)\b',
            # Databases
            r'\b(?:PostgreSQL|MySQL|MongoDB|Redis|Elasticsearch|Cassandra|DynamoDB)\b',
            # Cloud and DevOps
            r'\b(?:AWS|Azure|GCP|Docker|Kubernetes|Terraform|Ansible|Jenkins|GitLab)\b',
            # Tools and platforms
            r'\b(?:Git|GitHub|GitLab|Jira|Confluence|Slack|Figma|Adobe|Photoshop)\b'
        ]
        
        skills = []
        for pattern in skill_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills.extend(matches)
        
        # Remove duplicates and return
        return list(set(skills))
    
    def generate_comprehensive_optimization(self, resume_text: str, target_role: str = None) -> Dict:
        """Generate comprehensive resume optimization report"""
        
        logger.info(f"Generating comprehensive optimization for {len(resume_text)} character resume")
        
        # Run all analyses
        structure_analysis = self.analyze_resume_structure(resume_text)
        ats_analysis = self.analyze_ats_compatibility(resume_text)
        skill_analysis = self.suggest_skill_improvements(resume_text, target_role)
        content_analysis = self.suggest_content_improvements(resume_text)
        
        # Combine all suggestions
        all_suggestions = []
        all_suggestions.extend(structure_analysis["suggestions"])
        all_suggestions.extend(ats_analysis["suggestions"])
        all_suggestions.extend(skill_analysis["suggestions"])
        all_suggestions.extend(content_analysis["suggestions"])
        
        # Calculate overall score
        structure_score = structure_analysis["structure_score"]
        ats_score = ats_analysis["ats_score"]
        
        # Content score based on metrics
        content_metrics = content_analysis["metrics"]
        content_score = 0
        if content_metrics["strong_verbs"] > content_metrics["weak_verbs"]:
            content_score += 30
        if content_metrics["quantifiable_achievements"] >= 3:
            content_score += 40
        if content_metrics["buzzwords_found"] == 0:
            content_score += 30
        
        overall_score = (structure_score + ats_score + content_score) / 3
        
        # Prioritize suggestions
        critical_suggestions = [s for s in all_suggestions if s["type"] == "critical"]
        important_suggestions = [s for s in all_suggestions if s["type"] == "important"]
        other_suggestions = [s for s in all_suggestions if s["type"] not in ["critical", "important"]]
        
        return {
            "overall_score": round(overall_score, 1),
            "scores": {
                "structure": structure_score,
                "ats_compatibility": ats_score,
                "content_quality": content_score
            },
            "suggestions": {
                "critical": critical_suggestions,
                "important": important_suggestions,
                "other": other_suggestions,
                "total_count": len(all_suggestions)
            },
            "analysis_details": {
                "structure": structure_analysis,
                "ats": ats_analysis,
                "skills": skill_analysis,
                "content": content_analysis
            },
            "summary": {
                "sections_found": len(structure_analysis["sections_found"]),
                "missing_sections": len(structure_analysis["missing_sections"]),
                "word_count": structure_analysis["word_count"],
                "skills_identified": skill_analysis["skill_count"]
            }
        }

def main():
    """Test the resume optimizer"""
    optimizer = ResumeOptimizer()
    
    sample_resume = """
    John Doe
    Software Engineer
    
    I am a software engineer with experience in programming.
    
    Experience:
    - Worked on web applications
    - Responsible for bug fixes
    - Helped with database queries
    
    Skills: Python, JavaScript
    
    Education: Computer Science Degree
    """
    
    result = optimizer.generate_comprehensive_optimization(sample_resume, "Software Engineer")
    
    print("=== RESUME OPTIMIZATION REPORT ===")
    print(f"Overall Score: {result['overall_score']}/100")
    print(f"Critical Issues: {len(result['suggestions']['critical'])}")
    print(f"Important Suggestions: {len(result['suggestions']['important'])}")
    
    for suggestion in result['suggestions']['critical'][:3]:
        print(f"🚨 {suggestion['title']}: {suggestion['description']}")

if __name__ == "__main__":
    main()
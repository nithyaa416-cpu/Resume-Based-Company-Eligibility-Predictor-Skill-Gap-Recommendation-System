#!/usr/bin/env python3
"""
ATS (Applicant Tracking System) Analyzer
Detailed analysis of resume compatibility with ATS systems
"""

import re
import logging
from typing import Dict, List, Tuple
from collections import Counter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ATSAnalyzer:
    """Comprehensive ATS compatibility analyzer"""
    
    def __init__(self):
        logger.info("ATS Analyzer initialized")
        
        # ATS-friendly section headers
        self.standard_headers = [
            "contact", "summary", "objective", "profile", "experience", 
            "work experience", "employment", "education", "skills", 
            "technical skills", "projects", "certifications", "achievements"
        ]
        
        # Problematic formatting elements
        self.problematic_elements = {
            "special_chars": ['•', '→', '★', '◆', '▪', '▫', '◊', '✓', '✗'],
            "complex_formatting": ['tables', 'columns', 'text boxes', 'graphics'],
            "fonts": ['decorative fonts', 'script fonts', 'handwriting fonts']
        }
        
        # ATS-friendly keywords by category
        self.ats_keywords = {
            "action_verbs": [
                "achieved", "administered", "analyzed", "built", "created", "designed",
                "developed", "directed", "established", "executed", "implemented",
                "improved", "increased", "led", "managed", "optimized", "organized",
                "planned", "produced", "reduced", "resolved", "streamlined"
            ],
            "technical_skills": [
                "python", "javascript", "java", "sql", "aws", "docker", "kubernetes",
                "react", "node.js", "git", "linux", "agile", "scrum", "ci/cd"
            ],
            "soft_skills": [
                "leadership", "communication", "teamwork", "problem-solving",
                "analytical", "creative", "detail-oriented", "collaborative"
            ]
        }
    
    def calculate_ats_score(self, resume_text: str) -> Dict:
        """Calculate comprehensive ATS compatibility score"""
        
        logger.info("Calculating ATS compatibility score")
        
        score_breakdown = {
            "formatting": 0,
            "structure": 0,
            "keywords": 0,
            "contact_info": 0,
            "readability": 0
        }
        
        issues = []
        recommendations = []
        
        # 1. Formatting Analysis (25 points)
        formatting_result = self._analyze_formatting(resume_text)
        score_breakdown["formatting"] = formatting_result["score"]
        issues.extend(formatting_result["issues"])
        recommendations.extend(formatting_result["recommendations"])
        
        # 2. Structure Analysis (25 points)
        structure_result = self._analyze_structure(resume_text)
        score_breakdown["structure"] = structure_result["score"]
        issues.extend(structure_result["issues"])
        recommendations.extend(structure_result["recommendations"])
        
        # 3. Keywords Analysis (25 points)
        keywords_result = self._analyze_keywords(resume_text)
        score_breakdown["keywords"] = keywords_result["score"]
        issues.extend(keywords_result["issues"])
        recommendations.extend(keywords_result["recommendations"])
        
        # 4. Contact Information (15 points)
        contact_result = self._analyze_contact_info(resume_text)
        score_breakdown["contact_info"] = contact_result["score"]
        issues.extend(contact_result["issues"])
        recommendations.extend(contact_result["recommendations"])
        
        # 5. Readability (10 points)
        readability_result = self._analyze_readability(resume_text)
        score_breakdown["readability"] = readability_result["score"]
        issues.extend(readability_result["issues"])
        recommendations.extend(readability_result["recommendations"])
        
        # Calculate total score
        total_score = sum(score_breakdown.values())
        
        # Determine ATS compatibility level
        if total_score >= 85:
            compatibility_level = "Excellent"
            level_color = "green"
        elif total_score >= 70:
            compatibility_level = "Good"
            level_color = "blue"
        elif total_score >= 55:
            compatibility_level = "Fair"
            level_color = "yellow"
        else:
            compatibility_level = "Poor"
            level_color = "red"
        
        return {
            "total_score": total_score,
            "compatibility_level": compatibility_level,
            "level_color": level_color,
            "score_breakdown": score_breakdown,
            "issues": issues,
            "recommendations": recommendations,
            "summary": {
                "total_issues": len(issues),
                "critical_issues": len([i for i in issues if i["severity"] == "critical"]),
                "word_count": len(resume_text.split()),
                "character_count": len(resume_text)
            }
        }
    
    def _analyze_formatting(self, resume_text: str) -> Dict:
        """Analyze formatting compatibility"""
        
        score = 25  # Start with full points
        issues = []
        recommendations = []
        
        # Check for problematic special characters
        found_special_chars = []
        for char in self.problematic_elements["special_chars"]:
            if char in resume_text:
                found_special_chars.append(char)
        
        if found_special_chars:
            score -= 10
            issues.append({
                "type": "formatting",
                "severity": "medium",
                "title": "Special Characters Detected",
                "description": f"Found problematic characters: {', '.join(found_special_chars)}"
            })
            recommendations.append({
                "category": "formatting",
                "priority": "medium",
                "title": "Replace Special Characters",
                "description": "Replace special bullets and symbols with standard characters like '-' or '*'",
                "impact": "Improves ATS parsing accuracy"
            })
        
        # Check for consistent formatting
        lines = resume_text.split('\n')
        inconsistent_formatting = False
        
        # Simple check for mixed bullet styles
        bullet_styles = set()
        for line in lines:
            line = line.strip()
            if line.startswith(('•', '-', '*', '◦')):
                bullet_styles.add(line[0])
        
        if len(bullet_styles) > 2:
            score -= 5
            inconsistent_formatting = True
            issues.append({
                "type": "formatting",
                "severity": "low",
                "title": "Inconsistent Bullet Styles",
                "description": f"Multiple bullet styles detected: {', '.join(bullet_styles)}"
            })
        
        # Check for excessive capitalization
        caps_words = re.findall(r'\b[A-Z]{3,}\b', resume_text)
        if len(caps_words) > 10:
            score -= 3
            issues.append({
                "type": "formatting",
                "severity": "low",
                "title": "Excessive Capitalization",
                "description": "Too many words in ALL CAPS may confuse ATS systems"
            })
        
        return {
            "score": max(0, score),
            "issues": issues,
            "recommendations": recommendations
        }
    
    def _analyze_structure(self, resume_text: str) -> Dict:
        """Analyze resume structure for ATS compatibility"""
        
        score = 0
        issues = []
        recommendations = []
        
        resume_lower = resume_text.lower()
        
        # Check for standard section headers
        sections_found = []
        for header in self.standard_headers:
            if header in resume_lower:
                sections_found.append(header)
        
        # Score based on essential sections
        essential_sections = ["contact", "experience", "education", "skills"]
        found_essential = 0
        
        for section in essential_sections:
            section_keywords = {
                "contact": ["email", "phone", "linkedin"],
                "experience": ["experience", "work", "employment"],
                "education": ["education", "degree", "university"],
                "skills": ["skills", "technical", "technologies"]
            }
            
            if any(keyword in resume_lower for keyword in section_keywords[section]):
                found_essential += 1
                score += 6  # 6 points per essential section
        
        # Bonus points for additional sections
        additional_sections = ["summary", "projects", "certifications"]
        for section in additional_sections:
            if section in resume_lower:
                score += 1
        
        # Check section order (logical flow)
        section_order_score = self._check_section_order(resume_text)
        score += section_order_score
        
        # Issues and recommendations
        missing_essential = 4 - found_essential
        if missing_essential > 0:
            issues.append({
                "type": "structure",
                "severity": "critical" if missing_essential > 2 else "medium",
                "title": f"Missing Essential Sections",
                "description": f"Missing {missing_essential} essential sections"
            })
            
            recommendations.append({
                "category": "structure",
                "priority": "high",
                "title": "Add Missing Sections",
                "description": "Include Contact, Experience, Education, and Skills sections",
                "impact": "Critical for ATS parsing"
            })
        
        if len(sections_found) < 4:
            recommendations.append({
                "category": "structure",
                "priority": "medium",
                "title": "Use Clear Section Headers",
                "description": "Use standard headers like 'Experience', 'Education', 'Skills'",
                "impact": "Helps ATS identify and categorize information"
            })
        
        return {
            "score": min(25, score),
            "issues": issues,
            "recommendations": recommendations
        }
    
    def _analyze_keywords(self, resume_text: str) -> Dict:
        """Analyze keyword density and relevance"""
        
        score = 0
        issues = []
        recommendations = []
        
        resume_lower = resume_text.lower()
        words = resume_lower.split()
        total_words = len(words)
        
        if total_words == 0:
            return {"score": 0, "issues": [], "recommendations": []}
        
        # Count action verbs
        action_verb_count = sum(1 for word in words if word in self.ats_keywords["action_verbs"])
        action_verb_density = (action_verb_count / total_words) * 100
        
        if action_verb_density >= 3:
            score += 10
        elif action_verb_density >= 1.5:
            score += 7
        elif action_verb_density >= 0.5:
            score += 4
        else:
            issues.append({
                "type": "keywords",
                "severity": "medium",
                "title": "Low Action Verb Usage",
                "description": f"Only {action_verb_density:.1f}% action verbs found"
            })
        
        # Count technical skills
        tech_skill_count = sum(1 for word in words if word in self.ats_keywords["technical_skills"])
        tech_skill_density = (tech_skill_count / total_words) * 100
        
        if tech_skill_density >= 2:
            score += 10
        elif tech_skill_density >= 1:
            score += 7
        elif tech_skill_density >= 0.5:
            score += 4
        else:
            issues.append({
                "type": "keywords",
                "severity": "high",
                "title": "Insufficient Technical Keywords",
                "description": f"Only {tech_skill_density:.1f}% technical keywords found"
            })
        
        # Count soft skills
        soft_skill_count = sum(1 for word in words if word in self.ats_keywords["soft_skills"])
        if soft_skill_count >= 3:
            score += 5
        elif soft_skill_count >= 1:
            score += 3
        
        # Recommendations
        if action_verb_density < 2:
            recommendations.append({
                "category": "keywords",
                "priority": "high",
                "title": "Increase Action Verbs",
                "description": "Use more action verbs like 'developed', 'implemented', 'led'",
                "impact": "Improves ATS keyword matching"
            })
        
        if tech_skill_density < 1.5:
            recommendations.append({
                "category": "keywords",
                "priority": "high",
                "title": "Add Technical Keywords",
                "description": "Include more industry-specific technical terms and tools",
                "impact": "Essential for technical role matching"
            })
        
        return {
            "score": min(25, score),
            "issues": issues,
            "recommendations": recommendations
        }
    
    def _analyze_contact_info(self, resume_text: str) -> Dict:
        """Analyze contact information completeness"""
        
        score = 0
        issues = []
        recommendations = []
        
        # Email check
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.search(email_pattern, resume_text):
            score += 5
        else:
            issues.append({
                "type": "contact",
                "severity": "critical",
                "title": "Missing Email Address",
                "description": "No email address found"
            })
            recommendations.append({
                "category": "contact",
                "priority": "critical",
                "title": "Add Email Address",
                "description": "Include a professional email address",
                "impact": "Essential for recruiter contact"
            })
        
        # Phone check
        phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        if re.search(phone_pattern, resume_text):
            score += 5
        else:
            issues.append({
                "type": "contact",
                "severity": "medium",
                "title": "Missing Phone Number",
                "description": "No phone number found"
            })
        
        # LinkedIn check
        linkedin_patterns = [
            r'linkedin\.com/in/[\w-]+',
            r'linkedin\.com/pub/[\w-]+',
            r'linkedin'
        ]
        
        if any(re.search(pattern, resume_text.lower()) for pattern in linkedin_patterns):
            score += 3
        else:
            recommendations.append({
                "category": "contact",
                "priority": "medium",
                "title": "Add LinkedIn Profile",
                "description": "Include your LinkedIn profile URL",
                "impact": "Increases professional credibility"
            })
        
        # Location check
        location_keywords = ["city", "state", "country", "address", "location"]
        if any(keyword in resume_text.lower() for keyword in location_keywords):
            score += 2
        
        return {
            "score": min(15, score),
            "issues": issues,
            "recommendations": recommendations
        }
    
    def _analyze_readability(self, resume_text: str) -> Dict:
        """Analyze text readability for ATS"""
        
        score = 10  # Start with full points
        issues = []
        recommendations = []
        
        # Word count check
        word_count = len(resume_text.split())
        
        if word_count < 200:
            score -= 3
            issues.append({
                "type": "readability",
                "severity": "medium",
                "title": "Resume Too Short",
                "description": f"Only {word_count} words (recommended: 300-600)"
            })
        elif word_count > 800:
            score -= 2
            issues.append({
                "type": "readability",
                "severity": "low",
                "title": "Resume Too Long",
                "description": f"{word_count} words (recommended: 300-600)"
            })
        
        # Sentence length check
        sentences = re.split(r'[.!?]+', resume_text)
        long_sentences = [s for s in sentences if len(s.split()) > 25]
        
        if len(long_sentences) > 3:
            score -= 2
            issues.append({
                "type": "readability",
                "severity": "low",
                "title": "Long Sentences",
                "description": "Some sentences are too long for ATS parsing"
            })
        
        # Jargon and complexity check
        complex_words = re.findall(r'\b\w{12,}\b', resume_text)
        if len(complex_words) > 10:
            score -= 1
            recommendations.append({
                "category": "readability",
                "priority": "low",
                "title": "Simplify Complex Words",
                "description": "Consider using simpler alternatives for very long words",
                "impact": "Improves ATS text processing"
            })
        
        return {
            "score": max(0, score),
            "issues": issues,
            "recommendations": recommendations
        }
    
    def _check_section_order(self, resume_text: str) -> int:
        """Check if sections are in logical order"""
        
        # Ideal order: Contact -> Summary -> Experience -> Education -> Skills
        section_positions = {}
        lines = resume_text.lower().split('\n')
        
        for i, line in enumerate(lines):
            if any(contact_word in line for contact_word in ['email', 'phone', 'linkedin']):
                section_positions['contact'] = i
            elif any(summary_word in line for summary_word in ['summary', 'objective', 'profile']):
                section_positions['summary'] = i
            elif any(exp_word in line for exp_word in ['experience', 'work', 'employment']):
                section_positions['experience'] = i
            elif 'education' in line:
                section_positions['education'] = i
            elif 'skills' in line:
                section_positions['skills'] = i
        
        # Award points for logical order
        score = 0
        if 'contact' in section_positions and section_positions['contact'] < 5:
            score += 1
        if ('experience' in section_positions and 'education' in section_positions and 
            section_positions['experience'] < section_positions['education']):
            score += 1
        
        return score
    
    def generate_ats_report(self, resume_text: str) -> Dict:
        """Generate comprehensive ATS compatibility report"""
        
        logger.info("Generating comprehensive ATS report")
        
        # Get main ATS analysis
        ats_analysis = self.calculate_ats_score(resume_text)
        
        # Additional insights
        insights = self._generate_insights(ats_analysis)
        
        # Action plan
        action_plan = self._generate_action_plan(ats_analysis)
        
        return {
            **ats_analysis,
            "insights": insights,
            "action_plan": action_plan,
            "report_timestamp": "2024-01-24T13:00:00Z"
        }
    
    def _generate_insights(self, ats_analysis: Dict) -> List[Dict]:
        """Generate actionable insights from ATS analysis"""
        
        insights = []
        score = ats_analysis["total_score"]
        
        if score >= 85:
            insights.append({
                "type": "success",
                "title": "Excellent ATS Compatibility",
                "description": "Your resume is well-optimized for ATS systems and should pass most automated screenings."
            })
        elif score >= 70:
            insights.append({
                "type": "good",
                "title": "Good ATS Compatibility",
                "description": "Your resume should perform well with most ATS systems. Minor improvements could boost your score."
            })
        elif score >= 55:
            insights.append({
                "type": "warning",
                "title": "Fair ATS Compatibility",
                "description": "Your resume may face challenges with some ATS systems. Focus on critical improvements."
            })
        else:
            insights.append({
                "type": "critical",
                "title": "Poor ATS Compatibility",
                "description": "Your resume is likely to be filtered out by ATS systems. Immediate improvements needed."
            })
        
        # Specific insights based on score breakdown
        breakdown = ats_analysis["score_breakdown"]
        
        if breakdown["formatting"] < 20:
            insights.append({
                "type": "tip",
                "title": "Formatting Issues",
                "description": "Clean up formatting to improve ATS parsing accuracy."
            })
        
        if breakdown["keywords"] < 20:
            insights.append({
                "type": "tip",
                "title": "Keyword Optimization",
                "description": "Add more relevant keywords and action verbs to match job descriptions."
            })
        
        return insights
    
    def _generate_action_plan(self, ats_analysis: Dict) -> List[Dict]:
        """Generate prioritized action plan"""
        
        action_plan = []
        
        # Critical actions first
        critical_issues = [issue for issue in ats_analysis["issues"] if issue["severity"] == "critical"]
        if critical_issues:
            action_plan.append({
                "priority": "immediate",
                "title": "Fix Critical Issues",
                "actions": [issue["title"] for issue in critical_issues[:3]],
                "timeline": "Before applying to jobs"
            })
        
        # High priority recommendations
        high_priority_recs = [rec for rec in ats_analysis["recommendations"] if rec["priority"] == "high"]
        if high_priority_recs:
            action_plan.append({
                "priority": "high",
                "title": "High Impact Improvements",
                "actions": [rec["title"] for rec in high_priority_recs[:3]],
                "timeline": "This week"
            })
        
        # Medium priority recommendations
        medium_priority_recs = [rec for rec in ats_analysis["recommendations"] if rec["priority"] == "medium"]
        if medium_priority_recs:
            action_plan.append({
                "priority": "medium",
                "title": "Additional Optimizations",
                "actions": [rec["title"] for rec in medium_priority_recs[:3]],
                "timeline": "Next 2 weeks"
            })
        
        return action_plan

def main():
    """Test the ATS analyzer"""
    analyzer = ATSAnalyzer()
    
    sample_resume = """
    John Doe
    john.doe@email.com | (555) 123-4567 | linkedin.com/in/johndoe
    
    Professional Summary
    Experienced software engineer with 5 years of experience developing web applications.
    
    Experience
    Software Engineer - Tech Company (2020-2024)
    • Developed and maintained web applications using Python and JavaScript
    • Implemented new features that improved user engagement by 25%
    • Led a team of 3 developers on critical projects
    • Collaborated with cross-functional teams to deliver high-quality software
    
    Education
    Bachelor of Science in Computer Science
    University of Technology (2016-2020)
    
    Skills
    Python, JavaScript, React, Node.js, SQL, Git, AWS, Docker
    """
    
    result = analyzer.generate_ats_report(sample_resume)
    
    print("=== ATS COMPATIBILITY REPORT ===")
    print(f"Overall Score: {result['total_score']}/100 ({result['compatibility_level']})")
    print(f"Issues Found: {result['summary']['total_issues']}")
    print(f"Critical Issues: {result['summary']['critical_issues']}")
    
    for insight in result['insights']:
        print(f"💡 {insight['title']}: {insight['description']}")

if __name__ == "__main__":
    main()
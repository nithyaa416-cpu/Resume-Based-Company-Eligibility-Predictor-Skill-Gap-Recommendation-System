"""
Human-Readable Explanation Generator
Generates student-friendly explanations for eligibility scores
"""

class ExplanationGenerator:
    """
    A class to generate human-readable explanations for eligibility analysis
    """
    
    def __init__(self):
        """
        Initialize explanation templates and patterns
        """
        pass
    
    def generate_eligibility_explanation(self, company_name, role, overall_score, 
                                       skill_analysis, experience_analysis, eligibility_level):
        """
        Generate a comprehensive, student-friendly explanation
        
        Args:
            company_name (str): Name of the company
            role (str): Job role
            overall_score (float): Overall eligibility score
            skill_analysis (dict): Skill matching analysis
            experience_analysis (dict): Experience analysis
            eligibility_level (str): Eligibility level
            
        Returns:
            dict: Comprehensive explanation with multiple sections
        """
        explanation = {
            'summary': self._generate_summary(company_name, overall_score, eligibility_level),
            'detailed_breakdown': self._generate_detailed_breakdown(skill_analysis, experience_analysis),
            'strengths': self._identify_strengths(skill_analysis, experience_analysis),
            'areas_for_improvement': self._identify_improvement_areas(skill_analysis, experience_analysis),
            'next_steps': self._generate_next_steps(skill_analysis, eligibility_level),
            'encouragement': self._generate_encouragement(eligibility_level, overall_score)
        }
        
        return explanation
    
    def _generate_summary(self, company_name, overall_score, eligibility_level):
        """
        Generate a concise summary explanation
        
        Args:
            company_name (str): Company name
            overall_score (float): Overall score
            eligibility_level (str): Eligibility level
            
        Returns:
            str: Summary explanation
        """
        score_rounded = round(overall_score, 1)
        
        if eligibility_level == "Highly Eligible":
            return f"Great news! You are highly eligible for {company_name} with a {score_rounded}% match. Your profile strongly aligns with their requirements."
        elif eligibility_level == "Eligible":
            return f"Good news! You are eligible for {company_name} with a {score_rounded}% match. You meet most of their key requirements."
        else:  # Not Eligible
            return f"Currently, you have a {score_rounded}% match with {company_name}. Don't worry - with focused learning, you can improve your eligibility significantly."
    
    def _generate_detailed_breakdown(self, skill_analysis, experience_analysis):
        """
        Generate detailed breakdown of the analysis
        
        Args:
            skill_analysis (dict): Skill analysis results
            experience_analysis (dict): Experience analysis results
            
        Returns:
            list: List of detailed explanation points
        """
        breakdown = []
        
        # Skills breakdown
        total_skills = skill_analysis.get('total_required', 0)
        matched_skills = len(skill_analysis.get('matched_skills', []))
        missing_skills = len(skill_analysis.get('missing_skills', []))
        
        if total_skills > 0:
            skill_percentage = (matched_skills / total_skills) * 100
            breakdown.append(f"Skills Match: You have {matched_skills} out of {total_skills} required skills ({skill_percentage:.1f}%)")
            
            if matched_skills > 0:
                top_matched = skill_analysis.get('matched_skills', [])[:3]
                breakdown.append(f"Your strongest skills: {', '.join(top_matched)}")
            
            if missing_skills > 0:
                top_missing = skill_analysis.get('missing_skills', [])[:3]
                breakdown.append(f"Skills to develop: {', '.join(top_missing)}")
        
        # Experience breakdown
        exp_score = experience_analysis.get('score', 0)
        exp_message = experience_analysis.get('message', '')
        
        if exp_score >= 80:
            breakdown.append(f"Experience: Excellent! {exp_message}")
        elif exp_score >= 60:
            breakdown.append(f"Experience: Good. {exp_message}")
        else:
            breakdown.append(f"Experience: {exp_message}")
        
        return breakdown
    
    def _identify_strengths(self, skill_analysis, experience_analysis):
        """
        Identify and highlight candidate's strengths
        
        Args:
            skill_analysis (dict): Skill analysis results
            experience_analysis (dict): Experience analysis results
            
        Returns:
            list: List of strengths
        """
        strengths = []
        
        # Skill-based strengths
        matched_skills = skill_analysis.get('matched_skills', [])
        if len(matched_skills) >= 5:
            strengths.append("Strong technical skill set with multiple relevant technologies")
        elif len(matched_skills) >= 3:
            strengths.append("Good foundation in key technical skills")
        elif len(matched_skills) >= 1:
            strengths.append("Some relevant technical skills identified")
        
        # Experience-based strengths
        exp_score = experience_analysis.get('score', 0)
        if exp_score >= 90:
            strengths.append("Exceptional experience level - exceeds requirements")
        elif exp_score >= 80:
            strengths.append("Strong experience level - meets or exceeds requirements")
        elif exp_score >= 60:
            strengths.append("Adequate experience level for the role")
        
        # Specific skill strengths
        if matched_skills:
            if any(skill in ['python', 'java', 'javascript'] for skill in matched_skills):
                strengths.append("Strong programming foundation")
            if any(skill in ['react', 'angular', 'vue'] for skill in matched_skills):
                strengths.append("Modern web development skills")
            if any(skill in ['aws', 'azure', 'gcp'] for skill in matched_skills):
                strengths.append("Cloud technology experience")
            if any(skill in ['machine learning', 'deep learning', 'nlp'] for skill in matched_skills):
                strengths.append("AI/ML expertise")
        
        return strengths if strengths else ["Willingness to learn and grow"]
    
    def _identify_improvement_areas(self, skill_analysis, experience_analysis):
        """
        Identify areas that need improvement
        
        Args:
            skill_analysis (dict): Skill analysis results
            experience_analysis (dict): Experience analysis results
            
        Returns:
            list: List of improvement areas
        """
        improvements = []
        
        # Skill gaps
        missing_skills = skill_analysis.get('missing_skills', [])
        if len(missing_skills) > 5:
            improvements.append("Significant skill gaps - focus on learning key technologies")
        elif len(missing_skills) > 2:
            improvements.append("Some important skills missing - targeted learning recommended")
        elif len(missing_skills) > 0:
            improvements.append("Minor skill gaps - easy to address with focused study")
        
        # Experience gaps
        exp_score = experience_analysis.get('score', 0)
        if exp_score < 60:
            improvements.append("Experience level below requirements - consider internships or projects")
        elif exp_score < 80:
            improvements.append("Experience level could be strengthened")
        
        # Specific improvement suggestions
        if missing_skills:
            critical_missing = []
            for skill in missing_skills[:3]:  # Top 3 missing
                if skill.lower() in ['python', 'java', 'javascript']:
                    critical_missing.append("Core programming languages")
                elif skill.lower() in ['machine learning', 'deep learning']:
                    critical_missing.append("AI/ML fundamentals")
                elif skill.lower() in ['aws', 'cloud']:
                    critical_missing.append("Cloud computing skills")
            
            if critical_missing:
                improvements.extend(critical_missing)
        
        return improvements if improvements else ["Continue building on your existing strengths"]
    
    def _generate_next_steps(self, skill_analysis, eligibility_level):
        """
        Generate actionable next steps
        
        Args:
            skill_analysis (dict): Skill analysis results
            eligibility_level (str): Current eligibility level
            
        Returns:
            list: List of actionable next steps
        """
        next_steps = []
        missing_skills = skill_analysis.get('missing_skills', [])
        
        if eligibility_level == "Highly Eligible":
            next_steps = [
                "Apply to the company with confidence",
                "Prepare for technical interviews focusing on your strong skills",
                "Consider learning additional skills to stand out even more"
            ]
        elif eligibility_level == "Eligible":
            next_steps = [
                "Apply to the company - you're a good candidate",
                "Strengthen your weaker areas before interviews",
                "Build projects showcasing your matching skills"
            ]
        else:  # Not Eligible
            if missing_skills:
                top_missing = missing_skills[:3]
                next_steps = [
                    f"Start learning: {', '.join(top_missing)}",
                    "Follow a structured learning roadmap",
                    "Build projects to practice new skills",
                    "Reapply after 3-6 months of focused learning"
                ]
            else:
                next_steps = [
                    "Gain more experience in your field",
                    "Build a strong portfolio of projects",
                    "Consider additional certifications"
                ]
        
        return next_steps
    
    def _generate_encouragement(self, eligibility_level, overall_score):
        """
        Generate encouraging message based on current status
        
        Args:
            eligibility_level (str): Current eligibility level
            overall_score (float): Overall score
            
        Returns:
            str: Encouraging message
        """
        if eligibility_level == "Highly Eligible":
            return "You're in an excellent position! Your skills and experience make you a strong candidate."
        elif eligibility_level == "Eligible":
            return "You're on the right track! With your current skills, you have a good chance of success."
        else:  # Not Eligible
            return "Don't give up! You have a foundation to build on. Consistent learning will get you there."
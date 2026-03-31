"""
ML-Powered Eligibility Calculator
Combines semantic similarity, skill matching, and contextual analysis
"""

import logging
from .simple_semantic_analyzer import SimpleSemanticAnalyzer
from .learning_recommender import LearningRecommender
from .explanation_generator import ExplanationGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MLEligibilityCalculator:
    """
    Advanced eligibility calculator using ML and semantic analysis
    """
    
    def __init__(self):
        """
        Initialize the ML eligibility calculator
        """
        self.semantic_analyzer = SimpleSemanticAnalyzer()
        self.learning_recommender = LearningRecommender()
        self.explanation_generator = ExplanationGenerator()
        
        logger.info("ML Eligibility Calculator initialized")
    
    def calculate_comprehensive_eligibility(self, resume_info, job_requirements, company_name):
        """
        Calculate comprehensive eligibility using ML and semantic analysis
        
        Args:
            resume_info (dict): Comprehensive resume information from NLP extractor
            job_requirements (tuple): Job requirements from database
            company_name (str): Name of the company
            
        Returns:
            dict: Complete ML-powered eligibility analysis
        """
        if not job_requirements:
            return {
                'error': 'No job requirements found',
                'eligibility_score': 0
            }
        
        # Unpack job requirements
        role, required_skills_str, tools_str, experience_str, education_str, job_description = job_requirements
        
        # Parse required skills and tools
        required_skills = self._parse_skills_string(required_skills_str)
        required_tools = self._parse_skills_string(tools_str)
        all_required_skills = required_skills + required_tools
        
        # Prepare job requirements dict for semantic analysis
        job_req_dict = {
            'required_skills': required_skills_str,
            'tools': tools_str,
            'experience': experience_str,
            'education': education_str
        }
        
        # 1. Semantic Similarity Analysis
        semantic_analysis = self.semantic_analyzer.calculate_resume_job_similarity(
            resume_info['sections'], job_description, job_req_dict
        )
        
        # 2. Traditional Skill Matching
        skill_analysis = self._calculate_skill_matching(
            resume_info['skills'], all_required_skills
        )
        
        # 3. Semantic Skill Analysis
        semantic_skill_analysis = self.semantic_analyzer.analyze_skill_context_similarity(
            resume_info['skills'], all_required_skills
        )
        
        # 4. Experience Analysis
        experience_analysis = self._calculate_experience_matching(
            resume_info['experience'], experience_str
        )
        
        # 5. Education Analysis
        education_analysis = self._calculate_education_matching(
            resume_info['education'], education_str
        )
        
        # 6. Calculate ML-Enhanced Eligibility Score
        ml_eligibility = self.semantic_analyzer.calculate_eligibility_score(
            semantic_analysis, skill_analysis['match_percentage']
        )
        
        # 7. Skill Readiness Analysis
        skill_readiness = self._analyze_skill_readiness(
            resume_info['skills'], all_required_skills
        )
        
        # 8. Generate Learning Recommendations
        missing_skills = skill_analysis['missing_skills']
        learning_recommendations = self.learning_recommender.get_learning_recommendations(missing_skills)
        learning_roadmap = self.learning_recommender.get_skill_learning_roadmap(missing_skills)
        
        # 9. Generate Enhanced Explanation
        explanation = self._generate_ml_explanation(
            company_name, role, ml_eligibility, skill_analysis, 
            semantic_analysis, experience_analysis
        )
        
        return {
            'company': company_name,
            'role': role,
            'ml_eligibility_score': ml_eligibility['ml_eligibility_score'],
            'eligibility_level': ml_eligibility['eligibility_level'],
            'semantic_analysis': semantic_analysis,
            'skill_analysis': skill_analysis,
            'semantic_skill_analysis': semantic_skill_analysis,
            'experience_analysis': experience_analysis,
            'education_analysis': education_analysis,
            'skill_readiness_levels': skill_readiness,
            'learning_recommendations': learning_recommendations,
            'learning_roadmap': learning_roadmap,
            'ml_explanation': explanation,
            'score_breakdown': ml_eligibility,
            'processing_info': {
                'semantic_component': ml_eligibility['semantic_component'],
                'skill_component': ml_eligibility['skill_component'],
                'total_skills_analyzed': len(resume_info['skills']),
                'semantic_matches_found': semantic_skill_analysis['semantic_matches']
            }
        }
    
    def _calculate_skill_matching(self, resume_skills, required_skills):
        """
        Calculate traditional skill matching with enhanced logic
        
        Args:
            resume_skills (dict): Skills from resume with context
            required_skills (list): Required skills list
            
        Returns:
            dict: Skill matching analysis
        """
        if not required_skills:
            return {
                'score': 0,
                'matched_skills': [],
                'missing_skills': [],
                'match_percentage': 0,
                'total_required': 0
            }
        
        resume_skill_names = [skill.lower() for skill in resume_skills.keys()]
        required_skills_lower = [skill.lower() for skill in required_skills]
        
        matched_skills = []
        missing_skills = []
        
        for required_skill in required_skills_lower:
            is_matched = False
            
            # Check for exact or partial matches
            for resume_skill in resume_skill_names:
                if (required_skill in resume_skill or 
                    resume_skill in required_skill or 
                    required_skill == resume_skill):
                    matched_skills.append(required_skill)
                    is_matched = True
                    break
            
            if not is_matched:
                missing_skills.append(required_skill)
        
        total_required = len(required_skills_lower)
        matched_count = len(matched_skills)
        match_percentage = (matched_count / total_required) * 100 if total_required > 0 else 0
        
        return {
            'score': matched_count,
            'total_required': total_required,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'match_percentage': round(match_percentage, 2)
        }
    
    def _calculate_experience_matching(self, experience_info, required_experience):
        """
        Calculate experience matching with ML insights
        
        Args:
            experience_info (dict): Experience information from NLP
            required_experience (str): Required experience string
            
        Returns:
            dict: Experience matching analysis
        """
        if not required_experience:
            return {
                'score': 50, 
                'message': 'No experience requirement specified',
                'confidence': 'low'
            }
        
        candidate_years = experience_info.get('total_years', 0)
        confidence = experience_info.get('confidence', 'low')
        
        # Extract required years from string
        required_years = self._extract_years_from_text(required_experience)
        
        if not required_years:
            return {
                'score': 50, 
                'message': 'Could not parse experience requirement',
                'confidence': confidence
            }
        
        min_required = min(required_years)
        
        if candidate_years >= min_required:
            # Calculate score with bonus for exceeding requirements
            base_score = 80
            bonus = min(20, (candidate_years - min_required) * 3)
            score = min(100, base_score + bonus)
            message = f"Exceeds requirement ({candidate_years} >= {min_required} years)"
        else:
            # Partial score based on how close they are
            if candidate_years > 0:
                score = max(20, (candidate_years / min_required) * 70)
                message = f"Below requirement ({candidate_years} < {min_required} years)"
            else:
                score = 10
                message = "No clear experience mentioned"
        
        return {
            'score': round(score, 2),
            'candidate_years': candidate_years,
            'required_years': min_required,
            'message': message,
            'confidence': confidence
        }
    
    def _calculate_education_matching(self, education_info, required_education):
        """
        Calculate education matching
        
        Args:
            education_info (dict): Education information from NLP
            required_education (str): Required education string
            
        Returns:
            dict: Education matching analysis
        """
        if not required_education:
            return {
                'score': 50,
                'message': 'No education requirement specified'
            }
        
        degrees = education_info.get('degrees', [])
        fields = education_info.get('fields_of_study', [])
        
        if not degrees and not fields:
            return {
                'score': 30,
                'message': 'No clear education information found'
            }
        
        # Simple matching logic - can be enhanced with semantic similarity
        required_lower = required_education.lower()
        
        score = 50  # Base score for having education info
        
        # Check for degree level matches
        if any(degree in required_lower for degree in ['bachelor', 'master', 'phd']):
            if any(degree in ' '.join(degrees).lower() for degree in ['bachelor', 'master', 'phd']):
                score += 30
        
        # Check for field matches
        if fields:
            field_text = ' '.join(fields).lower()
            if any(field in required_lower for field in ['computer', 'engineering', 'science', 'technology']):
                if any(keyword in field_text for keyword in ['computer', 'engineering', 'science', 'technology']):
                    score += 20
        
        score = min(100, score)
        
        return {
            'score': score,
            'degrees_found': len(degrees),
            'fields_found': len(fields),
            'message': f"Education analysis complete (score: {score}%)"
        }
    
    def _analyze_skill_readiness(self, resume_skills, required_skills):
        """
        Analyze skill readiness levels with ML insights
        
        Args:
            resume_skills (dict): Skills with context from resume
            required_skills (list): Required skills list
            
        Returns:
            dict: Skill readiness analysis
        """
        skill_readiness = {
            'Advanced': [],
            'Intermediate': [],
            'Beginner': [],
            'Missing': []
        }
        
        # Analyze resume skills
        for skill, info in resume_skills.items():
            proficiency = info.get('proficiency', 'Intermediate')
            skill_readiness[proficiency].append({
                'skill': skill,
                'mentions': info.get('mentions', 0),
                'contexts': len(info.get('contexts', [])),
                'category': info.get('category', 'Other')
            })
        
        # Add missing skills
        resume_skill_names = [skill.lower() for skill in resume_skills.keys()]
        for required_skill in required_skills:
            if required_skill.lower() not in resume_skill_names:
                skill_readiness['Missing'].append({
                    'skill': required_skill,
                    'mentions': 0,
                    'contexts': 0,
                    'category': 'Required'
                })
        
        return skill_readiness
    
    def _generate_ml_explanation(self, company_name, role, ml_eligibility, 
                                skill_analysis, semantic_analysis, experience_analysis):
        """
        Generate ML-enhanced explanation
        
        Args:
            company_name (str): Company name
            role (str): Job role
            ml_eligibility (dict): ML eligibility results
            skill_analysis (dict): Skill analysis
            semantic_analysis (dict): Semantic analysis
            experience_analysis (dict): Experience analysis
            
        Returns:
            dict: Enhanced explanation
        """
        explanation = {
            'summary': '',
            'ml_insights': [],
            'semantic_insights': [],
            'recommendations': [],
            'confidence_level': 'medium'
        }
        
        score = ml_eligibility['ml_eligibility_score']
        level = ml_eligibility['eligibility_level']
        
        # Generate summary
        explanation['summary'] = f"Based on ML analysis, you are {level.lower()} for {company_name} with a {score}% match score."
        
        # ML insights
        semantic_component = ml_eligibility['semantic_component']
        skill_component = ml_eligibility['skill_component']
        
        explanation['ml_insights'] = [
            f"Semantic similarity analysis: {semantic_component}%",
            f"Traditional skill matching: {skill_component}%",
            f"Overall contextual match: {semantic_analysis.get('contextual_match', 0) * 100:.1f}%"
        ]
        
        # Semantic insights
        section_sims = semantic_analysis.get('section_similarities', {})
        explanation['semantic_insights'] = [
            f"Skills section similarity: {section_sims.get('skills', 0) * 100:.1f}%",
            f"Experience section similarity: {section_sims.get('experience', 0) * 100:.1f}%",
            f"Education section similarity: {section_sims.get('education', 0) * 100:.1f}%"
        ]
        
        # Generate recommendations
        if score >= 70:
            explanation['recommendations'] = [
                "You're a strong candidate - apply with confidence",
                "Prepare for technical interviews focusing on your matching skills",
                "Consider highlighting your strongest skills in your application"
            ]
            explanation['confidence_level'] = 'high'
        elif score >= 50:
            explanation['recommendations'] = [
                "You meet the basic requirements - apply and showcase your potential",
                "Focus on strengthening your weaker areas",
                "Build projects that demonstrate your matching skills"
            ]
            explanation['confidence_level'] = 'medium'
        else:
            missing_skills = skill_analysis.get('missing_skills', [])[:3]
            explanation['recommendations'] = [
                f"Focus on learning: {', '.join(missing_skills)}",
                "Build projects using these technologies",
                "Consider taking relevant courses or certifications",
                "Reapply after gaining more experience"
            ]
            explanation['confidence_level'] = 'low'
        
        return explanation
    
    def _parse_skills_string(self, skills_string):
        """Parse comma-separated skills string"""
        if not skills_string:
            return []
        return [skill.strip().lower() for skill in skills_string.split(',') if skill.strip()]
    
    def _extract_years_from_text(self, text):
        """Extract years from experience requirement text"""
        import re
        if not text:
            return []
        
        patterns = [
            r'(\d+)\s*(?:\+)?\s*years?',
            r'(\d+)\s*(?:\+)?\s*yrs?',
            r'(\d+)\s*to\s*(\d+)\s*years?'
        ]
        
        years = []
        text_lower = text.lower()
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                if isinstance(match, tuple):
                    years.extend([int(y) for y in match if y.isdigit()])
                else:
                    years.append(int(match))
        
        return years
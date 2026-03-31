"""
Eligibility Calculator Module
Calculates eligibility scores, identifies skill gaps, and provides comprehensive analysis
"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .learning_recommender import LearningRecommender
from .explanation_generator import ExplanationGenerator

class EligibilityCalculator:
    """
    A class to calculate eligibility scores and provide comprehensive analysis
    """
    
    def __init__(self):
        """
        Initialize the calculator with learning recommender and explanation generator
        """
        self.learning_recommender = LearningRecommender()
        self.explanation_generator = ExplanationGenerator()
    
    def parse_skills_string(self, skills_string):
        """
        Parse comma-separated skills string into list
        
        Args:
            skills_string (str): Comma-separated skills
            
        Returns:
            list: List of individual skills
        """
        if not skills_string:
            return []
            
        # Split by comma and clean each skill
        skills = [skill.strip().lower() for skill in skills_string.split(',')]
        return [skill for skill in skills if skill]  # Remove empty strings
    
    def calculate_skill_match_score(self, resume_skills, required_skills):
        """
        Calculate skill matching score between resume and job requirements
        
        Args:
            resume_skills (list): Skills extracted from resume
            required_skills (list): Required skills for the job
            
        Returns:
            dict: Detailed skill matching information
        """
        if not required_skills:
            return {
                'score': 0,
                'matched_skills': [],
                'missing_skills': [],
                'match_percentage': 0
            }
        
        # Convert to lowercase for comparison
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        required_skills_lower = [skill.lower() for skill in required_skills]
        
        # Find matched and missing skills
        matched_skills = []
        missing_skills = []
        
        for required_skill in required_skills_lower:
            # Check for exact match or partial match
            is_matched = False
            for resume_skill in resume_skills_lower:
                if (required_skill in resume_skill or 
                    resume_skill in required_skill or 
                    required_skill == resume_skill):
                    matched_skills.append(required_skill)
                    is_matched = True
                    break
            
            if not is_matched:
                missing_skills.append(required_skill)
        
        # Calculate score
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
    
    def calculate_experience_score(self, resume_experience_years, required_experience):
        """
        Calculate experience matching score
        
        Args:
            resume_experience_years (list): Years of experience from resume
            required_experience (str): Required experience string
            
        Returns:
            dict: Experience matching information
        """
        if not required_experience:
            return {'score': 50, 'message': 'No experience requirement specified'}
        
        # Extract required years from string
        required_years = self.extract_years_from_text(required_experience)
        
        if not required_years:
            return {'score': 50, 'message': 'Could not parse experience requirement'}
        
        max_resume_experience = max(resume_experience_years) if resume_experience_years else 0
        min_required = min(required_years)
        
        if max_resume_experience >= min_required:
            # Bonus for exceeding requirements
            bonus = min(20, (max_resume_experience - min_required) * 2)
            score = min(100, 80 + bonus)
            message = f"Meets requirement ({max_resume_experience} >= {min_required} years)"
        else:
            # Partial score based on how close they are
            score = max(0, (max_resume_experience / min_required) * 80)
            message = f"Below requirement ({max_resume_experience} < {min_required} years)"
        
        return {
            'score': round(score, 2),
            'resume_experience': max_resume_experience,
            'required_experience': min_required,
            'message': message
        }
    
    def extract_years_from_text(self, text):
        """
        Extract years from experience requirement text
        
        Args:
            text (str): Experience requirement text
            
        Returns:
            list: List of years found
        """
        if not text:
            return []
        
        # Patterns to match years
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
    
    def calculate_comprehensive_eligibility(self, resume_skills_with_levels, resume_experience, 
                                          job_requirements, company_name):
        """
        Calculate comprehensive eligibility analysis with all enhanced features
        
        Args:
            resume_skills_with_levels (dict): Skills from resume with readiness levels
            resume_experience (list): Experience years from resume
            job_requirements (tuple): Job requirements from database
            company_name (str): Name of the company
            
        Returns:
            dict: Complete eligibility analysis with all enhanced features
        """
        if not job_requirements:
            return {
                'error': 'No job requirements found',
                'eligibility_score': 0
            }
        
        role, required_skills_str, tools_str, experience_str, education_str, job_description = job_requirements
        
        # Parse required skills and tools
        required_skills = self.parse_skills_string(required_skills_str)
        required_tools = self.parse_skills_string(tools_str)
        all_required_skills = required_skills + required_tools
        
        # Extract resume skill names for matching
        resume_skill_names = list(resume_skills_with_levels.keys())
        
        # Calculate skill matching
        skill_analysis = self.calculate_skill_match_score(resume_skill_names, all_required_skills)
        
        # Calculate experience matching
        experience_analysis = self.calculate_experience_score(resume_experience, experience_str)
        
        # Calculate weighted overall score
        skill_weight = 0.7  # 70% weight for skills
        experience_weight = 0.3  # 30% weight for experience
        
        overall_score = (
            (skill_analysis['match_percentage'] * skill_weight) +
            (experience_analysis['score'] * experience_weight)
        )
        
        # Determine eligibility level (Revised Criteria)
        if overall_score >= 85:
            eligibility_level = "Highly Eligible"
        elif overall_score >= 70:
            eligibility_level = "Eligible"
        else:
            eligibility_level = "Not Eligible"
        
        # Generate comprehensive analysis
        missing_skills = skill_analysis['missing_skills']
        
        # Get learning recommendations
        learning_recommendations = self.learning_recommender.get_learning_recommendations(missing_skills)
        
        # Get learning roadmap
        learning_roadmap = self.learning_recommender.get_skill_learning_roadmap(missing_skills)
        
        # Generate human-readable explanation
        explanation = self.explanation_generator.generate_eligibility_explanation(
            company_name, role, overall_score, skill_analysis, 
            experience_analysis, eligibility_level
        )
        
        # Organize skill readiness levels
        skill_readiness = self._organize_skill_readiness(resume_skills_with_levels, all_required_skills)
        
        return {
            'company': company_name,
            'role': role,
            'overall_score': round(overall_score, 2),
            'eligibility_level': eligibility_level,
            'skill_analysis': skill_analysis,
            'experience_analysis': experience_analysis,
            'skill_readiness_levels': skill_readiness,
            'learning_recommendations': learning_recommendations,
            'learning_roadmap': learning_roadmap,
            'explanation': explanation,
            'recommendations': self.generate_recommendations(missing_skills)  # Keep legacy format
        }
    
    def _organize_skill_readiness(self, resume_skills_with_levels, required_skills):
        """
        Organize skills by readiness levels including missing skills
        
        Args:
            resume_skills_with_levels (dict): Skills with levels from resume
            required_skills (list): Required skills for the job
            
        Returns:
            dict: Skills organized by readiness levels
        """
        skill_readiness = {
            'Advanced': [],
            'Intermediate': [],
            'Beginner': [],
            'Missing': []
        }
        
        # Add resume skills with their levels
        for skill, info in resume_skills_with_levels.items():
            level = info['level']
            skill_readiness[level].append({
                'skill': skill,
                'occurrences': info['occurrences'],
                'category': info.get('category', 'Other')
            })
        
        # Add missing skills
        resume_skill_names = [skill.lower() for skill in resume_skills_with_levels.keys()]
        for required_skill in required_skills:
            if required_skill.lower() not in resume_skill_names:
                skill_readiness['Missing'].append({
                    'skill': required_skill,
                    'occurrences': 0,
                    'category': 'Required'
                })
        
        return skill_readiness
    
    def generate_eligibility_explanation(self, skill_analysis, experience_analysis, overall_score, eligibility_level):
        """
        Generate human-readable explanation for eligibility score
        
        Args:
            skill_analysis (dict): Skill matching analysis
            experience_analysis (dict): Experience analysis
            overall_score (float): Overall eligibility score
            eligibility_level (str): Eligibility level
            
        Returns:
            dict: Detailed explanation
        """
        explanation = {
            'summary': f"Your eligibility is {overall_score:.1f}% ({eligibility_level})",
            'reasons': [],
            'strengths': [],
            'weaknesses': []
        }
        
        # Analyze strengths
        if skill_analysis['match_percentage'] >= 70:
            explanation['strengths'].append(f"Strong skill match ({skill_analysis['match_percentage']:.1f}%)")
            explanation['reasons'].append(f"✅ {len(skill_analysis['matched_skills'])} out of {skill_analysis['total_required']} required skills match")
        elif skill_analysis['match_percentage'] >= 40:
            explanation['reasons'].append(f"⚠️ Moderate skill match ({skill_analysis['match_percentage']:.1f}%)")
        else:
            explanation['weaknesses'].append(f"Low skill match ({skill_analysis['match_percentage']:.1f}%)")
            explanation['reasons'].append(f"❌ Only {len(skill_analysis['matched_skills'])} out of {skill_analysis['total_required']} required skills match")
        
        # Analyze experience
        if experience_analysis['score'] >= 80:
            explanation['strengths'].append("Experience requirements exceeded")
            explanation['reasons'].append(f"✅ {experience_analysis['message']}")
        elif experience_analysis['score'] >= 60:
            explanation['reasons'].append(f"✅ {experience_analysis['message']}")
        else:
            explanation['weaknesses'].append("Experience requirements not met")
            explanation['reasons'].append(f"❌ {experience_analysis['message']}")
        
        # Add specific skill feedback
        if skill_analysis['matched_skills']:
            top_matched = skill_analysis['matched_skills'][:3]
            explanation['reasons'].append(f"✅ Strong in: {', '.join(top_matched)}")
        
        if skill_analysis['missing_skills']:
            top_missing = skill_analysis['missing_skills'][:3]
            explanation['reasons'].append(f"❌ Need to learn: {', '.join(top_missing)}")
        
        return explanation
    
    def generate_learning_roadmap(self, missing_skills):
        """
        Generate a structured learning roadmap for missing skills
        
        Args:
            missing_skills (list): List of missing skills
            
        Returns:
            dict: Structured learning roadmap
        """
        # Skill dependency mapping (prerequisite → advanced)
        skill_dependencies = {
            # Programming fundamentals
            'python': [],
            'java': [],
            'javascript': [],
            
            # Web development progression
            'html': [],
            'css': ['html'],
            'react': ['javascript', 'html', 'css'],
            'node.js': ['javascript'],
            'express': ['node.js', 'javascript'],
            'django': ['python'],
            'flask': ['python'],
            
            # Database progression
            'sql': [],
            'mysql': ['sql'],
            'postgresql': ['sql'],
            'mongodb': [],
            
            # Cloud and DevOps
            'git': [],
            'docker': [],
            'kubernetes': ['docker'],
            'aws': [],
            
            # Data Science progression
            'pandas': ['python'],
            'numpy': ['python'],
            'matplotlib': ['python', 'numpy'],
            'scikit-learn': ['python', 'pandas', 'numpy'],
            'tensorflow': ['python', 'numpy'],
            'pytorch': ['python', 'numpy'],
            'machine learning': ['python', 'pandas', 'numpy'],
            'deep learning': ['machine learning', 'tensorflow'],
            'nlp': ['python', 'machine learning']
        }
        
        # Organize skills by learning phases
        roadmap = {
            'total_skills': len(missing_skills),
            'estimated_time': f"{len(missing_skills) * 2}-{len(missing_skills) * 4} weeks",
            'phases': []
        }
        
        if not missing_skills:
            return roadmap
        
        # Sort skills by dependency level
        skill_levels = {}
        for skill in missing_skills:
            skill_lower = skill.lower()
            dependencies = skill_dependencies.get(skill_lower, [])
            
            # Count how many dependencies are also missing
            missing_deps = [dep for dep in dependencies if dep in [s.lower() for s in missing_skills]]
            skill_levels[skill] = len(missing_deps)
        
        # Group skills by phases
        phase_1 = [skill for skill, level in skill_levels.items() if level == 0]  # No dependencies
        phase_2 = [skill for skill, level in skill_levels.items() if level == 1]  # 1 dependency
        phase_3 = [skill for skill, level in skill_levels.items() if level >= 2]  # 2+ dependencies
        
        # Create phases
        if phase_1:
            roadmap['phases'].append({
                'phase': 1,
                'title': 'Foundation Skills',
                'description': 'Start with these fundamental skills',
                'skills': phase_1,
                'duration': f"{len(phase_1) * 1}-{len(phase_1) * 2} weeks"
            })
        
        if phase_2:
            roadmap['phases'].append({
                'phase': 2,
                'title': 'Intermediate Skills',
                'description': 'Build on your foundation',
                'skills': phase_2,
                'duration': f"{len(phase_2) * 2}-{len(phase_2) * 3} weeks"
            })
        
        if phase_3:
            roadmap['phases'].append({
                'phase': 3,
                'title': 'Advanced Skills',
                'description': 'Master these complex technologies',
                'skills': phase_3,
                'duration': f"{len(phase_3) * 3}-{len(phase_3) * 4} weeks"
            })
        
        return roadmap
    
    def generate_recommendations(self, missing_skills):
        """
        Generate learning recommendations for missing skills
        
        Args:
            missing_skills (list): List of missing skills
            
        Returns:
            list: List of learning recommendations
        """
        # Simple recommendation mapping
        skill_resources = {
            'python': 'Learn Python: Codecademy Python Course, Python.org Tutorial',
            'java': 'Learn Java: Oracle Java Tutorials, Codecademy Java Course',
            'javascript': 'Learn JavaScript: MDN Web Docs, freeCodeCamp',
            'react': 'Learn React: Official React Tutorial, React for Beginners',
            'node.js': 'Learn Node.js: Node.js Official Docs, Node.js Tutorial',
            'sql': 'Learn SQL: W3Schools SQL, SQLBolt',
            'mysql': 'Learn MySQL: MySQL Tutorial, W3Schools MySQL',
            'mongodb': 'Learn MongoDB: MongoDB University, MongoDB Tutorial',
            'aws': 'Learn AWS: AWS Free Tier, AWS Training and Certification',
            'docker': 'Learn Docker: Docker Official Tutorial, Docker for Beginners',
            'git': 'Learn Git: Git Official Tutorial, Atlassian Git Tutorial'
        }
        
        recommendations = []
        for skill in missing_skills[:5]:  # Limit to top 5 missing skills
            resource = skill_resources.get(skill.lower(), f'Search for "{skill}" tutorials online')
            recommendations.append({
                'skill': skill,
                'resource': resource
            })
        
        return recommendations
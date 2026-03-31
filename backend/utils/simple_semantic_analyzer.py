"""
Simple Semantic Analyzer using spaCy's built-in similarity
This replaces sentence-transformers for Python 3.10 compatibility
"""

import spacy
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SimpleSemanticAnalyzer:
    def __init__(self):
        """Initialize the semantic analyzer with spaCy model"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("Simple Semantic Analyzer initialized with spaCy")
        except OSError:
            logger.error("spaCy model 'en_core_web_sm' not found. Please install it with: python -m spacy download en_core_web_sm")
            raise
    
    def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity between two texts using spaCy
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score between 0 and 1
        """
        try:
            # Process texts with spaCy
            doc1 = self.nlp(text1)
            doc2 = self.nlp(text2)
            
            # Calculate similarity using spaCy's built-in similarity
            similarity = doc1.similarity(doc2)
            
            # Ensure similarity is between 0 and 1
            similarity = max(0.0, min(1.0, similarity))
            
            logger.info(f"Calculated semantic similarity: {similarity:.3f}")
            return similarity
            
        except Exception as e:
            logger.error(f"Error calculating semantic similarity: {e}")
            return 0.0
    
    def analyze_text_sections(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """
        Analyze semantic similarity between different sections
        
        Args:
            resume_text: Resume content
            job_description: Job description content
            
        Returns:
            Dictionary with section-wise similarity analysis
        """
        try:
            # Overall similarity
            overall_similarity = self.calculate_semantic_similarity(resume_text, job_description)
            
            # Extract key sections from resume
            resume_doc = self.nlp(resume_text)
            job_doc = self.nlp(job_description)
            
            # Simple section extraction based on keywords
            sections = {
                'skills': self._extract_skills_section(resume_text),
                'experience': self._extract_experience_section(resume_text),
                'education': self._extract_education_section(resume_text)
            }
            
            # Calculate section-wise similarities
            section_similarities = {}
            for section_name, section_text in sections.items():
                if section_text:
                    similarity = self.calculate_semantic_similarity(section_text, job_description)
                    section_similarities[f"{section_name}_similarity"] = similarity
                else:
                    section_similarities[f"{section_name}_similarity"] = 0.0
            
            # Calculate contextual match (average of section similarities)
            valid_similarities = [sim for sim in section_similarities.values() if sim > 0]
            contextual_match = sum(valid_similarities) / len(valid_similarities) if valid_similarities else 0.0
            
            return {
                'overall_similarity': overall_similarity,
                'contextual_match': contextual_match,
                'section_similarities': section_similarities,
                'analysis_method': 'spaCy built-in similarity'
            }
            
        except Exception as e:
            logger.error(f"Error in semantic analysis: {e}")
            return {
                'overall_similarity': 0.0,
                'contextual_match': 0.0,
                'section_similarities': {},
                'analysis_method': 'spaCy built-in similarity (error occurred)'
            }
    
    def _extract_skills_section(self, text: str) -> str:
        """Extract skills section from resume text"""
        lines = text.split('\n')
        skills_section = []
        in_skills = False
        
        for line in lines:
            line_lower = line.lower().strip()
            if any(keyword in line_lower for keyword in ['skill', 'technical', 'programming', 'technologies']):
                in_skills = True
                skills_section.append(line)
            elif in_skills and (line_lower.startswith(('experience', 'education', 'project', 'work')) or line.strip() == ''):
                if line.strip() == '':
                    continue
                else:
                    break
            elif in_skills:
                skills_section.append(line)
        
        return '\n'.join(skills_section)
    
    def _extract_experience_section(self, text: str) -> str:
        """Extract experience section from resume text"""
        lines = text.split('\n')
        experience_section = []
        in_experience = False
        
        for line in lines:
            line_lower = line.lower().strip()
            if any(keyword in line_lower for keyword in ['experience', 'work', 'employment', 'professional']):
                in_experience = True
                experience_section.append(line)
            elif in_experience and (line_lower.startswith(('education', 'skill', 'project', 'certification')) or line.strip() == ''):
                if line.strip() == '':
                    continue
                else:
                    break
            elif in_experience:
                experience_section.append(line)
        
        return '\n'.join(experience_section)
    
    def _extract_education_section(self, text: str) -> str:
        """Extract education section from resume text"""
        lines = text.split('\n')
        education_section = []
        in_education = False
        
        for line in lines:
            line_lower = line.lower().strip()
            if any(keyword in line_lower for keyword in ['education', 'degree', 'university', 'college', 'bachelor', 'master']):
                in_education = True
                education_section.append(line)
            elif in_education and (line_lower.startswith(('experience', 'skill', 'project', 'certification')) or line.strip() == ''):
                if line.strip() == '':
                    continue
                else:
                    break
            elif in_education:
                education_section.append(line)
        
        return '\n'.join(education_section)
    
    def calculate_resume_job_similarity(self, resume_sections: dict, job_description: str, job_requirements: dict) -> dict:
        """
        Calculate comprehensive similarity between resume and job requirements
        
        Args:
            resume_sections: Dictionary of resume sections
            job_description: Job description text
            job_requirements: Dictionary of job requirements
            
        Returns:
            Dictionary with similarity analysis
        """
        try:
            # Combine all resume sections into one text
            resume_text = ""
            for section_name, section_content in resume_sections.items():
                if section_content:
                    resume_text += f"{section_content}\n"
            
            # Calculate overall similarity
            overall_similarity = self.calculate_semantic_similarity(resume_text, job_description)
            
            # Calculate section-wise similarities
            section_similarities = {}
            for section_name, section_content in resume_sections.items():
                if section_content:
                    similarity = self.calculate_semantic_similarity(section_content, job_description)
                    section_similarities[f"{section_name}_similarity"] = similarity
                else:
                    section_similarities[f"{section_name}_similarity"] = 0.0
            
            # Calculate contextual match (average of section similarities)
            valid_similarities = [sim for sim in section_similarities.values() if sim > 0]
            contextual_match = sum(valid_similarities) / len(valid_similarities) if valid_similarities else 0.0
            
            # Generate insights
            insights = self.get_similarity_insights(overall_similarity)
            
            return {
                'overall_similarity': overall_similarity,
                'contextual_match': contextual_match,
                'section_similarities': section_similarities,
                'semantic_insights': insights,
                'analysis_method': 'spaCy built-in similarity'
            }
            
        except Exception as e:
            logger.error(f"Error in resume-job similarity calculation: {e}")
            return {
                'overall_similarity': 0.0,
                'contextual_match': 0.0,
                'section_similarities': {},
                'semantic_insights': ['Error in semantic analysis'],
                'analysis_method': 'spaCy built-in similarity (error occurred)'
            }

    def get_similarity_insights(self, similarity_score: float) -> list:
        """
        Generate insights based on similarity score
        
        Args:
            similarity_score: Similarity score between 0 and 1
            
        Returns:
            List of insight strings
        """
        insights = []
        
        if similarity_score >= 0.8:
            insights.append("Excellent semantic match - resume content strongly aligns with job requirements")
        elif similarity_score >= 0.6:
            insights.append("Good semantic match - resume shows relevant experience and skills")
        elif similarity_score >= 0.4:
            insights.append("Moderate semantic match - some relevant content but gaps exist")
        elif similarity_score >= 0.2:
            insights.append("Low semantic match - limited alignment with job requirements")
        else:
            insights.append("Very low semantic match - significant gaps in relevant experience")
        
        # Add technical insights
        if similarity_score > 0:
            insights.append(f"Semantic similarity analysis using spaCy word vectors")
            insights.append(f"Contextual understanding based on linguistic patterns")
        
        return insights
    def analyze_skill_context_similarity(self, resume_skills: list, required_skills: list) -> dict:
        """
        Analyze semantic similarity between resume skills and required skills
        
        Args:
            resume_skills: List of skills from resume
            required_skills: List of required skills
            
        Returns:
            Dictionary with skill similarity analysis
        """
        try:
            if not resume_skills or not required_skills:
                return {
                    'skill_matches': [],
                    'semantic_matches': 0,
                    'total_required': len(required_skills),
                    'semantic_score': 0.0
                }
            
            # Convert skills to text for similarity analysis
            resume_skills_text = " ".join(resume_skills)
            required_skills_text = " ".join(required_skills)
            
            # Calculate overall skill similarity
            overall_similarity = self.calculate_semantic_similarity(resume_skills_text, required_skills_text)
            
            # Analyze individual skill matches
            skill_matches = []
            semantic_matches = 0
            
            for req_skill in required_skills:
                best_match_score = 0.0
                best_match_skill = None
                
                for resume_skill in resume_skills:
                    similarity = self.calculate_semantic_similarity(resume_skill, req_skill)
                    if similarity > best_match_score:
                        best_match_score = similarity
                        best_match_skill = resume_skill
                
                # Consider it a semantic match if similarity > 0.5
                if best_match_score > 0.5:
                    semantic_matches += 1
                    skill_matches.append({
                        'required_skill': req_skill,
                        'matched_skill': best_match_skill,
                        'similarity': best_match_score,
                        'match_type': 'semantic'
                    })
                else:
                    skill_matches.append({
                        'required_skill': req_skill,
                        'matched_skill': None,
                        'similarity': best_match_score,
                        'match_type': 'none'
                    })
            
            semantic_score = semantic_matches / len(required_skills) if required_skills else 0.0
            
            return {
                'skill_matches': skill_matches,
                'semantic_matches': semantic_matches,
                'total_required': len(required_skills),
                'semantic_score': semantic_score,
                'overall_similarity': overall_similarity
            }
            
        except Exception as e:
            logger.error(f"Error in skill context similarity analysis: {e}")
            return {
                'skill_matches': [],
                'semantic_matches': 0,
                'total_required': len(required_skills),
                'semantic_score': 0.0
            }
    
    def calculate_eligibility_score(self, semantic_analysis: dict, skill_match_percentage: float) -> dict:
        """
        Calculate ML-enhanced eligibility score
        
        Args:
            semantic_analysis: Semantic similarity analysis results
            skill_match_percentage: Traditional skill matching percentage
            
        Returns:
            Dictionary with eligibility scoring
        """
        try:
            # Weight factors for different components
            semantic_weight = 0.6  # 60% weight to semantic analysis
            skill_weight = 0.4     # 40% weight to traditional skill matching
            
            # Get semantic components
            overall_similarity = semantic_analysis.get('overall_similarity', 0.0)
            contextual_match = semantic_analysis.get('contextual_match', 0.0)
            
            # Calculate semantic component (0-100)
            semantic_component = ((overall_similarity + contextual_match) / 2) * 100
            
            # Calculate skill component (already 0-100)
            skill_component = skill_match_percentage
            
            # Calculate weighted ML eligibility score
            ml_eligibility_score = (semantic_component * semantic_weight) + (skill_component * skill_weight)
            
            # Determine eligibility level (Revised Criteria)
            if ml_eligibility_score >= 85:
                eligibility_level = "Highly Eligible"
            elif ml_eligibility_score >= 70:
                eligibility_level = "Eligible"
            else:
                eligibility_level = "Not Eligible"
            
            return {
                'ml_eligibility_score': round(ml_eligibility_score, 2),
                'eligibility_level': eligibility_level,
                'semantic_component': round(semantic_component, 2),
                'skill_component': round(skill_component, 2),
                'semantic_weight': semantic_weight,
                'skill_weight': skill_weight,
                'calculation_method': 'spaCy-based semantic analysis'
            }
            
        except Exception as e:
            logger.error(f"Error calculating eligibility score: {e}")
            return {
                'ml_eligibility_score': 0.0,
                'eligibility_level': "Not Eligible",
                'semantic_component': 0.0,
                'skill_component': skill_match_percentage,
                'semantic_weight': semantic_weight,
                'skill_weight': skill_weight,
                'calculation_method': 'spaCy-based semantic analysis (error occurred)'
            }
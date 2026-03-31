"""
Semantic Similarity Engine using Sentence-BERT
Provides contextual embeddings and semantic matching for resume analysis
"""

import numpy as np
from sentence_transformers import SentenceTransformer
import logging
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SemanticAnalyzer:
    """
    Semantic analyzer using Sentence-BERT for contextual understanding
    """
    
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """
        Initialize the semantic analyzer with Sentence-BERT model
        
        Args:
            model_name (str): Name of the Sentence-BERT model to use
        """
        self.model_name = model_name
        self.model = None
        self.embedding_cache = {}
        self.cache_file = "embeddings_cache.pkl"
        
        # Load the model
        self._load_model()
        
        # Load embedding cache if exists
        self._load_cache()
    
    def _load_model(self):
        """Load the Sentence-BERT model"""
        try:
            logger.info(f"Loading Sentence-BERT model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info("Sentence-BERT model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Sentence-BERT model: {e}")
            raise e
    
    def _load_cache(self):
        """Load embedding cache from file"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'rb') as f:
                    self.embedding_cache = pickle.load(f)
                logger.info(f"Loaded {len(self.embedding_cache)} cached embeddings")
        except Exception as e:
            logger.warning(f"Could not load embedding cache: {e}")
            self.embedding_cache = {}
    
    def _save_cache(self):
        """Save embedding cache to file"""
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.embedding_cache, f)
        except Exception as e:
            logger.warning(f"Could not save embedding cache: {e}")
    
    def get_text_embedding(self, text, use_cache=True):
        """
        Get semantic embedding for text using Sentence-BERT
        
        Args:
            text (str): Input text
            use_cache (bool): Whether to use cached embeddings
            
        Returns:
            np.ndarray: Text embedding vector
        """
        if not text or not text.strip():
            return np.zeros(384)  # Default embedding size for all-MiniLM-L6-v2
        
        # Normalize text for caching
        text_key = text.strip().lower()
        
        # Check cache first
        if use_cache and text_key in self.embedding_cache:
            return self.embedding_cache[text_key]
        
        try:
            # Generate embedding
            embedding = self.model.encode(text, convert_to_numpy=True)
            
            # Cache the embedding
            if use_cache:
                self.embedding_cache[text_key] = embedding
                
                # Save cache periodically (every 10 new embeddings)
                if len(self.embedding_cache) % 10 == 0:
                    self._save_cache()
            
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return np.zeros(384)
    
    def calculate_semantic_similarity(self, text1, text2):
        """
        Calculate semantic similarity between two texts
        
        Args:
            text1 (str): First text
            text2 (str): Second text
            
        Returns:
            float: Similarity score between 0 and 1
        """
        # Get embeddings for both texts
        embedding1 = self.get_text_embedding(text1)
        embedding2 = self.get_text_embedding(text2)
        
        # Calculate cosine similarity
        similarity = cosine_similarity([embedding1], [embedding2])[0][0]
        
        # Ensure similarity is between 0 and 1
        similarity = max(0, min(1, similarity))
        
        return float(similarity)
    
    def calculate_resume_job_similarity(self, resume_sections, job_description, job_requirements):
        """
        Calculate comprehensive similarity between resume and job requirements
        
        Args:
            resume_sections (dict): Resume sections from NLP extractor
            job_description (str): Job description text
            job_requirements (dict): Structured job requirements
            
        Returns:
            dict: Detailed similarity analysis
        """
        similarity_analysis = {
            'overall_similarity': 0.0,
            'section_similarities': {},
            'skill_similarity': 0.0,
            'experience_similarity': 0.0,
            'education_similarity': 0.0,
            'contextual_match': 0.0
        }
        
        # 1. Overall resume vs job description similarity
        resume_full_text = resume_sections.get('full_text', '')
        overall_sim = self.calculate_semantic_similarity(resume_full_text, job_description)
        similarity_analysis['overall_similarity'] = overall_sim
        
        # 2. Section-wise similarities
        section_weights = {
            'skills': 0.4,
            'experience': 0.3,
            'education': 0.2,
            'projects': 0.1
        }
        
        weighted_similarity = 0.0
        
        for section, weight in section_weights.items():
            resume_section = resume_sections.get(section, '')
            if resume_section and job_description:
                section_sim = self.calculate_semantic_similarity(resume_section, job_description)
                similarity_analysis['section_similarities'][section] = section_sim
                weighted_similarity += section_sim * weight
            else:
                similarity_analysis['section_similarities'][section] = 0.0
        
        # 3. Skills-specific similarity
        resume_skills_text = resume_sections.get('skills', '')
        required_skills_text = job_requirements.get('required_skills', '') + ' ' + job_requirements.get('tools', '')
        
        if resume_skills_text and required_skills_text:
            skill_sim = self.calculate_semantic_similarity(resume_skills_text, required_skills_text)
            similarity_analysis['skill_similarity'] = skill_sim
        
        # 4. Experience similarity
        resume_experience = resume_sections.get('experience', '')
        job_experience_req = job_requirements.get('experience', '')
        
        if resume_experience and job_experience_req:
            exp_sim = self.calculate_semantic_similarity(resume_experience, job_experience_req)
            similarity_analysis['experience_similarity'] = exp_sim
        
        # 5. Education similarity
        resume_education = resume_sections.get('education', '')
        job_education_req = job_requirements.get('education', '')
        
        if resume_education and job_education_req:
            edu_sim = self.calculate_semantic_similarity(resume_education, job_education_req)
            similarity_analysis['education_similarity'] = edu_sim
        
        # 6. Calculate contextual match (weighted average)
        contextual_match = (
            similarity_analysis['skill_similarity'] * 0.4 +
            similarity_analysis['experience_similarity'] * 0.3 +
            similarity_analysis['education_similarity'] * 0.2 +
            overall_sim * 0.1
        )
        
        similarity_analysis['contextual_match'] = contextual_match
        
        return similarity_analysis
    
    def calculate_eligibility_score(self, similarity_analysis, skill_match_percentage):
        """
        Calculate final eligibility score combining semantic similarity and skill matching
        
        Args:
            similarity_analysis (dict): Semantic similarity analysis
            skill_match_percentage (float): Percentage of skills matched
            
        Returns:
            dict: Eligibility score with breakdown
        """
        # Weights for different components
        semantic_weight = 0.6  # 60% weight for semantic similarity
        skill_weight = 0.4     # 40% weight for exact skill matching
        
        # Get contextual similarity (0-1 range)
        contextual_similarity = similarity_analysis.get('contextual_match', 0.0)
        
        # Convert skill match percentage to 0-1 range
        skill_match_normalized = skill_match_percentage / 100.0
        
        # Calculate weighted eligibility score
        eligibility_score = (
            contextual_similarity * semantic_weight +
            skill_match_normalized * skill_weight
        ) * 100  # Convert to percentage
        
        # Determine eligibility level (Revised Criteria)
        if eligibility_score >= 85:
            eligibility_level = "Highly Eligible"
        elif eligibility_score >= 70:
            eligibility_level = "Eligible"
        else:
            eligibility_level = "Not Eligible"
        
        return {
            'eligibility_score': round(eligibility_score, 2),
            'eligibility_level': eligibility_level,
            'semantic_component': round(contextual_similarity * 100, 2),
            'skill_component': round(skill_match_percentage, 2),
            'breakdown': {
                'semantic_similarity': round(contextual_similarity * semantic_weight * 100, 2),
                'skill_matching': round(skill_match_normalized * skill_weight * 100, 2)
            }
        }
    
    def analyze_skill_context_similarity(self, resume_skills, required_skills):
        """
        Analyze semantic similarity between resume skills and required skills
        
        Args:
            resume_skills (dict): Resume skills with context
            required_skills (list): List of required skills
            
        Returns:
            dict: Skill similarity analysis
        """
        skill_similarities = {}
        
        # Create text representations
        resume_skills_text = []
        for skill, info in resume_skills.items():
            contexts = info.get('contexts', [])
            skill_text = f"{skill} " + " ".join(contexts[:2])  # Use skill name + top 2 contexts
            resume_skills_text.append(skill_text)
        
        resume_skills_combined = " ".join(resume_skills_text)
        required_skills_combined = " ".join(required_skills)
        
        # Calculate overall skill similarity
        overall_skill_similarity = self.calculate_semantic_similarity(
            resume_skills_combined, required_skills_combined
        )
        
        # Calculate individual skill similarities
        for required_skill in required_skills:
            best_similarity = 0.0
            best_match = None
            
            for resume_skill, info in resume_skills.items():
                skill_context = f"{resume_skill} " + " ".join(info.get('contexts', [])[:1])
                similarity = self.calculate_semantic_similarity(skill_context, required_skill)
                
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = resume_skill
            
            skill_similarities[required_skill] = {
                'similarity': best_similarity,
                'best_match': best_match,
                'is_semantic_match': best_similarity > 0.7  # Threshold for semantic match
            }
        
        return {
            'overall_similarity': overall_skill_similarity,
            'individual_similarities': skill_similarities,
            'semantic_matches': sum(1 for s in skill_similarities.values() if s['is_semantic_match'])
        }
    
    def __del__(self):
        """Destructor to save cache when object is destroyed"""
        if hasattr(self, 'embedding_cache') and self.embedding_cache:
            self._save_cache()
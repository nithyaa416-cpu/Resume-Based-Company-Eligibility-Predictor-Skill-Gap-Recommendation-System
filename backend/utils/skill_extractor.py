"""
Skill Extraction Module
Extracts technical skills from resume text using keyword matching
"""

import re
import nltk
from collections import Counter

class SkillExtractor:
    """
    A class to extract skills from resume text
    """
    
    def __init__(self):
        """
        Initialize with predefined skill categories
        """
        # Download required NLTK data (run once)
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
            
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        # Predefined skill categories
        self.skill_categories = {
            'programming_languages': [
                'python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 
                'swift', 'kotlin', 'scala', 'r', 'matlab', 'typescript', 'dart',
                'c', 'objective-c', 'perl', 'shell', 'bash'
            ],
            'web_technologies': [
                'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express',
                'django', 'flask', 'spring', 'bootstrap', 'jquery', 'sass', 'less',
                'webpack', 'babel', 'next.js', 'nuxt.js', 'gatsby'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'sqlite', 'oracle', 'redis',
                'cassandra', 'elasticsearch', 'dynamodb', 'firebase', 'mariadb'
            ],
            'cloud_platforms': [
                'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'digitalocean',
                'docker', 'kubernetes', 'jenkins', 'terraform', 'ansible'
            ],
            'data_science': [
                'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 
                'keras', 'matplotlib', 'seaborn', 'jupyter', 'tableau', 'power bi',
                'spark', 'hadoop', 'machine learning', 'deep learning', 'nlp'
            ],
            'tools': [
                'git', 'github', 'gitlab', 'jira', 'confluence', 'slack', 'trello',
                'postman', 'swagger', 'figma', 'photoshop', 'illustrator'
            ]
        }
        
        # Flatten all skills into one list for easier searching
        self.all_skills = []
        for category, skills in self.skill_categories.items():
            self.all_skills.extend(skills)
    
    def clean_text(self, text):
        """
        Clean and preprocess text
        
        Args:
            text (str): Raw text from resume
            
        Returns:
            str: Cleaned text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep spaces and dots
        text = re.sub(r'[^\w\s\.]', ' ', text)
        
        # Remove extra whitespaces
        text = ' '.join(text.split())
        
        return text
    
    def extract_skills_keyword_matching(self, text):
        """
        Extract skills using keyword matching
        
        Args:
            text (str): Resume text
            
        Returns:
            dict: Categorized skills found in resume
        """
        cleaned_text = self.clean_text(text)
        found_skills = {category: [] for category in self.skill_categories.keys()}
        
        # Search for each skill in each category
        for category, skills in self.skill_categories.items():
            for skill in skills:
                # Use word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                if re.search(pattern, cleaned_text):
                    found_skills[category].append(skill)
        
        # Remove empty categories
        found_skills = {k: v for k, v in found_skills.items() if v}
        
        return found_skills
    
    def extract_all_skills_flat(self, text):
        """
        Extract all skills as a flat list
        
        Args:
            text (str): Resume text
            
        Returns:
            list: List of all skills found
        """
        categorized_skills = self.extract_skills_keyword_matching(text)
        all_skills = []
        
        for category, skills in categorized_skills.items():
            all_skills.extend(skills)
            
        return list(set(all_skills))  # Remove duplicates
    
    def extract_skills_with_readiness_levels(self, text):
        """
        Extract skills with precise readiness levels (Advanced/Intermediate/Beginner/Missing)
        
        Args:
            text (str): Resume text
            
        Returns:
            dict: Skills with their readiness levels and occurrence counts
        """
        cleaned_text = self.clean_text(text)
        skills_with_levels = {}
        
        # Get skill frequency for all known skills
        for skill in self.all_skills:
            count = self._count_skill_occurrences(skill, cleaned_text)
            
            if count > 0:
                # Determine readiness level based on occurrence count
                if count >= 4:
                    level = "Advanced"
                elif count >= 2:
                    level = "Intermediate"
                else:  # count == 1
                    level = "Beginner"
                
                skills_with_levels[skill] = {
                    'level': level,
                    'occurrences': count,
                    'category': self._get_skill_category(skill)
                }
        
        return skills_with_levels
    
    def _count_skill_occurrences(self, skill, text):
        """
        Count exact occurrences of a skill in text
        
        Args:
            skill (str): Skill to count
            text (str): Text to search in
            
        Returns:
            int: Number of occurrences
        """
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        matches = re.findall(pattern, text.lower())
        return len(matches)
    
    def get_missing_skills_from_requirements(self, resume_skills, required_skills):
        """
        Get skills that are required but missing from resume
        
        Args:
            resume_skills (dict): Skills found in resume with levels
            required_skills (list): List of required skills
            
        Returns:
            list: Missing skills with "Missing" level
        """
        resume_skill_names = [skill.lower() for skill in resume_skills.keys()]
        missing_skills = []
        
        for required_skill in required_skills:
            if required_skill.lower() not in resume_skill_names:
                missing_skills.append({
                    'skill': required_skill,
                    'level': 'Missing',
                    'occurrences': 0,
                    'category': self._get_skill_category(required_skill)
                })
        
        return missing_skills
    
    def _determine_skill_level(self, skill, count, text):
        """
        Determine skill readiness level based on mentions and context
        
        Args:
            skill (str): Skill name
            count (int): Number of mentions
            text (str): Resume text
            
        Returns:
            str: Skill level (Beginner/Intermediate/Advanced)
        """
        # Context keywords that indicate proficiency
        advanced_keywords = [
            'expert', 'advanced', 'senior', 'lead', 'architect', 'proficient',
            'extensive', 'deep', 'mastery', 'specialized', 'years of experience'
        ]
        
        intermediate_keywords = [
            'experience', 'worked with', 'familiar', 'used', 'implemented',
            'developed', 'built', 'created', 'project'
        ]
        
        # Check for advanced indicators
        skill_pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        skill_contexts = []
        
        # Find sentences containing the skill
        sentences = text.split('.')
        for sentence in sentences:
            if re.search(skill_pattern, sentence.lower()):
                skill_contexts.append(sentence.lower())
        
        # Analyze context for proficiency indicators
        advanced_score = 0
        intermediate_score = 0
        
        for context in skill_contexts:
            for keyword in advanced_keywords:
                if keyword in context:
                    advanced_score += 1
            for keyword in intermediate_keywords:
                if keyword in context:
                    intermediate_score += 1
        
        # Determine level based on mentions and context
        if count >= 4 or advanced_score >= 2:
            return 'Advanced'
        elif count >= 2 or intermediate_score >= 1 or advanced_score >= 1:
            return 'Intermediate'
        else:
            return 'Beginner'
    
    def _get_skill_category(self, skill):
        """
        Get the category of a skill
        
        Args:
            skill (str): Skill name
            
        Returns:
            str: Category name
        """
        for category, skills in self.skill_categories.items():
            if skill.lower() in skills:
                return category.replace('_', ' ').title()
        return 'Other'
    
    def get_skill_frequency(self, text):
        """
        Get frequency of skills mentioned in text
        
        Args:
            text (str): Resume text
            
        Returns:
            dict: Skills with their frequency count
        """
        cleaned_text = self.clean_text(text)
        skill_counts = {}
        
        for skill in self.all_skills:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            count = len(re.findall(pattern, cleaned_text))
            if count > 0:
                skill_counts[skill] = count
                
        return skill_counts
    
    def extract_experience_years(self, text):
        """
        Extract years of experience mentioned in resume
        
        Args:
            text (str): Resume text
            
        Returns:
            list: List of experience years found
        """
        # Pattern to match experience mentions
        patterns = [
            r'(\d+)\s*(?:\+)?\s*years?\s*(?:of)?\s*experience',
            r'(\d+)\s*(?:\+)?\s*yrs?\s*(?:of)?\s*experience',
            r'experience\s*(?:of)?\s*(\d+)\s*(?:\+)?\s*years?',
            r'(\d+)\s*(?:\+)?\s*years?\s*in'
        ]
        
        years = []
        text_lower = text.lower()
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            years.extend([int(year) for year in matches])
            
        return years if years else [0]
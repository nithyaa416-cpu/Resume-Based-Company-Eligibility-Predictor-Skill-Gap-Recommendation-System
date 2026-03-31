"""
Advanced NLP-Based Resume Information Extractor
Uses spaCy for intelligent text processing and information extraction (with fallback)
"""

import re
import logging
from collections import defaultdict, Counter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NLPResumeExtractor:
    """
    Advanced resume information extractor using spaCy NLP
    """
    
    def __init__(self):
        """
        Initialize the NLP extractor with spaCy model (with fallback)
        """
        try:
            # Try to load spaCy English model
            import spacy
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy model loaded successfully")
        except (OSError, ImportError, Exception) as e:
            logger.warning(f"spaCy model not available: {e}. Using basic extraction.")
            self.nlp = None
        
        # Define section keywords for intelligent parsing
        self.section_keywords = {
            'experience': [
                'experience', 'work experience', 'professional experience', 
                'employment', 'work history', 'career', 'positions'
            ],
            'education': [
                'education', 'academic', 'qualifications', 'degree', 
                'university', 'college', 'school', 'certification'
            ],
            'skills': [
                'skills', 'technical skills', 'technologies', 'competencies',
                'expertise', 'proficiencies', 'tools', 'programming'
            ],
            'projects': [
                'projects', 'portfolio', 'work samples', 'achievements',
                'accomplishments', 'key projects'
            ]
        }
        
        # Enhanced skill patterns with context
        self.skill_patterns = {
            'programming_languages': [
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 
                'ruby', 'go', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'dart',
                'c', 'objective-c', 'perl', 'shell', 'bash', 'powershell'
            ],
            'web_technologies': [
                'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express',
                'django', 'flask', 'spring', 'bootstrap', 'jquery', 'sass', 'less',
                'webpack', 'babel', 'next.js', 'nuxt.js', 'gatsby', 'svelte'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'sqlite', 'oracle', 'redis',
                'cassandra', 'elasticsearch', 'dynamodb', 'firebase', 'mariadb',
                'neo4j', 'influxdb', 'couchdb'
            ],
            'cloud_platforms': [
                'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'digitalocean',
                'docker', 'kubernetes', 'jenkins', 'terraform', 'ansible',
                'vagrant', 'chef', 'puppet'
            ],
            'data_science': [
                'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 
                'keras', 'matplotlib', 'seaborn', 'jupyter', 'tableau', 'power bi',
                'spark', 'hadoop', 'machine learning', 'deep learning', 'nlp',
                'computer vision', 'data mining', 'statistics'
            ],
            'tools': [
                'git', 'github', 'gitlab', 'jira', 'confluence', 'slack', 'trello',
                'postman', 'swagger', 'figma', 'photoshop', 'illustrator',
                'vs code', 'intellij', 'eclipse', 'vim', 'emacs'
            ]
        }
        
        # Flatten all skills for easy searching
        self.all_skills = []
        for category, skills in self.skill_patterns.items():
            self.all_skills.extend(skills)
    
    def extract_resume_sections(self, text):
        """
        Extract different sections from resume using NLP and pattern matching
        
        Args:
            text (str): Resume text
            
        Returns:
            dict: Extracted sections with their content
        """
        sections = {
            'experience': '',
            'education': '',
            'skills': '',
            'projects': '',
            'summary': '',
            'full_text': text
        }
        
        # Clean and normalize text
        text = self._clean_text(text)
        lines = text.split('\n')
        
        current_section = 'summary'
        section_content = defaultdict(list)
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line is a section header
            detected_section = self._detect_section(line)
            if detected_section:
                current_section = detected_section
                continue
            
            # Add content to current section
            section_content[current_section].append(line)
        
        # Join content for each section
        for section in sections.keys():
            if section != 'full_text':
                sections[section] = '\n'.join(section_content[section])
        
        return sections
    
    def extract_skills_with_context(self, text):
        """
        Extract skills with contextual information using NLP
        
        Args:
            text (str): Resume text
            
        Returns:
            dict: Skills with context and frequency information
        """
        skills_with_context = {}
        text_lower = text.lower()
        
        # Use spaCy for better context understanding if available
        if self.nlp:
            doc = self.nlp(text)
            sentences = [sent.text for sent in doc.sents]
        else:
            sentences = text.split('.')
        
        for skill in self.all_skills:
            skill_lower = skill.lower()
            contexts = []
            total_mentions = 0
            
            # Find skill mentions with context
            for sentence in sentences:
                sentence_lower = sentence.lower()
                if self._skill_mentioned_in_sentence(skill_lower, sentence_lower):
                    contexts.append(sentence.strip())
                    total_mentions += sentence_lower.count(skill_lower)
            
            if total_mentions > 0:
                # Determine proficiency level based on context
                proficiency = self._determine_skill_proficiency(skill_lower, contexts, total_mentions)
                
                skills_with_context[skill] = {
                    'mentions': total_mentions,
                    'proficiency': proficiency,
                    'contexts': contexts[:3],  # Keep top 3 contexts
                    'category': self._get_skill_category(skill)
                }
        
        return skills_with_context
    
    def extract_experience_years(self, text):
        """
        Extract years of experience using advanced pattern matching
        
        Args:
            text (str): Resume text
            
        Returns:
            dict: Experience information with details
        """
        experience_info = {
            'total_years': 0,
            'experience_mentions': [],
            'confidence': 'low'
        }
        
        # Enhanced patterns for experience extraction
        patterns = [
            r'(\d+)\s*(?:\+)?\s*years?\s*(?:of)?\s*experience',
            r'(\d+)\s*(?:\+)?\s*yrs?\s*(?:of)?\s*experience',
            r'experience\s*(?:of)?\s*(\d+)\s*(?:\+)?\s*years?',
            r'(\d+)\s*(?:\+)?\s*years?\s*in\s*(?:the\s*)?(?:field|industry)',
            r'over\s*(\d+)\s*years?\s*(?:of)?\s*experience',
            r'more\s*than\s*(\d+)\s*years?\s*(?:of)?\s*experience'
        ]
        
        years_found = []
        text_lower = text.lower()
        
        for pattern in patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                years = int(match.group(1))
                context = text_lower[max(0, match.start()-50):match.end()+50]
                years_found.append({
                    'years': years,
                    'context': context.strip(),
                    'pattern': pattern
                })
        
        if years_found:
            # Take the maximum years mentioned
            experience_info['total_years'] = max(item['years'] for item in years_found)
            experience_info['experience_mentions'] = years_found
            experience_info['confidence'] = 'high' if len(years_found) > 1 else 'medium'
        
        return experience_info
    
    def extract_education_info(self, education_text):
        """
        Extract education information using NLP
        
        Args:
            education_text (str): Education section text
            
        Returns:
            dict: Education information
        """
        education_info = {
            'degrees': [],
            'institutions': [],
            'fields_of_study': [],
            'graduation_years': []
        }
        
        if not education_text:
            return education_info
        
        # Degree patterns
        degree_patterns = [
            r'\b(?:bachelor|master|phd|doctorate|associate|diploma|certificate)\b.*?(?:in|of)\s*([^,\n]+)',
            r'\b(b\.?s\.?|m\.?s\.?|m\.?a\.?|ph\.?d\.?|b\.?a\.?|b\.?tech|m\.?tech)\b.*?(?:in|of)?\s*([^,\n]*)',
        ]
        
        for pattern in degree_patterns:
            matches = re.finditer(pattern, education_text.lower())
            for match in matches:
                if len(match.groups()) > 1:
                    education_info['fields_of_study'].append(match.group(2).strip())
                education_info['degrees'].append(match.group(0).strip())
        
        # Extract years
        year_pattern = r'\b(19|20)\d{2}\b'
        years = re.findall(year_pattern, education_text)
        education_info['graduation_years'] = [int(year) for year in years]
        
        return education_info
    
    def _clean_text(self, text):
        """Clean and normalize text"""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\.\,\-\(\)]', ' ', text)
        return text.strip()
    
    def _detect_section(self, line):
        """Detect if a line is a section header"""
        line_lower = line.lower().strip()
        
        # Skip very short lines
        if len(line_lower) < 3:
            return None
        
        # Check against section keywords
        for section, keywords in self.section_keywords.items():
            for keyword in keywords:
                if keyword in line_lower and len(line_lower) < 50:
                    return section
        
        return None
    
    def _skill_mentioned_in_sentence(self, skill, sentence):
        """Check if skill is mentioned in sentence with word boundaries"""
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(skill) + r'\b'
        return bool(re.search(pattern, sentence))
    
    def _determine_skill_proficiency(self, skill, contexts, mentions):
        """Determine skill proficiency based on context and mentions"""
        # Context keywords that indicate proficiency levels
        expert_keywords = [
            'expert', 'advanced', 'senior', 'lead', 'architect', 'specialist',
            'proficient', 'extensive', 'deep', 'mastery', 'years of experience'
        ]
        
        intermediate_keywords = [
            'experience', 'worked with', 'familiar', 'used', 'implemented',
            'developed', 'built', 'created', 'project', 'good knowledge'
        ]
        
        beginner_keywords = [
            'learning', 'basic', 'introduction', 'beginner', 'started',
            'course', 'tutorial', 'fundamentals'
        ]
        
        # Analyze contexts for proficiency indicators
        context_text = ' '.join(contexts).lower()
        
        expert_score = sum(1 for keyword in expert_keywords if keyword in context_text)
        intermediate_score = sum(1 for keyword in intermediate_keywords if keyword in context_text)
        beginner_score = sum(1 for keyword in beginner_keywords if keyword in context_text)
        
        # Determine proficiency based on mentions and context
        if mentions >= 4 or expert_score >= 2:
            return 'Advanced'
        elif mentions >= 2 or intermediate_score >= 1 or expert_score >= 1:
            return 'Intermediate'
        elif beginner_score >= 1:
            return 'Beginner'
        else:
            return 'Intermediate'  # Default for single mention
    
    def _get_skill_category(self, skill):
        """Get the category of a skill"""
        for category, skills in self.skill_patterns.items():
            if skill.lower() in skills:
                return category.replace('_', ' ').title()
        return 'Other'
    
    def extract_comprehensive_info(self, resume_text):
        """
        Extract comprehensive information from resume
        
        Args:
            resume_text (str): Full resume text
            
        Returns:
            dict: Comprehensive resume information
        """
        # Extract sections
        sections = self.extract_resume_sections(resume_text)
        
        # Extract skills with context
        skills_info = self.extract_skills_with_context(resume_text)
        
        # Extract experience
        experience_info = self.extract_experience_years(resume_text)
        
        # Extract education
        education_info = self.extract_education_info(sections['education'])
        
        return {
            'sections': sections,
            'skills': skills_info,
            'experience': experience_info,
            'education': education_info,
            'total_skills_found': len(skills_info),
            'processing_status': 'success'
        }
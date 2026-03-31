"""
Learning Platform Recommendation System
Provides free and paid learning resources for missing skills
"""

class LearningRecommender:
    """
    A class to recommend learning platforms for missing skills
    """
    
    def __init__(self):
        """
        Initialize with predefined learning platform mappings
        """
        # Comprehensive learning platform mapping
        self.learning_platforms = {
            # Programming Languages
            'python': {
                'free': ['YouTube (Corey Schafer)', 'freeCodeCamp', 'Python.org Tutorial', 'Codecademy (Free Tier)'],
                'paid': ['Coursera (Python for Everybody)', 'Udemy (Complete Python Bootcamp)', 'Pluralsight', 'DataCamp']
            },
            'java': {
                'free': ['YouTube (Derek Banas)', 'Oracle Java Tutorials', 'Codecademy (Free Tier)', 'Java Code Geeks'],
                'paid': ['Coursera (Java Programming)', 'Udemy (Java Masterclass)', 'Pluralsight', 'LinkedIn Learning']
            },
            'javascript': {
                'free': ['YouTube (Traversy Media)', 'freeCodeCamp', 'MDN Web Docs', 'JavaScript.info'],
                'paid': ['Coursera (JavaScript Essentials)', 'Udemy (JavaScript Complete Course)', 'Pluralsight', 'Frontend Masters']
            },
            'c++': {
                'free': ['YouTube (The Cherno)', 'LearnCpp.com', 'GeeksforGeeks', 'Codecademy (Free Tier)'],
                'paid': ['Coursera (C++ Programming)', 'Udemy (C++ Complete Course)', 'Pluralsight', 'LinkedIn Learning']
            },
            'c#': {
                'free': ['YouTube (Brackeys)', 'Microsoft Learn', 'C# Corner', 'Codecademy (Free Tier)'],
                'paid': ['Coursera (C# Programming)', 'Udemy (C# Masterclass)', 'Pluralsight', 'LinkedIn Learning']
            },
            
            # Web Technologies
            'react': {
                'free': ['YouTube (Traversy Media)', 'React Official Docs', 'freeCodeCamp', 'Scrimba (Free Tier)'],
                'paid': ['Coursera (React Specialization)', 'Udemy (React Complete Guide)', 'Pluralsight', 'Frontend Masters']
            },
            'angular': {
                'free': ['YouTube (Academind)', 'Angular Official Docs', 'freeCodeCamp', 'Angular University (Free)'],
                'paid': ['Coursera (Angular Course)', 'Udemy (Angular Complete Guide)', 'Pluralsight', 'LinkedIn Learning']
            },
            'vue': {
                'free': ['YouTube (Vue Mastery Free)', 'Vue.js Official Docs', 'freeCodeCamp', 'Laracasts (Free Tier)'],
                'paid': ['Coursera (Vue.js Course)', 'Udemy (Vue Complete Guide)', 'Vue Mastery', 'Frontend Masters']
            },
            'node.js': {
                'free': ['YouTube (Traversy Media)', 'Node.js Official Docs', 'freeCodeCamp', 'NodeSchool'],
                'paid': ['Coursera (Node.js Course)', 'Udemy (Node.js Complete Guide)', 'Pluralsight', 'LinkedIn Learning']
            },
            'django': {
                'free': ['YouTube (Corey Schafer)', 'Django Official Tutorial', 'freeCodeCamp', 'Django Girls Tutorial'],
                'paid': ['Coursera (Django Course)', 'Udemy (Django Complete Course)', 'Pluralsight', 'Real Python']
            },
            'flask': {
                'free': ['YouTube (Corey Schafer)', 'Flask Official Docs', 'freeCodeCamp', 'Flask Mega-Tutorial'],
                'paid': ['Coursera (Flask Course)', 'Udemy (Flask Complete Course)', 'Pluralsight', 'Real Python']
            },
            
            # Databases
            'sql': {
                'free': ['YouTube (Programming with Mosh)', 'W3Schools SQL', 'SQLBolt', 'Mode Analytics SQL Tutorial'],
                'paid': ['Coursera (SQL Specialization)', 'Udemy (SQL Masterclass)', 'Pluralsight', 'DataCamp']
            },
            'mysql': {
                'free': ['YouTube (Derek Banas)', 'MySQL Official Tutorial', 'W3Schools MySQL', 'GeeksforGeeks'],
                'paid': ['Coursera (MySQL Course)', 'Udemy (MySQL Complete Course)', 'Pluralsight', 'LinkedIn Learning']
            },
            'postgresql': {
                'free': ['YouTube (Amigoscode)', 'PostgreSQL Official Tutorial', 'PostgreSQL Exercises', 'freeCodeCamp'],
                'paid': ['Coursera (PostgreSQL Course)', 'Udemy (PostgreSQL Masterclass)', 'Pluralsight', 'DataCamp']
            },
            'mongodb': {
                'free': ['YouTube (Traversy Media)', 'MongoDB University (Free)', 'freeCodeCamp', 'MongoDB Official Docs'],
                'paid': ['Coursera (MongoDB Course)', 'Udemy (MongoDB Complete Guide)', 'Pluralsight', 'LinkedIn Learning']
            },
            
            # Cloud Platforms
            'aws': {
                'free': ['YouTube (freeCodeCamp AWS)', 'AWS Free Tier', 'AWS Training (Free)', 'A Cloud Guru (Free Tier)'],
                'paid': ['Coursera (AWS Specialization)', 'Udemy (AWS Certified Solutions Architect)', 'A Cloud Guru', 'Linux Academy']
            },
            'azure': {
                'free': ['YouTube (Adam Marczak)', 'Microsoft Learn (Free)', 'Azure Free Account', 'freeCodeCamp'],
                'paid': ['Coursera (Azure Fundamentals)', 'Udemy (Azure Complete Course)', 'Pluralsight', 'A Cloud Guru']
            },
            'gcp': {
                'free': ['YouTube (Google Cloud)', 'Google Cloud Skills Boost (Free)', 'Coursera (Free Tier)', 'freeCodeCamp'],
                'paid': ['Coursera (GCP Specialization)', 'Udemy (GCP Complete Course)', 'A Cloud Guru', 'Linux Academy']
            },
            
            # DevOps Tools
            'docker': {
                'free': ['YouTube (TechWorld with Nana)', 'Docker Official Tutorial', 'freeCodeCamp', 'Play with Docker'],
                'paid': ['Coursera (Docker Course)', 'Udemy (Docker Mastery)', 'Pluralsight', 'A Cloud Guru']
            },
            'kubernetes': {
                'free': ['YouTube (TechWorld with Nana)', 'Kubernetes Official Tutorial', 'freeCodeCamp', 'Katacoda'],
                'paid': ['Coursera (Kubernetes Course)', 'Udemy (Kubernetes Mastery)', 'A Cloud Guru', 'Linux Academy']
            },
            'git': {
                'free': ['YouTube (Traversy Media)', 'Git Official Tutorial', 'Atlassian Git Tutorial', 'freeCodeCamp'],
                'paid': ['Coursera (Git Course)', 'Udemy (Git Complete Course)', 'Pluralsight', 'LinkedIn Learning']
            },
            
            # Data Science & ML
            'machine learning': {
                'free': ['YouTube (3Blue1Brown)', 'Coursera (Andrew Ng Free Audit)', 'Kaggle Learn', 'freeCodeCamp'],
                'paid': ['Coursera (Machine Learning Specialization)', 'Udemy (ML A-Z)', 'edX (MIT ML)', 'DataCamp']
            },
            'deep learning': {
                'free': ['YouTube (3Blue1Brown)', 'Fast.ai', 'Deep Learning AI (Free Audit)', 'Kaggle Learn'],
                'paid': ['Coursera (Deep Learning Specialization)', 'Udemy (Deep Learning A-Z)', 'edX (MIT Deep Learning)', 'DataCamp']
            },
            'tensorflow': {
                'free': ['YouTube (TensorFlow)', 'TensorFlow Official Tutorial', 'Kaggle Learn', 'freeCodeCamp'],
                'paid': ['Coursera (TensorFlow Specialization)', 'Udemy (TensorFlow Complete Course)', 'Pluralsight', 'DataCamp']
            },
            'pytorch': {
                'free': ['YouTube (PyTorch)', 'PyTorch Official Tutorial', 'Fast.ai', 'freeCodeCamp'],
                'paid': ['Coursera (PyTorch Course)', 'Udemy (PyTorch Complete Course)', 'Pluralsight', 'DataCamp']
            },
            'nlp': {
                'free': ['YouTube (Krish Naik)', 'Hugging Face Course', 'spaCy Tutorial', 'NLTK Tutorial'],
                'paid': ['Coursera (NLP Specialization)', 'Udemy (NLP Complete Course)', 'edX (NLP)', 'DataCamp']
            },
            'pandas': {
                'free': ['YouTube (Corey Schafer)', 'Pandas Official Tutorial', 'Kaggle Learn', 'freeCodeCamp'],
                'paid': ['Coursera (Pandas Course)', 'Udemy (Pandas Masterclass)', 'DataCamp', 'Real Python']
            },
            'numpy': {
                'free': ['YouTube (Keith Galli)', 'NumPy Official Tutorial', 'freeCodeCamp', 'Kaggle Learn'],
                'paid': ['Coursera (NumPy Course)', 'Udemy (NumPy Complete Course)', 'DataCamp', 'Real Python']
            }
        }
    
    def get_learning_recommendations(self, missing_skills):
        """
        Get learning platform recommendations for missing skills
        
        Args:
            missing_skills (list): List of missing skill names
            
        Returns:
            dict: Learning recommendations with free and paid options
        """
        recommendations = {}
        
        for skill in missing_skills:
            skill_lower = skill.lower()
            
            if skill_lower in self.learning_platforms:
                recommendations[skill] = self.learning_platforms[skill_lower]
            else:
                # Default recommendations for unknown skills
                recommendations[skill] = {
                    'free': ['YouTube', 'freeCodeCamp', 'GeeksforGeeks', 'Official Documentation'],
                    'paid': ['Coursera', 'Udemy', 'Pluralsight', 'LinkedIn Learning']
                }
        
        return recommendations
    
    def get_skill_learning_roadmap(self, missing_skills):
        """
        Generate a structured learning roadmap based on skill dependencies
        
        Args:
            missing_skills (list): List of missing skills
            
        Returns:
            dict: Structured learning roadmap with phases
        """
        # Skill dependency mapping (prerequisite → advanced)
        skill_dependencies = {
            # Programming fundamentals
            'python': [],
            'java': [],
            'javascript': [],
            'c++': [],
            'c#': [],
            
            # Web development progression
            'html': [],
            'css': ['html'],
            'react': ['javascript', 'html', 'css'],
            'angular': ['javascript', 'html', 'css'],
            'vue': ['javascript', 'html', 'css'],
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
            'azure': [],
            'gcp': [],
            
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
        
        # Calculate learning phases
        roadmap = {
            'total_skills': len(missing_skills),
            'estimated_duration': f"{len(missing_skills) * 2}-{len(missing_skills) * 4} weeks",
            'learning_path': []
        }
        
        if not missing_skills:
            return roadmap
        
        # Sort skills by dependency level
        skill_levels = {}
        for skill in missing_skills:
            skill_lower = skill.lower()
            dependencies = skill_dependencies.get(skill_lower, [])
            
            # Count dependencies that are also in missing skills
            missing_deps = [dep for dep in dependencies if dep in [s.lower() for s in missing_skills]]
            skill_levels[skill] = len(missing_deps)
        
        # Group skills by learning phases
        phase_1 = [skill for skill, level in skill_levels.items() if level == 0]
        phase_2 = [skill for skill, level in skill_levels.items() if level == 1]
        phase_3 = [skill for skill, level in skill_levels.items() if level >= 2]
        
        # Create structured learning path
        phase_counter = 1
        
        if phase_1:
            roadmap['learning_path'].append({
                'phase': phase_counter,
                'title': 'Foundation Phase',
                'description': 'Start with fundamental skills that have no prerequisites',
                'skills': phase_1,
                'estimated_time': f"{len(phase_1) * 2}-{len(phase_1) * 3} weeks",
                'priority': 'High'
            })
            phase_counter += 1
        
        if phase_2:
            roadmap['learning_path'].append({
                'phase': phase_counter,
                'title': 'Building Phase',
                'description': 'Build on your foundation with intermediate skills',
                'skills': phase_2,
                'estimated_time': f"{len(phase_2) * 2}-{len(phase_2) * 4} weeks",
                'priority': 'Medium'
            })
            phase_counter += 1
        
        if phase_3:
            roadmap['learning_path'].append({
                'phase': phase_counter,
                'title': 'Advanced Phase',
                'description': 'Master complex technologies and frameworks',
                'skills': phase_3,
                'estimated_time': f"{len(phase_3) * 3}-{len(phase_3) * 5} weeks",
                'priority': 'Low'
            })
        
        return roadmap
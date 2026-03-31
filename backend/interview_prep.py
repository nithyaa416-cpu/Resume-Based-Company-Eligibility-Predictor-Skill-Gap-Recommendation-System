#!/usr/bin/env python3
"""
Interview Preparation System
AI-powered interview question generation, practice sessions, and feedback
"""

import json
import logging
import random
from typing import List, Dict, Optional
from datetime import datetime
import sqlite3
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InterviewPrep:
    """AI-powered interview preparation system"""
    
    def __init__(self, db_path=None):
        if db_path is None:
            backend_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(backend_dir, "database", "jobs.db")
        else:
            self.db_path = db_path
        
        # Initialize interview prep tables
        self._create_interview_tables()
        
        # Load question templates
        self._load_question_templates()
        
        logger.info("Interview preparation system initialized")
    
    def _create_interview_tables(self):
        """Create interview preparation database tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Interview sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS interview_sessions (
                    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    company_name TEXT,
                    job_role TEXT,
                    session_type TEXT,
                    questions_asked TEXT,
                    user_responses TEXT,
                    feedback_scores TEXT,
                    overall_score REAL,
                    session_duration INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )
            """)
            
            # Interview feedback table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS interview_feedback (
                    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER,
                    question_id INTEGER,
                    user_response TEXT,
                    ai_feedback TEXT,
                    improvement_suggestions TEXT,
                    score REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(session_id) REFERENCES interview_sessions(session_id)
                )
            """)
            
            # Practice progress table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS practice_progress (
                    progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    skill_area TEXT,
                    practice_count INTEGER DEFAULT 0,
                    average_score REAL DEFAULT 0,
                    last_practiced TIMESTAMP,
                    improvement_rate REAL DEFAULT 0,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info("Interview preparation tables created successfully")
            
        except Exception as e:
            logger.error(f"Error creating interview tables: {e}")
            raise
    
    def _load_question_templates(self):
        """Load interview question templates by category"""
        self.question_templates = {
            'behavioral': [
                {
                    'question': "Tell me about a time when you had to work with a difficult team member.",
                    'category': 'teamwork',
                    'difficulty': 'medium',
                    'evaluation_criteria': ['situation_description', 'actions_taken', 'outcome', 'learning']
                },
                {
                    'question': "Describe a challenging project you worked on and how you overcame obstacles.",
                    'category': 'problem_solving',
                    'difficulty': 'medium',
                    'evaluation_criteria': ['problem_identification', 'solution_approach', 'implementation', 'results']
                },
                {
                    'question': "Tell me about a time when you had to learn a new technology quickly.",
                    'category': 'adaptability',
                    'difficulty': 'easy',
                    'evaluation_criteria': ['learning_approach', 'time_management', 'application', 'outcome']
                },
                {
                    'question': "Describe a situation where you had to make a decision with incomplete information.",
                    'category': 'decision_making',
                    'difficulty': 'hard',
                    'evaluation_criteria': ['analysis_process', 'risk_assessment', 'decision_rationale', 'outcome']
                }
            ],
            'technical': {
                'software_engineer': [
                    {
                        'question': "Explain the difference between SQL and NoSQL databases. When would you use each?",
                        'category': 'databases',
                        'difficulty': 'medium',
                        'evaluation_criteria': ['technical_accuracy', 'use_cases', 'trade_offs', 'examples']
                    },
                    {
                        'question': "How would you design a URL shortener like bit.ly?",
                        'category': 'system_design',
                        'difficulty': 'hard',
                        'evaluation_criteria': ['requirements_gathering', 'architecture', 'scalability', 'trade_offs']
                    },
                    {
                        'question': "What is the difference between synchronous and asynchronous programming?",
                        'category': 'programming_concepts',
                        'difficulty': 'medium',
                        'evaluation_criteria': ['concept_understanding', 'examples', 'use_cases', 'implementation']
                    }
                ],
                'data_scientist': [
                    {
                        'question': "Explain the bias-variance tradeoff in machine learning.",
                        'category': 'ml_theory',
                        'difficulty': 'medium',
                        'evaluation_criteria': ['concept_understanding', 'examples', 'practical_implications', 'solutions']
                    },
                    {
                        'question': "How would you handle missing data in a dataset?",
                        'category': 'data_preprocessing',
                        'difficulty': 'easy',
                        'evaluation_criteria': ['methods_knowledge', 'decision_criteria', 'impact_analysis', 'implementation']
                    }
                ],
                'frontend_engineer': [
                    {
                        'question': "Explain the concept of virtual DOM and its benefits.",
                        'category': 'react',
                        'difficulty': 'medium',
                        'evaluation_criteria': ['concept_understanding', 'benefits', 'implementation', 'alternatives']
                    },
                    {
                        'question': "How would you optimize the performance of a React application?",
                        'category': 'performance',
                        'difficulty': 'hard',
                        'evaluation_criteria': ['optimization_techniques', 'measurement_tools', 'best_practices', 'trade_offs']
                    }
                ]
            },
            'company_specific': {
                'Google': [
                    {
                        'question': "How would you improve Google Search?",
                        'category': 'product_thinking',
                        'difficulty': 'hard',
                        'evaluation_criteria': ['user_understanding', 'problem_identification', 'solution_creativity', 'feasibility']
                    }
                ],
                'Amazon': [
                    {
                        'question': "Tell me about a time when you had to work backwards from a customer need.",
                        'category': 'customer_obsession',
                        'difficulty': 'medium',
                        'evaluation_criteria': ['customer_focus', 'problem_solving', 'innovation', 'results']
                    }
                ]
            }
        }
    
    def generate_interview_questions(self, company_name: str, job_role: str, difficulty: str = 'mixed', count: int = 10) -> List[Dict]:
        """Generate personalized interview questions"""
        questions = []
        
        # Add behavioral questions (40%)
        behavioral_count = max(1, int(count * 0.4))
        behavioral_questions = self._select_questions(
            self.question_templates['behavioral'], 
            behavioral_count, 
            difficulty
        )
        questions.extend(behavioral_questions)
        
        # Add technical questions based on role (50%)
        technical_count = max(1, int(count * 0.5))
        role_key = self._map_role_to_key(job_role)
        if role_key in self.question_templates['technical']:
            technical_questions = self._select_questions(
                self.question_templates['technical'][role_key],
                technical_count,
                difficulty
            )
            questions.extend(technical_questions)
        
        # Add company-specific questions (10%)
        company_count = max(1, int(count * 0.1))
        if company_name in self.question_templates['company_specific']:
            company_questions = self._select_questions(
                self.question_templates['company_specific'][company_name],
                company_count,
                difficulty
            )
            questions.extend(company_questions)
        
        # Fill remaining with general questions if needed
        while len(questions) < count:
            all_questions = (self.question_templates['behavioral'] + 
                           [q for role_qs in self.question_templates['technical'].values() for q in role_qs])
            remaining = self._select_questions(all_questions, count - len(questions), difficulty)
            questions.extend(remaining)
        
        # Add question IDs and metadata
        for i, question in enumerate(questions):
            question['id'] = i + 1
            question['company'] = company_name
            question['role'] = job_role
        
        return questions[:count]
    
    def _select_questions(self, question_pool: List[Dict], count: int, difficulty: str) -> List[Dict]:
        """Select questions based on difficulty and count"""
        if difficulty == 'mixed':
            selected = random.sample(question_pool, min(count, len(question_pool)))
        else:
            filtered = [q for q in question_pool if q.get('difficulty') == difficulty]
            if not filtered:
                filtered = question_pool
            selected = random.sample(filtered, min(count, len(filtered)))
        
        return selected
    
    def _map_role_to_key(self, job_role: str) -> str:
        """Map job role to technical question category"""
        role_lower = job_role.lower()
        if 'software' in role_lower or 'backend' in role_lower or 'full stack' in role_lower:
            return 'software_engineer'
        elif 'frontend' in role_lower or 'react' in role_lower or 'ui' in role_lower:
            return 'frontend_engineer'
        elif 'data scientist' in role_lower or 'ml engineer' in role_lower or 'ai engineer' in role_lower:
            return 'data_scientist'
        else:
            return 'software_engineer'  # Default
    
    def start_practice_session(self, user_id: int, company_name: str, job_role: str, session_type: str = 'mixed') -> Dict:
        """Start a new interview practice session"""
        try:
            # Generate questions for the session
            questions = self.generate_interview_questions(company_name, job_role, session_type, 5)
            
            # Save session to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO interview_sessions 
                (user_id, company_name, job_role, session_type, questions_asked)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, company_name, job_role, session_type, json.dumps(questions)))
            
            session_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            logger.info(f"Interview practice session started for user {user_id}, session_id: {session_id}")
            
            return {
                'session_id': session_id,
                'questions': questions,
                'total_questions': len(questions),
                'session_type': session_type,
                'company_name': company_name,
                'job_role': job_role
            }
            
        except Exception as e:
            logger.error(f"Error starting practice session: {e}")
            return {'error': 'Failed to start practice session'}
    
    def evaluate_response(self, session_id: int, question_id: int, user_response: str) -> Dict:
        """Evaluate user's response to interview question"""
        try:
            # Get question details
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT questions_asked FROM interview_sessions WHERE session_id = ?", (session_id,))
            result = cursor.fetchone()
            
            if not result:
                return {'error': 'Session not found'}
            
            questions = json.loads(result[0])
            question = next((q for q in questions if q['id'] == question_id), None)
            
            if not question:
                return {'error': 'Question not found'}
            
            # Generate AI feedback (simplified version)
            feedback = self._generate_feedback(question, user_response)
            
            # Save feedback
            cursor.execute("""
                INSERT INTO interview_feedback 
                (session_id, question_id, user_response, ai_feedback, improvement_suggestions, score)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                session_id, question_id, user_response, 
                feedback['feedback'], json.dumps(feedback['suggestions']), feedback['score']
            ))
            
            conn.commit()
            conn.close()
            
            return feedback
            
        except Exception as e:
            logger.error(f"Error evaluating response: {e}")
            return {'error': 'Failed to evaluate response'}
    
    def _generate_feedback(self, question: Dict, response: str) -> Dict:
        """Generate AI feedback for user response (simplified)"""
        # This is a simplified version. In production, you'd use more sophisticated NLP
        
        response_length = len(response.split())
        criteria = question.get('evaluation_criteria', [])
        
        # Basic scoring logic
        score = 50  # Base score
        
        # Length check
        if response_length < 20:
            score -= 20
            feedback = "Your response is too brief. Try to provide more detailed examples and context."
        elif response_length > 200:
            score -= 10
            feedback = "Your response is quite long. Try to be more concise while maintaining key details."
        else:
            score += 10
            feedback = "Good response length. "
        
        # Check for STAR method (Situation, Task, Action, Result) in behavioral questions
        if question['category'] in ['teamwork', 'problem_solving', 'adaptability']:
            star_keywords = ['situation', 'task', 'action', 'result', 'challenge', 'outcome']
            found_keywords = sum(1 for keyword in star_keywords if keyword.lower() in response.lower())
            
            if found_keywords >= 3:
                score += 20
                feedback += "Great use of structured storytelling. "
            elif found_keywords >= 1:
                score += 10
                feedback += "Good examples provided. Consider using the STAR method for more structure. "
            else:
                score -= 15
                feedback += "Try to include specific examples with clear situation, actions, and results. "
        
        # Technical accuracy check (simplified)
        if 'technical' in question.get('category', ''):
            technical_terms = ['algorithm', 'database', 'api', 'framework', 'architecture', 'performance', 'scalability']
            found_terms = sum(1 for term in technical_terms if term.lower() in response.lower())
            
            if found_terms >= 2:
                score += 15
                feedback += "Good technical depth. "
            else:
                score -= 10
                feedback += "Consider adding more technical details and terminology. "
        
        # Ensure score is within bounds
        score = max(0, min(100, score))
        
        suggestions = self._generate_improvement_suggestions(question, response, score)
        
        return {
            'score': score,
            'feedback': feedback,
            'suggestions': suggestions,
            'criteria_met': len(criteria)  # Simplified
        }
    
    def _generate_improvement_suggestions(self, question: Dict, response: str, score: int) -> List[str]:
        """Generate specific improvement suggestions"""
        suggestions = []
        
        if score < 60:
            suggestions.append("Practice answering this type of question with more specific examples")
            suggestions.append("Research common interview questions for this role")
        
        if question.get('category') == 'behavioral':
            suggestions.append("Use the STAR method: Situation, Task, Action, Result")
            suggestions.append("Quantify your achievements with specific numbers or metrics")
        
        if 'technical' in question.get('category', ''):
            suggestions.append("Review fundamental concepts related to this topic")
            suggestions.append("Practice explaining technical concepts in simple terms")
        
        if len(response.split()) < 30:
            suggestions.append("Provide more detailed explanations and examples")
        
        return suggestions
    
    def get_practice_progress(self, user_id: int) -> Dict:
        """Get user's interview practice progress and analytics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get session statistics
            cursor.execute("""
                SELECT COUNT(*) as total_sessions, AVG(overall_score) as avg_score
                FROM interview_sessions 
                WHERE user_id = ? AND overall_score IS NOT NULL
            """, (user_id,))
            
            session_stats = cursor.fetchone()
            total_sessions = session_stats[0] if session_stats else 0
            avg_score = round(session_stats[1], 2) if session_stats and session_stats[1] else 0
            
            # Get recent sessions
            cursor.execute("""
                SELECT company_name, job_role, overall_score, created_at
                FROM interview_sessions 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT 10
            """, (user_id,))
            
            recent_sessions = []
            for row in cursor.fetchall():
                recent_sessions.append({
                    'company': row[0],
                    'role': row[1],
                    'score': row[2],
                    'date': row[3]
                })
            
            # Get skill area progress
            cursor.execute("""
                SELECT skill_area, practice_count, average_score, improvement_rate
                FROM practice_progress 
                WHERE user_id = ?
                ORDER BY average_score DESC
            """, (user_id,))
            
            skill_progress = []
            for row in cursor.fetchall():
                skill_progress.append({
                    'skill': row[0],
                    'practice_count': row[1],
                    'average_score': row[2],
                    'improvement_rate': row[3]
                })
            
            conn.close()
            
            return {
                'total_sessions': total_sessions,
                'average_score': avg_score,
                'recent_sessions': recent_sessions,
                'skill_progress': skill_progress,
                'recommendations': self._generate_practice_recommendations(avg_score, skill_progress)
            }
            
        except Exception as e:
            logger.error(f"Error getting practice progress: {e}")
            return {'error': 'Failed to get practice progress'}
    
    def _generate_practice_recommendations(self, avg_score: float, skill_progress: List[Dict]) -> List[str]:
        """Generate personalized practice recommendations"""
        recommendations = []
        
        if avg_score < 60:
            recommendations.append("Focus on fundamental interview skills and practice basic questions")
            recommendations.append("Record yourself answering questions to improve delivery")
        elif avg_score < 80:
            recommendations.append("Work on advanced behavioral questions and technical depth")
            recommendations.append("Practice company-specific questions for your target companies")
        else:
            recommendations.append("Excellent progress! Focus on leadership and strategic questions")
            recommendations.append("Consider mock interviews with industry professionals")
        
        # Skill-specific recommendations
        if skill_progress:
            weakest_skill = min(skill_progress, key=lambda x: x['average_score'])
            recommendations.append(f"Improve your {weakest_skill['skill']} interview skills")
        
        return recommendations
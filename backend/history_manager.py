#!/usr/bin/env python3
"""
Resume History Tracking System
Track user resume uploads, analyses, and provide historical insights
"""

import sqlite3
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HistoryManager:
    """Manage resume upload and analysis history"""
    
    def __init__(self, db_path=None):
        if db_path is None:
            backend_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(backend_dir, "database", "jobs.db")
        else:
            self.db_path = db_path
        
        # Initialize history tables
        self._create_history_tables()
        logger.info("History manager initialized")
    
    def _create_history_tables(self):
        """Create history tracking database tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Resume uploads table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS resume_uploads (
                    upload_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    resume_filename TEXT,
                    resume_text TEXT,
                    extracted_skills TEXT,
                    extracted_experience TEXT,
                    extracted_education TEXT,
                    upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    file_size INTEGER,
                    file_type TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )
            """)
            
            # Analysis history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analysis_history (
                    analysis_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    upload_id INTEGER,
                    company_name TEXT,
                    job_role TEXT,
                    eligibility_score REAL,
                    ml_score REAL,
                    semantic_score REAL,
                    skill_match_score REAL,
                    matched_skills TEXT,
                    missing_skills TEXT,
                    recommendations TEXT,
                    analysis_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    analysis_type TEXT,
                    full_analysis_data TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(user_id),
                    FOREIGN KEY(upload_id) REFERENCES resume_uploads(upload_id)
                )
            """)
            
            # User preferences table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_preferences (
                    preference_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    preferred_companies TEXT,
                    preferred_roles TEXT,
                    target_skills TEXT,
                    notification_settings TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )
            """)
            
            # Resume versions table (for tracking improvements)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS resume_versions (
                    version_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    version_number INTEGER,
                    resume_text TEXT,
                    changes_made TEXT,
                    improvement_score REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info("History tracking tables created successfully")
            
        except Exception as e:
            logger.error(f"Error creating history tables: {e}")
            raise
    
    def save_resume_upload(self, user_id: int, resume_data: dict) -> int:
        """Save resume upload to history"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO resume_uploads 
                (user_id, resume_filename, resume_text, extracted_skills, 
                 extracted_experience, extracted_education, file_size, file_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                resume_data.get('filename', 'unknown'),
                resume_data.get('text', ''),
                json.dumps(resume_data.get('skills', [])),
                json.dumps(resume_data.get('experience', {})),
                json.dumps(resume_data.get('education', {})),
                resume_data.get('file_size', 0),
                resume_data.get('file_type', 'text')
            ))
            
            upload_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            logger.info(f"Resume upload saved for user {user_id}, upload_id: {upload_id}")
            return upload_id
            
        except Exception as e:
            logger.error(f"Error saving resume upload: {e}")
            return None
    
    def save_analysis_result(self, user_id: int, upload_id: int, analysis_data: dict) -> int:
        """Save analysis result to history"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO analysis_history 
                (user_id, upload_id, company_name, job_role, eligibility_score, 
                 ml_score, semantic_score, skill_match_score, matched_skills, 
                 missing_skills, recommendations, analysis_type, full_analysis_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                upload_id,
                analysis_data.get('company_name', ''),
                analysis_data.get('job_role', ''),
                analysis_data.get('eligibility_score', 0),
                analysis_data.get('ml_score', 0),
                analysis_data.get('semantic_score', 0),
                analysis_data.get('skill_match_score', 0),
                json.dumps(analysis_data.get('matched_skills', [])),
                json.dumps(analysis_data.get('missing_skills', [])),
                json.dumps(analysis_data.get('recommendations', [])),
                analysis_data.get('analysis_type', 'single'),
                json.dumps(analysis_data)
            ))
            
            analysis_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            logger.info(f"Analysis result saved for user {user_id}, analysis_id: {analysis_id}")
            return analysis_id
            
        except Exception as e:
            logger.error(f"Error saving analysis result: {e}")
            return None
    
    def get_user_history(self, user_id: int, limit: int = 50) -> dict:
        """Get user's resume and analysis history"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get resume uploads
            cursor.execute("""
                SELECT upload_id, resume_filename, upload_timestamp, file_type, file_size
                FROM resume_uploads 
                WHERE user_id = ? 
                ORDER BY upload_timestamp DESC 
                LIMIT ?
            """, (user_id, limit))
            
            uploads = []
            for row in cursor.fetchall():
                uploads.append({
                    'upload_id': row[0],
                    'filename': row[1],
                    'timestamp': row[2],
                    'file_type': row[3],
                    'file_size': row[4]
                })
            
            # Get analysis history
            cursor.execute("""
                SELECT analysis_id, company_name, job_role, eligibility_score, 
                       analysis_timestamp, analysis_type
                FROM analysis_history 
                WHERE user_id = ? 
                ORDER BY analysis_timestamp DESC 
                LIMIT ?
            """, (user_id, limit))
            
            analyses = []
            for row in cursor.fetchall():
                analyses.append({
                    'analysis_id': row[0],
                    'company_name': row[1],
                    'job_role': row[2],
                    'eligibility_score': row[3],
                    'timestamp': row[4],
                    'analysis_type': row[5]
                })
            
            conn.close()
            
            return {
                'uploads': uploads,
                'analyses': analyses,
                'total_uploads': len(uploads),
                'total_analyses': len(analyses)
            }
            
        except Exception as e:
            logger.error(f"Error getting user history: {e}")
            return {'error': 'Failed to get user history'}
    
    def get_analysis_trends(self, user_id: int) -> dict:
        """Get user's analysis trends and improvements over time"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get score trends over time
            cursor.execute("""
                SELECT DATE(analysis_timestamp) as date, 
                       AVG(eligibility_score) as avg_score,
                       COUNT(*) as analysis_count
                FROM analysis_history 
                WHERE user_id = ? 
                GROUP BY DATE(analysis_timestamp)
                ORDER BY date DESC
                LIMIT 30
            """, (user_id,))
            
            trends = []
            for row in cursor.fetchall():
                trends.append({
                    'date': row[0],
                    'avg_score': round(row[1], 2),
                    'analysis_count': row[2]
                })
            
            # Get top companies analyzed
            cursor.execute("""
                SELECT company_name, COUNT(*) as count, AVG(eligibility_score) as avg_score
                FROM analysis_history 
                WHERE user_id = ? 
                GROUP BY company_name
                ORDER BY count DESC
                LIMIT 10
            """, (user_id,))
            
            top_companies = []
            for row in cursor.fetchall():
                top_companies.append({
                    'company': row[0],
                    'analysis_count': row[1],
                    'avg_score': round(row[2], 2)
                })
            
            # Get skill improvement suggestions
            cursor.execute("""
                SELECT missing_skills, COUNT(*) as frequency
                FROM analysis_history 
                WHERE user_id = ? AND missing_skills != '[]'
                GROUP BY missing_skills
                ORDER BY frequency DESC
                LIMIT 5
            """, (user_id,))
            
            skill_gaps = []
            for row in cursor.fetchall():
                try:
                    skills = json.loads(row[0])
                    skill_gaps.extend(skills)
                except:
                    continue
            
            # Count skill frequency
            from collections import Counter
            skill_counter = Counter(skill_gaps)
            most_needed_skills = [{'skill': skill, 'frequency': count} 
                                for skill, count in skill_counter.most_common(10)]
            
            conn.close()
            
            return {
                'score_trends': trends,
                'top_companies': top_companies,
                'most_needed_skills': most_needed_skills,
                'improvement_areas': self._generate_improvement_suggestions(trends, most_needed_skills)
            }
            
        except Exception as e:
            logger.error(f"Error getting analysis trends: {e}")
            return {'error': 'Failed to get analysis trends'}
    
    def _generate_improvement_suggestions(self, trends: List[dict], needed_skills: List[dict]) -> List[str]:
        """Generate personalized improvement suggestions"""
        suggestions = []
        
        if trends:
            recent_avg = sum(t['avg_score'] for t in trends[:7]) / min(len(trends), 7)
            if recent_avg < 60:
                suggestions.append("Focus on improving your resume content and skill alignment")
            elif recent_avg < 80:
                suggestions.append("You're making good progress! Consider targeting specific skill gaps")
            else:
                suggestions.append("Excellent progress! Consider exploring senior-level positions")
        
        if needed_skills:
            top_skill = needed_skills[0]['skill']
            suggestions.append(f"Consider learning '{top_skill}' - it appears frequently in job requirements")
        
        return suggestions
    
    def save_user_preferences(self, user_id: int, preferences: dict) -> bool:
        """Save user preferences for personalized experience"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if preferences exist
            cursor.execute("SELECT preference_id FROM user_preferences WHERE user_id = ?", (user_id,))
            existing = cursor.fetchone()
            
            if existing:
                cursor.execute("""
                    UPDATE user_preferences 
                    SET preferred_companies = ?, preferred_roles = ?, target_skills = ?, 
                        notification_settings = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                """, (
                    json.dumps(preferences.get('companies', [])),
                    json.dumps(preferences.get('roles', [])),
                    json.dumps(preferences.get('skills', [])),
                    json.dumps(preferences.get('notifications', {})),
                    user_id
                ))
            else:
                cursor.execute("""
                    INSERT INTO user_preferences 
                    (user_id, preferred_companies, preferred_roles, target_skills, notification_settings)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    user_id,
                    json.dumps(preferences.get('companies', [])),
                    json.dumps(preferences.get('roles', [])),
                    json.dumps(preferences.get('skills', [])),
                    json.dumps(preferences.get('notifications', {}))
                ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"User preferences saved for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving user preferences: {e}")
            return False
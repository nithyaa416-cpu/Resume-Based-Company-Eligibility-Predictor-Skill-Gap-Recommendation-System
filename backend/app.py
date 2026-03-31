from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import tempfile
import logging

# Configure logging FIRST
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import our custom modules
from database.db_utils import get_job_requirements, get_all_companies, get_all_companies_with_roles, get_job_requirements_by_company_and_role
from utils.resume_optimizer import ResumeOptimizer
from utils.ats_analyzer import ATSAnalyzer
from utils.resume_parser import ResumeParser
from utils.nlp_resume_extractor import NLPResumeExtractor
from utils.simple_semantic_analyzer import SimpleSemanticAnalyzer
from utils.ml_eligibility_calculator import MLEligibilityCalculator
from utils.skill_extractor import SkillExtractor
from utils.eligibility_calculator import EligibilityCalculator
from utils.report_generator import ReportGenerator

# Import new modules (optional - will be None if dependencies not installed)
try:
    from auth import AuthManager, require_auth
    from history_manager import HistoryManager
    from interview_prep import InterviewPrep
    NEW_FEATURES_ENABLED = True
    logger.info("Enhanced features (auth, history, interview) loaded successfully")
except ImportError as e:
    logger.warning(f"Enhanced features not available. Install dependencies: {e}")
    AuthManager = None
    require_auth = None
    HistoryManager = None
    InterviewPrep = None
    NEW_FEATURES_ENABLED = False

app = Flask(__name__, static_folder='static', template_folder='static')
CORS(app)

# Initialize our ML-powered utility classes
nlp_extractor = NLPResumeExtractor()
semantic_analyzer = SimpleSemanticAnalyzer()
ml_calculator = MLEligibilityCalculator()
resume_optimizer = ResumeOptimizer()
ats_analyzer = ATSAnalyzer()
report_generator = ReportGenerator()

# Initialize new systems (if available)
if NEW_FEATURES_ENABLED:
    auth_manager = AuthManager()
    history_manager = HistoryManager()
    interview_prep = InterviewPrep()
else:
    auth_manager = None
    history_manager = None
    interview_prep = None

# Keep legacy extractors for backward compatibility
skill_extractor = SkillExtractor()
eligibility_calculator = EligibilityCalculator()

logger.info("Flask app initialized with ML components")

@app.route("/")
def home():
    """
    Serve the main web interface
    """
    return send_from_directory('static', 'index.html')

@app.route("/test")
def test_page():
    """
    Serve the test interface for troubleshooting
    """
    return send_from_directory('.', 'test_interface_simple.html')

@app.route("/api")
def api_info():
    """
    API information endpoint
    """
    return jsonify({
        "message": "Resume-Based Company Eligibility System API",
        "status": "OK",
        "version": "1.0",
        "endpoints": [
            "/upload - Upload and analyze resume",
            "/companies - Get all companies",
            "/companies-with-roles - Get all companies with their roles",
            "/analyze - Analyze resume against specific company (and role)",
            "/analyze-all - Analyze resume against all companies and roles",
            "/recommendations - Get skill gap recommendations",
            "/optimize-resume - Get AI-powered resume optimization suggestions",
            "/ats-score - Calculate detailed ATS compatibility score",
            "/export-pdf - Export analysis report as PDF",
            "/export-excel - Export analysis report as Excel/CSV",
            "/export-json - Export analysis report as JSON",
            "/job-data/status - Get job data update status",
            "/job-data/update - Force job data update"
        ]
    })

@app.route("/companies", methods=["GET"])
def get_companies():
    """
    Get list of all available companies
    """
    try:
        companies = get_all_companies()
        return jsonify({
            "status": "success",
            "companies": companies
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/companies-with-roles", methods=["GET"])
def get_companies_with_roles():
    """
    Get list of all available companies with their roles
    """
    try:
        companies_with_roles = get_all_companies_with_roles()
        return jsonify({
            "status": "success",
            "companies_with_roles": companies_with_roles,
            "total_positions": len(companies_with_roles)
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/upload", methods=["POST"])
def upload_resume():
    """
    Upload resume file and extract comprehensive information using ML/NLP
    """
    try:
        # Check if file is present
        if 'resume' not in request.files:
            return jsonify({
                "status": "error",
                "message": "No resume file provided"
            }), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({
                "status": "error",
                "message": "No file selected"
            }), 400
        
        # Save file temporarily and extract text
        temp_path, file_extension = ResumeParser.save_uploaded_file(file)
        
        if not temp_path:
            return jsonify({
                "status": "error",
                "message": "Failed to save uploaded file"
            }), 500
        
        try:
            # Extract text from resume
            resume_text = ResumeParser.parse_resume(temp_path, file_extension)
            
            if not resume_text:
                return jsonify({
                    "status": "error",
                    "message": "Could not extract text from resume"
                }), 400
            
            # Use ML/NLP for comprehensive information extraction
            logger.info("Starting ML-powered resume analysis")
            comprehensive_info = nlp_extractor.extract_comprehensive_info(resume_text)
            
            # Legacy skill extraction for backward compatibility
            skills = skill_extractor.extract_all_skills_flat(resume_text)
            skills_with_levels = skill_extractor.extract_skills_with_readiness_levels(resume_text)
            experience_years = skill_extractor.extract_experience_years(resume_text)
            
            return jsonify({
                "status": "success",
                "message": "Resume processed successfully with ML/NLP analysis",
                "data": {
                    "filename": file.filename,
                    "text_length": len(resume_text),
                    "ml_analysis": comprehensive_info,
                    "skills_found": comprehensive_info['total_skills_found'],
                    "skills": skills,  # Legacy format
                    "skills_with_levels": skills_with_levels,  # Legacy format
                    "experience_years": experience_years,  # Legacy format
                    "resume_text": resume_text[:500] + "..." if len(resume_text) > 500 else resume_text
                }
            })
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except Exception as e:
        logger.error(f"Error in resume upload: {e}")
        return jsonify({
            "status": "error",
            "message": f"Error processing resume: {str(e)}"
        }), 500

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    """
    Analyze resume against specific company requirements using ML/semantic analysis
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided"
            }), 400
        
        resume_text = data.get("resume_text", "")
        company_name = data.get("company", "")
        role = data.get("role", "")
        
        if not resume_text:
            return jsonify({
                "status": "error",
                "message": "resume_text is required"
            }), 400
        
        if not company_name:
            return jsonify({
                "status": "error",
                "message": "company is required"
            }), 400
        
        logger.info(f"Starting ML analysis for {company_name}" + (f" - {role}" if role else ""))
        
        # Extract comprehensive resume information using ML/NLP
        resume_info = nlp_extractor.extract_comprehensive_info(resume_text)
        
        # Get job requirements for the company (and role if specified)
        if role:
            job_requirements = get_job_requirements_by_company_and_role(company_name, role)
        else:
            job_requirements = get_job_requirements(company_name)
        
        if not job_requirements:
            error_msg = f"No job requirements found for company: {company_name}"
            if role:
                error_msg += f" and role: {role}"
            return jsonify({
                "status": "error",
                "message": error_msg
            }), 404
        
        # Calculate ML-powered comprehensive eligibility analysis
        ml_analysis = ml_calculator.calculate_comprehensive_eligibility(
            resume_info, job_requirements, company_name
        )
        
        # Legacy analysis for backward compatibility
        skills = skill_extractor.extract_all_skills_flat(resume_text)
        skills_with_levels = skill_extractor.extract_skills_with_readiness_levels(resume_text)
        experience_years = skill_extractor.extract_experience_years(resume_text)
        
        response_data = {
            "status": "success",
            "company": company_name,
            "ml_analysis": ml_analysis,
            "resume_info": resume_info,
            "legacy_data": {
                "resume_skills": skills,
                "resume_skills_with_levels": skills_with_levels,
                "resume_experience": experience_years
            }
        }
        
        # Add role to response if specified
        if role:
            response_data["role"] = role
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error in ML analysis: {e}")
        return jsonify({
            "status": "error",
            "message": f"Error analyzing resume: {str(e)}"
        }), 500

@app.route("/analyze-all", methods=["POST"])
def analyze_all_companies():
    """
    Analyze resume against all companies and roles using ML-powered analysis
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided"
            }), 400
        
        resume_text = data.get("resume_text", "")
        
        if not resume_text:
            return jsonify({
                "status": "error",
                "message": "resume_text is required"
            }), 400
        
        logger.info("Starting ML-powered multi-company analysis")
        
        # Extract comprehensive resume information using ML/NLP
        resume_info = nlp_extractor.extract_comprehensive_info(resume_text)
        
        # Get all companies with roles
        companies_with_roles = get_all_companies_with_roles()
        
        results = []
        
        for company_role in companies_with_roles:
            company = company_role["company"]
            role = company_role["role"]
            
            # Get job requirements for each company and role
            job_requirements = get_job_requirements_by_company_and_role(company, role)
            
            if job_requirements:
                # Calculate ML-powered comprehensive eligibility
                ml_analysis = ml_calculator.calculate_comprehensive_eligibility(
                    resume_info, job_requirements, company
                )
                
                results.append({
                    "company": company,
                    "role": role,
                    "display_name": company_role["display_name"],
                    "ml_analysis": ml_analysis  # Use ml_analysis instead of analysis
                })
        
        # Sort by ML eligibility score (highest first)
        results.sort(key=lambda x: x["ml_analysis"]["ml_eligibility_score"], reverse=True)
        
        # Legacy skill extraction for backward compatibility
        skills = skill_extractor.extract_all_skills_flat(resume_text)
        skills_with_levels = skill_extractor.extract_skills_with_readiness_levels(resume_text)
        experience_years = skill_extractor.extract_experience_years(resume_text)
        
        return jsonify({
            "status": "success",
            "total_positions": len(results),
            "resume_skills": skills,
            "resume_skills_with_levels": skills_with_levels,
            "resume_experience": experience_years,
            "company_analysis": results
        })
        
    except Exception as e:
        logger.error(f"Error in ML multi-company analysis: {e}")
        return jsonify({
            "status": "error",
            "message": f"Error analyzing resume: {str(e)}"
        }), 500

@app.route("/recommendations", methods=["POST"])
def get_recommendations():
    """
    Get skill gap recommendations for a specific company
    """
    try:
        data = request.get_json()
        
        company_name = data.get("company", "")
        resume_skills = data.get("resume_skills", [])
        
        if not company_name:
            return jsonify({
                "status": "error",
                "message": "Company name is required"
            }), 400
        
        # Get job requirements
        job_requirements = get_job_requirements(company_name)
        
        if not job_requirements:
            return jsonify({
                "status": "error",
                "message": f"No job requirements found for company: {company_name}"
            }), 404
        
        role, required_skills_str, tools_str, experience_str, education_str, job_description = job_requirements
        
        # Parse required skills
        required_skills = eligibility_calculator.parse_skills_string(required_skills_str)
        required_tools = eligibility_calculator.parse_skills_string(tools_str)
        all_required_skills = required_skills + required_tools
        
        # Calculate skill gaps
        skill_analysis = eligibility_calculator.calculate_skill_match_score(
            resume_skills, all_required_skills
        )
        
        # Generate recommendations
        recommendations = eligibility_calculator.generate_recommendations(
            skill_analysis['missing_skills']
        )
        
        return jsonify({
            "status": "success",
            "company": company_name,
            "role": role,
            "skill_gap_analysis": skill_analysis,
            "recommendations": recommendations
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error generating recommendations: {str(e)}"
        }), 500

@app.route("/skill-analysis", methods=["POST"])
def analyze_skills():
    """
    Analyze skills with readiness levels
    """
    try:
        data = request.get_json()
        
        resume_text = data.get("resume_text", "")
        
        if not resume_text:
            return jsonify({
                "status": "error",
                "message": "resume_text is required"
            }), 400
        
        # Extract skills with readiness levels
        skills_with_levels = skill_extractor.extract_skills_with_readiness_levels(resume_text)
        
        # Organize by readiness level
        skills_by_level = {
            'Advanced': [],
            'Intermediate': [],
            'Beginner': []
        }
        
        for skill, info in skills_with_levels.items():
            skills_by_level[info['level']].append({
                'skill': skill,
                'mentions': info['mentions'],
                'category': info['category']
            })
        
        return jsonify({
            "status": "success",
            "total_skills": len(skills_with_levels),
            "skills_by_level": skills_by_level,
            "skill_breakdown": {
                "advanced_count": len(skills_by_level['Advanced']),
                "intermediate_count": len(skills_by_level['Intermediate']),
                "beginner_count": len(skills_by_level['Beginner'])
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error analyzing skills: {str(e)}"
        }), 500

@app.route("/ml-analyze", methods=["POST"])
def ml_analyze_resume():
    """
    Advanced ML-powered resume analysis with semantic similarity
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided"
            }), 400
        
        resume_text = data.get("resume_text", "")
        company_name = data.get("company", "")
        
        if not resume_text or not company_name:
            return jsonify({
                "status": "error",
                "message": "Both resume_text and company are required"
            }), 400
        
        logger.info(f"Starting advanced ML analysis for {company_name}")
        
        # Extract comprehensive resume information
        resume_info = nlp_extractor.extract_comprehensive_info(resume_text)
        
        # Get job requirements
        job_requirements = get_job_requirements(company_name)
        
        if not job_requirements:
            return jsonify({
                "status": "error",
                "message": f"No job requirements found for company: {company_name}"
            }), 404
        
        # ML-powered analysis
        ml_analysis = ml_calculator.calculate_comprehensive_eligibility(
            resume_info, job_requirements, company_name
        )
        
        return jsonify({
            "status": "success",
            "message": "Advanced ML analysis completed",
            "company": company_name,
            "ml_analysis": ml_analysis,
            "resume_analysis": {
                "sections_extracted": list(resume_info['sections'].keys()),
                "skills_found": resume_info['total_skills_found'],
                "experience_confidence": resume_info['experience']['confidence'],
                "processing_status": resume_info['processing_status']
            }
        })
        
    except Exception as e:
        logger.error(f"Error in advanced ML analysis: {e}")
        return jsonify({
            "status": "error",
            "message": f"Error in ML analysis: {str(e)}"
        }), 500

@app.route("/job-data/status", methods=["GET"])
def get_job_data_status():
    """
    Get status of job data updates
    """
    try:
        # Simple status without scheduler
        status = {
            "is_running": True,
            "last_update": "2024-01-24T13:00:00Z",
            "update_stats": {
                "total_scraped": 64,
                "total_saved": 61
            },
            "next_run": "Manual updates available"
        }
        
        return jsonify({
            "status": "success",
            "job_data_status": status
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error getting job data status: {str(e)}"
        }), 500

@app.route("/job-data/update", methods=["POST"])
def force_job_data_update():
    """
    Force an immediate job data update using market data generator
    """
    try:
        logger.info("🔄 Manual job data update requested")
        
        # Import and run the market data generator
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'job_scraper'))
        
        from market_data_generator import MarketDataGenerator
        
        generator = MarketDataGenerator()
        results = generator.update_market_data()
        
        return jsonify({
            "status": "success",
            "message": "Job data update completed",
            "update_results": results
        })
    except Exception as e:
        logger.error(f"Error in manual job update: {e}")
        return jsonify({
            "status": "error",
            "message": f"Error updating job data: {str(e)}"
        }), 500

@app.route("/job-data/stats", methods=["GET"])
def get_job_data_stats():
    """
    Get statistics about current job data
    """
    try:
        from database.db_utils import get_job_data_statistics
        stats = get_job_data_statistics()
        
        return jsonify({
            "status": "success",
            "job_data_stats": stats
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error getting job data stats: {str(e)}"
        }), 500

@app.route("/semantic-similarity", methods=["POST"])
def calculate_semantic_similarity():
    """
    Calculate semantic similarity between resume and job description
    """
    try:
        data = request.get_json()
        
        resume_text = data.get("resume_text", "")
        job_description = data.get("job_description", "")
        
        if not resume_text or not job_description:
            return jsonify({
                "status": "error",
                "message": "Both resume_text and job_description are required"
            }), 400
        
        # Calculate semantic similarity
        similarity_score = semantic_analyzer.calculate_semantic_similarity(
            resume_text, job_description
        )
        
        return jsonify({
            "status": "success",
            "semantic_similarity": round(similarity_score * 100, 2),
            "similarity_level": "High" if similarity_score > 0.7 else "Medium" if similarity_score > 0.4 else "Low"
        })
        
    except Exception as e:
        logger.error(f"Error in semantic similarity calculation: {e}")
        return jsonify({
            "status": "error",
            "message": f"Error calculating similarity: {str(e)}"
        }), 500

@app.route("/optimize-resume", methods=["POST"])
def optimize_resume():
    """
    Get AI-powered resume optimization suggestions
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided"
            }), 400
        
        resume_text = data.get("resume_text", "")
        target_role = data.get("target_role", None)
        
        if not resume_text:
            return jsonify({
                "status": "error",
                "message": "resume_text is required"
            }), 400
        
        logger.info(f"Generating resume optimization suggestions for {len(resume_text)} character resume")
        
        # Generate comprehensive optimization report
        optimization_result = resume_optimizer.generate_comprehensive_optimization(
            resume_text, target_role
        )
        
        return jsonify({
            "status": "success",
            "message": "Resume optimization completed",
            "optimization": optimization_result,
            "target_role": target_role
        })
        
    except Exception as e:
        logger.error(f"Error in resume optimization: {e}")
        return jsonify({
            "status": "error",
            "message": f"Error optimizing resume: {str(e)}"
        }), 500

@app.route("/ats-score", methods=["POST"])
def calculate_ats_score():
    """
    Calculate detailed ATS compatibility score
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided"
            }), 400
        
        resume_text = data.get("resume_text", "")
        
        if not resume_text:
            return jsonify({
                "status": "error",
                "message": "resume_text is required"
            }), 400
        
        logger.info(f"Calculating ATS score for {len(resume_text)} character resume")
        
        # Generate comprehensive ATS report
        ats_report = ats_analyzer.generate_ats_report(resume_text)
        
        return jsonify({
            "status": "success",
            "message": "ATS analysis completed",
            "ats_report": ats_report
        })
        
    except Exception as e:
        logger.error(f"Error in ATS analysis: {e}")
        return jsonify({
            "status": "error",
            "message": f"Error calculating ATS score: {str(e)}"
        }), 500

@app.route("/export-pdf", methods=["POST"])
def export_pdf_report():
    """
    Export comprehensive analysis report as PDF
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided"
            }), 400
        
        analysis_data = data.get("analysis_data", {})
        user_info = data.get("user_info", {})
        
        if not analysis_data:
            return jsonify({
                "status": "error",
                "message": "analysis_data is required"
            }), 400
        
        logger.info("Generating PDF report")
        
        # Generate PDF report
        pdf_content = report_generator.generate_pdf_report(analysis_data, user_info)
        
        # Create response with PDF content
        from flask import make_response
        response = make_response(pdf_content)
        response.headers['Content-Type'] = 'text/html'
        response.headers['Content-Disposition'] = f'attachment; filename="resume_analysis_report.html"'
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating PDF report: {e}")
        return jsonify({
            "status": "error",
            "message": f"Error generating PDF report: {str(e)}"
        }), 500

@app.route("/export-excel", methods=["POST"])
def export_excel_report():
    """
    Export comprehensive analysis report as Excel/CSV
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided"
            }), 400
        
        analysis_data = data.get("analysis_data", {})
        user_info = data.get("user_info", {})
        
        if not analysis_data:
            return jsonify({
                "status": "error",
                "message": "analysis_data is required"
            }), 400
        
        logger.info("Generating Excel report")
        
        # Generate Excel report (CSV format)
        excel_content = report_generator.generate_excel_report(analysis_data, user_info)
        
        # Create response with Excel content
        from flask import make_response
        response = make_response(excel_content)
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename="resume_analysis_report.csv"'
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating Excel report: {e}")
        return jsonify({
            "status": "error",
            "message": f"Error generating Excel report: {str(e)}"
        }), 500

@app.route("/export-json", methods=["POST"])
def export_json_report():
    """
    Export comprehensive analysis report as JSON
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided"
            }), 400
        
        analysis_data = data.get("analysis_data", {})
        user_info = data.get("user_info", {})
        
        if not analysis_data:
            return jsonify({
                "status": "error",
                "message": "analysis_data is required"
            }), 400
        
        logger.info("Generating JSON report")
        
        # Generate JSON report
        json_content = report_generator.generate_json_report(analysis_data, user_info)
        
        # Create response with JSON content
        from flask import make_response
        response = make_response(json_content)
        response.headers['Content-Type'] = 'application/json'
        response.headers['Content-Disposition'] = f'attachment; filename="resume_analysis_report.json"'
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating JSON report: {e}")
        return jsonify({
            "status": "error",
            "message": f"Error generating JSON report: {str(e)}"
        }), 500

# ============================================================================
# REAL-TIME JOB API ENDPOINTS
# ============================================================================

@app.route("/jobs/fetch-realtime", methods=["POST"])
def fetch_realtime_jobs():
    """Fetch real-time jobs from external APIs"""
    try:
        from job_scraper.real_job_api_scraper import RealJobAPIScraper
        
        scraper = RealJobAPIScraper()
        stats = scraper.fetch_all_jobs()
        
        return jsonify({
            "status": "success",
            "message": "Real-time job data fetched successfully",
            "stats": stats
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching real-time jobs: {e}")
        return jsonify({
            "status": "error",
            "message": f"Failed to fetch jobs: {str(e)}"
        }), 500

@app.route("/jobs/status", methods=["GET"])
def get_jobs_status():
    """Get status of job database and last update"""
    try:
        from job_scraper.real_job_api_scraper import RealJobAPIScraper
        
        scraper = RealJobAPIScraper()
        status = scraper.get_update_status()
        
        return jsonify({
            "status": "success",
            "data": status
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting job status: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/jobs/auto-update", methods=["POST"])
def setup_auto_update():
    """Setup automatic job updates (requires scheduler)"""
    try:
        data = request.get_json()
        interval_hours = data.get('interval_hours', 24)
        
        # This would require a background scheduler like APScheduler
        # For now, return configuration info
        
        return jsonify({
            "status": "success",
            "message": "Auto-update configuration received",
            "config": {
                "interval_hours": interval_hours,
                "next_update": "Manual trigger required",
                "note": "Install APScheduler for automatic updates"
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error setting up auto-update: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/jobs/sources", methods=["GET"])
def get_job_sources():
    """Get available job API sources and their status"""
    try:
        from job_scraper.real_job_api_scraper import RealJobAPIScraper
        
        scraper = RealJobAPIScraper()
        sources = []
        
        for name, config in scraper.api_configs.items():
            sources.append({
                "name": name.title(),
                "enabled": config['enabled'],
                "requires_api_key": 'app_id' in config or 'api_key' in config,
                "base_url": config['base_url']
            })
        
        return jsonify({
            "status": "success",
            "sources": sources,
            "total_enabled": sum(1 for s in sources if s['enabled'])
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting job sources: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    print("Starting Flask server with ML/NLP capabilities...")
    print("Server will be available at: http://localhost:5000")
    print("ML Models: Sentence-BERT (all-MiniLM-L6-v2), spaCy NLP")
    app.run(debug=True, host='0.0.0.0', port=5000)

# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@app.route("/auth/register", methods=["POST"])
def register():
    """Register a new user"""
    if not NEW_FEATURES_ENABLED:
        return jsonify({'error': 'Authentication features not enabled. Install dependencies: pip install PyJWT bcrypt'}), 503
    
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        result = auth_manager.register_user(email, password, first_name, last_name)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 201
        
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({'error': 'Registration failed'}), 500

@app.route("/auth/login", methods=["POST"])
def login():
    """Authenticate user login"""
    if not NEW_FEATURES_ENABLED:
        return jsonify({'error': 'Authentication features not enabled. Install dependencies: pip install PyJWT bcrypt'}), 503
    
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        result = auth_manager.login_user(email, password)
        
        if 'error' in result:
            return jsonify(result), 401
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'error': 'Login failed'}), 500

@app.route("/auth/profile", methods=["GET"])
@require_auth
def get_profile():
    """Get user profile"""
    try:
        user_id = request.current_user['user_id']
        profile = auth_manager.get_user_profile(user_id)
        
        if 'error' in profile:
            return jsonify(profile), 404
        
        return jsonify(profile), 200
        
    except Exception as e:
        logger.error(f"Get profile error: {e}")
        return jsonify({'error': 'Failed to get profile'}), 500

# ============================================================================
# HISTORY TRACKING ROUTES
# ============================================================================

@app.route("/history", methods=["GET"])
@require_auth
def get_user_history():
    """Get user's resume and analysis history"""
    try:
        user_id = request.current_user['user_id']
        limit = request.args.get('limit', 50, type=int)
        
        history = history_manager.get_user_history(user_id, limit)
        
        if 'error' in history:
            return jsonify(history), 500
        
        return jsonify(history), 200
        
    except Exception as e:
        logger.error(f"Get history error: {e}")
        return jsonify({'error': 'Failed to get history'}), 500

@app.route("/history/trends", methods=["GET"])
@require_auth
def get_analysis_trends():
    """Get user's analysis trends and improvements"""
    try:
        user_id = request.current_user['user_id']
        trends = history_manager.get_analysis_trends(user_id)
        
        if 'error' in trends:
            return jsonify(trends), 500
        
        return jsonify(trends), 200
        
    except Exception as e:
        logger.error(f"Get trends error: {e}")
        return jsonify({'error': 'Failed to get trends'}), 500

@app.route("/history/preferences", methods=["POST"])
@require_auth
def save_preferences():
    """Save user preferences"""
    try:
        user_id = request.current_user['user_id']
        preferences = request.get_json()
        
        success = history_manager.save_user_preferences(user_id, preferences)
        
        if success:
            return jsonify({'message': 'Preferences saved successfully'}), 200
        else:
            return jsonify({'error': 'Failed to save preferences'}), 500
        
    except Exception as e:
        logger.error(f"Save preferences error: {e}")
        return jsonify({'error': 'Failed to save preferences'}), 500

# ============================================================================
# INTERVIEW PREPARATION ROUTES
# ============================================================================

@app.route("/interview/start-session", methods=["POST"])
@require_auth
def start_interview_session():
    """Start a new interview practice session"""
    try:
        user_id = request.current_user['user_id']
        data = request.get_json()
        
        company_name = data.get('company_name')
        job_role = data.get('job_role')
        session_type = data.get('session_type', 'mixed')
        
        if not company_name or not job_role:
            return jsonify({'error': 'Company name and job role are required'}), 400
        
        session = interview_prep.start_practice_session(user_id, company_name, job_role, session_type)
        
        if 'error' in session:
            return jsonify(session), 500
        
        return jsonify(session), 201
        
    except Exception as e:
        logger.error(f"Start interview session error: {e}")
        return jsonify({'error': 'Failed to start interview session'}), 500

@app.route("/interview/submit-response", methods=["POST"])
@require_auth
def submit_interview_response():
    """Submit response to interview question"""
    try:
        data = request.get_json()
        
        session_id = data.get('session_id')
        question_id = data.get('question_id')
        response = data.get('response')
        
        if not all([session_id, question_id, response]):
            return jsonify({'error': 'Session ID, question ID, and response are required'}), 400
        
        feedback = interview_prep.evaluate_response(session_id, question_id, response)
        
        if 'error' in feedback:
            return jsonify(feedback), 500
        
        return jsonify(feedback), 200
        
    except Exception as e:
        logger.error(f"Submit response error: {e}")
        return jsonify({'error': 'Failed to submit response'}), 500

@app.route("/interview/progress", methods=["GET"])
@require_auth
def get_interview_progress():
    """Get user's interview practice progress"""
    try:
        user_id = request.current_user['user_id']
        progress = interview_prep.get_practice_progress(user_id)
        
        if 'error' in progress:
            return jsonify(progress), 500
        
        return jsonify(progress), 200
        
    except Exception as e:
        logger.error(f"Get interview progress error: {e}")
        return jsonify({'error': 'Failed to get interview progress'}), 500

@app.route("/interview/sessions", methods=["GET"])
@require_auth
def get_interview_sessions():
    """Get user's interview session history"""
    try:
        user_id = request.current_user['user_id']
        # This would be implemented in interview_prep.py
        sessions = {'sessions': [], 'message': 'Feature coming soon'}
        
        return jsonify(sessions), 200
        
    except Exception as e:
        logger.error(f"Get interview sessions error: {e}")
        return jsonify({'error': 'Failed to get interview sessions'}), 500

# ============================================================================
# ENHANCED UPLOAD WITH HISTORY TRACKING
# ============================================================================

@app.route("/upload-with-history", methods=["POST"])
@require_auth
def upload_resume_with_history():
    """Upload resume with history tracking for authenticated users"""
    try:
        user_id = request.current_user['user_id']
        
        # Handle file upload or text input
        resume_text = ""
        filename = "manual_input.txt"
        file_size = 0
        file_type = "text"
        
        if 'resume' in request.files:
            file = request.files['resume']
            if file.filename != '':
                filename = file.filename
                file_size = len(file.read())
                file.seek(0)  # Reset file pointer
                
                # Save file temporarily and extract text
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
                    file.save(temp_file.name)
                    resume_text = ResumeParser.extract_text_from_file(temp_file.name)
                    file_type = os.path.splitext(filename)[1][1:]  # Remove dot
                
                os.unlink(temp_file.name)
        elif request.json and 'resume_text' in request.json:
            resume_text = request.json['resume_text']
            file_size = len(resume_text)
        
        if not resume_text.strip():
            return jsonify({"error": "No resume content provided"}), 400
        
        # Extract resume information
        resume_info = nlp_extractor.extract_comprehensive_resume_info(resume_text)
        
        # Save to history
        resume_data = {
            'filename': filename,
            'text': resume_text,
            'skills': resume_info.get('skills', []),
            'experience': resume_info.get('experience', {}),
            'education': resume_info.get('education', {}),
            'file_size': file_size,
            'file_type': file_type
        }
        
        upload_id = history_manager.save_resume_upload(user_id, resume_data)
        
        return jsonify({
            "status": "success",
            "message": "Resume uploaded and processed successfully",
            "upload_id": upload_id,
            "resume_info": resume_info
        }), 200
        
    except Exception as e:
        logger.error(f"Upload with history error: {e}")
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

# ============================================================================
# ENHANCED ANALYSIS WITH HISTORY TRACKING
# ============================================================================

@app.route("/ml-analyze-with-history", methods=["POST"])
@require_auth
def ml_analyze_with_history():
    """ML analysis with history tracking for authenticated users"""
    try:
        user_id = request.current_user['user_id']
        data = request.get_json()
        
        resume_text = data.get('resume_text', '')
        company_name = data.get('company_name', '')
        job_role = data.get('job_role', '')
        upload_id = data.get('upload_id')  # Optional, from previous upload
        
        if not all([resume_text, company_name]):
            return jsonify({"error": "Resume text and company name are required"}), 400
        
        # Get job requirements
        job_requirements = get_job_requirements_by_company_and_role(company_name, job_role) if job_role else get_job_requirements(company_name)
        
        if not job_requirements:
            return jsonify({"error": f"No job requirements found for {company_name}"}), 404
        
        # Extract resume information
        resume_info = nlp_extractor.extract_comprehensive_resume_info(resume_text)
        
        # Calculate ML eligibility
        ml_analysis = ml_calculator.calculate_comprehensive_eligibility(resume_info, job_requirements, company_name)
        
        # Save analysis to history
        analysis_data = {
            'company_name': company_name,
            'job_role': job_role or job_requirements[0],  # Use role from requirements if not provided
            'eligibility_score': ml_analysis.get('eligibility_score', 0),
            'ml_score': ml_analysis.get('ml_eligibility_score', 0),
            'semantic_score': ml_analysis.get('semantic_analysis', {}).get('overall_similarity', 0),
            'skill_match_score': ml_analysis.get('skill_analysis', {}).get('match_percentage', 0),
            'matched_skills': ml_analysis.get('skill_analysis', {}).get('matched_skills', []),
            'missing_skills': ml_analysis.get('skill_analysis', {}).get('missing_skills', []),
            'recommendations': ml_analysis.get('recommendations', []),
            'analysis_type': 'single',
            'full_analysis_data': ml_analysis
        }
        
        analysis_id = history_manager.save_analysis_result(user_id, upload_id, analysis_data)
        
        # Add analysis ID to response
        ml_analysis['analysis_id'] = analysis_id
        
        return jsonify(ml_analysis), 200
        
    except Exception as e:
        logger.error(f"ML analysis with history error: {e}")
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500
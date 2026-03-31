#!/usr/bin/env python3
"""
Report Generator
Creates professional PDF and Excel reports for resume analysis
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any
import io
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReportGenerator:
    """Generate professional reports for resume analysis"""
    
    def __init__(self):
        logger.info("Report Generator initialized")
        
    def generate_pdf_report(self, analysis_data: Dict, user_info: Dict = None) -> bytes:
        """
        Generate a professional PDF report
        Using HTML to PDF conversion (works without external dependencies)
        """
        
        logger.info("Generating PDF report")
        
        # Create HTML content for the report
        html_content = self._create_html_report(analysis_data, user_info)
        
        # Convert HTML to PDF (simplified version)
        # In a production environment, you'd use libraries like weasyprint or reportlab
        pdf_content = self._html_to_pdf_simple(html_content)
        
        return pdf_content
    
    def generate_excel_report(self, analysis_data: Dict, user_info: Dict = None) -> bytes:
        """
        Generate detailed Excel report with multiple sheets
        Using CSV format for simplicity (can be opened in Excel)
        """
        
        logger.info("Generating Excel report")
        
        # Create CSV content that can be opened in Excel
        csv_content = self._create_csv_report(analysis_data, user_info)
        
        return csv_content.encode('utf-8')
    
    def generate_json_report(self, analysis_data: Dict, user_info: Dict = None) -> bytes:
        """Generate detailed JSON report for developers/APIs"""
        
        logger.info("Generating JSON report")
        
        report_data = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "report_type": "resume_analysis",
                "version": "1.0"
            },
            "user_info": user_info or {},
            "analysis_data": analysis_data
        }
        
        return json.dumps(report_data, indent=2).encode('utf-8')
    
    def _create_html_report(self, analysis_data: Dict, user_info: Dict = None) -> str:
        """Create HTML content for PDF report"""
        
        # Extract data
        company = analysis_data.get('company', 'Multiple Companies')
        role = analysis_data.get('role', '')
        ml_analysis = analysis_data.get('ml_analysis', {})
        optimization = analysis_data.get('optimization', {})
        ats_report = analysis_data.get('ats_report', {})
        
        # Get current date
        report_date = datetime.now().strftime("%B %d, %Y")
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Resume Analysis Report</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    text-align: center;
                    border-bottom: 3px solid #4C5FFF;
                    padding-bottom: 20px;
                    margin-bottom: 30px;
                }}
                .header h1 {{
                    color: #4C5FFF;
                    margin: 0;
                    font-size: 2.5em;
                }}
                .header p {{
                    color: #666;
                    margin: 10px 0 0 0;
                    font-size: 1.1em;
                }}
                .section {{
                    margin: 30px 0;
                    padding: 20px;
                    border-radius: 8px;
                    background: #f8f9fa;
                }}
                .section h2 {{
                    color: #4C5FFF;
                    border-bottom: 2px solid #00E0FF;
                    padding-bottom: 10px;
                    margin-top: 0;
                }}
                .score-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin: 20px 0;
                }}
                .score-card {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                    border-left: 4px solid #00E0FF;
                }}
                .score-value {{
                    font-size: 2.5em;
                    font-weight: bold;
                    color: #4C5FFF;
                    margin: 0;
                }}
                .score-label {{
                    color: #666;
                    font-size: 0.9em;
                    margin: 5px 0 0 0;
                }}
                .suggestions {{
                    margin: 20px 0;
                }}
                .suggestion {{
                    background: white;
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 6px;
                    border-left: 4px solid #ffc107;
                }}
                .suggestion.critical {{
                    border-left-color: #dc3545;
                }}
                .suggestion.important {{
                    border-left-color: #fd7e14;
                }}
                .suggestion h4 {{
                    margin: 0 0 8px 0;
                    color: #333;
                }}
                .suggestion p {{
                    margin: 0;
                    color: #666;
                    font-size: 0.9em;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    color: #666;
                    font-size: 0.9em;
                }}
                .company-info {{
                    background: linear-gradient(135deg, #4C5FFF, #00E0FF);
                    color: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                }}
                .insights {{
                    background: #e3f2fd;
                    padding: 15px;
                    border-radius: 6px;
                    margin: 15px 0;
                }}
                .skills-list {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                    margin: 10px 0;
                }}
                .skill-tag {{
                    background: #4C5FFF;
                    color: white;
                    padding: 4px 12px;
                    border-radius: 20px;
                    font-size: 0.8em;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>AI Resume Analysis Report</h1>
                <p>Generated on {report_date}</p>
                {f'<p><strong>Analysis for:</strong> {company}' + (f' - {role}' if role else '') + '</p>' if company != 'Multiple Companies' else ''}
            </div>
        """
        
        # Add ML Analysis section if available
        if ml_analysis:
            eligibility_score = ml_analysis.get('ml_eligibility_score', 0)
            eligibility_level = ml_analysis.get('eligibility_level', 'Unknown')
            
            html_content += f"""
            <div class="section">
                <h2>🤖 ML-Powered Analysis</h2>
                <div class="company-info">
                    <h3>Eligibility Assessment</h3>
                    <div class="score-grid">
                        <div class="score-card">
                            <div class="score-value">{eligibility_score}%</div>
                            <div class="score-label">ML Eligibility Score</div>
                        </div>
                        <div class="score-card">
                            <div class="score-value" style="font-size: 1.5em;">{eligibility_level}</div>
                            <div class="score-label">Eligibility Level</div>
                        </div>
                    </div>
                </div>
            </div>
            """
        
        # Add Resume Optimization section if available
        if optimization:
            overall_score = optimization.get('overall_score', 0)
            scores = optimization.get('scores', {})
            suggestions = optimization.get('suggestions', {})
            
            html_content += f"""
            <div class="section">
                <h2>📊 Resume Optimization Analysis</h2>
                <div class="score-grid">
                    <div class="score-card">
                        <div class="score-value">{overall_score}</div>
                        <div class="score-label">Overall Score</div>
                    </div>
                    <div class="score-card">
                        <div class="score-value">{scores.get('structure', 0)}</div>
                        <div class="score-label">Structure</div>
                    </div>
                    <div class="score-card">
                        <div class="score-value">{scores.get('ats_compatibility', 0)}</div>
                        <div class="score-label">ATS Compatible</div>
                    </div>
                    <div class="score-card">
                        <div class="score-value">{scores.get('content_quality', 0)}</div>
                        <div class="score-label">Content Quality</div>
                    </div>
                </div>
                
                <h3>🚨 Critical Suggestions</h3>
                <div class="suggestions">
            """
            
            # Add critical suggestions
            for suggestion in suggestions.get('critical', [])[:5]:
                html_content += f"""
                <div class="suggestion critical">
                    <h4>{suggestion.get('title', 'Suggestion')}</h4>
                    <p>{suggestion.get('description', 'No description available')}</p>
                </div>
                """
            
            # Add important suggestions
            html_content += "<h3>⚠️ Important Suggestions</h3>"
            for suggestion in suggestions.get('important', [])[:5]:
                html_content += f"""
                <div class="suggestion important">
                    <h4>{suggestion.get('title', 'Suggestion')}</h4>
                    <p>{suggestion.get('description', 'No description available')}</p>
                </div>
                """
            
            html_content += "</div></div>"
        
        # Add ATS Analysis section if available
        if ats_report:
            total_score = ats_report.get('total_score', 0)
            compatibility_level = ats_report.get('compatibility_level', 'Unknown')
            score_breakdown = ats_report.get('score_breakdown', {})
            
            html_content += f"""
            <div class="section">
                <h2>🎯 ATS Compatibility Analysis</h2>
                <div class="score-grid">
                    <div class="score-card">
                        <div class="score-value">{total_score}</div>
                        <div class="score-label">ATS Score</div>
                    </div>
                    <div class="score-card">
                        <div class="score-value" style="font-size: 1.5em;">{compatibility_level}</div>
                        <div class="score-label">Compatibility Level</div>
                    </div>
                </div>
                
                <h3>Score Breakdown</h3>
                <div class="score-grid">
                    <div class="score-card">
                        <div class="score-value">{score_breakdown.get('formatting', 0)}</div>
                        <div class="score-label">Formatting</div>
                    </div>
                    <div class="score-card">
                        <div class="score-value">{score_breakdown.get('structure', 0)}</div>
                        <div class="score-label">Structure</div>
                    </div>
                    <div class="score-card">
                        <div class="score-value">{score_breakdown.get('keywords', 0)}</div>
                        <div class="score-label">Keywords</div>
                    </div>
                    <div class="score-card">
                        <div class="score-value">{score_breakdown.get('contact_info', 0)}</div>
                        <div class="score-label">Contact Info</div>
                    </div>
                </div>
            </div>
            """
        
        # Add insights and recommendations
        html_content += """
            <div class="section">
                <h2>💡 Key Insights & Next Steps</h2>
                <div class="insights">
                    <h4>🎯 Priority Actions</h4>
                    <p>Focus on critical and important suggestions first for maximum impact on your job search success.</p>
                </div>
                <div class="insights">
                    <h4>🔄 Continuous Improvement</h4>
                    <p>Re-analyze your resume after implementing changes to track your progress and identify new optimization opportunities.</p>
                </div>
                <div class="insights">
                    <h4>📈 Market Alignment</h4>
                    <p>This analysis is based on current market trends and real job requirements from top companies in 2024-2025.</p>
                </div>
            </div>
        """
        
        # Add footer
        html_content += f"""
            <div class="footer">
                <p><strong>AI Resume Analyzer</strong> - ML-Powered Career Intelligence</p>
                <p>Report generated on {report_date} using advanced AI and machine learning models</p>
                <p>For best results, implement suggestions and re-analyze your resume regularly</p>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def _html_to_pdf_simple(self, html_content: str) -> bytes:
        """
        Simple HTML to PDF conversion
        In production, use libraries like weasyprint, reportlab, or puppeteer
        """
        
        # For now, return the HTML as bytes (can be saved as .html and printed to PDF)
        # In a real implementation, you'd use a proper HTML to PDF converter
        
        return html_content.encode('utf-8')
    
    def _create_csv_report(self, analysis_data: Dict, user_info: Dict = None) -> str:
        """Create CSV content for Excel report"""
        
        csv_content = "AI Resume Analysis Report\\n"
        csv_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n"
        
        # Company information
        company = analysis_data.get('company', 'Multiple Companies')
        role = analysis_data.get('role', '')
        if company != 'Multiple Companies':
            csv_content += f"Company: {company}\\n"
            if role:
                csv_content += f"Role: {role}\\n"
        csv_content += "\\n"
        
        # ML Analysis scores
        ml_analysis = analysis_data.get('ml_analysis', {})
        if ml_analysis:
            csv_content += "ML ANALYSIS SCORES\\n"
            csv_content += "Metric,Score\\n"
            csv_content += f"ML Eligibility Score,{ml_analysis.get('ml_eligibility_score', 0)}%\\n"
            csv_content += f"Eligibility Level,{ml_analysis.get('eligibility_level', 'Unknown')}\\n"
            csv_content += "\\n"
        
        # Resume Optimization scores
        optimization = analysis_data.get('optimization', {})
        if optimization:
            csv_content += "RESUME OPTIMIZATION SCORES\\n"
            csv_content += "Category,Score\\n"
            csv_content += f"Overall Score,{optimization.get('overall_score', 0)}\\n"
            
            scores = optimization.get('scores', {})
            csv_content += f"Structure,{scores.get('structure', 0)}\\n"
            csv_content += f"ATS Compatibility,{scores.get('ats_compatibility', 0)}\\n"
            csv_content += f"Content Quality,{scores.get('content_quality', 0)}\\n"
            csv_content += "\\n"
            
            # Suggestions
            suggestions = optimization.get('suggestions', {})
            if suggestions.get('critical'):
                csv_content += "CRITICAL SUGGESTIONS\\n"
                csv_content += "Title,Description,Category,Impact\\n"
                for suggestion in suggestions['critical']:
                    title = suggestion.get('title', '').replace(',', ';')
                    description = suggestion.get('description', '').replace(',', ';')
                    category = suggestion.get('category', '')
                    impact = suggestion.get('impact', '')
                    csv_content += f'"{title}","{description}",{category},{impact}\\n'
                csv_content += "\\n"
        
        # ATS Analysis
        ats_report = analysis_data.get('ats_report', {})
        if ats_report:
            csv_content += "ATS COMPATIBILITY ANALYSIS\\n"
            csv_content += "Metric,Score\\n"
            csv_content += f"Total ATS Score,{ats_report.get('total_score', 0)}\\n"
            csv_content += f"Compatibility Level,{ats_report.get('compatibility_level', 'Unknown')}\\n"
            
            score_breakdown = ats_report.get('score_breakdown', {})
            csv_content += f"Formatting,{score_breakdown.get('formatting', 0)}\\n"
            csv_content += f"Structure,{score_breakdown.get('structure', 0)}\\n"
            csv_content += f"Keywords,{score_breakdown.get('keywords', 0)}\\n"
            csv_content += f"Contact Info,{score_breakdown.get('contact_info', 0)}\\n"
            csv_content += f"Readability,{score_breakdown.get('readability', 0)}\\n"
            csv_content += "\\n"
        
        # Summary statistics
        csv_content += "SUMMARY STATISTICS\\n"
        csv_content += "Metric,Value\\n"
        
        if optimization:
            summary = optimization.get('summary', {})
            csv_content += f"Word Count,{summary.get('word_count', 0)}\\n"
            csv_content += f"Sections Found,{summary.get('sections_found', 0)}\\n"
            csv_content += f"Skills Identified,{summary.get('skills_identified', 0)}\\n"
            csv_content += f"Total Suggestions,{optimization.get('suggestions', {}).get('total_count', 0)}\\n"
        
        return csv_content
    
    def create_analysis_summary(self, analysis_data: Dict) -> Dict:
        """Create a summary of the analysis for quick viewing"""
        
        summary = {
            "report_date": datetime.now().strftime("%Y-%m-%d"),
            "company": analysis_data.get('company', 'Multiple Companies'),
            "role": analysis_data.get('role', ''),
            "scores": {},
            "key_insights": [],
            "top_suggestions": []
        }
        
        # Extract scores
        ml_analysis = analysis_data.get('ml_analysis', {})
        if ml_analysis:
            summary["scores"]["ml_eligibility"] = ml_analysis.get('ml_eligibility_score', 0)
            summary["scores"]["eligibility_level"] = ml_analysis.get('eligibility_level', 'Unknown')
        
        optimization = analysis_data.get('optimization', {})
        if optimization:
            summary["scores"]["overall_optimization"] = optimization.get('overall_score', 0)
            summary["scores"]["ats_compatibility"] = optimization.get('scores', {}).get('ats_compatibility', 0)
        
        ats_report = analysis_data.get('ats_report', {})
        if ats_report:
            summary["scores"]["ats_score"] = ats_report.get('total_score', 0)
            summary["scores"]["ats_level"] = ats_report.get('compatibility_level', 'Unknown')
        
        # Extract top suggestions
        if optimization:
            suggestions = optimization.get('suggestions', {})
            critical = suggestions.get('critical', [])[:3]
            important = suggestions.get('important', [])[:3]
            
            for suggestion in critical + important:
                summary["top_suggestions"].append({
                    "title": suggestion.get('title', ''),
                    "type": suggestion.get('type', ''),
                    "impact": suggestion.get('impact', '')
                })
        
        # Generate key insights
        if summary["scores"].get("overall_optimization", 0) >= 80:
            summary["key_insights"].append("Your resume is well-optimized and ready for applications")
        elif summary["scores"].get("overall_optimization", 0) >= 60:
            summary["key_insights"].append("Good foundation with room for improvement")
        else:
            summary["key_insights"].append("Significant improvements needed before applying")
        
        if summary["scores"].get("ats_score", 0) >= 85:
            summary["key_insights"].append("Excellent ATS compatibility")
        elif summary["scores"].get("ats_score", 0) < 60:
            summary["key_insights"].append("ATS compatibility needs attention")
        
        return summary

def main():
    """Test the report generator"""
    generator = ReportGenerator()
    
    # Sample analysis data
    sample_data = {
        "company": "Google",
        "role": "Software Engineer",
        "ml_analysis": {
            "ml_eligibility_score": 87,
            "eligibility_level": "Highly Eligible"
        },
        "optimization": {
            "overall_score": 75.5,
            "scores": {
                "structure": 80,
                "ats_compatibility": 70,
                "content_quality": 76
            },
            "suggestions": {
                "critical": [
                    {
                        "title": "Add Contact Information",
                        "description": "Include email, phone, and LinkedIn profile",
                        "type": "critical",
                        "impact": "high"
                    }
                ],
                "important": [
                    {
                        "title": "Use Stronger Action Verbs",
                        "description": "Replace weak phrases with strong action verbs",
                        "type": "important",
                        "impact": "high"
                    }
                ],
                "total_count": 8
            },
            "summary": {
                "word_count": 450,
                "sections_found": 4,
                "skills_identified": 12
            }
        }
    }
    
    # Generate reports
    html_report = generator._create_html_report(sample_data)
    csv_report = generator._create_csv_report(sample_data)
    summary = generator.create_analysis_summary(sample_data)
    
    print("=== REPORT GENERATOR TEST ===")
    print(f"HTML Report Length: {len(html_report)} characters")
    print(f"CSV Report Length: {len(csv_report)} characters")
    print(f"Summary: {summary['key_insights']}")

if __name__ == "__main__":
    main()
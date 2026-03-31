#!/usr/bin/env python3
"""
Complete Export System Test
Tests the entire export functionality including optimization, ATS analysis, and multi-company reports
"""

import requests
import json
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:5000"

def test_complete_workflow():
    """Test the complete workflow from resume upload to export"""
    
    logger.info("🚀 Testing Complete Export Workflow")
    logger.info("=" * 60)
    
    # Sample resume text
    sample_resume = """
    John Doe
    Software Engineer
    Email: john.doe@email.com
    Phone: (555) 123-4567
    LinkedIn: linkedin.com/in/johndoe
    
    EXPERIENCE
    Senior Software Engineer - Google (2020-2023)
    - Developed scalable web applications using React and Node.js
    - Led a team of 5 engineers in building microservices architecture
    - Implemented CI/CD pipelines reducing deployment time by 60%
    - Collaborated with product managers to define technical requirements
    
    Software Engineer - Microsoft (2018-2020)
    - Built REST APIs using Python and Django
    - Optimized database queries improving performance by 40%
    - Participated in code reviews and mentored junior developers
    
    SKILLS
    Programming Languages: Python, JavaScript, Java, C++
    Frameworks: React, Node.js, Django, Flask
    Databases: PostgreSQL, MongoDB, Redis
    Cloud: AWS, Azure, Docker, Kubernetes
    Tools: Git, Jenkins, JIRA, Agile methodologies
    
    EDUCATION
    Bachelor of Science in Computer Science
    Stanford University (2014-2018)
    GPA: 3.8/4.0
    """
    
    # Step 1: Upload Resume
    logger.info("📄 Step 1: Testing Resume Upload")
    upload_response = requests.post(
        f"{BASE_URL}/upload",
        files={'resume': ('test_resume.txt', sample_resume, 'text/plain')},
        timeout=30
    )
    
    if upload_response.status_code != 200:
        logger.error(f"❌ Resume upload failed: {upload_response.status_code}")
        return False
    
    upload_data = upload_response.json()
    logger.info("✅ Resume uploaded successfully")
    logger.info(f"   Skills found: {upload_data['data']['skills_found']}")
    
    # Step 2: Test Resume Optimization
    logger.info("\n🔧 Step 2: Testing Resume Optimization")
    optimization_response = requests.post(
        f"{BASE_URL}/optimize-resume",
        json={
            'resume_text': sample_resume,
            'target_role': 'Software Engineer'
        },
        timeout=30
    )
    
    if optimization_response.status_code != 200:
        logger.error(f"❌ Resume optimization failed: {optimization_response.status_code}")
        return False
    
    optimization_data = optimization_response.json()
    logger.info("✅ Resume optimization completed")
    logger.info(f"   Overall Score: {optimization_data['optimization']['overall_score']}")
    logger.info(f"   Total Suggestions: {optimization_data['optimization']['suggestions']['total_count']}")
    
    # Step 3: Test ATS Analysis
    logger.info("\n🎯 Step 3: Testing ATS Analysis")
    ats_response = requests.post(
        f"{BASE_URL}/ats-score",
        json={'resume_text': sample_resume},
        timeout=30
    )
    
    if ats_response.status_code != 200:
        logger.error(f"❌ ATS analysis failed: {ats_response.status_code}")
        return False
    
    ats_data = ats_response.json()
    logger.info("✅ ATS analysis completed")
    logger.info(f"   ATS Score: {ats_data['ats_report']['total_score']}")
    logger.info(f"   Compatibility Level: {ats_data['ats_report']['compatibility_level']}")
    
    # Step 4: Test Company Analysis
    logger.info("\n🏢 Step 4: Testing Company Analysis")
    company_response = requests.post(
        f"{BASE_URL}/analyze",
        json={
            'resume_text': sample_resume,
            'company': 'Google',
            'role': 'Software Engineer'
        },
        timeout=30
    )
    
    if company_response.status_code != 200:
        logger.error(f"❌ Company analysis failed: {company_response.status_code}")
        return False
    
    company_data = company_response.json()
    logger.info("✅ Company analysis completed")
    logger.info(f"   ML Eligibility Score: {company_data['ml_analysis']['ml_eligibility_score']}%")
    logger.info(f"   Eligibility Level: {company_data['ml_analysis']['eligibility_level']}")
    
    # Step 5: Test Export Functionality
    logger.info("\n📊 Step 5: Testing Export Functionality")
    
    # Prepare comprehensive analysis data
    comprehensive_data = {
        "company": "Google",
        "role": "Software Engineer",
        "optimization": optimization_data['optimization'],
        "ml_analysis": company_data['ml_analysis'],
        "ats_report": ats_data['ats_report'],
        "generated_at": "2024-01-24T13:00:00Z",
        "report_type": "comprehensive_analysis"
    }
    
    user_info = {
        "filename": "john_doe_resume.txt",
        "analysis_date": "2024-01-24",
        "analysis_type": "comprehensive"
    }
    
    export_data = {
        "analysis_data": comprehensive_data,
        "user_info": user_info
    }
    
    # Test all export formats
    formats = ['pdf', 'excel', 'json']
    export_results = {}
    
    for format_type in formats:
        logger.info(f"   Testing {format_type.upper()} export...")
        
        try:
            export_response = requests.post(
                f"{BASE_URL}/export-{format_type}",
                json=export_data,
                timeout=30
            )
            
            if export_response.status_code == 200:
                logger.info(f"   ✅ {format_type.upper()} export successful ({len(export_response.content)} bytes)")
                
                # Save comprehensive report
                filename = f"comprehensive_report.{format_type}"
                if format_type == 'pdf':
                    filename = "comprehensive_report.html"
                elif format_type == 'excel':
                    filename = "comprehensive_report.csv"
                
                with open(filename, 'wb') as f:
                    f.write(export_response.content)
                
                export_results[format_type] = True
            else:
                logger.error(f"   ❌ {format_type.upper()} export failed: {export_response.status_code}")
                export_results[format_type] = False
                
        except Exception as e:
            logger.error(f"   ❌ Error exporting {format_type.upper()}: {e}")
            export_results[format_type] = False
    
    # Step 6: Test Multi-Company Analysis Export
    logger.info("\n🌐 Step 6: Testing Multi-Company Analysis")
    multi_response = requests.post(
        f"{BASE_URL}/analyze-all",
        json={'resume_text': sample_resume},
        timeout=60
    )
    
    if multi_response.status_code == 200:
        multi_data = multi_response.json()
        logger.info("✅ Multi-company analysis completed")
        logger.info(f"   Total positions analyzed: {multi_data['total_positions']}")
        
        # Test multi-company export
        multi_export_data = {
            "analysis_data": {
                "report_type": "comprehensive_multi_company",
                "generated_at": "2024-01-24T13:00:00Z",
                "total_positions": multi_data['total_positions'],
                "company_analysis": multi_data['company_analysis'][:5],  # Top 5 matches
                "summary": {
                    "top_matches": [
                        {
                            "company": item['company'],
                            "role": item['role'],
                            "score": item['ml_analysis']['ml_eligibility_score']
                        }
                        for item in multi_data['company_analysis'][:5]
                    ]
                }
            },
            "user_info": {
                "analysis_type": "multi_company",
                "total_companies": multi_data['total_positions']
            }
        }
        
        # Test JSON export for multi-company
        multi_export_response = requests.post(
            f"{BASE_URL}/export-json",
            json=multi_export_data,
            timeout=30
        )
        
        if multi_export_response.status_code == 200:
            logger.info("   ✅ Multi-company JSON export successful")
            with open("multi_company_analysis.json", 'wb') as f:
                f.write(multi_export_response.content)
        else:
            logger.error(f"   ❌ Multi-company export failed: {multi_export_response.status_code}")
    
    else:
        logger.error(f"❌ Multi-company analysis failed: {multi_response.status_code}")
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("📋 EXPORT SYSTEM TEST SUMMARY")
    logger.info("=" * 60)
    
    successful_exports = sum(export_results.values())
    total_exports = len(export_results)
    
    logger.info(f"✅ Resume Upload: Success")
    logger.info(f"✅ Resume Optimization: Success")
    logger.info(f"✅ ATS Analysis: Success")
    logger.info(f"✅ Company Analysis: Success")
    logger.info(f"📊 Export Success Rate: {successful_exports}/{total_exports}")
    
    for format_type, success in export_results.items():
        status = "✅" if success else "❌"
        logger.info(f"   {status} {format_type.upper()} Export")
    
    if successful_exports == total_exports:
        logger.info("\n🎉 ALL TESTS PASSED! Export system is fully functional.")
        return True
    else:
        logger.info(f"\n⚠️  {total_exports - successful_exports} export format(s) failed.")
        return False

if __name__ == "__main__":
    success = test_complete_workflow()
    
    if success:
        logger.info("\n✨ Export system is ready for production!")
    else:
        logger.info("\n🔧 Some issues need to be addressed.")
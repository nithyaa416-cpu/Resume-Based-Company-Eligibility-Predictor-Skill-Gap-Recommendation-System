#!/usr/bin/env python3
"""
Test Export Endpoints
Tests the new PDF, Excel, and JSON export functionality
"""

import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:5000"

def test_export_endpoints():
    """Test all export endpoints with sample data"""
    
    # Sample analysis data
    sample_analysis_data = {
        "company": "Google",
        "role": "Software Engineer",
        "optimization": {
            "overall_score": 85.5,
            "scores": {
                "structure": 90,
                "ats_compatibility": 80,
                "content_quality": 86
            },
            "suggestions": {
                "critical": [
                    {
                        "title": "Add Contact Information",
                        "description": "Include email, phone, and LinkedIn profile",
                        "type": "critical",
                        "impact": "high",
                        "category": "structure"
                    }
                ],
                "important": [
                    {
                        "title": "Use Stronger Action Verbs",
                        "description": "Replace weak phrases with strong action verbs",
                        "type": "important",
                        "impact": "high",
                        "category": "content"
                    }
                ],
                "other": [],
                "total_count": 8
            },
            "summary": {
                "word_count": 450,
                "sections_found": 4,
                "skills_identified": 12
            }
        },
        "ml_analysis": {
            "ml_eligibility_score": 87,
            "eligibility_level": "Highly Eligible"
        },
        "ats_report": {
            "total_score": 82,
            "compatibility_level": "Good",
            "score_breakdown": {
                "formatting": 85,
                "structure": 80,
                "keywords": 78,
                "contact_info": 90,
                "readability": 84
            }
        },
        "generated_at": "2024-01-24T13:00:00Z"
    }
    
    user_info = {
        "filename": "test_resume.pdf",
        "analysis_date": "2024-01-24"
    }
    
    test_data = {
        "analysis_data": sample_analysis_data,
        "user_info": user_info
    }
    
    # Test each export format
    formats = ['pdf', 'excel', 'json']
    
    for format_type in formats:
        logger.info(f"Testing {format_type.upper()} export...")
        
        try:
            response = requests.post(
                f"{BASE_URL}/export-{format_type}",
                json=test_data,
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info(f"✅ {format_type.upper()} export successful")
                logger.info(f"   Content-Type: {response.headers.get('Content-Type')}")
                logger.info(f"   Content-Length: {len(response.content)} bytes")
                
                # Save the file for inspection
                filename = f"test_export.{format_type}"
                if format_type == 'pdf':
                    filename = "test_export.html"  # Currently exports as HTML
                elif format_type == 'excel':
                    filename = "test_export.csv"
                
                with open(filename, 'wb') as f:
                    f.write(response.content)
                logger.info(f"   Saved as: {filename}")
                
            else:
                logger.error(f"❌ {format_type.upper()} export failed")
                logger.error(f"   Status: {response.status_code}")
                logger.error(f"   Response: {response.text}")
                
        except Exception as e:
            logger.error(f"❌ Error testing {format_type.upper()} export: {e}")
    
    logger.info("Export endpoint testing completed!")

def test_api_info():
    """Test that the API info endpoint includes export endpoints"""
    try:
        response = requests.get(f"{BASE_URL}/api")
        if response.status_code == 200:
            data = response.json()
            endpoints = data.get('endpoints', [])
            
            export_endpoints = [ep for ep in endpoints if 'export' in ep.lower()]
            
            logger.info("Export endpoints found in API info:")
            for endpoint in export_endpoints:
                logger.info(f"  - {endpoint}")
                
            if len(export_endpoints) >= 3:
                logger.info("✅ All export endpoints are documented")
            else:
                logger.warning("⚠️  Some export endpoints may be missing from documentation")
        else:
            logger.error(f"Failed to get API info: {response.status_code}")
            
    except Exception as e:
        logger.error(f"Error testing API info: {e}")

if __name__ == "__main__":
    logger.info("🧪 Testing Export Functionality")
    logger.info("=" * 50)
    
    # Test API documentation first
    test_api_info()
    print()
    
    # Test export endpoints
    test_export_endpoints()
    
    logger.info("=" * 50)
    logger.info("✨ Export testing completed!")
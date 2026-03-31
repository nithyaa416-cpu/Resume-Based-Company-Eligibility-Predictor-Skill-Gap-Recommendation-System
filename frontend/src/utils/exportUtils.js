/**
 * Export Utilities for Resume Analysis Reports
 * Handles PDF, Excel, and JSON exports with proper formatting
 */

import toast from 'react-hot-toast';

export class ExportUtils {
  static async exportAnalysisReport(analysisData, format = 'json', userInfo = {}) {
    try {
      toast.loading(`Generating ${format.toUpperCase()} report...`, { id: 'export' });

      const response = await fetch(`/export-${format}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          analysis_data: analysisData,
          user_info: userInfo
        }),
      });

      if (response.ok) {
        const blob = await response.blob();
        this.downloadBlob(blob, format, analysisData);
        toast.success(`${format.toUpperCase()} report downloaded!`, { id: 'export' });
        return true;
      } else {
        const errorData = await response.json();
        toast.error(`Export failed: ${errorData.message}`, { id: 'export' });
        return false;
      }
    } catch (error) {
      toast.error(`Error exporting ${format}: ${error.message}`, { id: 'export' });
      return false;
    }
  }

  static downloadBlob(blob, format, analysisData) {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    
    // Generate filename with timestamp
    const timestamp = new Date().toISOString().split('T')[0];
    const company = analysisData.company || 'analysis';
    const role = analysisData.role || '';
    
    let filename = `resume_${company.toLowerCase().replace(/\s+/g, '_')}`;
    if (role) {
      filename += `_${role.toLowerCase().replace(/\s+/g, '_')}`;
    }
    filename += `_${timestamp}`;
    
    switch (format) {
      case 'pdf':
        filename += '.html'; // Currently exports as HTML
        break;
      case 'excel':
        filename += '.csv';
        break;
      case 'json':
        filename += '.json';
        break;
      default:
        filename += '.txt';
    }
    
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  }

  static async exportMultipleAnalysis(results, format = 'json') {
    try {
      toast.loading(`Generating comprehensive ${format.toUpperCase()} report...`, { id: 'export-multi' });

      // Prepare comprehensive analysis data
      const comprehensiveData = {
        report_type: 'comprehensive_analysis',
        generated_at: new Date().toISOString(),
        total_positions: results.total_positions || 0,
        resume_skills: results.resume_skills || [],
        company_analysis: results.company_analysis || [],
        summary: {
          top_matches: results.company_analysis?.slice(0, 5).map(item => ({
            company: item.company,
            role: item.role,
            score: item.ml_analysis?.ml_eligibility_score || 0
          })) || [],
          average_score: this.calculateAverageScore(results.company_analysis),
          skills_coverage: results.resume_skills?.length || 0
        }
      };

      const response = await fetch(`/export-${format}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          analysis_data: comprehensiveData,
          user_info: {
            analysis_type: 'comprehensive',
            total_companies: results.total_positions || 0
          }
        }),
      });

      if (response.ok) {
        const blob = await response.blob();
        this.downloadBlob(blob, format, { company: 'comprehensive', role: 'analysis' });
        toast.success(`Comprehensive ${format.toUpperCase()} report downloaded!`, { id: 'export-multi' });
        return true;
      } else {
        const errorData = await response.json();
        toast.error(`Export failed: ${errorData.message}`, { id: 'export-multi' });
        return false;
      }
    } catch (error) {
      toast.error(`Error exporting comprehensive ${format}: ${error.message}`, { id: 'export-multi' });
      return false;
    }
  }

  static calculateAverageScore(companyAnalysis) {
    if (!companyAnalysis || companyAnalysis.length === 0) return 0;
    
    const totalScore = companyAnalysis.reduce((sum, item) => {
      return sum + (item.ml_analysis?.ml_eligibility_score || 0);
    }, 0);
    
    return Math.round(totalScore / companyAnalysis.length);
  }

  static async exportOptimizationReport(optimization, resumeData, targetRole = null) {
    const analysisData = {
      company: targetRole?.company || 'Resume Optimization',
      role: targetRole?.role || '',
      optimization: optimization,
      generated_at: new Date().toISOString(),
      report_type: 'optimization'
    };

    const userInfo = {
      filename: resumeData?.filename || 'resume.pdf',
      analysis_date: new Date().toLocaleDateString(),
      optimization_focus: targetRole ? `${targetRole.company} - ${targetRole.role}` : 'General'
    };

    return this.exportAnalysisReport(analysisData, 'pdf', userInfo);
  }

  static async exportATSReport(atsReport, resumeData) {
    const analysisData = {
      company: 'ATS Compatibility Analysis',
      role: '',
      ats_report: atsReport,
      generated_at: new Date().toISOString(),
      report_type: 'ats_analysis'
    };

    const userInfo = {
      filename: resumeData?.filename || 'resume.pdf',
      analysis_date: new Date().toLocaleDateString()
    };

    return this.exportAnalysisReport(analysisData, 'pdf', userInfo);
  }

  // Legacy JSON export for backward compatibility
  static exportAsJSON(data, filename = 'analysis-results') {
    const dataStr = JSON.stringify(data, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const timestamp = new Date().toISOString().split('T')[0];
    const exportFileDefaultName = `${filename}-${timestamp}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
    
    toast.success('Results exported successfully!');
  }
}

// Export button component for reuse
export const ExportButton = ({ 
  onClick, 
  format = 'pdf', 
  disabled = false, 
  className = '', 
  children 
}) => {
  const getFormatIcon = () => {
    switch (format) {
      case 'pdf':
        return '📄';
      case 'excel':
        return '📊';
      case 'json':
        return '📋';
      default:
        return '💾';
    }
  };

  const getFormatColor = () => {
    switch (format) {
      case 'pdf':
        return 'border-red-200 hover:bg-red-50 text-red-700';
      case 'excel':
        return 'border-green-200 hover:bg-green-50 text-green-700';
      case 'json':
        return 'border-blue-200 hover:bg-blue-50 text-blue-700';
      default:
        return 'border-gray-200 hover:bg-gray-50 text-gray-700';
    }
  };

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`
        flex items-center justify-center space-x-2 p-3 border rounded-lg 
        transition-colors disabled:opacity-50 disabled:cursor-not-allowed
        ${getFormatColor()} ${className}
      `}
    >
      <span className="text-lg">{getFormatIcon()}</span>
      <span className="font-medium">
        {children || `Export as ${format.toUpperCase()}`}
      </span>
    </button>
  );
};

export default ExportUtils;
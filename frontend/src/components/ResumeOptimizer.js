import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Zap, 
  AlertTriangle, 
  AlertCircle, 
  Lightbulb,
  ArrowRight,
  Download,
  FileDown,
  FileSpreadsheet,
  FileText
} from 'lucide-react';
import toast from 'react-hot-toast';
import { ExportUtils } from '../utils/exportUtils';

const ResumeOptimizer = ({ resumeData, targetRole = null }) => {
  const [optimization, setOptimization] = useState(null);
  const [loading, setLoading] = useState(false);
  const [exporting, setExporting] = useState(false);

  const handleOptimize = async () => {
    if (!resumeData) {
      toast.error('Please upload a resume first');
      return;
    }

    try {
      setLoading(true);
      toast.loading('Analyzing resume for optimization...', { id: 'optimize' });

      const response = await fetch('/optimize-resume', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          resume_text: resumeData.resume_text || resumeData.text,
          target_role: targetRole
        }),
      });

      const data = await response.json();

      if (data.status === 'success') {
        setOptimization(data.optimization);
        toast.success('Resume optimization complete!', { id: 'optimize' });
      } else {
        toast.error('Optimization failed: ' + data.message, { id: 'optimize' });
      }

    } catch (error) {
      toast.error('Error optimizing resume: ' + error.message, { id: 'optimize' });
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async (format) => {
    if (!optimization) {
      toast.error('Please run optimization first');
      return;
    }

    setExporting(true);
    
    try {
      await ExportUtils.exportOptimizationReport(optimization, resumeData, targetRole);
    } finally {
      setExporting(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600 bg-green-50 border-green-200';
    if (score >= 60) return 'text-blue-600 bg-blue-50 border-blue-200';
    if (score >= 40) return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    return 'text-red-600 bg-red-50 border-red-200';
  };

  const getScoreBarColor = (score) => {
    if (score >= 80) return 'from-green-500 to-green-600';
    if (score >= 60) return 'from-blue-500 to-blue-600';
    if (score >= 40) return 'from-yellow-500 to-yellow-600';
    return 'from-red-500 to-red-600';
  };

  const getSuggestionIcon = (type) => {
    switch (type) {
      case 'critical': return <AlertCircle className="w-5 h-5 text-red-500" />;
      case 'important': return <AlertTriangle className="w-5 h-5 text-yellow-500" />;
      case 'warning': return <AlertTriangle className="w-5 h-5 text-orange-500" />;
      default: return <Lightbulb className="w-5 h-5 text-blue-500" />;
    }
  };

  const getSuggestionBorderColor = (type) => {
    switch (type) {
      case 'critical': return 'border-red-200 bg-red-50';
      case 'important': return 'border-yellow-200 bg-yellow-50';
      case 'warning': return 'border-orange-200 bg-orange-50';
      default: return 'border-blue-200 bg-blue-50';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
            <Zap className="w-5 h-5 text-purple-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">AI Resume Optimizer</h3>
            <p className="text-sm text-gray-600">Get personalized suggestions to improve your resume</p>
          </div>
        </div>

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleOptimize}
          disabled={!resumeData || loading}
          className="btn-primary flex items-center space-x-2"
        >
          <Zap className={`w-4 h-4 ${loading ? 'animate-pulse' : ''}`} />
          <span>{loading ? 'Optimizing...' : 'Optimize Resume'}</span>
        </motion.button>
      </div>

      {/* Optimization Results */}
      {optimization && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="space-y-6"
        >
          {/* Overall Score */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h4 className="text-lg font-semibold text-gray-900 mb-4">Overall Resume Score</h4>
            
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
              <div className="text-center">
                <div className={`text-3xl font-bold mb-2 ${getScoreColor(optimization.overall_score).split(' ')[0]}`}>
                  {optimization.overall_score}
                </div>
                <div className="text-sm text-gray-600">Overall Score</div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <div 
                    className={`h-2 rounded-full bg-gradient-to-r ${getScoreBarColor(optimization.overall_score)}`}
                    style={{ width: `${optimization.overall_score}%` }}
                  ></div>
                </div>
              </div>

              <div className="text-center">
                <div className={`text-2xl font-bold mb-2 ${getScoreColor(optimization.scores.structure).split(' ')[0]}`}>
                  {optimization.scores.structure}
                </div>
                <div className="text-sm text-gray-600">Structure</div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <div 
                    className={`h-2 rounded-full bg-gradient-to-r ${getScoreBarColor(optimization.scores.structure)}`}
                    style={{ width: `${optimization.scores.structure}%` }}
                  ></div>
                </div>
              </div>

              <div className="text-center">
                <div className={`text-2xl font-bold mb-2 ${getScoreColor(optimization.scores.ats_compatibility).split(' ')[0]}`}>
                  {optimization.scores.ats_compatibility}
                </div>
                <div className="text-sm text-gray-600">ATS Compatible</div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <div 
                    className={`h-2 rounded-full bg-gradient-to-r ${getScoreBarColor(optimization.scores.ats_compatibility)}`}
                    style={{ width: `${optimization.scores.ats_compatibility}%` }}
                  ></div>
                </div>
              </div>

              <div className="text-center">
                <div className={`text-2xl font-bold mb-2 ${getScoreColor(optimization.scores.content_quality).split(' ')[0]}`}>
                  {optimization.scores.content_quality}
                </div>
                <div className="text-sm text-gray-600">Content Quality</div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <div 
                    className={`h-2 rounded-full bg-gradient-to-r ${getScoreBarColor(optimization.scores.content_quality)}`}
                    style={{ width: `${optimization.scores.content_quality}%` }}
                  ></div>
                </div>
              </div>
            </div>

            {/* Summary Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-4 border-t border-gray-200">
              <div className="text-center">
                <div className="text-lg font-semibold text-gray-900">{optimization.summary.word_count}</div>
                <div className="text-xs text-gray-600">Words</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold text-gray-900">{optimization.summary.sections_found}</div>
                <div className="text-xs text-gray-600">Sections Found</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold text-gray-900">{optimization.summary.skills_identified}</div>
                <div className="text-xs text-gray-600">Skills Identified</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold text-gray-900">{optimization.suggestions.total_count}</div>
                <div className="text-xs text-gray-600">Suggestions</div>
              </div>
            </div>
          </div>

          {/* Export Options */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h4 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <Download className="w-5 h-5 text-blue-600 mr-2" />
              Export Analysis Report
            </h4>
            <p className="text-sm text-gray-600 mb-4">
              Download your resume analysis in different formats for sharing or record keeping.
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => handleExport('pdf')}
                disabled={exporting}
                className="flex items-center justify-center space-x-2 p-4 border border-red-200 rounded-lg hover:bg-red-50 transition-colors disabled:opacity-50"
              >
                <FileText className="w-5 h-5 text-red-600" />
                <span className="font-medium text-red-700">Export as PDF</span>
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => handleExport('excel')}
                disabled={exporting}
                className="flex items-center justify-center space-x-2 p-4 border border-green-200 rounded-lg hover:bg-green-50 transition-colors disabled:opacity-50"
              >
                <FileSpreadsheet className="w-5 h-5 text-green-600" />
                <span className="font-medium text-green-700">Export as Excel</span>
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => handleExport('json')}
                disabled={exporting}
                className="flex items-center justify-center space-x-2 p-4 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors disabled:opacity-50"
              >
                <FileDown className="w-5 h-5 text-blue-600" />
                <span className="font-medium text-blue-700">Export as JSON</span>
              </motion.button>
            </div>

            {exporting && (
              <div className="mt-4 text-center">
                <div className="inline-flex items-center space-x-2 text-blue-600">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                  <span className="text-sm">Generating report...</span>
                </div>
              </div>
            )}
          </div>

          {/* Critical Issues */}
          {optimization.suggestions.critical.length > 0 && (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h4 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
                Critical Issues ({optimization.suggestions.critical.length})
              </h4>
              <div className="space-y-3">
                {optimization.suggestions.critical.map((suggestion, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.3, delay: index * 0.1 }}
                    className={`p-4 rounded-lg border ${getSuggestionBorderColor(suggestion.type)}`}
                  >
                    <div className="flex items-start space-x-3">
                      {getSuggestionIcon(suggestion.type)}
                      <div className="flex-1">
                        <h5 className="font-medium text-gray-900">{suggestion.title}</h5>
                        <p className="text-sm text-gray-600 mt-1">{suggestion.description}</p>
                        <div className="flex items-center mt-2">
                          <span className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
                            {suggestion.category}
                          </span>
                          <span className={`text-xs px-2 py-1 rounded ml-2 ${
                            suggestion.impact === 'high' ? 'bg-red-100 text-red-700' :
                            suggestion.impact === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                            'bg-blue-100 text-blue-700'
                          }`}>
                            {suggestion.impact} impact
                          </span>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          )}

          {/* Important Suggestions */}
          {optimization.suggestions.important.length > 0 && (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h4 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <AlertTriangle className="w-5 h-5 text-yellow-500 mr-2" />
                Important Suggestions ({optimization.suggestions.important.length})
              </h4>
              <div className="space-y-3">
                {optimization.suggestions.important.map((suggestion, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.3, delay: index * 0.1 }}
                    className={`p-4 rounded-lg border ${getSuggestionBorderColor(suggestion.type)}`}
                  >
                    <div className="flex items-start space-x-3">
                      {getSuggestionIcon(suggestion.type)}
                      <div className="flex-1">
                        <h5 className="font-medium text-gray-900">{suggestion.title}</h5>
                        <p className="text-sm text-gray-600 mt-1">{suggestion.description}</p>
                        {suggestion.skills && (
                          <div className="flex flex-wrap gap-1 mt-2">
                            {suggestion.skills.slice(0, 5).map((skill, idx) => (
                              <span key={idx} className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                                {skill}
                              </span>
                            ))}
                          </div>
                        )}
                        <div className="flex items-center mt-2">
                          <span className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
                            {suggestion.category}
                          </span>
                          <span className={`text-xs px-2 py-1 rounded ml-2 ${
                            suggestion.impact === 'high' ? 'bg-red-100 text-red-700' :
                            suggestion.impact === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                            'bg-blue-100 text-blue-700'
                          }`}>
                            {suggestion.impact} impact
                          </span>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          )}

          {/* Other Suggestions */}
          {optimization.suggestions.other.length > 0 && (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h4 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <Lightbulb className="w-5 h-5 text-blue-500 mr-2" />
                Additional Suggestions ({optimization.suggestions.other.length})
              </h4>
              <div className="space-y-3">
                {optimization.suggestions.other.map((suggestion, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.3, delay: index * 0.1 }}
                    className={`p-4 rounded-lg border ${getSuggestionBorderColor(suggestion.type)}`}
                  >
                    <div className="flex items-start space-x-3">
                      {getSuggestionIcon(suggestion.type)}
                      <div className="flex-1">
                        <h5 className="font-medium text-gray-900">{suggestion.title}</h5>
                        <p className="text-sm text-gray-600 mt-1">{suggestion.description}</p>
                        {suggestion.skills && (
                          <div className="flex flex-wrap gap-1 mt-2">
                            {suggestion.skills.slice(0, 5).map((skill, idx) => (
                              <span key={idx} className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                                {skill}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          )}

          {/* Next Steps */}
          <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-xl p-6">
            <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
              <ArrowRight className="w-5 h-5 text-blue-600 mr-2" />
              Next Steps
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-white p-4 rounded-lg">
                <h5 className="font-medium text-gray-900 mb-2">🎯 Priority Actions</h5>
                <p className="text-sm text-gray-600">
                  Focus on critical and important suggestions first for maximum impact
                </p>
              </div>
              <div className="bg-white p-4 rounded-lg">
                <h5 className="font-medium text-gray-900 mb-2">🔄 Re-analyze</h5>
                <p className="text-sm text-gray-600">
                  Update your resume and run optimization again to track improvements
                </p>
              </div>
            </div>
          </div>
        </motion.div>
      )}

      {/* Call to Action */}
      {!optimization && resumeData && (
        <div className="bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-200 rounded-xl p-6 text-center">
          <Zap className="w-12 h-12 text-purple-600 mx-auto mb-4" />
          <h4 className="font-semibold text-gray-900 mb-2">Ready to Optimize Your Resume?</h4>
          <p className="text-gray-600 mb-4">
            Get smart suggestions to improve your resume's structure, ATS compatibility, and content quality.
          </p>
          <button
            onClick={handleOptimize}
            className="btn-primary"
          >
            Start Optimization
          </button>
        </div>
      )}
    </div>
  );
};

export default ResumeOptimizer;
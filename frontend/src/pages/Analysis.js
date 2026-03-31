import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import ImprovedAnalysisResults from '../components/ImprovedAnalysisResults';
import { ArrowLeft, Share2, RefreshCw, FileText, FileSpreadsheet, FileDown } from 'lucide-react';
import toast from 'react-hot-toast';
import { ExportUtils } from '../utils/exportUtils';

const Analysis = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [results, setResults] = useState(null);
  const [type, setType] = useState('single');
  const [exporting, setExporting] = useState(false);

  useEffect(() => {
    if (location.state?.results) {
      setResults(location.state.results);
      setType(location.state.type || 'single');
      // Persist so nav "Last Results" link works
      sessionStorage.setItem('lastAnalysisResults', JSON.stringify(location.state.results));
      sessionStorage.setItem('lastAnalysisType', location.state.type || 'single');
    } else {
      // Try to restore from sessionStorage
      const saved = sessionStorage.getItem('lastAnalysisResults');
      const savedType = sessionStorage.getItem('lastAnalysisType');
      if (saved) {
        setResults(JSON.parse(saved));
        setType(savedType || 'single');
      } else {
        navigate('/dashboard');
      }
    }
  }, [location.state, navigate]);

  const handleExportResults = async (format = 'json') => {
    if (!results) return;

    setExporting(true);
    
    try {
      if (type === 'multiple') {
        await ExportUtils.exportMultipleAnalysis(results, format);
      } else {
        // Single company analysis
        const analysisData = {
          company: results.company || 'Analysis',
          role: results.role || '',
          ml_analysis: results.ml_analysis,
          generated_at: new Date().toISOString(),
          report_type: 'single_analysis'
        };
        
        await ExportUtils.exportAnalysisReport(analysisData, format);
      }
    } finally {
      setExporting(false);
    }
  };

  const handleShareResults = async () => {
    if (!results) return;

    try {
      const shareData = {
        title: 'Resume Analysis Results',
        text: `Check out my resume analysis results!`,
        url: window.location.href,
      };

      if (navigator.share) {
        await navigator.share(shareData);
      } else {
        // Fallback: copy to clipboard
        await navigator.clipboard.writeText(window.location.href);
        toast.success('Link copied to clipboard!');
      }
    } catch (error) {
      toast.error('Failed to share results');
    }
  };

  const handleNewAnalysis = () => {
    navigate('/dashboard');
  };

  if (!results) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading analysis results...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4"
      >
        <div className="flex items-center space-x-4">
          <button
            onClick={() => navigate('/dashboard')}
            className="btn-secondary flex items-center space-x-2"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Dashboard</span>
          </button>
          
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              {type === 'multiple' ? 'Multi-Company Analysis' : 'Company Analysis'}
            </h1>
            <p className="text-gray-600">
              {type === 'multiple' 
                ? `Analysis across ${results.total_positions || results.total_companies} positions`
                : `Detailed analysis for ${results.company}${results.role ? ` - ${results.role}` : ''}`
              }
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2">
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => handleExportResults('pdf')}
              disabled={exporting}
              className="btn-secondary flex items-center space-x-2 disabled:opacity-50"
            >
              <FileText className="w-4 h-4" />
              <span>PDF</span>
            </motion.button>
            
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => handleExportResults('excel')}
              disabled={exporting}
              className="btn-secondary flex items-center space-x-2 disabled:opacity-50"
            >
              <FileSpreadsheet className="w-4 h-4" />
              <span>Excel</span>
            </motion.button>
            
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => handleExportResults('json')}
              disabled={exporting}
              className="btn-secondary flex items-center space-x-2 disabled:opacity-50"
            >
              <FileDown className="w-4 h-4" />
              <span>JSON</span>
            </motion.button>
          </div>
          
          <button
            onClick={handleShareResults}
            className="btn-secondary flex items-center space-x-2"
          >
            <Share2 className="w-4 h-4" />
            <span>Share</span>
          </button>
          
          <button
            onClick={handleNewAnalysis}
            className="btn-primary flex items-center space-x-2"
          >
            <RefreshCw className="w-4 h-4" />
            <span>New Analysis</span>
          </button>
        </div>
      </motion.div>

      {/* Analysis Results */}
      <ImprovedAnalysisResults results={results} type={type} />

      {/* Action Items */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.4 }}
        className="bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-xl border border-blue-100"
      >
        <h3 className="font-semibold text-gray-900 mb-4">🚀 Next Steps</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-white p-4 rounded-lg">
            <h4 className="font-medium text-gray-900 mb-2">📚 Focus on Learning</h4>
            <p className="text-sm text-gray-600">
              Review the personalized learning roadmap and start with high-priority skills
            </p>
          </div>
          <div className="bg-white p-4 rounded-lg">
            <h4 className="font-medium text-gray-900 mb-2">🎯 Target Applications</h4>
            <p className="text-sm text-gray-600">
              Apply to companies where you scored 70%+ for the best chances of success
            </p>
          </div>
          <div className="bg-white p-4 rounded-lg">
            <h4 className="font-medium text-gray-900 mb-2">🔄 Regular Updates</h4>
            <p className="text-sm text-gray-600">
              Re-analyze your resume after gaining new skills or experience
            </p>
          </div>
          <div className="bg-white p-4 rounded-lg">
            <h4 className="font-medium text-gray-900 mb-2">📊 Track Progress</h4>
            <p className="text-sm text-gray-600">
              Use the comparison feature to see how your scores improve over time
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Analysis;
import React from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, Users, Award, Sparkles } from 'lucide-react';
import CompanyCard from './CompanyCard';

const ImprovedAnalysisResults = ({ results, type = 'single' }) => {
  if (!results) return null;

  // Multi-company analysis
  if (type === 'multiple') {
    const companyAnalysis = results.company_analysis || [];
    
    // Calculate statistics
    const highlyEligible = companyAnalysis.filter(c => c.ml_analysis?.eligibility_level === 'Highly Eligible').length;
    const eligible = companyAnalysis.filter(c => c.ml_analysis?.eligibility_level === 'Eligible').length;
    const notEligible = companyAnalysis.filter(c => c.ml_analysis?.eligibility_level === 'Not Eligible').length;

    return (
      <div className="space-y-8">
        {/* Success Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="bg-gradient-to-r from-blue-500 to-indigo-600 rounded-2xl p-8 text-white shadow-lg"
        >
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center">
              <Sparkles className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-3xl font-bold">Analysis Complete!</h2>
              <p className="text-blue-100">We analyzed {companyAnalysis.length} companies for you</p>
            </div>
          </div>
        </motion.div>

        {/* Statistics Overview */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6"
        >
          <div className="bg-gradient-to-br from-green-50 to-emerald-50 p-6 rounded-xl border-2 border-green-200">
            <div className="flex items-center justify-between mb-2">
              <Award className="w-8 h-8 text-green-600" />
              <span className="text-3xl font-bold text-green-700">{highlyEligible}</span>
            </div>
            <h3 className="text-lg font-semibold text-gray-900">Highly Eligible</h3>
            <p className="text-sm text-gray-600">Strong matches for you</p>
          </div>

          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 p-6 rounded-xl border-2 border-blue-200">
            <div className="flex items-center justify-between mb-2">
              <Users className="w-8 h-8 text-blue-600" />
              <span className="text-3xl font-bold text-blue-700">{eligible}</span>
            </div>
            <h3 className="text-lg font-semibold text-gray-900">Eligible</h3>
            <p className="text-sm text-gray-600">Good opportunities</p>
          </div>

          <div className="bg-gradient-to-br from-orange-50 to-red-50 p-6 rounded-xl border-2 border-orange-200">
            <div className="flex items-center justify-between mb-2">
              <TrendingUp className="w-8 h-8 text-orange-600" />
              <span className="text-3xl font-bold text-orange-700">{notEligible}</span>
            </div>
            <h3 className="text-lg font-semibold text-gray-900">Growth Opportunities</h3>
            <p className="text-sm text-gray-600">Skills to develop</p>
          </div>
        </motion.div>

        {/* Company Cards */}
        <div>
          <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
            <TrendingUp className="w-6 h-6 mr-3 text-blue-500" />
            Your Company Matches
          </h3>
          <div className="space-y-4">
            {companyAnalysis.map((result, index) => (
              <CompanyCard
                key={`${result.company}-${result.role || 'default'}`}
                company={result.company}
                role={result.role}
                analysis={result.ml_analysis}
                index={index}
              />
            ))}
          </div>
        </div>

        {/* Action Tips */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-xl border border-purple-200"
        >
          <h3 className="text-lg font-bold text-gray-900 mb-4">💡 Next Steps</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0 w-6 h-6 bg-purple-500 text-white rounded-full flex items-center justify-center text-sm font-bold">1</div>
              <div>
                <h4 className="font-semibold text-gray-900">Apply to Top Matches</h4>
                <p className="text-sm text-gray-600">Focus on companies where you're Highly Eligible or Eligible</p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0 w-6 h-6 bg-purple-500 text-white rounded-full flex items-center justify-center text-sm font-bold">2</div>
              <div>
                <h4 className="font-semibold text-gray-900">Start Learning</h4>
                <p className="text-sm text-gray-600">Use the learning roadmaps to improve your skills</p>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    );
  }

  // Single company analysis
  const analysis = results.ml_analysis;
  if (!analysis) return null;

  return (
    <div className="space-y-6">
      <CompanyCard
        company={results.company}
        role={results.role}
        analysis={analysis}
        index={0}
      />
    </div>
  );
};

export default ImprovedAnalysisResults;

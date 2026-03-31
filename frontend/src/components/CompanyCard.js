import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, ChevronUp, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import EligibilityBadge from './EligibilityBadge';
import SkillMatchSection from './SkillMatchSection';
import ImprovedRoadmapSection from './ImprovedRoadmapSection';

const CompanyCard = ({ company, role, analysis, index }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [showRoadmap, setShowRoadmap] = useState(false);

  const score = analysis?.ml_eligibility_score || 0;
  const eligibilityLevel = analysis?.eligibility_level || 'Not Eligible';

  const getScoreColor = (score) => {
    if (score >= 85) return 'from-green-500 to-green-600';
    if (score >= 70) return 'from-blue-500 to-blue-600';
    return 'from-red-500 to-red-600';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: index * 0.1 }}
      className="bg-white rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-all duration-300 overflow-hidden"
    >
      {/* Company Header */}
      <div className="p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h3 className="text-xl font-semibold text-gray-900 mb-1">{company}</h3>
            {role && <p className="text-sm text-gray-600">{role}</p>}
          </div>
          <EligibilityBadge level={eligibilityLevel} />
        </div>

        {/* Eligibility Score */}
        <div className="mb-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">Eligibility Score</span>
            <span className="text-2xl font-bold text-gray-900">{score}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${score}%` }}
              transition={{ duration: 1, delay: 0.3 }}
              className={`h-full bg-gradient-to-r ${getScoreColor(score)} rounded-full`}
            />
          </div>
        </div>

        {/* View Details Button */}
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="w-full flex items-center justify-center space-x-2 px-4 py-3 bg-gray-50 hover:bg-gray-100 text-gray-700 font-medium rounded-lg transition-colors duration-200"
        >
          <span>{isExpanded ? 'Hide' : 'View'} Detailed Analysis</span>
          {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>
      </div>

      {/* Expandable Detailed Analysis */}
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="border-t border-gray-200"
          >
            <div className="p-6 bg-gray-50">
              {/* Skill Match Section */}
              <SkillMatchSection analysis={analysis} />

              {/* See Learning Roadmap Button */}
              {!showRoadmap && (
                <motion.button
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                  onClick={() => setShowRoadmap(true)}
                  className="w-full mt-6 px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-medium rounded-lg transition-all duration-200 shadow-sm hover:shadow-md"
                >
                  See Learning Roadmap
                </motion.button>
              )}

              {/* Learning Roadmap Section */}
              <AnimatePresence>
                {showRoadmap && (
                  <ImprovedRoadmapSection 
                    analysis={analysis} 
                    company={company}
                  />
                )}
              </AnimatePresence>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

export default CompanyCard;

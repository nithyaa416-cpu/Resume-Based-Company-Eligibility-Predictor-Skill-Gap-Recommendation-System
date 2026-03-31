import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, XCircle, TrendingUp } from 'lucide-react';

const SkillMatchSection = ({ analysis }) => {
  const skillReadiness = analysis?.skill_readiness_levels || {};
  
  // Combine Advanced and Intermediate as "Matched Skills"
  const matchedSkills = [
    ...(skillReadiness.Advanced || []),
    ...(skillReadiness.Intermediate || [])
  ];

  // Missing skills
  const missingSkills = skillReadiness.Missing || [];

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="space-y-6"
    >
      {/* Matched Skills */}
      {matchedSkills.length > 0 && (
        <div>
          <div className="flex items-center space-x-2 mb-3">
            <CheckCircle className="w-5 h-5 text-green-600" />
            <h4 className="text-lg font-semibold text-gray-900">Matched Skills</h4>
            <span className="text-sm text-gray-500">({matchedSkills.length})</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {matchedSkills.slice(0, 12).map((skillObj, idx) => (
              <motion.span
                key={idx}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: idx * 0.05 }}
                className="inline-flex items-center px-3 py-1.5 bg-green-50 text-green-700 rounded-lg text-sm font-medium border border-green-200"
              >
                {skillObj.skill || skillObj}
              </motion.span>
            ))}
            {matchedSkills.length > 12 && (
              <span className="inline-flex items-center px-3 py-1.5 bg-gray-100 text-gray-600 rounded-lg text-sm">
                +{matchedSkills.length - 12} more
              </span>
            )}
          </div>
        </div>
      )}

      {/* Missing Skills */}
      {missingSkills.length > 0 && (
        <div>
          <div className="flex items-center space-x-2 mb-3">
            <TrendingUp className="w-5 h-5 text-orange-600" />
            <h4 className="text-lg font-semibold text-gray-900">Skills to Improve</h4>
            <span className="text-sm text-gray-500">({missingSkills.length})</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {missingSkills.slice(0, 12).map((skillObj, idx) => (
              <motion.span
                key={idx}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: idx * 0.05 }}
                className="inline-flex items-center px-3 py-1.5 bg-orange-50 text-orange-700 rounded-lg text-sm font-medium border border-orange-200"
              >
                {skillObj.skill || skillObj}
              </motion.span>
            ))}
            {missingSkills.length > 12 && (
              <span className="inline-flex items-center px-3 py-1.5 bg-gray-100 text-gray-600 rounded-lg text-sm">
                +{missingSkills.length - 12} more
              </span>
            )}
          </div>
        </div>
      )}

      {/* Match Breakdown */}
      {analysis?.processing_info && (
        <div className="grid grid-cols-2 gap-4 pt-4 border-t border-gray-200">
          <div className="text-center p-4 bg-purple-50 rounded-lg">
            <div className="text-2xl font-bold text-purple-700">
              {analysis.processing_info.semantic_component}%
            </div>
            <div className="text-sm text-purple-600 mt-1">Profile Match</div>
          </div>
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <div className="text-2xl font-bold text-blue-700">
              {analysis.processing_info.skill_component}%
            </div>
            <div className="text-sm text-blue-600 mt-1">Skills Match</div>
          </div>
        </div>
      )}
    </motion.div>
  );
};

export default SkillMatchSection;

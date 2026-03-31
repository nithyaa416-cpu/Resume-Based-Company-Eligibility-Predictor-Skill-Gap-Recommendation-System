import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { BookOpen, DollarSign, ChevronDown, ChevronUp } from 'lucide-react';
import ResourceList from './ResourceList';

const SkillRoadmapCard = ({ skill, freeResources, paidResources, index }) => {
  const [showFree, setShowFree] = useState(false);
  const [showPaid, setShowPaid] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: index * 0.05 }}
      className="bg-white rounded-xl border-2 border-gray-200 hover:border-gray-300 transition-all duration-200 overflow-hidden"
    >
      {/* Skill Header */}
      <div className="bg-gradient-to-r from-indigo-50 to-purple-50 p-5 border-b border-gray-200">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-lg">
              {skill.charAt(0).toUpperCase()}
            </span>
          </div>
          <div>
            <h4 className="text-lg font-bold text-gray-900">{skill}</h4>
            <p className="text-sm text-gray-600">
              {freeResources.length + paidResources.length} learning resources available
            </p>
          </div>
        </div>
      </div>

      {/* Resource Buttons */}
      <div className="p-5 space-y-3">
        {/* Free Resources Button */}
        {freeResources.length > 0 && (
          <div>
            <button
              onClick={() => setShowFree(!showFree)}
              className="w-full flex items-center justify-between p-4 bg-gradient-to-r from-green-50 to-emerald-50 hover:from-green-100 hover:to-emerald-100 rounded-lg border-2 border-green-200 transition-all duration-200"
            >
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
                  <BookOpen className="w-4 h-4 text-white" />
                </div>
                <div className="text-left">
                  <p className="font-semibold text-gray-900">Free Resources</p>
                  <p className="text-xs text-gray-600">{freeResources.length} platforms</p>
                </div>
              </div>
              {showFree ? (
                <ChevronUp className="w-5 h-5 text-gray-600" />
              ) : (
                <ChevronDown className="w-5 h-5 text-gray-600" />
              )}
            </button>

            <AnimatePresence>
              {showFree && (
                <ResourceList
                  resources={freeResources}
                  type="free"
                  title={`🆓 Free Learning Options for ${skill}`}
                />
              )}
            </AnimatePresence>
          </div>
        )}

        {/* Paid Resources Button */}
        {paidResources.length > 0 && (
          <div>
            <button
              onClick={() => setShowPaid(!showPaid)}
              className="w-full flex items-center justify-between p-4 bg-gradient-to-r from-blue-50 to-indigo-50 hover:from-blue-100 hover:to-indigo-100 rounded-lg border-2 border-blue-200 transition-all duration-200"
            >
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
                  <DollarSign className="w-4 h-4 text-white" />
                </div>
                <div className="text-left">
                  <p className="font-semibold text-gray-900">Paid Resources</p>
                  <p className="text-xs text-gray-600">{paidResources.length} premium courses</p>
                </div>
              </div>
              {showPaid ? (
                <ChevronUp className="w-5 h-5 text-gray-600" />
              ) : (
                <ChevronDown className="w-5 h-5 text-gray-600" />
              )}
            </button>

            <AnimatePresence>
              {showPaid && (
                <ResourceList
                  resources={paidResources}
                  type="paid"
                  title={`💎 Premium Courses for ${skill}`}
                />
              )}
            </AnimatePresence>
          </div>
        )}

        {/* No Resources Message */}
        {freeResources.length === 0 && paidResources.length === 0 && (
          <div className="text-center py-4 text-gray-500 text-sm">
            No learning resources available for this skill
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default SkillRoadmapCard;

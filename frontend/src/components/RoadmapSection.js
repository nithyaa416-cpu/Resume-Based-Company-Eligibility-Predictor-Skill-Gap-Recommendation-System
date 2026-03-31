import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { BookOpen, DollarSign, GraduationCap } from 'lucide-react';
import ResourceCard from './ResourceCard';

const RoadmapSection = ({ analysis, company }) => {
  const [selectedType, setSelectedType] = useState(null);

  const learningRecommendations = analysis?.learning_recommendations || {};
  const learningRoadmap = analysis?.learning_roadmap?.learning_path || [];

  // Organize resources by type
  const organizeResources = () => {
    const freeResources = [];
    const paidResources = [];

    Object.entries(learningRecommendations).forEach(([skill, platforms]) => {
      if (platforms.free && platforms.free.length > 0) {
        platforms.free.forEach(platform => {
          freeResources.push({
            skill,
            platform,
            type: 'free'
          });
        });
      }
      if (platforms.paid && platforms.paid.length > 0) {
        platforms.paid.forEach(platform => {
          paidResources.push({
            skill,
            platform,
            type: 'paid'
          });
        });
      }
    });

    return { freeResources, paidResources };
  };

  const { freeResources, paidResources } = organizeResources();

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="mt-6 space-y-6"
    >
      {/* Roadmap Header */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-lg border border-blue-200">
        <div className="flex items-center space-x-3 mb-3">
          <GraduationCap className="w-6 h-6 text-blue-600" />
          <h3 className="text-xl font-bold text-gray-900">Learning Roadmap</h3>
        </div>
        <p className="text-gray-700">
          Choose how you'd like to learn the skills needed for {company}
        </p>
      </div>

      {/* Learning Path Overview */}
      {learningRoadmap.length > 0 && !selectedType && (
        <div className="bg-white p-5 rounded-lg border border-gray-200">
          <h4 className="font-semibold text-gray-900 mb-4">Recommended Learning Path</h4>
          <div className="space-y-3">
            {learningRoadmap.map((phase, idx) => (
              <div key={idx} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                <div className="flex-shrink-0 w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-bold text-sm">
                  {phase.phase}
                </div>
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-1">
                    <h5 className="font-medium text-gray-900">{phase.title}</h5>
                    <span className="text-xs text-blue-600 bg-blue-100 px-2 py-1 rounded">
                      {phase.estimated_time}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600">{phase.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Resource Type Selection */}
      {!selectedType && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => setSelectedType('free')}
            className="p-6 bg-gradient-to-br from-green-50 to-emerald-50 hover:from-green-100 hover:to-emerald-100 rounded-xl border-2 border-green-200 hover:border-green-300 transition-all duration-200 text-left"
          >
            <div className="flex items-center space-x-3 mb-3">
              <div className="w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center">
                <BookOpen className="w-6 h-6 text-white" />
              </div>
              <div>
                <h4 className="text-lg font-bold text-gray-900">Free Learning Resources</h4>
                <p className="text-sm text-gray-600">{freeResources.length} resources available</p>
              </div>
            </div>
            <p className="text-sm text-gray-700">
              Access free courses, tutorials, and documentation to build your skills
            </p>
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => setSelectedType('paid')}
            className="p-6 bg-gradient-to-br from-blue-50 to-indigo-50 hover:from-blue-100 hover:to-indigo-100 rounded-xl border-2 border-blue-200 hover:border-blue-300 transition-all duration-200 text-left"
          >
            <div className="flex items-center space-x-3 mb-3">
              <div className="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center">
                <DollarSign className="w-6 h-6 text-white" />
              </div>
              <div>
                <h4 className="text-lg font-bold text-gray-900">Paid Learning Resources</h4>
                <p className="text-sm text-gray-600">{paidResources.length} premium courses</p>
              </div>
            </div>
            <p className="text-sm text-gray-700">
              Structured courses with certificates and expert instruction
            </p>
          </motion.button>
        </div>
      )}

      {/* Resource Display */}
      {selectedType && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="space-y-4"
        >
          <div className="flex items-center justify-between">
            <h4 className="text-lg font-bold text-gray-900">
              {selectedType === 'free' ? '🆓 Free Resources' : '💎 Premium Courses'}
            </h4>
            <button
              onClick={() => setSelectedType(null)}
              className="text-sm text-blue-600 hover:text-blue-700 font-medium"
            >
              ← Back to options
            </button>
          </div>

          <div className="grid grid-cols-1 gap-4">
            {(selectedType === 'free' ? freeResources : paidResources).map((resource, idx) => (
              <ResourceCard
                key={idx}
                skill={resource.skill}
                platform={resource.platform}
                type={resource.type}
                index={idx}
              />
            ))}
          </div>

          {(selectedType === 'free' ? freeResources : paidResources).length === 0 && (
            <div className="text-center py-8 text-gray-500">
              No {selectedType} resources available for this role
            </div>
          )}
        </motion.div>
      )}
    </motion.div>
  );
};

export default RoadmapSection;

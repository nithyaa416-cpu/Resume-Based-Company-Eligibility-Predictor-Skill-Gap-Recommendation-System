import React from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import JobDataStatus from '../components/JobDataStatus';

const JobData = () => {
  const navigate = useNavigate();

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="flex items-center space-x-4"
      >
        <button
          onClick={() => navigate('/dashboard')}
          className="btn-secondary flex items-center space-x-2"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Dashboard</span>
        </button>
        
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Job Data Management</h1>
          <p className="text-gray-600">
            Monitor and manage real-time job market data
          </p>
        </div>
      </motion.div>

      {/* Job Data Status Component */}
      <JobDataStatus />

      {/* Information Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-4">How Real-Time Data Works</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-900 mb-2">🔄 Automatic Updates</h4>
            <p className="text-sm text-gray-600 mb-4">
              Job data is automatically updated every 6 hours with the latest market trends, 
              company requirements, and skill demands.
            </p>
            
            <h4 className="font-medium text-gray-900 mb-2">📊 Market Intelligence</h4>
            <p className="text-sm text-gray-600">
              Our system analyzes current hiring trends from top tech companies including 
              AI/ML startups, big tech, and high-growth companies.
            </p>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-900 mb-2">🎯 Relevant Positions</h4>
            <p className="text-sm text-gray-600 mb-4">
              Focus on in-demand roles like AI Engineer, ML Engineer, Full Stack Developer, 
              DevOps Engineer, and other high-growth positions.
            </p>
            
            <h4 className="font-medium text-gray-900 mb-2">🔧 Current Tech Stack</h4>
            <p className="text-sm text-gray-600">
              Requirements reflect modern technologies: React, TypeScript, Python, 
              Kubernetes, AI/ML tools, and cloud platforms.
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default JobData;
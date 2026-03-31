import React from 'react';
import { motion } from 'framer-motion';
import { ExternalLink, Clock, Award } from 'lucide-react';

const ResourceCard = ({ skill, platform, type, index }) => {
  // Platform-specific configurations
  const platformConfig = {
    'Coursera': { 
      icon: '🎓', 
      duration: '4-6 weeks',
      url: `https://www.coursera.org/search?query=${encodeURIComponent(skill)}`
    },
    'Udemy': { 
      icon: '📚', 
      duration: '10-20 hours',
      url: `https://www.udemy.com/courses/search/?q=${encodeURIComponent(skill)}`
    },
    'YouTube': { 
      icon: '▶️', 
      duration: 'Self-paced',
      url: `https://www.youtube.com/results?search_query=${encodeURIComponent(skill)}+tutorial`
    },
    'FreeCodeCamp': { 
      icon: '💻', 
      duration: 'Self-paced',
      url: `https://www.freecodecamp.org/news/search/?query=${encodeURIComponent(skill)}`
    },
    'LinkedIn Learning': { 
      icon: '💼', 
      duration: '2-4 hours',
      url: `https://www.linkedin.com/learning/search?keywords=${encodeURIComponent(skill)}`
    },
    'Pluralsight': { 
      icon: '🎯', 
      duration: '3-5 hours',
      url: `https://www.pluralsight.com/search?q=${encodeURIComponent(skill)}`
    },
    'edX': { 
      icon: '🏛️', 
      duration: '6-8 weeks',
      url: `https://www.edx.org/search?q=${encodeURIComponent(skill)}`
    },
    'Khan Academy': { 
      icon: '🌟', 
      duration: 'Self-paced',
      url: `https://www.khanacademy.org/search?page_search_query=${encodeURIComponent(skill)}`
    }
  };

  const config = platformConfig[platform] || { 
    icon: '📖', 
    duration: 'Varies',
    url: `https://www.google.com/search?q=learn+${encodeURIComponent(skill)}`
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.3, delay: index * 0.05 }}
      className={`p-5 rounded-lg border-2 transition-all duration-200 hover:shadow-md ${
        type === 'free' 
          ? 'bg-green-50 border-green-200 hover:border-green-300' 
          : 'bg-blue-50 border-blue-200 hover:border-blue-300'
      }`}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-2">
            <span className="text-2xl">{config.icon}</span>
            <div>
              <h5 className="font-semibold text-gray-900">{skill}</h5>
              <p className="text-sm text-gray-600">{platform}</p>
            </div>
          </div>

          <div className="flex items-center space-x-4 mt-3">
            <div className="flex items-center space-x-1 text-sm text-gray-600">
              <Clock className="w-4 h-4" />
              <span>{config.duration}</span>
            </div>
            {type === 'paid' && (
              <div className="flex items-center space-x-1 text-sm text-blue-600">
                <Award className="w-4 h-4" />
                <span>Certificate</span>
              </div>
            )}
          </div>
        </div>

        <a
          href={config.url}
          target="_blank"
          rel="noopener noreferrer"
          className={`flex-shrink-0 px-4 py-2 rounded-lg font-medium text-sm transition-colors duration-200 flex items-center space-x-2 ${
            type === 'free'
              ? 'bg-green-500 hover:bg-green-600 text-white'
              : 'bg-blue-500 hover:bg-blue-600 text-white'
          }`}
        >
          <span>Start Learning</span>
          <ExternalLink className="w-4 h-4" />
        </a>
      </div>
    </motion.div>
  );
};

export default ResourceCard;

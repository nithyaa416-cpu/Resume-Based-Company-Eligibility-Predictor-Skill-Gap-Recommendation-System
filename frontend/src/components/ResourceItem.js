import React from 'react';
import { ExternalLink, Clock } from 'lucide-react';

const ResourceItem = ({ platform, url, duration, type }) => {
  // Platform-specific durations
  const platformDurations = {
    'Coursera': '4-6 weeks',
    'Udemy': '10-20 hours',
    'YouTube': 'Self-paced',
    'FreeCodeCamp': 'Self-paced',
    'LinkedIn Learning': '2-4 hours',
    'Pluralsight': '3-5 hours',
    'edX': '6-8 weeks',
    'Khan Academy': 'Self-paced',
    'GeeksforGeeks': 'Self-paced',
    'Official Documentation': 'Self-paced',
    'W3Schools': 'Self-paced',
    'MDN Web Docs': 'Self-paced'
  };

  const estimatedDuration = duration || platformDurations[platform] || 'Varies';

  return (
    <div className="flex items-center justify-between py-2 px-3 hover:bg-gray-50 rounded-lg transition-colors duration-150">
      <div className="flex items-center space-x-3 flex-1">
        <div className="flex-1">
          <p className="font-medium text-gray-900">{platform}</p>
          <div className="flex items-center space-x-1 text-xs text-gray-500 mt-0.5">
            <Clock className="w-3 h-3" />
            <span>{estimatedDuration}</span>
          </div>
        </div>
      </div>
      <a
        href={url}
        target="_blank"
        rel="noopener noreferrer"
        className={`flex items-center space-x-1 px-3 py-1.5 rounded-md text-sm font-medium transition-all duration-200 ${
          type === 'free'
            ? 'bg-green-500 hover:bg-green-600 text-white'
            : 'bg-blue-500 hover:bg-blue-600 text-white'
        }`}
      >
        <span>Start Learning</span>
        <ExternalLink className="w-3 h-3" />
      </a>
    </div>
  );
};

export default ResourceItem;

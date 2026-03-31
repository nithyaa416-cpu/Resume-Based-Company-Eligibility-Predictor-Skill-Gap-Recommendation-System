import React from 'react';
import { ExternalLink } from 'lucide-react';

const ResourceButton = ({ platform, url, type }) => {
  return (
    <a
      href={url}
      target="_blank"
      rel="noopener noreferrer"
      className={`inline-flex items-center justify-between px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 hover:shadow-md ${
        type === 'free'
          ? 'bg-green-50 text-green-700 hover:bg-green-100 border border-green-200'
          : 'bg-blue-50 text-blue-700 hover:bg-blue-100 border border-blue-200'
      }`}
    >
      <span>{platform}</span>
      <ExternalLink className="w-4 h-4 ml-2" />
    </a>
  );
};

export default ResourceButton;

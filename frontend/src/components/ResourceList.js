import React from 'react';
import { motion } from 'framer-motion';
import ResourceItem from './ResourceItem';

const ResourceList = ({ resources, type, title }) => {
  if (!resources || resources.length === 0) {
    return null;
  }

  return (
    <motion.div
      initial={{ opacity: 0, height: 0 }}
      animate={{ opacity: 1, height: 'auto' }}
      exit={{ opacity: 0, height: 0 }}
      transition={{ duration: 0.3 }}
      className="mt-3"
    >
      <div className={`p-4 rounded-lg border-2 ${
        type === 'free' 
          ? 'bg-green-50 border-green-200' 
          : 'bg-blue-50 border-blue-200'
      }`}>
        <h5 className={`text-sm font-semibold mb-3 ${
          type === 'free' ? 'text-green-900' : 'text-blue-900'
        }`}>
          {title}
        </h5>
        <div className="space-y-1">
          {resources.map((resource, idx) => (
            <ResourceItem
              key={idx}
              platform={resource.platform}
              url={resource.url}
              duration={resource.duration}
              type={type}
            />
          ))}
        </div>
      </div>
    </motion.div>
  );
};

export default ResourceList;

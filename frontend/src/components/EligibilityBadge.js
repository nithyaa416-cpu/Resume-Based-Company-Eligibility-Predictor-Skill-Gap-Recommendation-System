import React from 'react';
import { CheckCircle, AlertCircle, XCircle } from 'lucide-react';

const EligibilityBadge = ({ level }) => {
  const getBadgeConfig = (level) => {
    switch (level) {
      case 'Highly Eligible':
        return {
          bg: 'bg-green-100',
          text: 'text-green-700',
          border: 'border-green-300',
          icon: CheckCircle,
          iconColor: 'text-green-600'
        };
      case 'Eligible':
        return {
          bg: 'bg-blue-100',
          text: 'text-blue-700',
          border: 'border-blue-300',
          icon: CheckCircle,
          iconColor: 'text-blue-600'
        };
      case 'Not Eligible':
        return {
          bg: 'bg-red-100',
          text: 'text-red-700',
          border: 'border-red-300',
          icon: XCircle,
          iconColor: 'text-red-600'
        };
      default:
        return {
          bg: 'bg-gray-100',
          text: 'text-gray-700',
          border: 'border-gray-300',
          icon: AlertCircle,
          iconColor: 'text-gray-600'
        };
    }
  };

  const config = getBadgeConfig(level);
  const Icon = config.icon;

  return (
    <div className={`inline-flex items-center space-x-2 px-4 py-2 rounded-full border ${config.bg} ${config.text} ${config.border}`}>
      <Icon className={`w-4 h-4 ${config.iconColor}`} />
      <span className="font-medium text-sm">{level}</span>
    </div>
  );
};

export default EligibilityBadge;

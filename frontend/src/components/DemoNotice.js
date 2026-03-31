import React from 'react';
import { AlertCircle, Info } from 'lucide-react';

const DemoNotice = ({ 
  type = 'info', 
  title = 'Demo Application', 
  message = 'This is a demonstration application.',
  className = '',
  showIcon = true 
}) => {
  const getStyles = () => {
    switch (type) {
      case 'warning':
        return {
          container: 'bg-yellow-50 border-yellow-200 text-yellow-700',
          icon: 'text-yellow-500',
          IconComponent: AlertCircle
        };
      case 'error':
        return {
          container: 'bg-red-50 border-red-200 text-red-700',
          icon: 'text-red-500',
          IconComponent: AlertCircle
        };
      case 'success':
        return {
          container: 'bg-green-50 border-green-200 text-green-700',
          icon: 'text-green-500',
          IconComponent: Info
        };
      default:
        return {
          container: 'bg-blue-50 border-blue-200 text-blue-700',
          icon: 'text-blue-500',
          IconComponent: Info
        };
    }
  };

  const styles = getStyles();
  const { IconComponent } = styles;

  return (
    <div className={`border rounded-lg p-4 ${styles.container} ${className}`}>
      <div className="flex items-start">
        {showIcon && (
          <IconComponent className={`w-5 h-5 mt-0.5 mr-3 flex-shrink-0 ${styles.icon}`} />
        )}
        <div className="text-sm">
          <p className="font-medium mb-1">{title}</p>
          <p>{message}</p>
        </div>
      </div>
    </div>
  );
};

export default DemoNotice;
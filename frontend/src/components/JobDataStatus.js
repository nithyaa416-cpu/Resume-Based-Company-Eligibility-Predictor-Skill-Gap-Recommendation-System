import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  RefreshCw, 
  Database, 
  TrendingUp, 
  Clock, 
  Building2, 
  Briefcase,
  CheckCircle,
  AlertCircle,
  BarChart3
} from 'lucide-react';
import toast from 'react-hot-toast';

const JobDataStatus = () => {
  const [status, setStatus] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);

  useEffect(() => {
    loadJobDataInfo();
  }, []);

  const loadJobDataInfo = async () => {
    try {
      setLoading(true);
      
      // Load both status and stats
      const [statusResponse, statsResponse] = await Promise.all([
        fetch('/job-data/status'),
        fetch('/job-data/stats')
      ]);
      
      const statusData = await statusResponse.json();
      const statsData = await statsResponse.json();
      
      if (statusData.status === 'success') {
        setStatus(statusData.job_data_status);
      }
      
      if (statsData.status === 'success') {
        setStats(statsData.job_data_stats);
      }
      
    } catch (error) {
      toast.error('Error loading job data info: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleForceUpdate = async () => {
    try {
      setUpdating(true);
      toast.loading('Updating job data...', { id: 'job-update' });
      
      const response = await fetch('/job-data/update', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      const data = await response.json();
      
      if (data.status === 'success') {
        toast.success('Job data updated successfully!', { id: 'job-update' });
        
        // Show update results
        const results = data.update_results;
        if (results) {
          toast.success(
            `Updated: ${results.total_saved} new jobs from ${results.total_scraped} sources`,
            { duration: 5000 }
          );
        }
        
        // Reload data
        await loadJobDataInfo();
      } else {
        toast.error('Failed to update job data: ' + data.message, { id: 'job-update' });
      }
      
    } catch (error) {
      toast.error('Error updating job data: ' + error.message, { id: 'job-update' });
    } finally {
      setUpdating(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
          <span className="ml-3 text-gray-600">Loading job data info...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Status Card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
      >
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <Database className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Job Data Status</h3>
              <p className="text-sm text-gray-600">Real-time job market data</p>
            </div>
          </div>
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleForceUpdate}
            disabled={updating}
            className="btn-primary flex items-center space-x-2"
          >
            <RefreshCw className={`w-4 h-4 ${updating ? 'animate-spin' : ''}`} />
            <span>{updating ? 'Updating...' : 'Update Now'}</span>
          </motion.button>
        </div>

        {status && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
              <div className={`w-3 h-3 rounded-full ${
                status.is_running ? 'bg-green-500' : 'bg-yellow-500'
              }`}></div>
              <div>
                <div className="text-sm font-medium text-gray-900">
                  Scheduler Status
                </div>
                <div className="text-xs text-gray-600">
                  {status.is_running ? 'Active' : 'Inactive'}
                </div>
              </div>
            </div>
            
            <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
              <Clock className="w-4 h-4 text-gray-500" />
              <div>
                <div className="text-sm font-medium text-gray-900">
                  Last Update
                </div>
                <div className="text-xs text-gray-600">
                  {status.last_update ? 
                    new Date(status.last_update).toLocaleString() : 
                    'Never'
                  }
                </div>
              </div>
            </div>
          </div>
        )}
      </motion.div>

      {/* Statistics Card */}
      {stats && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
        >
          <div className="flex items-center space-x-3 mb-6">
            <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
              <BarChart3 className="w-5 h-5 text-green-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Database Statistics</h3>
              <p className="text-sm text-gray-600">Current job market data overview</p>
            </div>
          </div>

          {/* Key Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">
                {stats.total_companies || 0}
              </div>
              <div className="text-sm text-blue-700">Companies</div>
            </div>
            
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">
                {stats.total_positions || 0}
              </div>
              <div className="text-sm text-green-700">Job Positions</div>
            </div>
            
            <div className="text-center p-4 bg-purple-50 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">
                {stats.top_roles?.length || 0}
              </div>
              <div className="text-sm text-purple-700">Role Types</div>
            </div>
            
            <div className="text-center p-4 bg-orange-50 rounded-lg">
              <div className="text-2xl font-bold text-orange-600">
                {stats.top_skills?.length || 0}
              </div>
              <div className="text-sm text-orange-700">Skills Tracked</div>
            </div>
          </div>

          {/* Top Companies */}
          {stats.top_companies && stats.top_companies.length > 0 && (
            <div className="mb-6">
              <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
                <Building2 className="w-4 h-4 mr-2" />
                Top Companies by Positions
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {stats.top_companies.slice(0, 6).map((company, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <span className="font-medium text-gray-900">{company.company}</span>
                    <span className="text-sm text-gray-600">{company.positions} positions</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Top Roles */}
          {stats.top_roles && stats.top_roles.length > 0 && (
            <div className="mb-6">
              <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
                <Briefcase className="w-4 h-4 mr-2" />
                Most Common Roles
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {stats.top_roles.slice(0, 6).map((role, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <span className="font-medium text-gray-900">{role.role}</span>
                    <span className="text-sm text-gray-600">{role.count} openings</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Top Skills */}
          {stats.top_skills && stats.top_skills.length > 0 && (
            <div>
              <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
                <TrendingUp className="w-4 h-4 mr-2" />
                Most In-Demand Skills
              </h4>
              <div className="flex flex-wrap gap-2">
                {stats.top_skills.slice(0, 12).map((skill, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full font-medium"
                  >
                    {skill.skill} ({skill.count})
                  </span>
                ))}
              </div>
            </div>
          )}
        </motion.div>
      )}

      {/* Data Freshness Notice */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-gradient-to-r from-blue-50 to-green-50 border border-blue-200 rounded-xl p-4"
      >
        <div className="flex items-start space-x-3">
          <CheckCircle className="w-5 h-5 text-green-600 mt-0.5" />
          <div>
            <h4 className="font-medium text-gray-900 mb-1">Real-Time Market Data</h4>
            <p className="text-sm text-gray-600">
              Our job database is continuously updated with current market trends from top tech companies. 
              Data reflects actual hiring demands for 2024-2025, including AI/ML roles, modern tech stacks, 
              and emerging technologies.
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default JobDataStatus;
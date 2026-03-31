import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { GitCompare, Upload, ArrowRight } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import toast from 'react-hot-toast';

const Compare = () => {
  const [comparisons, setComparisons] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleAddComparison = async (file, label) => {
    if (!file) return;

    setIsLoading(true);
    
    try {
      const formData = new FormData();
      formData.append('resume', file);

      const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
      });

      const uploadData = await response.json();

      if (uploadData.status === 'success') {
        // Get analysis for all companies
        const analysisResponse = await fetch('/analyze-all', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            resume_text: uploadData.data.resume_text,
          }),
        });

        const analysisData = await analysisResponse.json();

        if (analysisData.status === 'success') {
          const newComparison = {
            id: Date.now(),
            label: label || `Resume ${comparisons.length + 1}`,
            uploadData: uploadData.data,
            analysisData: analysisData,
            timestamp: new Date().toISOString(),
          };

          setComparisons(prev => [...prev, newComparison]);
          toast.success(`${newComparison.label} added for comparison!`);
        } else {
          toast.error('Failed to analyze resume');
        }
      } else {
        toast.error('Failed to upload resume');
      }
    } catch (error) {
      toast.error('Error processing resume: ' + error.message);
    } finally {
      setIsLoading(false);
    }
  };

  const removeComparison = (id) => {
    setComparisons(prev => prev.filter(comp => comp.id !== id));
    toast.success('Comparison removed');
  };

  const getComparisonChartData = () => {
    if (comparisons.length === 0) return [];

    // Get top 10 companies that appear in all comparisons
    const allCompanies = new Set();
    comparisons.forEach(comp => {
      comp.analysisData.company_analysis?.forEach(ca => {
        allCompanies.add(ca.company);
      });
    });

    const topCompanies = Array.from(allCompanies).slice(0, 10);

    return topCompanies.map(company => {
      const dataPoint = { company };
      
      comparisons.forEach(comp => {
        const companyAnalysis = comp.analysisData.company_analysis?.find(ca => ca.company === company);
        dataPoint[comp.label] = companyAnalysis?.ml_analysis?.ml_eligibility_score || 0;
      });

      return dataPoint;
    });
  };

  const getRadarChartData = () => {
    if (comparisons.length === 0) return [];

    const skillCategories = ['Programming', 'Web Technologies', 'Databases', 'Cloud', 'DevOps', 'AI/ML'];
    
    return skillCategories.map(category => {
      const dataPoint = { category };
      
      comparisons.forEach(comp => {
        // This would need to be calculated based on actual skill categorization
        // For now, using mock data
        dataPoint[comp.label] = Math.floor(Math.random() * 100);
      });

      return dataPoint;
    });
  };

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center"
      >
        <div className="flex justify-center mb-6">
          <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-600 rounded-2xl flex items-center justify-center">
            <GitCompare className="w-8 h-8 text-white" />
          </div>
        </div>
        
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Resume Comparison</h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Compare multiple versions of your resume to see which performs better across different companies
        </p>
      </motion.div>

      {/* Upload Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="card"
      >
        <h2 className="text-xl font-bold text-gray-900 mb-6">Add Resume for Comparison</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Resume Label
            </label>
            <input
              type="text"
              placeholder="e.g., Current Resume, Updated Resume"
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              id="resumeLabel"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Upload Resume
            </label>
            <input
              type="file"
              accept=".pdf,.docx,.doc"
              onChange={(e) => {
                const file = e.target.files[0];
                const label = document.getElementById('resumeLabel').value;
                if (file) {
                  handleAddComparison(file, label);
                }
              }}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              disabled={isLoading}
            />
          </div>
        </div>

        {isLoading && (
          <div className="mt-4 flex items-center justify-center py-4">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-purple-500 mr-3"></div>
            <span className="text-gray-600">Processing resume...</span>
          </div>
        )}
      </motion.div>

      {/* Comparison Results */}
      {comparisons.length > 0 && (
        <>
          {/* Summary Cards */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="grid grid-cols-1 md:grid-cols-3 gap-6"
          >
            {comparisons.map((comp, index) => (
              <div key={comp.id} className="card relative">
                <button
                  onClick={() => removeComparison(comp.id)}
                  className="absolute top-4 right-4 text-gray-400 hover:text-red-500"
                >
                  ×
                </button>
                
                <h3 className="font-semibold text-gray-900 mb-4">{comp.label}</h3>
                
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Skills Found</span>
                    <span className="font-medium">{comp.uploadData.skills_found}</span>
                  </div>
                  
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Companies Analyzed</span>
                    <span className="font-medium">{comp.analysisData.total_companies}</span>
                  </div>
                  
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Avg Score</span>
                    <span className="font-medium">
                      {Math.round(
                        comp.analysisData.company_analysis?.reduce((sum, ca) => 
                          sum + (ca.ml_analysis?.ml_eligibility_score || 0), 0
                        ) / (comp.analysisData.company_analysis?.length || 1)
                      )}%
                    </span>
                  </div>
                  
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Top Match</span>
                    <span className="font-medium text-green-600">
                      {comp.analysisData.company_analysis?.[0]?.company || 'N/A'}
                    </span>
                  </div>
                </div>
                
                <div className="mt-4 text-xs text-gray-500">
                  Added: {new Date(comp.timestamp).toLocaleDateString()}
                </div>
              </div>
            ))}
          </motion.div>

          {/* Comparison Charts */}
          {comparisons.length >= 2 && (
            <>
              {/* Bar Chart Comparison */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.3 }}
                className="card"
              >
                <h3 className="text-xl font-bold text-gray-900 mb-6">Company Score Comparison</h3>
                
                <div className="h-96">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={getComparisonChartData()}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="company" angle={-45} textAnchor="end" height={100} />
                      <YAxis />
                      <Tooltip />
                      {comparisons.map((comp, index) => (
                        <Bar 
                          key={comp.id}
                          dataKey={comp.label} 
                          fill={`hsl(${index * 120}, 70%, 50%)`}
                        />
                      ))}
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </motion.div>

              {/* Radar Chart */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.4 }}
                className="card"
              >
                <h3 className="text-xl font-bold text-gray-900 mb-6">Skill Category Comparison</h3>
                
                <div className="h-96">
                  <ResponsiveContainer width="100%" height="100%">
                    <RadarChart data={getRadarChartData()}>
                      <PolarGrid />
                      <PolarAngleAxis dataKey="category" />
                      <PolarRadiusAxis angle={90} domain={[0, 100]} />
                      {comparisons.map((comp, index) => (
                        <Radar
                          key={comp.id}
                          name={comp.label}
                          dataKey={comp.label}
                          stroke={`hsl(${index * 120}, 70%, 50%)`}
                          fill={`hsl(${index * 120}, 70%, 50%)`}
                          fillOpacity={0.1}
                        />
                      ))}
                      <Tooltip />
                    </RadarChart>
                  </ResponsiveContainer>
                </div>
              </motion.div>

              {/* Insights */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.5 }}
                className="card"
              >
                <h3 className="text-xl font-bold text-gray-900 mb-6">Comparison Insights</h3>
                
                <div className="space-y-4">
                  {comparisons.length >= 2 && (
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <h4 className="font-medium text-blue-900 mb-2">📊 Performance Analysis</h4>
                      <p className="text-blue-800 text-sm">
                        {comparisons[0].label} vs {comparisons[1].label}: 
                        {Math.round(
                          comparisons[0].analysisData.company_analysis?.reduce((sum, ca) => 
                            sum + (ca.ml_analysis?.ml_eligibility_score || 0), 0
                          ) / (comparisons[0].analysisData.company_analysis?.length || 1)
                        ) > Math.round(
                          comparisons[1].analysisData.company_analysis?.reduce((sum, ca) => 
                            sum + (ca.ml_analysis?.ml_eligibility_score || 0), 0
                          ) / (comparisons[1].analysisData.company_analysis?.length || 1)
                        ) ? ` ${comparisons[0].label} performs better overall` : ` ${comparisons[1].label} performs better overall`}
                      </p>
                    </div>
                  )}
                  
                  <div className="bg-green-50 p-4 rounded-lg">
                    <h4 className="font-medium text-green-900 mb-2">💡 Recommendations</h4>
                    <ul className="text-green-800 text-sm space-y-1">
                      <li>• Focus on the resume version with higher average scores</li>
                      <li>• Identify which specific skills or experiences make the difference</li>
                      <li>• Consider combining the best elements from both versions</li>
                      <li>• Test different versions for different types of companies</li>
                    </ul>
                  </div>
                </div>
              </motion.div>
            </>
          )}
        </>
      )}

      {/* Empty State */}
      {comparisons.length === 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="text-center py-12"
        >
          <Upload className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Comparisons Yet</h3>
          <p className="text-gray-600 mb-6">
            Upload at least two resume versions to start comparing their performance
          </p>
          
          <div className="bg-gray-50 p-6 rounded-lg max-w-2xl mx-auto">
            <h4 className="font-medium text-gray-900 mb-3">How Resume Comparison Works:</h4>
            <div className="space-y-2 text-sm text-gray-600 text-left">
              <div className="flex items-center">
                <ArrowRight className="w-4 h-4 mr-2 text-purple-500" />
                Upload multiple versions of your resume
              </div>
              <div className="flex items-center">
                <ArrowRight className="w-4 h-4 mr-2 text-purple-500" />
                Each resume is analyzed against all companies using AI
              </div>
              <div className="flex items-center">
                <ArrowRight className="w-4 h-4 mr-2 text-purple-500" />
                Compare scores, skill matches, and performance metrics
              </div>
              <div className="flex items-center">
                <ArrowRight className="w-4 h-4 mr-2 text-purple-500" />
                Get insights on which version performs better
              </div>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default Compare;
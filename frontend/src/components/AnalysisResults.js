import React from 'react';
import { motion } from 'framer-motion';
import { 
  TrendingUp, 
  Brain, 
  Target, 
  BookOpen, 
  Clock, 
  Award,
  ChevronRight,
  ExternalLink
} from 'lucide-react';

const AnalysisResults = ({ results, type = 'single' }) => {
  if (!results) return null;

  const getEligibilityColor = (level) => {
    switch (level) {
      case 'Highly Eligible': return 'text-green-600 bg-green-50 border-green-200';
      case 'Eligible': return 'text-blue-600 bg-blue-50 border-blue-200';
      case 'Not Eligible': return 'text-red-600 bg-red-50 border-red-200';
      default: return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const getScoreColor = (score) => {
    if (score >= 85) return 'from-green-500 to-green-600';
    if (score >= 70) return 'from-blue-500 to-blue-600';
    return 'from-red-500 to-red-600';
    return 'from-red-500 to-red-600';
  };

  if (type === 'multiple') {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="space-y-6"
      >
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <div className="flex items-center space-x-2">
            <Brain className="w-5 h-5 text-green-600" />
            <span className="font-medium text-green-800">
              🤖 Resume Analysis Complete! Analyzed {results.total_companies} companies.
            </span>
          </div>
        </div>

        <div className="space-y-4">
          <h3 className="text-xl font-bold text-gray-900 flex items-center">
            <TrendingUp className="w-6 h-6 mr-2 text-blue-500" />
            Best Matching Companies
          </h3>
          <p className="text-gray-600">
            These companies match your resume and skills the best.
          </p>

          {results.company_analysis?.map((result, index) => {
            const analysis = result.ml_analysis;
            const score = analysis?.ml_eligibility_score || 0;
            
            return (
              <motion.div
                key={`${result.company}-${result.role || 'default'}`}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
                className="card hover:shadow-lg transition-all duration-300"
              >
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-bold">
                      {index + 1}
                    </div>
                    <div>
                      <h4 className="text-lg font-semibold text-gray-900">{result.company}</h4>
                      {result.role && (
                        <p className="text-sm text-gray-600">{result.role}</p>
                      )}
                    </div>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium border ${getEligibilityColor(analysis?.eligibility_level)}`}>
                    {analysis?.eligibility_level}
                  </span>
                </div>

                <div className="space-y-4">
                  {/* Score Bar */}
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm font-medium text-gray-700">Overall Match Score</span>
                      <span className="text-sm font-bold text-gray-900">{score}%</span>
                    </div>
                    <div className="progress-bar">
                      <div 
                        className={`progress-fill bg-gradient-to-r ${getScoreColor(score)}`}
                        style={{ width: `${score}%` }}
                      ></div>
                    </div>
                  </div>

                  {/* Processing Info */}
                  {analysis?.processing_info && (
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div className="bg-purple-50 p-3 rounded-lg">
                        <span className="text-purple-600 font-medium">🔬 Profile Match: {analysis.processing_info.semantic_component}%</span>
                      </div>
                      <div className="bg-blue-50 p-3 rounded-lg">
                        <span className="text-blue-600 font-medium">📊 Skills Match: {analysis.processing_info.skill_component}%</span>
                      </div>
                    </div>
                  )}

                  {/* Skills You May Need Preview */}
                  {analysis?.skill_readiness_levels?.Missing?.length > 0 && (
                    <div className="bg-red-50 p-3 rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium text-red-800">Skills You May Need ({analysis.skill_readiness_levels.Missing.length})</span>
                      </div>
                      <div className="flex flex-wrap gap-1">
                        {analysis.skill_readiness_levels.Missing.slice(0, 5).map((skill, idx) => (
                          <span key={idx} className="skill-tag skill-tag-missing text-xs">
                            {skill.skill}
                          </span>
                        ))}
                        {analysis.skill_readiness_levels.Missing.length > 5 && (
                          <span className="text-xs text-gray-500">+{analysis.skill_readiness_levels.Missing.length - 5} more</span>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              </motion.div>
            );
          })}
        </div>
      </motion.div>
    );
  }

  // Single company analysis
  const analysis = results.ml_analysis;
  if (!analysis) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-6"
    >
      {/* Header */}
      <div className="bg-green-50 border border-green-200 rounded-lg p-4">
        <div className="flex items-center space-x-2">
          <Brain className="w-5 h-5 text-green-600" />
          <span className="font-medium text-green-800">
            🤖 Resume Analysis Complete for {results.company}!
          </span>
        </div>
        <p className="text-sm text-green-700 mt-1">
          Advanced analysis of your resume and profile compatibility
        </p>
      </div>

      {/* Main Score Card */}
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-2xl font-bold text-gray-900">{results.company}</h3>
            <p className="text-gray-600">{analysis.role}</p>
          </div>
          <span className={`px-4 py-2 rounded-full text-lg font-medium border ${getEligibilityColor(analysis.eligibility_level)}`}>
            {analysis.eligibility_level}
          </span>
        </div>

        <div className="space-y-6">
          {/* Overall Match Score */}
          <div>
            <div className="flex justify-between items-center mb-3">
              <span className="text-lg font-semibold text-gray-900">🤖 Overall Match Score</span>
              <span className="text-2xl font-bold text-gray-900">{analysis.ml_eligibility_score}%</span>
            </div>
            <div className="progress-bar h-4">
              <div 
                className={`progress-fill bg-gradient-to-r ${getScoreColor(analysis.ml_eligibility_score)}`}
                style={{ width: `${analysis.ml_eligibility_score}%` }}
              ></div>
            </div>
          </div>

          {/* Match Breakdown */}
          {analysis.processing_info && (
            <div className="bg-blue-50 p-6 rounded-lg">
              <h4 className="font-semibold text-blue-900 mb-4 flex items-center">
                <Brain className="w-5 h-5 mr-2" />
                Match Breakdown
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-white p-4 rounded-lg">
                  <div className="text-purple-600 font-medium">🔬 Profile Match</div>
                  <div className="text-2xl font-bold text-purple-700">{analysis.processing_info.semantic_component}%</div>
                  <div className="text-sm text-gray-600">How well your profile fits the role</div>
                </div>
                <div className="bg-white p-4 rounded-lg">
                  <div className="text-blue-600 font-medium">📊 Skills Match</div>
                  <div className="text-2xl font-bold text-blue-700">{analysis.processing_info.skill_component}%</div>
                  <div className="text-sm text-gray-600">Skills alignment with requirements</div>
                </div>
              </div>
              <div className="mt-4 text-sm text-gray-600">
                <span className="font-medium">🎯 Skills Analyzed:</span> {analysis.processing_info.total_skills_analyzed} | 
                <span className="font-medium ml-2">🔗 Semantic Matches:</span> {analysis.processing_info.semantic_matches_found}
              </div>
            </div>
          )}

          {/* Profile Compatibility */}
          {analysis.semantic_analysis && (
            <div className="bg-purple-50 p-6 rounded-lg">
              <h4 className="font-semibold text-purple-900 mb-4 flex items-center">
                <Target className="w-5 h-5 mr-2" />
                Profile Compatibility
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <div className="flex justify-between items-center mb-2">
                    <span className="font-medium text-purple-800">Overall Similarity</span>
                    <span className="font-bold text-purple-900">{(analysis.semantic_analysis.overall_similarity * 100).toFixed(1)}%</span>
                  </div>
                  <div className="progress-bar">
                    <div 
                      className="progress-fill bg-gradient-to-r from-purple-500 to-pink-500"
                      style={{ width: `${analysis.semantic_analysis.overall_similarity * 100}%` }}
                    ></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between items-center mb-2">
                    <span className="font-medium text-purple-800">Contextual Match</span>
                    <span className="font-bold text-purple-900">{(analysis.semantic_analysis.contextual_match * 100).toFixed(1)}%</span>
                  </div>
                  <div className="progress-bar">
                    <div 
                      className="progress-fill bg-gradient-to-r from-indigo-500 to-blue-500"
                      style={{ width: `${analysis.semantic_analysis.contextual_match * 100}%` }}
                    ></div>
                  </div>
                </div>
              </div>
              <p className="text-sm text-purple-700 mt-3">
                Advanced analysis of how your experience aligns with the role
              </p>
            </div>
          )}

          {/* Resume Insights */}
          {analysis.ml_explanation && (
            <div className="bg-orange-50 p-6 rounded-lg">
              <h4 className="font-semibold text-orange-900 mb-4 flex items-center">
                <Brain className="w-5 h-5 mr-2" />
                Resume Insights
              </h4>
              <p className="text-orange-800 font-medium mb-4">{analysis.ml_explanation.summary}</p>
              
              {analysis.ml_explanation.ml_insights?.length > 0 && (
                <div className="mb-4">
                  <h5 className="font-medium text-orange-800 mb-2">🔬 Key Insights:</h5>
                  <ul className="space-y-1">
                    {analysis.ml_explanation.ml_insights.map((insight, idx) => (
                      <li key={idx} className="text-orange-700 flex items-start">
                        <ChevronRight className="w-4 h-4 mr-1 mt-0.5 flex-shrink-0" />
                        {insight}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              
              {analysis.ml_explanation.semantic_insights?.length > 0 && (
                <div className="mb-4">
                  <h5 className="font-medium text-orange-800 mb-2">🧠 Profile Insights:</h5>
                  <ul className="space-y-1">
                    {analysis.ml_explanation.semantic_insights.map((insight, idx) => (
                      <li key={idx} className="text-orange-700 flex items-start">
                        <ChevronRight className="w-4 h-4 mr-1 mt-0.5 flex-shrink-0" />
                        {insight}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              
              <div className="bg-orange-100 p-3 rounded-lg">
                <span className="font-medium text-orange-800">🎯 Confidence Level: </span>
                <span className="font-bold text-orange-900">{analysis.ml_explanation.confidence_level?.toUpperCase() || 'MEDIUM'}</span>
              </div>
            </div>
          )}

          {/* Skills Analysis */}
          {analysis.skill_readiness_levels && (
            <div className="space-y-4">
              <h4 className="font-semibold text-gray-900 flex items-center">
                <Award className="w-5 h-5 mr-2" />
                Skill Readiness Analysis
              </h4>
              
              {Object.entries(analysis.skill_readiness_levels).map(([level, skills]) => {
                if (!skills || skills.length === 0) return null;
                
                const levelConfig = {
                  'Advanced': { emoji: '🟢', color: 'green' },
                  'Intermediate': { emoji: '🟡', color: 'yellow' },
                  'Beginner': { emoji: '🟠', color: 'orange' },
                  'Missing': { emoji: '🔴', color: 'red' }
                };
                
                const config = levelConfig[level] || { emoji: '⚪', color: 'gray' };
                
                return (
                  <div key={level} className={`bg-${config.color}-50 p-4 rounded-lg`}>
                    <h5 className={`font-medium text-${config.color}-800 mb-3`}>
                      {config.emoji} {level} Skills ({skills.length})
                    </h5>
                    <div className="flex flex-wrap gap-2">
                      {skills.slice(0, 10).map((skill, idx) => (
                        <span 
                          key={idx} 
                          className={`skill-tag skill-tag-${level.toLowerCase()}`}
                          title={`${skill.mentions || 0} mentions`}
                        >
                          {skill.skill}
                        </span>
                      ))}
                      {skills.length > 10 && (
                        <span className="text-sm text-gray-500">+{skills.length - 10} more</span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          {/* Learning Roadmap */}
          {analysis.learning_roadmap?.learning_path?.length > 0 && (
            <div className="bg-green-50 p-6 rounded-lg">
              <h4 className="font-semibold text-green-900 mb-4 flex items-center">
                <BookOpen className="w-5 h-5 mr-2" />
                Personalized Learning Roadmap
              </h4>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div className="bg-white p-3 rounded-lg">
                  <span className="text-green-600 font-medium">Total Skills to Learn</span>
                  <div className="text-xl font-bold text-green-800">{analysis.learning_roadmap.total_skills}</div>
                </div>
                <div className="bg-white p-3 rounded-lg">
                  <span className="text-green-600 font-medium flex items-center">
                    <Clock className="w-4 h-4 mr-1" />
                    Estimated Duration
                  </span>
                  <div className="text-xl font-bold text-green-800">{analysis.learning_roadmap.estimated_duration}</div>
                </div>
              </div>
              
              <div className="space-y-3">
                {analysis.learning_roadmap.learning_path.map((phase, idx) => (
                  <div key={idx} className="bg-white p-4 rounded-lg border-l-4 border-green-500">
                    <div className="flex justify-between items-start mb-2">
                      <h5 className="font-semibold text-green-900">Phase {phase.phase}: {phase.title}</h5>
                      <span className="text-sm text-green-600 bg-green-100 px-2 py-1 rounded">{phase.estimated_time}</span>
                    </div>
                    <p className="text-green-700 text-sm mb-3">{phase.description}</p>
                    <div className="flex flex-wrap gap-1">
                      {phase.skills.map((skill, skillIdx) => (
                        <span key={skillIdx} className="bg-green-500 text-white text-xs px-2 py-1 rounded-full">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Learning Recommendations */}
          {analysis.learning_recommendations && Object.keys(analysis.learning_recommendations).length > 0 && (
            <div className="bg-yellow-50 p-6 rounded-lg">
              <h4 className="font-semibold text-yellow-900 mb-4 flex items-center">
                <ExternalLink className="w-5 h-5 mr-2" />
                Learning Recommendations
              </h4>
              
              <div className="space-y-4">
                {Object.entries(analysis.learning_recommendations).slice(0, 3).map(([skill, platforms]) => (
                  <div key={skill} className="bg-white p-4 rounded-lg border-l-4 border-yellow-500">
                    <h5 className="font-semibold text-yellow-900 mb-3">📚 {skill.charAt(0).toUpperCase() + skill.slice(1)}</h5>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      <div>
                        <span className="text-sm font-medium text-yellow-800">🆓 Free Resources:</span>
                        <div className="text-sm text-yellow-700 mt-1">
                          {platforms.free?.slice(0, 3).join(', ') || 'N/A'}
                        </div>
                      </div>
                      <div>
                        <span className="text-sm font-medium text-yellow-800">💰 Paid Resources:</span>
                        <div className="text-sm text-yellow-700 mt-1">
                          {platforms.paid?.slice(0, 3).join(', ') || 'N/A'}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
                
                {Object.keys(analysis.learning_recommendations).length > 3 && (
                  <p className="text-center text-yellow-700">
                    ... and recommendations for {Object.keys(analysis.learning_recommendations).length - 3} more skills
                  </p>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default AnalysisResults;
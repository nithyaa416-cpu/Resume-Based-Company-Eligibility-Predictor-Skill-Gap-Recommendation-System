import React from 'react';
import { motion } from 'framer-motion';
import { GraduationCap, TrendingUp } from 'lucide-react';
import SkillRoadmapCard from './SkillRoadmapCard';

const ImprovedRoadmapSection = ({ analysis, company }) => {
  const learningRecommendations = analysis?.learning_recommendations || {};
  const learningRoadmap = analysis?.learning_roadmap?.learning_path || [];

  // Group resources by skill (eliminate duplicates)
  const organizeResourcesBySkill = () => {
    const skillsMap = {};

    Object.entries(learningRecommendations).forEach(([skill, platforms]) => {
      if (!skillsMap[skill]) {
        skillsMap[skill] = {
          skill,
          freeResources: [],
          paidResources: []
        };
      }

      // Add free resources with URLs
      if (platforms.free && platforms.free.length > 0) {
        platforms.free.forEach(platform => {
          skillsMap[skill].freeResources.push({
            platform,
            url: generateLearningUrl(skill, platform),
            duration: null
          });
        });
      }

      // Add paid resources with URLs
      if (platforms.paid && platforms.paid.length > 0) {
        platforms.paid.forEach(platform => {
          skillsMap[skill].paidResources.push({
            platform,
            url: generateLearningUrl(skill, platform),
            duration: null
          });
        });
      }
    });

    return Object.values(skillsMap);
  };

  // Generate learning URLs for different platforms
  const generateLearningUrl = (skill, platform) => {
    const encodedSkill = encodeURIComponent(skill);
    
    const platformUrls = {
      'Coursera': `https://www.coursera.org/search?query=${encodedSkill}`,
      'Udemy': `https://www.udemy.com/courses/search/?q=${encodedSkill}`,
      'YouTube': `https://www.youtube.com/results?search_query=${encodedSkill}+tutorial`,
      'FreeCodeCamp': `https://www.freecodecamp.org/news/search/?query=${encodedSkill}`,
      'LinkedIn Learning': `https://www.linkedin.com/learning/search?keywords=${encodedSkill}`,
      'Pluralsight': `https://www.pluralsight.com/search?q=${encodedSkill}`,
      'edX': `https://www.edx.org/search?q=${encodedSkill}`,
      'Khan Academy': `https://www.khanacademy.org/search?page_search_query=${encodedSkill}`,
      'GeeksforGeeks': `https://www.geeksforgeeks.org/${encodedSkill.toLowerCase().replace(/\s+/g, '-')}/`,
      'W3Schools': `https://www.w3schools.com/${encodedSkill.toLowerCase().replace(/\s+/g, '')}/`,
      'MDN Web Docs': `https://developer.mozilla.org/en-US/search?q=${encodedSkill}`,
      'Official Documentation': `https://www.google.com/search?q=${encodedSkill}+official+documentation`,
      'Codecademy': `https://www.codecademy.com/search?query=${encodedSkill}`,
      'DataCamp': `https://www.datacamp.com/search?q=${encodedSkill}`,
      'Udacity': `https://www.udacity.com/courses/all?search=${encodedSkill}`
    };

    return platformUrls[platform] || `https://www.google.com/search?q=learn+${encodedSkill}`;
  };

  const skillsWithResources = organizeResourcesBySkill();

  if (skillsWithResources.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="mt-6 p-6 bg-gray-50 rounded-lg text-center"
      >
        <p className="text-gray-600">No learning recommendations available</p>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="mt-6 space-y-6"
    >
      {/* Roadmap Header */}
      <div className="bg-gradient-to-r from-indigo-500 to-purple-600 p-6 rounded-xl text-white shadow-lg">
        <div className="flex items-center space-x-3 mb-3">
          <div className="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center">
            <GraduationCap className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-2xl font-bold">Learning Roadmap</h3>
            <p className="text-indigo-100">
              Master these {skillsWithResources.length} skills to qualify for {company}
            </p>
          </div>
        </div>
      </div>

      {/* Learning Path Overview */}
      {learningRoadmap.length > 0 && (
        <div className="bg-white p-6 rounded-xl border-2 border-gray-200 shadow-sm">
          <div className="flex items-center space-x-2 mb-4">
            <TrendingUp className="w-5 h-5 text-blue-600" />
            <h4 className="text-lg font-bold text-gray-900">Recommended Learning Path</h4>
          </div>
          <div className="space-y-3">
            {learningRoadmap.map((phase, idx) => (
              <div key={idx} className="flex items-start space-x-3 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-200">
                <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 text-white rounded-full flex items-center justify-center font-bold text-sm shadow-md">
                  {phase.phase}
                </div>
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-1">
                    <h5 className="font-semibold text-gray-900">{phase.title}</h5>
                    <span className="text-xs text-blue-700 bg-blue-100 px-3 py-1 rounded-full font-medium">
                      {phase.estimated_time}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">{phase.description}</p>
                  <div className="flex flex-wrap gap-1">
                    {phase.skills && phase.skills.map((skill, skillIdx) => (
                      <span key={skillIdx} className="text-xs bg-white text-gray-700 px-2 py-1 rounded border border-gray-200">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Skill Cards */}
      <div>
        <h4 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
          <span className="mr-2">📚</span>
          Skills & Learning Resources
        </h4>
        <div className="grid grid-cols-1 gap-4">
          {skillsWithResources.map((skillData, index) => (
            <SkillRoadmapCard
              key={skillData.skill}
              skill={skillData.skill}
              freeResources={skillData.freeResources}
              paidResources={skillData.paidResources}
              index={index}
            />
          ))}
        </div>
      </div>

      {/* Learning Tips */}
      <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-xl border-2 border-purple-200">
        <h4 className="font-bold text-gray-900 mb-3">💡 Learning Tips</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
          <div className="flex items-start space-x-2">
            <span className="text-purple-600 font-bold">1.</span>
            <p className="text-gray-700">Start with free resources to understand basics</p>
          </div>
          <div className="flex items-start space-x-2">
            <span className="text-purple-600 font-bold">2.</span>
            <p className="text-gray-700">Invest in paid courses for structured learning & certificates</p>
          </div>
          <div className="flex items-start space-x-2">
            <span className="text-purple-600 font-bold">3.</span>
            <p className="text-gray-700">Build projects while learning to gain practical experience</p>
          </div>
          <div className="flex items-start space-x-2">
            <span className="text-purple-600 font-bold">4.</span>
            <p className="text-gray-700">Follow the recommended learning path for best results</p>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default ImprovedRoadmapSection;

import React from 'react';
import { motion } from 'framer-motion';
import ThemeToggle from './ThemeToggle';
import { useTheme } from '../contexts/ThemeContext';

const ThemeToggleDemo = () => {
  const { isDark } = useTheme();

  return (
    <div className={`min-h-screen transition-all duration-500 ${
      isDark ? 'bg-[#0A0F29]' : 'bg-white'
    }`}>
      <div className="container mx-auto px-6 py-20">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h1 className={`text-5xl font-bold mb-4 ${
            isDark 
              ? 'bg-gradient-to-r from-[#F8FAFC] to-[#A8B2D1] bg-clip-text text-transparent' 
              : 'text-[#0A0F29]'
          }`}>
            Dual Palette Theme Toggle
          </h1>
          <p className={`text-xl ${isDark ? 'text-[#A8B2D1]' : 'text-[#555]'}`}>
            Neon AI theme for dark mode • Soft tech colors for light mode
          </p>
          
          {/* Color Palette Display */}
          <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className={`p-6 rounded-2xl border ${
                isDark 
                  ? 'bg-white/5 backdrop-blur-sm border-white/12' 
                  : 'bg-[#F2F4F7] border-[#E0E4EC]'
              }`}
            >
              <h3 className={`text-lg font-semibold mb-4 ${
                isDark ? 'text-[#F8FAFC]' : 'text-[#0A0F29]'
              }`}>
                Dark Mode - Neon AI Theme
              </h3>
              <div className="grid grid-cols-3 gap-3">
                <div className="text-center">
                  <div className="w-12 h-12 bg-[#00E0FF] rounded-lg mx-auto mb-2 shadow-lg shadow-[#00E0FF]/30"></div>
                  <span className={`text-xs ${isDark ? 'text-[#A8B2D1]' : 'text-[#555]'}`}>Neon Cyan</span>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-[#33F1FF] rounded-lg mx-auto mb-2 shadow-lg shadow-[#33F1FF]/30"></div>
                  <span className={`text-xs ${isDark ? 'text-[#A8B2D1]' : 'text-[#555]'}`}>Neon Glow</span>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-[#4C5FFF] rounded-lg mx-auto mb-2 shadow-lg shadow-[#4C5FFF]/30"></div>
                  <span className={`text-xs ${isDark ? 'text-[#A8B2D1]' : 'text-[#555]'}`}>Indigo</span>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className={`p-6 rounded-2xl border ${
                isDark 
                  ? 'bg-white/5 backdrop-blur-sm border-white/12' 
                  : 'bg-[#F2F4F7] border-[#E0E4EC]'
              }`}
            >
              <h3 className={`text-lg font-semibold mb-4 ${
                isDark ? 'text-[#F8FAFC]' : 'text-[#0A0F29]'
              }`}>
                Light Mode - Soft Tech Theme
              </h3>
              <div className="grid grid-cols-3 gap-3">
                <div className="text-center">
                  <div className="w-12 h-12 bg-[#2BB8CC] rounded-lg mx-auto mb-2 shadow-sm"></div>
                  <span className={`text-xs ${isDark ? 'text-[#A8B2D1]' : 'text-[#555]'}`}>Soft Cyan</span>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-[#5A6FFF] rounded-lg mx-auto mb-2 shadow-sm"></div>
                  <span className={`text-xs ${isDark ? 'text-[#A8B2D1]' : 'text-[#555]'}`}>Soft Indigo</span>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-[#F2F4F7] border-2 border-[#E0E4EC] rounded-lg mx-auto mb-2"></div>
                  <span className={`text-xs ${isDark ? 'text-[#A8B2D1]' : 'text-[#555]'}`}>Card BG</span>
                </div>
              </div>
            </motion.div>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          
          {/* Default Toggle */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className={`p-8 rounded-2xl border transition-all duration-500 ${
              isDark 
                ? 'bg-white/5 backdrop-blur-sm border-white/12' 
                : 'bg-[#F2F4F7] border-[#E0E4EC] shadow-black/7'
            }`}
          >
            <h3 className={`text-xl font-semibold mb-4 ${
              isDark ? 'text-[#F8FAFC]' : 'text-[#0A0F29]'
            }`}>
              Default Toggle
            </h3>
            <p className={`text-sm mb-6 ${
              isDark ? 'text-[#A8B2D1]' : 'text-[#555]'
            }`}>
              Futuristic glassmorphism with dual palette system
            </p>
            <div className="flex justify-center">
              <ThemeToggle variant="default" showLabel={true} />
            </div>
          </motion.div>

          {/* Circular Toggle */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className={`p-8 rounded-2xl border transition-all duration-500 ${
              isDark 
                ? 'bg-white/5 backdrop-blur-sm border-white/12' 
                : 'bg-[#F2F4F7] border-[#E0E4EC] shadow-black/7'
            }`}
          >
            <h3 className={`text-xl font-semibold mb-4 ${
              isDark ? 'text-[#F8FAFC]' : 'text-[#0A0F29]'
            }`}>
              Circular Toggle
            </h3>
            <p className={`text-sm mb-6 ${
              isDark ? 'text-[#A8B2D1]' : 'text-[#555]'
            }`}>
              Circular design with rotating animations and adaptive colors
            </p>
            <div className="flex justify-center">
              <ThemeToggle variant="circular" />
            </div>
          </motion.div>

          {/* Minimal Toggle */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className={`p-8 rounded-2xl border transition-all duration-500 ${
              isDark 
                ? 'bg-white/5 backdrop-blur-sm border-white/12' 
                : 'bg-[#F2F4F7] border-[#E0E4EC] shadow-black/7'
            }`}
          >
            <h3 className={`text-xl font-semibold mb-4 ${
              isDark ? 'text-[#F8FAFC]' : 'text-[#0A0F29]'
            }`}>
              Minimal Toggle
            </h3>
            <p className={`text-sm mb-6 ${
              isDark ? 'text-[#A8B2D1]' : 'text-[#555]'
            }`}>
              Clean, minimal design with soft colors in light mode
            </p>
            <div className="flex justify-center">
              <ThemeToggle variant="minimal" />
            </div>
          </motion.div>

          {/* Settings Panel */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="md:col-span-2 lg:col-span-3"
          >
            <h3 className={`text-xl font-semibold mb-4 text-center ${
              isDark ? 'text-[#F8FAFC]' : 'text-[#0A0F29]'
            }`}>
              Settings Panel Toggle
            </h3>
            <div className="flex justify-center">
              <ThemeToggle variant="settings" />
            </div>
          </motion.div>

          {/* Navbar Integration Preview */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.5 }}
            className="md:col-span-2 lg:col-span-3"
          >
            <h3 className={`text-xl font-semibold mb-4 text-center ${
              isDark ? 'text-[#F8FAFC]' : 'text-[#0A0F29]'
            }`}>
              Navbar Integration
            </h3>
            <div className={`rounded-2xl border overflow-hidden transition-all duration-500 ${
              isDark 
                ? 'bg-white/5 backdrop-blur-sm border-white/12' 
                : 'bg-[#F2F4F7] border-[#E0E4EC] shadow-black/7'
            }`}>
              <nav className={`backdrop-blur-xl border-b transition-all duration-500 ${
                isDark 
                  ? 'bg-white/5 border-white/12' 
                  : 'bg-white/80 border-[#E0E4EC]'
              }`}>
                <div className="px-6 py-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                        isDark 
                          ? 'bg-gradient-to-r from-[#00E0FF] to-[#4C5FFF]' 
                          : 'bg-gradient-to-r from-[#2BB8CC] to-[#5A6FFF]'
                      }`}>
                        <span className="text-white font-bold">AI</span>
                      </div>
                      <div>
                        <span className={`text-xl font-bold ${
                          isDark ? 'text-[#F8FAFC]' : 'text-[#0A0F29]'
                        }`}>
                          Resume Analyzer
                        </span>
                        <div className={`text-xs ${
                          isDark ? 'text-[#A8B2D1]' : 'text-[#555]'
                        }`}>Smart Career Matching</div>
                      </div>
                    </div>

                    <div className="flex items-center space-x-6">
                      <span className={`${isDark ? 'text-[#A8B2D1]' : 'text-[#555]'}`}>
                        About
                      </span>
                      <span className={`${isDark ? 'text-[#A8B2D1]' : 'text-[#555]'}`}>
                        Features
                      </span>
                      <ThemeToggle variant="default" size="sm" />
                      <button className={`px-4 py-2 rounded-lg font-semibold transition-all duration-300 ${
                        isDark 
                          ? 'bg-gradient-to-r from-[#00E0FF] to-[#33F1FF] text-[#0A0F29] shadow-lg shadow-[#00E0FF]/25' 
                          : 'bg-gradient-to-r from-[#2BB8CC] to-[#5A6FFF] text-white shadow-sm'
                      }`}>
                        Get Started
                      </button>
                    </div>
                  </div>
                </div>
              </nav>
              <div className="p-8 text-center">
                <p className={`${isDark ? 'text-[#A8B2D1]' : 'text-[#555]'}`}>
                  Toggle seamlessly adapts colors based on theme mode
                </p>
              </div>
            </div>
          </motion.div>

          {/* Size Variations */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.6 }}
            className="md:col-span-2 lg:col-span-3"
          >
            <h3 className={`text-xl font-semibold mb-6 text-center ${
              isDark ? 'text-[#F8FAFC]' : 'text-[#0A0F29]'
            }`}>
              Size Variations
            </h3>
            <div className={`p-8 rounded-2xl border transition-all duration-500 ${
              isDark 
                ? 'bg-white/5 backdrop-blur-sm border-white/12' 
                : 'bg-[#F2F4F7] border-[#E0E4EC] shadow-black/7'
            }`}>
              <div className="flex items-center justify-center space-x-8">
                <div className="text-center">
                  <ThemeToggle variant="default" size="sm" showLabel={true} />
                  <p className={`text-sm mt-2 ${
                    isDark ? 'text-[#A8B2D1]' : 'text-[#555]'
                  }`}>Small</p>
                </div>
                <div className="text-center">
                  <ThemeToggle variant="default" size="md" showLabel={true} />
                  <p className={`text-sm mt-2 ${
                    isDark ? 'text-[#A8B2D1]' : 'text-[#555]'
                  }`}>Medium</p>
                </div>
                <div className="text-center">
                  <ThemeToggle variant="default" size="lg" showLabel={true} />
                  <p className={`text-sm mt-2 ${
                    isDark ? 'text-[#A8B2D1]' : 'text-[#555]'
                  }`}>Large</p>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Theme Comparison */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.7 }}
            className="md:col-span-2 lg:col-span-3"
          >
            <h3 className={`text-xl font-semibold mb-6 text-center ${
              isDark ? 'text-[#F8FAFC]' : 'text-[#0A0F29]'
            }`}>
              Theme Comparison
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Dark Mode Preview */}
              <div className="bg-[#0A0F29] p-6 rounded-2xl border border-[#00E0FF]/20">
                <div className="flex items-center justify-between mb-4">
                  <h4 className="text-[#F8FAFC] font-semibold">Dark Mode - Neon AI</h4>
                  <div className="w-12 h-6 bg-white/5 backdrop-blur-xl border border-white/12 rounded-full relative">
                    <div className="absolute left-0.5 top-0.5 w-5 h-5 bg-gradient-to-r from-[#00E0FF] to-[#33F1FF] rounded-full flex items-center justify-center">
                      <div className="w-3 h-3 text-white">🌙</div>
                    </div>
                  </div>
                </div>
                <div className="space-y-3">
                  <div className="h-3 bg-[#00E0FF]/20 rounded animate-pulse"></div>
                  <div className="h-3 bg-[#33F1FF]/20 rounded animate-pulse"></div>
                  <div className="h-3 bg-[#4C5FFF]/20 rounded animate-pulse"></div>
                </div>
              </div>

              {/* Light Mode Preview */}
              <div className="bg-white p-6 rounded-2xl border border-[#E0E4EC] shadow-black/7">
                <div className="flex items-center justify-between mb-4">
                  <h4 className="text-[#0A0F29] font-semibold">Light Mode - Soft Tech</h4>
                  <div className="w-12 h-6 bg-[#F2F4F7] border border-[#E0E4EC] rounded-full relative">
                    <div className="absolute right-0.5 top-0.5 w-5 h-5 bg-gradient-to-r from-[#2BB8CC] to-[#5A6FFF] rounded-full flex items-center justify-center">
                      <div className="w-3 h-3 text-white">☀️</div>
                    </div>
                  </div>
                </div>
                <div className="space-y-3">
                  <div className="h-3 bg-[#2BB8CC]/20 rounded"></div>
                  <div className="h-3 bg-[#5A6FFF]/20 rounded"></div>
                  <div className="h-3 bg-[#E0E4EC] rounded"></div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Current Theme Display */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.8 }}
          className="mt-16 text-center"
        >
          <div className={`inline-flex items-center px-6 py-3 rounded-full border transition-all duration-500 ${
            isDark 
              ? 'bg-white/5 backdrop-blur-sm border-white/12' 
              : 'bg-[#F2F4F7] border-[#E0E4EC] shadow-black/7'
          }`}>
            <div className={`w-3 h-3 rounded-full mr-3 ${
              isDark ? 'bg-[#00E0FF] shadow-lg shadow-[#00E0FF]/50' : 'bg-[#2BB8CC]'
            }`} />
            <span className={`font-medium ${
              isDark ? 'text-[#F8FAFC]' : 'text-[#0A0F29]'
            }`}>
              Current Theme: {isDark ? 'Dark Mode (Neon AI)' : 'Light Mode (Soft Tech)'}
            </span>
          </div>
        </motion.div>
      </div>

      {/* Floating Toggle */}
      <ThemeToggle variant="floating" />
    </div>
  );
};

export default ThemeToggleDemo;
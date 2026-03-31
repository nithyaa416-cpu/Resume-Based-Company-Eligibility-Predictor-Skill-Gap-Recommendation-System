import React from 'react';
import { Sun, Moon, Settings } from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';
import { motion, AnimatePresence } from 'framer-motion';

const ThemeToggle = ({ 
  variant = 'default', 
  className = '',
  showLabel = false,
  size = 'md'
}) => {
  const { isDark, toggleTheme } = useTheme();

  const sizes = {
    sm: { toggle: 'w-12 h-6', handle: 'w-5 h-5', icon: 'w-3 h-3' },
    md: { toggle: 'w-14 h-7', handle: 'w-6 h-6', icon: 'w-4 h-4' },
    lg: { toggle: 'w-16 h-8', handle: 'w-7 h-7', icon: 'w-5 h-5' }
  };

  const currentSize = sizes[size];

  // Dual palette system
  const darkModeStyles = {
    background: 'bg-white/5 backdrop-blur-xl border-white/12',
    handleBg: 'bg-gradient-to-r from-[#00E0FF] to-[#33F1FF]',
    handleBorder: 'border-[#00E0FF]/50',
    handleShadow: 'shadow-lg shadow-[#00E0FF]/30',
    glow: 'shadow-[#00E0FF]/20',
    hoverGlow: 'hover:shadow-[#00E0FF]/40',
    iconColor: 'text-white',
    floatingIcon: 'text-[#00E0FF]',
    textColor: 'text-[#F8FAFC]'
  };

  const lightModeStyles = {
    background: 'bg-[#F2F4F7] border-[#E0E4EC]',
    handleBg: 'bg-gradient-to-r from-[#2BB8CC] to-[#5A6FFF]',
    handleBorder: 'border-[#2BB8CC]/30',
    handleShadow: 'shadow-sm',
    glow: 'shadow-black/7',
    hoverGlow: 'hover:shadow-black/10',
    iconColor: 'text-white',
    floatingIcon: 'text-[#555]',
    textColor: 'text-[#555]'
  };

  const currentStyles = isDark ? darkModeStyles : lightModeStyles;

  // Default Premium Toggle
  if (variant === 'default') {
    return (
      <div className={`flex items-center space-x-3 ${className}`}>
        {showLabel && (
          <span className={`text-sm font-medium ${currentStyles.textColor}`}>
            {isDark ? 'Dark' : 'Light'}
          </span>
        )}
        
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={toggleTheme}
          className={`relative ${currentSize.toggle} rounded-full border transition-all duration-500 ${
            currentStyles.background
          } ${currentStyles.glow} ${currentStyles.hoverGlow}`}
          aria-label="Toggle theme"
        >
          {/* Background Glow Effect - Only for dark mode */}
          {isDark && (
            <div className="absolute inset-0 rounded-full bg-gradient-to-r from-[#00E0FF]/10 to-[#33F1FF]/10 animate-pulse" />
          )}
          
          {/* Toggle Handle */}
          <motion.div
            layout
            className={`absolute top-0.5 ${currentSize.handle} rounded-full border flex items-center justify-center transition-all duration-500 ${
              currentStyles.handleBg
            } ${currentStyles.handleBorder} ${currentStyles.handleShadow} ${
              isDark ? 'left-0.5' : `right-0.5`
            }`}
            animate={{
              x: isDark ? 0 : 0,
            }}
            transition={{ type: "spring", stiffness: 500, damping: 30 }}
          >
            <AnimatePresence mode="wait">
              {isDark ? (
                <motion.div
                  key="moon"
                  initial={{ scale: 0, rotate: -180 }}
                  animate={{ scale: 1, rotate: 0 }}
                  exit={{ scale: 0, rotate: 180 }}
                  transition={{ duration: 0.3 }}
                >
                  <Moon className={`${currentSize.icon} ${currentStyles.iconColor}`} />
                </motion.div>
              ) : (
                <motion.div
                  key="sun"
                  initial={{ scale: 0, rotate: 180 }}
                  animate={{ scale: 1, rotate: 0 }}
                  exit={{ scale: 0, rotate: -180 }}
                  transition={{ duration: 0.3 }}
                >
                  <Sun className={`${currentSize.icon} ${currentStyles.iconColor}`} />
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>

          {/* Floating Icons */}
          <div className="absolute inset-0 flex items-center justify-between px-1.5">
            <motion.div
              animate={{ 
                opacity: isDark ? 0.3 : 0.7,
                scale: isDark ? 0.8 : 1
              }}
              transition={{ duration: 0.3 }}
            >
              <Sun className={`w-3 h-3 ${currentStyles.floatingIcon}`} />
            </motion.div>
            <motion.div
              animate={{ 
                opacity: isDark ? 0.7 : 0.3,
                scale: isDark ? 1 : 0.8
              }}
              transition={{ duration: 0.3 }}
            >
              <Moon className={`w-3 h-3 ${currentStyles.floatingIcon}`} />
            </motion.div>
          </div>
        </motion.button>
      </div>
    );
  }

  // Circular Icon Toggle
  if (variant === 'circular') {
    return (
      <motion.button
        whileHover={{ 
          scale: 1.05, 
          boxShadow: isDark ? "0 0 20px rgba(0, 224, 255, 0.3)" : "0 0 20px rgba(43, 184, 204, 0.2)" 
        }}
        whileTap={{ scale: 0.95 }}
        onClick={toggleTheme}
        className={`relative w-12 h-12 rounded-full border transition-all duration-500 ${
          currentStyles.background
        } ${currentStyles.glow} ${className}`}
        aria-label="Toggle theme"
      >
        {/* Rotating Background */}
        <motion.div
          className={`absolute inset-1 rounded-full transition-all duration-500 ${
            isDark ? 'bg-[#00E0FF]/10' : 'bg-[#2BB8CC]/10'
          }`}
          animate={{ rotate: isDark ? 180 : 0 }}
          transition={{ duration: 0.5 }}
        />
        
        <div className="relative w-full h-full flex items-center justify-center">
          <AnimatePresence mode="wait">
            {isDark ? (
              <motion.div
                key="moon"
                initial={{ scale: 0, rotate: -180, opacity: 0 }}
                animate={{ scale: 1, rotate: 0, opacity: 1 }}
                exit={{ scale: 0, rotate: 180, opacity: 0 }}
                transition={{ duration: 0.4 }}
              >
                <Moon className="w-5 h-5 text-[#00E0FF]" />
              </motion.div>
            ) : (
              <motion.div
                key="sun"
                initial={{ scale: 0, rotate: 180, opacity: 0 }}
                animate={{ scale: 1, rotate: 0, opacity: 1 }}
                exit={{ scale: 0, rotate: -180, opacity: 0 }}
                transition={{ duration: 0.4 }}
              >
                <Sun className="w-5 h-5 text-[#2BB8CC]" />
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Pulse Ring */}
        <motion.div
          className={`absolute inset-0 rounded-full border-2 ${
            isDark ? 'border-[#00E0FF]/20' : 'border-[#2BB8CC]/20'
          }`}
          animate={{
            scale: [1, 1.1, 1],
            opacity: [0.5, 0.8, 0.5]
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
      </motion.button>
    );
  }

  // Floating Bottom-Right Toggle
  if (variant === 'floating') {
    return (
      <motion.div
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className={`fixed bottom-6 right-6 z-50 ${className}`}
      >
        <motion.button
          whileHover={{ 
            scale: 1.1, 
            boxShadow: isDark ? "0 0 30px rgba(0, 224, 255, 0.4)" : "0 0 30px rgba(43, 184, 204, 0.3)" 
          }}
          whileTap={{ scale: 0.9 }}
          onClick={toggleTheme}
          className={`w-14 h-14 rounded-full border-2 transition-all duration-500 shadow-2xl ${
            isDark 
              ? 'bg-[#0A0F29]/90 backdrop-blur-xl border-[#00E0FF]/40 shadow-[#00E0FF]/20' 
              : 'bg-white/90 backdrop-blur-xl border-[#2BB8CC]/40 shadow-black/10'
          }`}
          aria-label="Toggle theme"
        >
          <div className="relative w-full h-full flex items-center justify-center">
            <AnimatePresence mode="wait">
              {isDark ? (
                <motion.div
                  key="moon"
                  initial={{ scale: 0, rotate: -90, opacity: 0 }}
                  animate={{ scale: 1, rotate: 0, opacity: 1 }}
                  exit={{ scale: 0, rotate: 90, opacity: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <Moon className="w-6 h-6 text-[#00E0FF]" />
                </motion.div>
              ) : (
                <motion.div
                  key="sun"
                  initial={{ scale: 0, rotate: 90, opacity: 0 }}
                  animate={{ scale: 1, rotate: 0, opacity: 1 }}
                  exit={{ scale: 0, rotate: -90, opacity: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <Sun className="w-6 h-6 text-[#2BB8CC]" />
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Animated Ring */}
          <motion.div
            className={`absolute inset-0 rounded-full border ${
              isDark ? 'border-[#00E0FF]/30' : 'border-[#2BB8CC]/30'
            }`}
            animate={{ rotate: 360 }}
            transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
          />
        </motion.button>
      </motion.div>
    );
  }

  // Settings Panel Toggle
  if (variant === 'settings') {
    return (
      <div className={`rounded-2xl p-6 shadow-xl transition-all duration-500 ${
        isDark 
          ? 'bg-white/5 backdrop-blur-xl border border-white/12' 
          : 'bg-[#F2F4F7] border border-[#E0E4EC] shadow-black/7'
      } ${className}`}>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className={`w-10 h-10 rounded-xl flex items-center justify-center border ${
              isDark 
                ? 'bg-gradient-to-r from-[#00E0FF]/20 to-[#4C5FFF]/20 border-white/12' 
                : 'bg-gradient-to-r from-[#2BB8CC]/20 to-[#5A6FFF]/20 border-[#E0E4EC]'
            }`}>
              <Settings className={`w-5 h-5 ${
                isDark ? 'text-[#00E0FF]' : 'text-[#2BB8CC]'
              }`} />
            </div>
            <div>
              <h3 className={`font-semibold ${currentStyles.textColor}`}>Appearance</h3>
              <p className={`text-sm ${
                isDark ? 'text-[#A8B2D1]' : 'text-[#555]'
              }`}>Customize your interface</p>
            </div>
          </div>
        </div>

        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-all duration-300 ${
              !isDark 
                ? 'bg-[#2BB8CC]/20 border border-[#2BB8CC]/30' 
                : 'bg-white/5 border border-white/10'
            }`}>
              <Sun className={`w-4 h-4 ${
                isDark ? 'text-[#555]' : 'text-[#2BB8CC]'
              }`} />
              <span className={`text-sm ${currentStyles.textColor}`}>Light</span>
            </div>
            
            <div className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-all duration-300 ${
              isDark 
                ? 'bg-[#00E0FF]/20 border border-[#00E0FF]/30' 
                : 'bg-white/5 border border-white/10'
            }`}>
              <Moon className={`w-4 h-4 ${
                isDark ? 'text-[#00E0FF]' : 'text-[#555]'
              }`} />
              <span className={`text-sm ${currentStyles.textColor}`}>Dark</span>
            </div>
          </div>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={toggleTheme}
            className={`relative w-16 h-8 rounded-full border transition-all duration-500 ${
              currentStyles.background
            } ${currentStyles.glow}`}
            aria-label="Toggle theme"
          >
            <motion.div
              className={`absolute top-0.5 w-7 h-7 rounded-full border flex items-center justify-center transition-all duration-500 ${
                currentStyles.handleBg
              } ${currentStyles.handleBorder} ${currentStyles.handleShadow} ${
                isDark ? 'right-0.5' : 'left-0.5'
              }`}
              layout
              transition={{ type: "spring", stiffness: 500, damping: 30 }}
            >
              <AnimatePresence mode="wait">
                {isDark ? (
                  <motion.div
                    key="moon"
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    exit={{ scale: 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    <Moon className="w-4 h-4 text-white" />
                  </motion.div>
                ) : (
                  <motion.div
                    key="sun"
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    exit={{ scale: 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    <Sun className="w-4 h-4 text-white" />
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          </motion.button>
        </div>
      </div>
    );
  }

  // Minimal Version
  if (variant === 'minimal') {
    return (
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={toggleTheme}
        className={`relative w-10 h-10 rounded-lg border transition-all duration-300 ${
          currentStyles.background
        } ${currentStyles.glow} ${currentStyles.hoverGlow} ${className}`}
        aria-label="Toggle theme"
      >
        <AnimatePresence mode="wait">
          {isDark ? (
            <motion.div
              key="moon"
              initial={{ scale: 0, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0, opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="flex items-center justify-center w-full h-full"
            >
              <Moon className="w-5 h-5 text-[#00E0FF]" />
            </motion.div>
          ) : (
            <motion.div
              key="sun"
              initial={{ scale: 0, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0, opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="flex items-center justify-center w-full h-full"
            >
              <Sun className="w-5 h-5 text-[#2BB8CC]" />
            </motion.div>
          )}
        </AnimatePresence>
      </motion.button>
    );
  }

  return null;
};

export default ThemeToggle;
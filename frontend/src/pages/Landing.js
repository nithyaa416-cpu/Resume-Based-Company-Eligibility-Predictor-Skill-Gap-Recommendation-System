import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Brain, Target, TrendingUp, Star, ArrowRight, BarChart3, Sparkles, Play,
  Upload, Eye, ChevronRight, CheckCircle, Code, Database, Cpu, Network,
  GraduationCap, Briefcase, UserCheck, TrendingDown, PieChart, BarChart, Radar,
  Github, Twitter, Linkedin, FileText, Search, Layers, X, Heart
} from 'lucide-react';
import ThemeToggle from '../components/ThemeToggle';
import { useTheme } from '../contexts/ThemeContext';

const Landing = () => {
  const [particles, setParticles] = useState([]);
  const { isDark } = useTheme();
  const loggedInUser = (() => { try { return JSON.parse(localStorage.getItem('user')); } catch { return null; } })();

  useEffect(() => {
    // Generate floating particles
    const newParticles = Array.from({ length: 20 }, (_, i) => ({
      id: i,
      x: Math.random() * 100,
      y: Math.random() * 100,
      size: Math.random() * 4 + 2,
      duration: Math.random() * 20 + 10,
      delay: Math.random() * 5
    }));
    setParticles(newParticles);
  }, []);

  const features = [
    {
      icon: Brain,
      title: "Smart Analysis",
      description: "Advanced technology to deeply understand your resume content and match it with opportunities.",
      color: "from-[#00E0FF] to-[#33F1FF]",
      glowColor: "shadow-[#00E0FF]/20"
    },
    {
      icon: Target,
      title: "Smart Company Matching", 
      description: "Intelligent algorithms match your profile with company requirements and predict eligibility scores.",
      color: "from-[#4C5FFF] to-[#00E0FF]",
      glowColor: "shadow-[#4C5FFF]/20"
    },
    {
      icon: Search,
      title: "Skill Gap Detection",
      description: "Identify missing skills and get personalized learning recommendations to bridge career gaps.",
      color: "from-[#33F1FF] to-[#4C5FFF]",
      glowColor: "shadow-[#33F1FF]/20"
    },
    {
      icon: BarChart3,
      title: "Performance Analytics",
      description: "Comprehensive scoring system with detailed metrics and actionable insights for optimization.",
      color: "from-[#00E0FF] to-[#4C5FFF]",
      glowColor: "shadow-[#00E0FF]/20"
    }
  ];

  return (
    <div className={`min-h-screen overflow-hidden relative transition-all duration-500 ${
      isDark ? 'bg-[#0A0F29] text-[#F8FAFC]' : 'bg-white text-gray-900'
    }`}>
      {/* Floating Particles Background */}
      <div className="fixed inset-0 pointer-events-none">
        {particles.map((particle) => (
          <motion.div
            key={particle.id}
            className={`absolute w-1 h-1 rounded-full ${
              isDark ? 'bg-[#00E0FF]/30' : 'bg-[#4C5FFF]/20'
            }`}
            style={{
              left: `${particle.x}%`,
              top: `${particle.y}%`,
              width: `${particle.size}px`,
              height: `${particle.size}px`,
            }}
            animate={{
              y: [0, -100, 0],
              opacity: [0, 1, 0],
            }}
            transition={{
              duration: particle.duration,
              repeat: Infinity,
              delay: particle.delay,
              ease: "easeInOut"
            }}
          />
        ))}
      </div>

      {/* Sticky Navbar */}
      <nav className={`fixed top-0 left-0 right-0 z-50 backdrop-blur-xl border-b transition-all duration-500 ${
        isDark 
          ? 'bg-white/5 border-white/12 shadow-lg shadow-[#00E0FF]/5' 
          : 'bg-white/90 border-gray-200/50 shadow-lg shadow-gray-900/5'
      }`}>
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <motion.div 
              className="flex items-center space-x-4"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
            >
              <div className="relative">
                <div className={`w-12 h-12 rounded-xl flex items-center justify-center shadow-lg ${
                  isDark 
                    ? 'bg-gradient-to-r from-[#00E0FF] to-[#4C5FFF] shadow-[#00E0FF]/25' 
                    : 'bg-gradient-to-r from-[#4C5FFF] to-[#00E0FF] shadow-[#4C5FFF]/25'
                }`}>
                  <Brain className="w-7 h-7 text-white" />
                </div>
                <div className={`absolute -top-1 -right-1 w-4 h-4 rounded-full animate-pulse ${
                  isDark 
                    ? 'bg-gradient-to-r from-[#33F1FF] to-[#00E0FF]' 
                    : 'bg-gradient-to-r from-[#00E0FF] to-[#33F1FF]'
                }`}></div>
              </div>
              <div>
                <span className={`text-xl font-bold ${
                  isDark 
                    ? 'bg-gradient-to-r from-[#F8FAFC] to-[#A8B2D1] bg-clip-text text-transparent' 
                    : 'text-[#0A0F29]'
                }`}>
                  Resume Analyzer
                </span>
                <div className={`text-xs font-medium ${
                  isDark ? 'text-[#A8B2D1]' : 'text-gray-500'
                }`}>Smart Career Matching</div>
              </div>
            </motion.div>

            <div className="hidden md:flex items-center space-x-8">
              <Link to="/about" className={`transition-colors duration-300 ${
                isDark 
                  ? 'text-[#A8B2D1] hover:text-[#00E0FF]' 
                  : 'text-gray-700 hover:text-[#4C5FFF] font-medium'
              }`}>About</Link>
              <a href="#features" className={`transition-colors duration-300 ${
                isDark 
                  ? 'text-[#A8B2D1] hover:text-[#00E0FF]' 
                  : 'text-gray-700 hover:text-[#4C5FFF] font-medium'
              }`}>Features</a>
              <a href="#how-it-works" className={`transition-colors duration-300 ${
                isDark 
                  ? 'text-[#A8B2D1] hover:text-[#00E0FF]' 
                  : 'text-gray-700 hover:text-[#4C5FFF] font-medium'
              }`}>How it Works</a>

              {!loggedInUser && (
                <Link to="/login" className={`transition-colors duration-300 ${
                  isDark 
                    ? 'text-[#A8B2D1] hover:text-[#00E0FF]' 
                    : 'text-gray-700 hover:text-[#4C5FFF] font-medium'
                }`}>Sign In</Link>
              )}
              <ThemeToggle />
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                {loggedInUser ? (
                  <Link to="/dashboard" className={`px-6 py-2.5 rounded-xl font-semibold shadow-lg transition-all duration-300 ${
                    isDark 
                      ? 'bg-gradient-to-r from-[#00E0FF] to-[#33F1FF] text-[#0A0F29] shadow-[#00E0FF]/25 hover:shadow-[#00E0FF]/40' 
                      : 'bg-gradient-to-r from-[#4C5FFF] to-[#00E0FF] text-white shadow-[#4C5FFF]/25 hover:shadow-[#4C5FFF]/40'
                  }`}>
                    Go to Dashboard
                  </Link>
                ) : (
                  <Link to="/register" className={`px-6 py-2.5 rounded-xl font-semibold shadow-lg transition-all duration-300 ${
                    isDark 
                      ? 'bg-gradient-to-r from-[#00E0FF] to-[#33F1FF] text-[#0A0F29] shadow-[#00E0FF]/25 hover:shadow-[#00E0FF]/40' 
                      : 'bg-gradient-to-r from-[#4C5FFF] to-[#00E0FF] text-white shadow-[#4C5FFF]/25 hover:shadow-[#4C5FFF]/40'
                  }`}>
                    Get Started
                  </Link>
                )}
              </motion.div>
            </div>
          </div>
        </div>
      </nav>
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center pt-20 overflow-hidden">
        {/* Animated Background Mesh */}
        <div className="absolute inset-0">
          <div className={`absolute inset-0 transition-all duration-500 ${
            isDark 
              ? 'bg-gradient-to-br from-[#0A0F29] via-[#1a1f3a] to-[#0A0F29]' 
              : 'bg-gradient-to-br from-white via-gray-50 to-white'
          }`}></div>
          <div className={`absolute inset-0 transition-all duration-500 ${
            isDark 
              ? 'bg-gradient-to-tr from-[#00E0FF]/5 via-transparent to-[#4C5FFF]/5' 
              : 'bg-gradient-to-tr from-[#4C5FFF]/5 via-transparent to-[#00E0FF]/5'
          }`}></div>
          
          {/* Floating Mesh Gradients */}
          <motion.div
            className="absolute top-20 right-20 w-96 h-96 bg-gradient-to-r from-[#00E0FF]/10 to-[#33F1FF]/10 rounded-full blur-3xl"
            animate={{
              scale: [1, 1.2, 1],
              opacity: [0.3, 0.6, 0.3],
            }}
            transition={{
              duration: 8,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          />
          <motion.div
            className="absolute bottom-32 left-32 w-80 h-80 bg-gradient-to-r from-[#4C5FFF]/10 to-[#00E0FF]/10 rounded-full blur-3xl"
            animate={{
              scale: [1.2, 1, 1.2],
              opacity: [0.4, 0.7, 0.4],
            }}
            transition={{
              duration: 6,
              repeat: Infinity,
              ease: "easeInOut",
              delay: 3
            }}
          />
        </div>

        <div className="relative container mx-auto px-6 text-center z-10">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="max-w-6xl mx-auto"
          >
            

            {/* Main Headline */}
            <motion.h1
              className="text-4xl md:text-6xl font-bold mb-8 leading-tight"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.3 }}
            >
              <span className={`${
                isDark 
                  ? 'bg-gradient-to-r from-[#F8FAFC] via-[#F8FAFC] to-[#A8B2D1] bg-clip-text text-transparent' 
                  : 'text-[#0A0F29]'
              }`}>
                Resume-Based
              </span>
              <br />
              <span className="bg-gradient-to-r from-[#00E0FF] via-[#33F1FF] to-[#4C5FFF] bg-clip-text text-transparent">
                Company Eligibility Predictor &
              </span>
              <br />
              <span className="bg-gradient-to-r from-[#4C5FFF] via-[#00E0FF] to-[#33F1FF] bg-clip-text text-transparent">
                Skill Gap Analysis

              </span>
            </motion.h1>
            
            <motion.p
              className={`text-xl md:text-2xl mb-12 leading-relaxed max-w-4xl mx-auto ${
                isDark ? 'text-[#A8B2D1]' : 'text-gray-700'
              }`}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.5 }}
            >
              Get smart insights, company eligibility predictions, and personalized skill recommendations from your resume.
              Transform your career with advanced analysis.
            </motion.p>

            {/* CTA Buttons */}
            <motion.div
              className="flex flex-col sm:flex-row gap-6 justify-center mb-16"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.7 }}
            >
              <motion.div 
                whileHover={{ scale: 1.05, boxShadow: "0 20px 40px rgba(0, 224, 255, 0.3)" }} 
                whileTap={{ scale: 0.95 }}
                transition={{ type: "spring", stiffness: 300 }}
              >
                <Link
                  to="/register"
                  className="group relative inline-flex items-center justify-center px-8 py-4 text-lg font-semibold bg-gradient-to-r from-[#00E0FF] to-[#33F1FF] text-[#0A0F29] rounded-xl shadow-xl shadow-[#00E0FF]/25 hover:shadow-[#00E0FF]/40 transition-all duration-300 border border-[#00E0FF]/20"
                >
                  <Upload className="w-5 h-5 mr-2" />
                  <span className="relative z-10 flex items-center">
                    Upload Resume
                  </span>
                </Link>
              </motion.div>
              
              <motion.div 
                whileHover={{ scale: 1.05 }} 
                whileTap={{ scale: 0.95 }}
                transition={{ type: "spring", stiffness: 300 }}
              >
                <Link
                  to="/register"
                  className="group inline-flex items-center justify-center px-8 py-4 text-lg font-semibold bg-white/5 backdrop-blur-sm border border-white/12 rounded-xl hover:bg-white/10 hover:border-[#00E0FF]/30 transition-all duration-300"
                >
                  Start Free Analysis
                  <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
                </Link>
              </motion.div>

              <motion.div 
                whileHover={{ scale: 1.05 }} 
                whileTap={{ scale: 0.95 }}
                transition={{ type: "spring", stiffness: 300 }}
              >
                <Link
                  to="/demo-info"
                  className="group inline-flex items-center justify-center px-8 py-4 text-lg font-semibold border border-[#4C5FFF]/50 text-[#4C5FFF] hover:bg-[#4C5FFF]/10 hover:border-[#4C5FFF] rounded-xl transition-all duration-300"
                >
                  <Play className="w-5 h-5 mr-2 group-hover:scale-110 transition-transform" />
                  View Demo
                </Link>
              </motion.div>
            </motion.div>


          </motion.div>
        </div>
      </section>
      
      {/* Features Section */}
      <section id="features" className="py-20 relative">
        <div className={`absolute inset-0 transition-all duration-500 ${
          isDark 
            ? 'bg-gradient-to-b from-[#0A0F29] to-[#1a1f3a]' 
            : 'bg-gradient-to-b from-gray-50 to-white'
        }`}></div>
        <div className="relative container mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className={`text-5xl font-bold mb-4 ${
              isDark 
                ? 'bg-gradient-to-r from-[#F8FAFC] to-[#A8B2D1] bg-clip-text text-transparent' 
                : 'text-gray-900'
            }`}>
              Powered by Advanced AI
            </h2>
            <p className={`text-xl max-w-3xl mx-auto ${
              isDark ? 'text-[#A8B2D1]' : 'text-gray-600'
            }`}>
              Our platform uses state-of-the-art machine learning models to provide 
              unprecedented insights into your resume and career potential.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                whileHover={{ y: -8, scale: 1.02 }}
                className="group"
              >
                <div className={`p-8 rounded-2xl border transition-all duration-500 h-full shadow-xl hover:shadow-2xl ${
                  isDark 
                    ? `bg-white/5 backdrop-blur-sm border-white/12 hover:bg-white/10 hover:border-[#00E0FF]/30 ${feature.glowColor}` 
                    : 'bg-white border-gray-200 hover:bg-gray-50 hover:border-[#4C5FFF]/30 shadow-gray-900/5'
                }`}>
                  <motion.div
                    className={`w-16 h-16 bg-gradient-to-r ${feature.color} rounded-xl flex items-center justify-center mb-6 shadow-lg`}
                    whileHover={{ rotate: 5, scale: 1.1 }}
                    transition={{ type: "spring", stiffness: 300 }}
                  >
                    <feature.icon className="w-8 h-8 text-white" />
                  </motion.div>
                  
                  <h3 className={`text-xl font-semibold mb-3 ${
                    isDark ? 'text-[#F8FAFC]' : 'text-gray-900'
                  }`}>
                    {feature.title}
                  </h3>
                  
                  <p className={`leading-relaxed ${
                    isDark ? 'text-[#A8B2D1]' : 'text-gray-600'
                  }`}>
                    {feature.description}
                  </p>

                  {/* Neon Glow Border on Hover */}
                  <div className="absolute inset-0 rounded-2xl border border-[#00E0FF]/0 group-hover:border-[#00E0FF]/50 transition-all duration-500 pointer-events-none"></div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
      {/* Why Our AI Works - Technical Trust Section */}
      <section className="py-20 relative">
        <div className="container mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className={`text-5xl font-bold mb-4 ${
              isDark 
                ? 'bg-gradient-to-r from-[#F8FAFC] to-[#A8B2D1] bg-clip-text text-transparent' 
                : 'text-gray-900'
            }`}>
              Why Our AI Works
            </h2>
            <p className={`text-xl max-w-3xl mx-auto ${
              isDark ? 'text-[#A8B2D1]' : 'text-gray-600'
            }`}>
              Built on cutting-edge technology stack for maximum accuracy and reliability
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              {
                icon: Code,
                title: "NLP/BERT Embeddings",
                description: "Advanced natural language processing with contextual understanding",
                color: "from-[#00E0FF] to-[#33F1FF]"
              },
              {
                icon: Network,
                title: "Semantic Matching",
                description: "Deep semantic analysis beyond simple keyword matching",
                color: "from-[#4C5FFF] to-[#00E0FF]"
              },
              {
                icon: Cpu,
                title: "ML-based Classification",
                description: "Machine learning models trained on millions of resumes",
                color: "from-[#33F1FF] to-[#4C5FFF]"
              },
              {
                icon: FileText,
                title: "Resume ATS Understanding",
                description: "Optimized for Applicant Tracking System compatibility",
                color: "from-[#00E0FF] to-[#4C5FFF]"
              }
            ].map((tech, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                whileHover={{ scale: 1.05 }}
                className="group"
              >
                <div className={`p-6 rounded-xl border transition-all duration-300 h-full ${
                  isDark 
                    ? 'bg-white/5 backdrop-blur-sm border-white/12 hover:bg-white/10 hover:border-[#00E0FF]/30' 
                    : 'bg-white border-gray-200 hover:bg-gray-50 hover:border-[#00E0FF]/30 shadow-sm'
                }`}>
                  <motion.div
                    className={`w-12 h-12 bg-gradient-to-r ${tech.color} rounded-lg flex items-center justify-center mb-4 shadow-lg`}
                    whileHover={{ rotate: 10 }}
                    transition={{ type: "spring", stiffness: 300 }}
                  >
                    <tech.icon className="w-6 h-6 text-white" />
                  </motion.div>
                  
                  <h3 className={`text-lg font-semibold mb-2 ${
                    isDark ? 'text-[#F8FAFC]' : 'text-gray-900'
                  }`}>
                    {tech.title}
                  </h3>
                  
                  <p className={`text-sm leading-relaxed ${
                    isDark ? 'text-[#A8B2D1]' : 'text-gray-600'
                  }`}>
                    {tech.description}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20 relative">
        <div className={`absolute inset-0 transition-all duration-500 ${
          isDark 
            ? 'bg-gradient-to-br from-[#1a1f3a] via-[#0A0F29] to-[#1a1f3a]' 
            : 'bg-gradient-to-br from-white via-gray-50 to-white'
        }`}></div>
        <div className="relative container mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className={`text-5xl font-bold mb-4 ${
              isDark 
                ? 'bg-gradient-to-r from-[#F8FAFC] to-[#A8B2D1] bg-clip-text text-transparent' 
                : 'text-gray-900'
            }`}>
              How It Works
            </h2>
            <p className={`text-xl ${
              isDark ? 'text-[#A8B2D1]' : 'text-gray-600'
            }`}>
              Get professional insights in just three simple steps
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {[
              {
                step: "01",
                title: "Upload Resume",
                description: "Simply drag and drop your resume or paste the text. Our AI supports PDF, DOCX, and text formats with instant processing.",
                icon: Upload,
                color: "from-[#00E0FF] to-[#33F1FF]"
              },
              {
                step: "02", 
                title: "Smart Analysis",
                description: "Our advanced system analyzes your resume for deep contextual understanding and skill extraction.",
                icon: Brain,
                color: "from-[#4C5FFF] to-[#00E0FF]"
              },
              {
                step: "03",
                title: "Get Insights",
                description: "Receive detailed analysis, eligibility scores, skill recommendations, and personalized learning roadmaps instantly.",
                icon: Eye,
                color: "from-[#33F1FF] to-[#4C5FFF]"
              }
            ].map((item, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                viewport={{ once: true }}
                whileHover={{ scale: 1.02 }}
                className="text-center relative"
              >
                <div className={`p-8 rounded-2xl border transition-all duration-300 relative z-10 shadow-xl ${
                  isDark 
                    ? 'bg-white/5 backdrop-blur-sm border-white/12 hover:bg-white/10 hover:border-[#00E0FF]/30' 
                    : 'bg-white border-gray-200 hover:bg-gray-50 hover:border-[#00E0FF]/30'
                }`}>
                  <motion.div
                    className={`w-20 h-20 bg-gradient-to-r ${item.color} rounded-xl flex items-center justify-center text-4xl mb-6 mx-auto shadow-xl`}
                    whileHover={{ scale: 1.1, rotate: 5 }}
                    transition={{ type: "spring", stiffness: 300 }}
                  >
                    <item.icon className="w-10 h-10 text-white" />
                  </motion.div>
                  <div className="text-sm font-bold text-[#00E0FF] mb-2">STEP {item.step}</div>
                  <h3 className={`text-xl font-semibold mb-3 ${
                    isDark ? 'text-[#F8FAFC]' : 'text-gray-900'
                  }`}>{item.title}</h3>
                  <p className={`${
                    isDark ? 'text-[#A8B2D1]' : 'text-gray-600'
                  }`}>{item.description}</p>

                  {/* Neon Borders */}
                  <div className="absolute inset-0 rounded-2xl border-2 border-[#00E0FF]/0 group-hover:border-[#00E0FF]/50 transition-all duration-500 pointer-events-none"></div>
                </div>
                
                {index < 2 && (
                  <div className="hidden md:block absolute top-1/2 -right-4 transform -translate-y-1/2 z-0">
                    <motion.div
                      animate={{ x: [0, 10, 0] }}
                      transition={{ duration: 2, repeat: Infinity }}
                    >
                      <ChevronRight className="w-8 h-8 text-[#00E0FF]/50" />
                    </motion.div>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
      </section>
      {/* User Personas Section */}
      <section className="py-20 relative">
        <div className="container mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className={`text-5xl font-bold mb-4 ${
              isDark 
                ? 'bg-gradient-to-r from-[#F8FAFC] to-[#A8B2D1] bg-clip-text text-transparent' 
                : 'text-gray-900'
            }`}>
              Perfect for Every Career Stage
            </h2>
            <p className={`text-xl max-w-3xl mx-auto ${
              isDark ? 'text-[#A8B2D1]' : 'text-gray-600'
            }`}>
              Whether you're starting out or advancing your career, our AI adapts to your needs
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                icon: GraduationCap,
                title: "Students",
                description: "Get insights on how to structure your first resume and identify key skills for your target industry.",
                color: "from-[#00E0FF] to-[#33F1FF]",
                features: ["Resume structuring", "Skill identification", "Industry insights"]
              },
              {
                icon: UserCheck,
                title: "Freshers",
                description: "Bridge the gap between academic knowledge and industry requirements with personalized recommendations.",
                color: "from-[#4C5FFF] to-[#00E0FF]",
                features: ["Gap analysis", "Skill mapping", "Entry-level optimization"]
              },
              {
                icon: TrendingUp,
                title: "Job Switchers",
                description: "Optimize your resume for career transitions and identify transferable skills for new roles.",
                color: "from-[#33F1FF] to-[#4C5FFF]",
                features: ["Career transition", "Skill transfer", "Role optimization"]
              },
              {
                icon: Briefcase,
                title: "Working Professionals",
                description: "Enhance your profile for promotions and leadership roles with advanced skill recommendations.",
                color: "from-[#00E0FF] to-[#4C5FFF]",
                features: ["Leadership skills", "Promotion readiness", "Advanced analysis"]
              }
            ].map((persona, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                whileHover={{ y: -8, scale: 1.02 }}
                className="group"
              >
                <div className={`p-8 rounded-2xl border transition-all duration-500 h-full shadow-xl ${
                  isDark 
                    ? 'bg-white/5 backdrop-blur-sm border-white/12 hover:bg-white/10 hover:border-[#00E0FF]/30' 
                    : 'bg-white border-gray-200 hover:bg-gray-50 hover:border-[#00E0FF]/30'
                }`}>
                  <motion.div
                    className={`w-16 h-16 bg-gradient-to-r ${persona.color} rounded-xl flex items-center justify-center mb-6 shadow-lg`}
                    whileHover={{ rotate: 5, scale: 1.1 }}
                    transition={{ type: "spring", stiffness: 300 }}
                  >
                    <persona.icon className="w-8 h-8 text-white" />
                  </motion.div>
                  
                  <h3 className={`text-xl font-semibold mb-3 ${
                    isDark ? 'text-[#F8FAFC]' : 'text-gray-900'
                  }`}>
                    {persona.title}
                  </h3>
                  
                  <p className={`leading-relaxed mb-4 ${
                    isDark ? 'text-[#A8B2D1]' : 'text-gray-600'
                  }`}>
                    {persona.description}
                  </p>

                  <div className="space-y-2">
                    {persona.features.map((feature, idx) => (
                      <div key={idx} className={`flex items-center text-sm ${
                        isDark ? 'text-[#A8B2D1]' : 'text-gray-600'
                      }`}>
                        <CheckCircle className="w-4 h-4 text-[#00E0FF] mr-2" />
                        {feature}
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Graphical Insight Section */}
      <section className="py-20 relative">
        <div className="container mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className={`text-5xl font-bold mb-4 ${
              isDark 
                ? 'bg-gradient-to-r from-[#F8FAFC] to-[#A8B2D1] bg-clip-text text-transparent' 
                : 'text-gray-900'
            }`}>
              Visual Analytics Dashboard
            </h2>
            <p className={`text-xl max-w-3xl mx-auto ${
              isDark ? 'text-[#A8B2D1]' : 'text-gray-600'
            }`}>
              Get comprehensive insights through interactive charts and visual analytics
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {/* Skill Radar Chart */}
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              whileInView={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              whileHover={{ scale: 1.02 }}
              className={`p-8 rounded-2xl border transition-all duration-300 shadow-xl ${
                isDark 
                  ? 'bg-white/5 backdrop-blur-sm border-white/12 hover:border-[#00E0FF]/30' 
                  : 'bg-white border-gray-200 hover:border-[#00E0FF]/30'
              }`}
            >
              <div className="flex items-center mb-6">
                <Radar className="w-8 h-8 text-[#00E0FF] mr-3" />
                <h3 className={`text-xl font-semibold ${
                  isDark ? 'text-[#F8FAFC]' : 'text-gray-900'
                }`}>Skill Radar Chart</h3>
              </div>
              
              <div className="relative w-48 h-48 mx-auto mb-4">
                <svg className="w-full h-full" viewBox="0 0 200 200">
                  <defs>
                    <radialGradient id="radarGradient" cx="50%" cy="50%" r="50%">
                      <stop offset="0%" stopColor="#00E0FF" stopOpacity="0.3" />
                      <stop offset="100%" stopColor="#4C5FFF" stopOpacity="0.1" />
                    </radialGradient>
                  </defs>
                  
                  {/* Radar Grid */}
                  {[20, 40, 60, 80].map((radius, i) => (
                    <circle
                      key={i}
                      cx="100"
                      cy="100"
                      r={radius}
                      fill="none"
                      stroke="#00E0FF"
                      strokeOpacity="0.2"
                      strokeWidth="1"
                    />
                  ))}
                  
                  {/* Radar Lines */}
                  {[0, 60, 120, 180, 240, 300].map((angle, i) => {
                    const x = 100 + 80 * Math.cos((angle - 90) * Math.PI / 180);
                    const y = 100 + 80 * Math.sin((angle - 90) * Math.PI / 180);
                    return (
                      <line
                        key={i}
                        x1="100"
                        y1="100"
                        x2={x}
                        y2={y}
                        stroke="#00E0FF"
                        strokeOpacity="0.2"
                        strokeWidth="1"
                      />
                    );
                  })}
                  
                  {/* Data Polygon */}
                  <motion.polygon
                    points="100,40 140,60 160,120 120,160 80,140 60,80"
                    fill="url(#radarGradient)"
                    stroke="#00E0FF"
                    strokeWidth="2"
                    initial={{ pathLength: 0 }}
                    whileInView={{ pathLength: 1 }}
                    transition={{ duration: 2 }}
                  />
                </svg>
              </div>
              
              <div className="text-center">
                <p className="text-[#A8B2D1] text-sm">Technical Skills, Soft Skills, Experience, Education, Certifications</p>
              </div>
            </motion.div>

            {/* Eligibility Bar Graph */}
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              whileInView={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              viewport={{ once: true }}
              whileHover={{ scale: 1.02 }}
              className="bg-white/5 backdrop-blur-sm p-8 rounded-2xl border border-white/12 hover:border-[#4C5FFF]/30 transition-all duration-300 shadow-xl"
            >
              <div className="flex items-center mb-6">
                <BarChart className="w-8 h-8 text-[#4C5FFF] mr-3" />
                <h3 className="text-xl font-semibold text-[#F8FAFC]">Eligibility Analysis</h3>
              </div>
              
              <div className="space-y-4">
                {[
                  { company: "Google", score: 87, color: "#00E0FF" },
                  { company: "Microsoft", score: 92, color: "#4C5FFF" },
                  { company: "Amazon", score: 78, color: "#33F1FF" },
                  { company: "Meta", score: 85, color: "#00E0FF" },
                  { company: "Apple", score: 90, color: "#4C5FFF" }
                ].map((item, i) => (
                  <div key={i} className="flex items-center justify-between">
                    <span className="text-[#A8B2D1] text-sm w-20">{item.company}</span>
                    <div className="flex-1 mx-3 bg-white/10 rounded-full h-2">
                      <motion.div
                        className="h-2 rounded-full"
                        style={{ backgroundColor: item.color }}
                        initial={{ width: 0 }}
                        whileInView={{ width: `${item.score}%` }}
                        transition={{ duration: 1.5, delay: i * 0.1 }}
                      />
                    </div>
                    <span className="text-[#F8FAFC] text-sm font-semibold w-10">{item.score}%</span>
                  </div>
                ))}
              </div>
            </motion.div>

            {/* Missing Skills Pie Chart */}
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              whileInView={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              viewport={{ once: true }}
              whileHover={{ scale: 1.02 }}
              className="bg-white/5 backdrop-blur-sm p-8 rounded-2xl border border-white/12 hover:border-[#33F1FF]/30 transition-all duration-300 shadow-xl"
            >
              <div className="flex items-center mb-6">
                <PieChart className="w-8 h-8 text-[#33F1FF] mr-3" />
                <h3 className="text-xl font-semibold text-[#F8FAFC]">Skill Gap Analysis</h3>
              </div>
              
              <div className="relative w-48 h-48 mx-auto mb-4">
                <svg className="w-full h-full" viewBox="0 0 200 200">
                  <defs>
                    <linearGradient id="pieGradient1" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stopColor="#00E0FF" />
                      <stop offset="100%" stopColor="#33F1FF" />
                    </linearGradient>
                    <linearGradient id="pieGradient2" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stopColor="#4C5FFF" />
                      <stop offset="100%" stopColor="#00E0FF" />
                    </linearGradient>
                    <linearGradient id="pieGradient3" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stopColor="#33F1FF" />
                      <stop offset="100%" stopColor="#4C5FFF" />
                    </linearGradient>
                  </defs>
                  
                  {/* Pie Slices */}
                  <motion.path
                    d="M 100 100 L 100 20 A 80 80 0 0 1 180 100 Z"
                    fill="url(#pieGradient1)"
                    initial={{ pathLength: 0 }}
                    whileInView={{ pathLength: 1 }}
                    transition={{ duration: 1.5 }}
                  />
                  <motion.path
                    d="M 100 100 L 180 100 A 80 80 0 0 1 100 180 Z"
                    fill="url(#pieGradient2)"
                    initial={{ pathLength: 0 }}
                    whileInView={{ pathLength: 1 }}
                    transition={{ duration: 1.5, delay: 0.3 }}
                  />
                  <motion.path
                    d="M 100 100 L 100 180 A 80 80 0 0 1 100 20 Z"
                    fill="url(#pieGradient3)"
                    initial={{ pathLength: 0 }}
                    whileInView={{ pathLength: 1 }}
                    transition={{ duration: 1.5, delay: 0.6 }}
                  />
                </svg>
              </div>
              
              <div className="space-y-2 text-sm">
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-[#00E0FF] rounded-full mr-2"></div>
                  <span className="text-[#A8B2D1]">Technical Skills (60%)</span>
                </div>
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-[#4C5FFF] rounded-full mr-2"></div>
                  <span className="text-[#A8B2D1]">Soft Skills (25%)</span>
                </div>
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-[#33F1FF] rounded-full mr-2"></div>
                  <span className="text-[#A8B2D1]">Certifications (15%)</span>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>
      
            
                          }
            

              

      {/* Tech Stack Strip */}
      <section className="py-16 relative">
        <div className="container mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h3 className="text-2xl font-bold text-[#454545] mb-4">Built with Industry-Leading Technology</h3>
            <p className="text-[#A8B2D1]">Powered by the most advanced AI and ML frameworks</p>
          </motion.div>

          <div className="flex flex-wrap justify-center items-center gap-8 md:gap-12">
            {[
              { name: "Python", icon: Code },
              { name: "NLP/BERT", icon: Brain },
              { name: "Flask", icon: Database },
              { name: "Scikit-learn", icon: Cpu },
              { name: "React", icon: Layers },
              { name: "ML Models", icon: Network }
            ].map((tech, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                whileHover={{ scale: 1.1, y: -5 }}
                className="group"
              >
                <div className="flex flex-col items-center p-4 bg-white/5 backdrop-blur-sm rounded-xl border border-white/12 hover:border-[#00E0FF]/30 transition-all duration-300 shadow-lg hover:shadow-[#00E0FF]/20">
                  <tech.icon className="w-8 h-8 text-[#00E0FF] mb-2 group-hover:text-[#33F1FF] transition-colors" />
                  <span className="text-[#A8B2D1] text-sm font-medium group-hover:text-[#F8FAFC] transition-colors">{tech.name}</span>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="py-20 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-[#0A0F29] via-[#4C5FFF]/20 to-[#00E0FF]/20"></div>
        <div className="absolute inset-0 bg-gradient-to-br from-[#1a1f3a] to-[#0A0F29]"></div>
        
        {/* Neon Glow Background */}
        <div className="absolute inset-0 opacity-30">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-gradient-radial from-[#00E0FF]/30 via-[#00E0FF]/10 to-transparent rounded-full blur-3xl"></div>
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-gradient-radial from-[#4C5FFF]/30 via-[#4C5FFF]/10 to-transparent rounded-full blur-3xl"></div>
        </div>

        <div className="container mx-auto px-6 text-center relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="max-w-4xl mx-auto"
          >
            <h2 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-[#F8FAFC] via-[#00E0FF] to-[#4C5FFF] bg-clip-text text-transparent mb-6">
              Ready to Transform Your Career with AI?
            </h2>
            
            
            <div className="flex flex-col sm:flex-row gap-6 justify-center mb-12">
              <motion.div 
                whileHover={{ scale: 1.05, boxShadow: "0 20px 40px rgba(0, 224, 255, 0.3)" }} 
                whileTap={{ scale: 0.95 }}
                transition={{ type: "spring", stiffness: 300 }}
              >
                <Link
                  to="/register"
                  className="group inline-flex items-center justify-center px-8 py-4 text-lg font-semibold bg-gradient-to-r from-[#00E0FF] to-[#33F1FF] text-[#0A0F29] rounded-xl shadow-xl shadow-[#00E0FF]/25 hover:shadow-[#00E0FF]/40 transition-all duration-300"
                >
                  Start Free Analysis
                  <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
                </Link>
              </motion.div>
              
              <motion.div 
                whileHover={{ scale: 1.05 }} 
                whileTap={{ scale: 0.95 }}
                transition={{ type: "spring", stiffness: 300 }}
              >
                <Link
                  to="/about"
                  className="inline-flex items-center justify-center px-8 py-4 text-lg font-semibold border-2 border-[#00E0FF]/50 text-[#00E0FF] hover:bg-[#00E0FF]/10 hover:border-[#00E0FF] rounded-xl transition-all duration-300"
                >
                  Learn More
                </Link>
              </motion.div>
            </div>

            {/* Newsletter Signup */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.3 }}
              viewport={{ once: true }}
              className="max-w-md mx-auto"
            >
              <div className="flex bg-white/5 backdrop-blur-sm border border-white/12 rounded-xl p-2">
                <input
                  type="email"
                  placeholder="Enter your email for updates"
                  className="flex-1 bg-transparent text-[#F8FAFC] placeholder-[#A8B2D1] px-4 py-2 focus:outline-none"
                />
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-6 py-2 bg-gradient-to-r from-[#00E0FF] to-[#33F1FF] text-[#0A0F29] rounded-lg font-semibold shadow-lg hover:shadow-[#00E0FF]/25 transition-all duration-300"
                >
                  Subscribe
                </motion.button>
              </div>
            </motion.div>
          </motion.div>
        </div>
      </section>
      {/* Footer */}
      <footer className="bg-gradient-to-b from-[#0A0F29] to-[#050814] border-t border-white/12 py-12">
        <div className="container mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div>
              <div className="flex items-center mb-4">
                <div className="w-10 h-10 bg-gradient-to-r from-[#00E0FF] to-[#4C5FFF] rounded-lg flex items-center justify-center mr-3 shadow-lg">
                  <Brain className="w-6 h-6 text-white" />
                </div>
                <div>
                  <span className="text-xl font-bold bg-gradient-to-r from-[#F8FAFC] to-[#A8B2D1] bg-clip-text text-transparent">
                    AI Resume Analyzer
                  </span>
                  <div className="text-xs text-[#A8B2D1]">Smart Career Matching</div>
                </div>
              </div>
              <p className="text-[#A8B2D1] mb-4">
                Empowering careers with resume analysis and personalized insights.
              </p>
              
              {/* Social Icons */}
              <div className="flex space-x-4">
                {[
                  { icon: Twitter, href: "#" },
                  { icon: Linkedin, href: "#" },
                  { icon: Github, href: "#" }
                ].map((social, index) => (
                  <motion.a
                    key={index}
                    href={social.href}
                    whileHover={{ scale: 1.1, y: -2 }}
                    className="w-10 h-10 bg-white/5 backdrop-blur-sm border border-white/12 rounded-lg flex items-center justify-center hover:border-[#00E0FF]/30 hover:bg-[#00E0FF]/10 transition-all duration-300"
                  >
                    <social.icon className="w-5 h-5 text-[#A8B2D1] hover:text-[#00E0FF] transition-colors" />
                  </motion.a>
                ))}
              </div>
            </div>
            
            <div>
              <h4 className="font-semibold text-[#F8FAFC] mb-4">Product</h4>
              <ul className="space-y-2 text-[#A8B2D1]">
                <li><Link to="/dashboard" className="hover:text-[#00E0FF] transition-colors">Dashboard</Link></li>
                <li><Link to="/analysis" className="hover:text-[#00E0FF] transition-colors">Analysis</Link></li>
                <li><Link to="/compare" className="hover:text-[#00E0FF] transition-colors">Compare</Link></li>
                <li><a href="#" className="hover:text-[#00E0FF] transition-colors">API</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold text-[#F8FAFC] mb-4">Company</h4>
              <ul className="space-y-2 text-[#A8B2D1]">
                <li><Link to="/about" className="hover:text-[#00E0FF] transition-colors">About</Link></li>
                <li><a href="#" className="hover:text-[#00E0FF] transition-colors">Careers</a></li>
                <li><a href="#" className="hover:text-[#00E0FF] transition-colors">Contact</a></li>
                <li><a href="#" className="hover:text-[#00E0FF] transition-colors">Blog</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold text-[#F8FAFC] mb-4">Support</h4>
              <ul className="space-y-2 text-[#A8B2D1]">
                <li><a href="#" className="hover:text-[#00E0FF] transition-colors">Help Center</a></li>
                <li><a href="#" className="hover:text-[#00E0FF] transition-colors">Privacy Policy</a></li>
                <li><a href="#" className="hover:text-[#00E0FF] transition-colors">Terms of Service</a></li>
                <li><a href="#" className="hover:text-[#00E0FF] transition-colors">Status</a></li>
              </ul>
            </div>
          </div>
          
          {/* Neon Top Border */}
          <div className="border-t border-gradient-to-r from-[#00E0FF]/20 via-[#4C5FFF]/20 to-[#00E0FF]/20 pt-8">
            <div className="flex flex-col md:flex-row justify-between items-center">
              <p className="text-[#A8B2D1] text-sm">
                &copy; 2024 AI Resume Analyzer. All rights reserved.
              </p>
              <div className="flex items-center space-x-4 mt-4 md:mt-0">
                <span className="text-[#A8B2D1] text-sm">Made with</span>
                <motion.div
                  animate={{ scale: [1, 1.2, 1] }}
                  transition={{ duration: 1, repeat: Infinity }}
                >
                  <Heart className="w-5 h-5 text-[#00E0FF] fill-current" />
                </motion.div>
                <span className="text-[#A8B2D1] text-sm">by AI Engineers</span>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing;

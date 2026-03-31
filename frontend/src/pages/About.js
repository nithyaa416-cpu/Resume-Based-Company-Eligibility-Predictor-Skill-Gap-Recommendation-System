import React from 'react';
import { motion } from 'framer-motion';
import { 
  Brain, 
  Target, 
  Users, 
  Award, 
  Zap, 
  Heart,
  Code,
  Database,
  Cpu,
  Globe
} from 'lucide-react';

const About = () => {
  const team = [
    {
      name: "Dr. Sarah Chen",
      role: "AI Research Lead",
      bio: "PhD in Machine Learning from Stanford. Former Google AI researcher specializing in NLP and semantic analysis.",
      avatar: "SC",
      expertise: ["Machine Learning", "NLP", "Deep Learning"]
    },
    {
      name: "Michael Rodriguez",
      role: "Full Stack Engineer",
      bio: "10+ years building scalable web applications. Expert in React, Node.js, and cloud architecture.",
      avatar: "MR",
      expertise: ["React", "Node.js", "AWS"]
    },
    {
      name: "Emily Johnson",
      role: "Product Manager",
      bio: "Former HR executive turned product manager. Deep understanding of recruitment and career development.",
      avatar: "EJ",
      expertise: ["Product Strategy", "UX Design", "HR Tech"]
    },
    {
      name: "David Kim",
      role: "Data Scientist",
      bio: "Specialist in career analytics and predictive modeling. PhD in Statistics from MIT.",
      avatar: "DK",
      expertise: ["Data Science", "Statistics", "Analytics"]
    }
  ];

  const technologies = [
    {
      name: "Sentence-BERT",
      description: "Advanced transformer model for semantic text understanding",
      icon: Brain,
      color: "blue"
    },
    {
      name: "spaCy NLP",
      description: "Industrial-strength natural language processing",
      icon: Code,
      color: "green"
    },
    {
      name: "React 18",
      description: "Modern frontend framework with concurrent features",
      icon: Zap,
      color: "cyan"
    },
    {
      name: "Flask API",
      description: "Lightweight and flexible backend framework",
      icon: Database,
      color: "orange"
    },
    {
      name: "Machine Learning",
      description: "Custom ML models for career prediction and analysis",
      icon: Cpu,
      color: "purple"
    },
    {
      name: "Cloud Infrastructure",
      description: "Scalable and secure cloud-based architecture",
      icon: Globe,
      color: "indigo"
    }
  ];

  const values = [
    {
      title: "Innovation",
      description: "We push the boundaries of AI technology to create breakthrough solutions for career development.",
      icon: Zap
    },
    {
      title: "Accuracy",
      description: "Our ML models are trained on diverse datasets to provide precise and unbiased career insights.",
      icon: Target
    },
    {
      title: "Privacy",
      description: "Your data is encrypted and secure. We never share personal information with third parties.",
      icon: Heart
    },
    {
      title: "Accessibility",
      description: "We believe everyone deserves access to advanced career tools, regardless of background.",
      icon: Users
    }
  ];

  const milestones = [
    {
      year: "2023",
      title: "Company Founded",
      description: "Started with a vision to democratize career insights"
    },
    {
      year: "2023",
      title: "First AI Model",
      description: "Launched our proprietary resume analysis algorithm using Sentence-BERT"
    },
    {
      year: "2024",
      title: "50K+ Users",
      description: "Reached 50,000 professionals using our platform worldwide"
    },
    {
      year: "2024",
      title: "Advanced Features",
      description: "Introduced semantic analysis and personalized learning roadmaps"
    }
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-blue-50 via-white to-purple-50 pt-20 pb-16">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center max-w-4xl mx-auto"
          >
            <h1 className="text-5xl font-bold text-gray-900 mb-6">
              About AI Resume Analyzer
            </h1>
            <p className="text-xl text-gray-600 leading-relaxed">
              We're on a mission to revolutionize career development through cutting-edge AI technology. 
              Our platform empowers professionals worldwide with personalized insights and data-driven career guidance.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
            >
              <h2 className="text-4xl font-bold text-gray-900 mb-6">
                Our Mission
              </h2>
              <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                We believe that everyone deserves access to advanced career insights that were once 
                available only to Fortune 500 companies. Our platform democratizes 
                professional development by providing personalized, actionable recommendations.
              </p>
              <p className="text-lg text-gray-600 leading-relaxed">
                By combining cutting-edge machine learning with deep industry expertise, we help 
                professionals make informed career decisions and achieve their full potential.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="grid grid-cols-2 gap-6"
            >
              <div className="bg-blue-50 p-6 rounded-2xl">
                <Users className="w-8 h-8 text-blue-600 mb-4" />
                <div className="text-2xl font-bold text-gray-900 mb-2">50K+</div>
                <div className="text-gray-600">Professionals Helped</div>
              </div>
              <div className="bg-green-50 p-6 rounded-2xl">
                <Award className="w-8 h-8 text-green-600 mb-4" />
                <div className="text-2xl font-bold text-gray-900 mb-2">95%</div>
                <div className="text-gray-600">Success Rate</div>
              </div>
              <div className="bg-purple-50 p-6 rounded-2xl">
                <Brain className="w-8 h-8 text-purple-600 mb-4" />
                <div className="text-2xl font-bold text-gray-900 mb-2">200+</div>
                <div className="text-gray-600">Companies Analyzed</div>
              </div>
              <div className="bg-orange-50 p-6 rounded-2xl">
                <Target className="w-8 h-8 text-orange-600 mb-4" />
                <div className="text-2xl font-bold text-gray-900 mb-2">4.9/5</div>
                <div className="text-gray-600">User Rating</div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Technology Section */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Powered by Advanced Technology
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our platform leverages state-of-the-art AI and machine learning technologies 
              to provide unprecedented insights into your career potential.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {technologies.map((tech, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-lg transition-all duration-300"
              >
                <div className={`w-12 h-12 bg-${tech.color}-100 rounded-xl flex items-center justify-center mb-6`}>
                  <tech.icon className={`w-6 h-6 text-${tech.color}-600`} />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  {tech.name}
                </h3>
                <p className="text-gray-600">
                  {tech.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

     >

      {/* Values Section */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Our Values
            </h2>
            <p className="text-xl text-gray-600">
              The principles that guide everything we do
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {values.map((value, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="text-center"
              >
                <div className="w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
                  <value.icon className="w-8 h-8 text-blue-600" />
                </div>
                
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  {value.title}
                </h3>
                
                <p className="text-gray-600 leading-relaxed">
                  {value.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="container mx-auto px-4 text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="max-w-3xl mx-auto"
          >
            <h2 className="text-4xl font-bold text-white mb-4">
              Ready to Join Our Mission?
            </h2>
            <p className="text-xl text-blue-100 mb-8">
              Whether you're looking to advance your career or join our team, 
              we'd love to hear from you.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-white text-blue-600 hover:bg-gray-50 font-semibold py-4 px-8 rounded-lg transition-colors duration-200">
                Get Started
              </button>
              <button className="border-2 border-white text-white hover:bg-white hover:text-blue-600 font-semibold py-4 px-8 rounded-lg transition-colors duration-200">
                Contact Us
              </button>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default About;
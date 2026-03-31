import React, { useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import ResumeUpload from "../components/ResumeUpload";
import CompanySelector from "../components/CompanySelector";
import { Brain, Zap, Target, TrendingUp, ChevronRight, Sparkles, FileCheck, Building } from "lucide-react";
import ResumeOptimizer from "../components/ResumeOptimizer";
import { Link } from "react-router-dom";
import toast from "react-hot-toast";

const Dashboard = () => {
  const [resumeData, setResumeData] = useState(null);
  const [selectedCompany, setSelectedCompany] = useState(null);
  const [selectedRole, setSelectedRole] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleUploadSuccess = (data) => { setResumeData(data); };

  const handleCompanySelect = async (company, role, positions) => {
    if (!resumeData) { toast.error("Please upload a resume first"); return; }
    setSelectedCompany(company); setSelectedRole(role); setIsLoading(true);
    try {
      if (company === "all") {
        const response = await fetch("/analyze-all", {
          method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ resume_text: resumeData.resume_text || resumeData.text }),
        });
        const data = await response.json();
        if (data.status === "success") navigate("/analysis", { state: { results: data, type: "multiple" } });
        else toast.error("Error analyzing resume: " + data.message);
      } else if (company.startsWith("category:") || company === "selected") {
        const positionsToAnalyze = positions || [];
        if (!positionsToAnalyze.length) { toast.error("No companies to analyze"); setIsLoading(false); return; }
        const results = [];
        for (const pos of positionsToAnalyze.slice(0, 20)) {
          try {
            const res = await fetch("/ml-analyze", {
              method: "POST", headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ resume_text: resumeData.resume_text || resumeData.text, company: pos.company, role: pos.role }),
            });
            const d = await res.json();
            if (d.status === "success") results.push({ company: pos.company, role: pos.role, ml_analysis: d.ml_analysis });
          } catch (_) {}
        }
        if (results.length > 0) navigate("/analysis", { state: { results: { company_analysis: results, total_positions: results.length, status: "success" }, type: "multiple" } });
        else toast.error("Analysis failed. Please try again.");
      } else {
        const response = await fetch("/ml-analyze", {
          method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ resume_text: resumeData.resume_text || resumeData.text, company, role }),
        });
        const data = await response.json();
        if (data.status === "success") navigate("/analysis", { state: { results: data, type: "single" } });
        else toast.error("Error analyzing resume: " + data.message);
      }
    } catch (error) { toast.error("Error analyzing resume: " + error.message); }
    finally { setIsLoading(false); }
  };

  const features = [
    { icon: Zap, label: "Smart Analysis", desc: "Instant resume-to-role matching", color: "from-blue-500 to-blue-600", bg: "bg-blue-50", iconColor: "text-blue-600" },
    { icon: Target, label: "Skill Matching", desc: "Gap analysis & recommendations", color: "from-violet-500 to-violet-600", bg: "bg-violet-50", iconColor: "text-violet-600" },
    { icon: TrendingUp, label: "Career Insights", desc: "Personalized learning roadmaps", color: "from-emerald-500 to-emerald-600", bg: "bg-emerald-50", iconColor: "text-emerald-600" },
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-8 pb-12">

      {/* Hero Banner */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}
        className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-blue-600 via-blue-700 to-violet-700 p-8 md:p-12 text-white shadow-2xl shadow-blue-200">
        <div className="absolute inset-0 opacity-10" style={{ backgroundImage: "radial-gradient(circle at 20% 50%, white 1px, transparent 1px), radial-gradient(circle at 80% 20%, white 1px, transparent 1px)", backgroundSize: "40px 40px" }} />
        <div className="relative z-10 flex flex-col md:flex-row md:items-center md:justify-between gap-6">
          <div>
            <div className="flex items-center gap-3 mb-3">
              <div className="w-12 h-12 bg-white/20 backdrop-blur rounded-2xl flex items-center justify-center">
                <Brain className="w-6 h-6 text-white" />
              </div>
              <span className="text-blue-200 text-sm font-semibold tracking-wide uppercase">AI Resume Analyzer</span>
            </div>
            <h1 className="text-3xl md:text-4xl font-extrabold mb-2 leading-tight">
              Find Your Perfect<br />Career Match
            </h1>
            <p className="text-blue-100 text-base max-w-lg">
              Upload your resume, select companies, and get instant eligibility scores with personalized learning roadmaps.
            </p>
          </div>
          <div className="flex flex-col gap-3 min-w-fit">
            {resumeData ? (
              <div className="bg-white/15 backdrop-blur rounded-2xl p-4 border border-white/20">
                <div className="flex items-center gap-2 mb-2">
                  <FileCheck className="w-5 h-5 text-emerald-300" />
                  <span className="text-sm font-semibold text-emerald-200">Resume Ready</span>
                </div>
                <p className="text-white/80 text-xs">{resumeData.filename || "Text Input"}</p>
                <p className="text-white font-bold text-lg mt-1">{resumeData.skills_found || 0} skills detected</p>
              </div>
            ) : (
              <div className="bg-white/10 backdrop-blur rounded-2xl p-4 border border-white/20 text-center">
                <Sparkles className="w-8 h-8 text-yellow-300 mx-auto mb-2" />
                <p className="text-white/80 text-sm">Upload your resume to get started</p>
              </div>
            )}
          </div>
        </div>

        {/* Feature pills */}
        <div className="relative z-10 flex flex-wrap gap-2 mt-6">
          {features.map(f => (
            <div key={f.label} className="flex items-center gap-2 bg-white/10 backdrop-blur px-3 py-1.5 rounded-full border border-white/20">
              <f.icon className="w-3.5 h-3.5 text-white" />
              <span className="text-white text-xs font-medium">{f.label}</span>
            </div>
          ))}
          <div className="flex items-center gap-2 bg-emerald-400/20 backdrop-blur px-3 py-1.5 rounded-full border border-emerald-300/30">
            <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
            <span className="text-emerald-200 text-xs font-medium">Live Job Data Active</span>
          </div>
        </div>
      </motion.div>

      {/* Real-time notice */}
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }}
        className="flex items-center justify-between bg-white rounded-2xl border border-gray-100 shadow-sm px-5 py-3.5">
        <div className="flex items-center gap-3">
          <div className="w-2.5 h-2.5 bg-emerald-500 rounded-full animate-pulse" />
          <div>
            <span className="font-semibold text-gray-900 text-sm">Real-time Job Data Active</span>
            <p className="text-gray-500 text-xs">Analyzing 60+ companies with current market requirements</p>
          </div>
        </div>
        <Link to="/job-data" className="flex items-center gap-1 text-blue-600 hover:text-blue-700 text-sm font-semibold transition-colors">
          View Details <ChevronRight className="w-4 h-4" />
        </Link>
      </motion.div>

      {/* Main Two-Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

        {/* Left — Resume Upload */}
        <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.5, delay: 0.2 }}>
          <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden h-full">
            <div className="px-6 py-5 border-b border-gray-100 flex items-center gap-3">
              <div className="w-9 h-9 bg-gradient-to-br from-blue-500 to-violet-600 rounded-xl flex items-center justify-center shadow-md shadow-blue-200">
                <Brain className="w-5 h-5 text-white" />
              </div>
              <div>
                <h2 className="font-bold text-gray-900">Upload Your Resume</h2>
                <p className="text-xs text-gray-500">PDF or DOCX · Max 10MB</p>
              </div>
              {resumeData && (
                <span className="ml-auto flex items-center gap-1.5 text-xs font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 px-2.5 py-1 rounded-full">
                  <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full" /> Ready
                </span>
              )}
            </div>
            <div className="p-6">
              <ResumeUpload onUploadSuccess={handleUploadSuccess} isLoading={isLoading} setIsLoading={setIsLoading} />
            </div>
          </div>
        </motion.div>

        {/* Right — Company Selection */}
        <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.5, delay: 0.3 }}>
          <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden h-full">
            <div className="px-6 py-5 border-b border-gray-100 flex items-center gap-3">
              <div className="w-9 h-9 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-xl flex items-center justify-center shadow-md shadow-emerald-200">
                <Building className="w-5 h-5 text-white" />
              </div>
              <div>
                <h2 className="font-bold text-gray-900">Select Companies</h2>
                <p className="text-xs text-gray-500">Search, filter, and analyze by role or category</p>
              </div>
            </div>
            <div className="p-6 max-h-[680px] overflow-y-auto">
              <CompanySelector
                selectedCompany={selectedCompany}
                selectedRole={selectedRole}
                onCompanySelect={handleCompanySelect}
                resumeData={resumeData}
              />
            </div>
          </div>
        </motion.div>
      </div>

      {/* Resume Stats (after upload) */}
      {resumeData && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}
          className="grid grid-cols-3 gap-4">
          {[
            { label: "Skills Detected", value: resumeData.skills_found || resumeData.ml_analysis?.total_skills_found || 0, color: "text-blue-600", bg: "bg-blue-50", border: "border-blue-100" },
            { label: "Characters Analyzed", value: (resumeData.text_length || resumeData.resume_text?.length || 0).toLocaleString(), color: "text-violet-600", bg: "bg-violet-50", border: "border-violet-100" },
            { label: "Source", value: resumeData.filename || "Text Input", color: "text-emerald-600", bg: "bg-emerald-50", border: "border-emerald-100" },
          ].map(stat => (
            <div key={stat.label} className={"rounded-2xl border p-5 " + stat.bg + " " + stat.border}>
              <p className={"text-xl font-extrabold truncate " + stat.color}>{stat.value}</p>
              <p className="text-xs text-gray-500 mt-1 font-medium">{stat.label}</p>
            </div>
          ))}
        </motion.div>
      )}

      {/* Resume Optimizer */}
      {resumeData && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay: 0.1 }}
          className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
          <ResumeOptimizer resumeData={resumeData} targetRole={selectedRole} />
        </motion.div>
      )}

      {/* Loading Overlay */}
      {isLoading && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
          className="fixed inset-0 bg-gray-900/60 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-white rounded-3xl shadow-2xl p-10 text-center max-w-sm mx-4">
            <div className="relative w-16 h-16 mx-auto mb-5">
              <div className="absolute inset-0 rounded-full border-4 border-blue-100" />
              <div className="absolute inset-0 rounded-full border-4 border-blue-600 border-t-transparent animate-spin" />
              <Brain className="absolute inset-0 m-auto w-7 h-7 text-blue-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-1">Analyzing Resume</h3>
            <p className="text-gray-500 text-sm">Matching your profile with companies...</p>
            <div className="mt-4 h-1.5 bg-gray-100 rounded-full overflow-hidden">
              <div className="h-full bg-gradient-to-r from-blue-500 to-violet-500 rounded-full animate-pulse" style={{ width: "70%" }} />
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default Dashboard;
import React, { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Building2, Search, Briefcase, ChevronDown, ChevronUp,
  Layers, Globe, Rocket, BarChart2, Filter, Zap, X,
  Star, TrendingUp, SlidersHorizontal
} from "lucide-react";
import toast from "react-hot-toast";

const CATEGORIES = {
  "MNC / Big Tech": {
    Icon: Globe, bg: "bg-blue-50", border: "border-blue-300", text: "text-blue-700",
    badge: "bg-blue-100 text-blue-700", btn: "bg-blue-600 hover:bg-blue-700", iconCls: "text-blue-500",
    keywords: ["google","microsoft","amazon","apple","meta","netflix","ibm","oracle","sap","intel","cisco","adobe","salesforce","uber","airbnb","spotify","paypal","nvidia","twitter","linkedin"]
  },
  "Product Based": {
    Icon: Zap, bg: "bg-purple-50", border: "border-purple-300", text: "text-purple-700",
    badge: "bg-purple-100 text-purple-700", btn: "bg-purple-600 hover:bg-purple-700", iconCls: "text-purple-500",
    keywords: ["flipkart","swiggy","zomato","paytm","ola","byju","razorpay","freshworks","zoho","phonepe","cred","meesho","dream11","nykaa","lenskart","dunzo"]
  },
  "Service Based": {
    Icon: Layers, bg: "bg-green-50", border: "border-green-300", text: "text-green-700",
    badge: "bg-green-100 text-green-700", btn: "bg-green-600 hover:bg-green-700", iconCls: "text-green-500",
    keywords: ["tcs","infosys","wipro","hcl","tech mahindra","cognizant","capgemini","mphasis","hexaware","mindtree","zensar","persistent","cyient","niit","mastech"]
  },
  "Consulting": {
    Icon: BarChart2, bg: "bg-orange-50", border: "border-orange-300", text: "text-orange-700",
    badge: "bg-orange-100 text-orange-700", btn: "bg-orange-600 hover:bg-orange-700", iconCls: "text-orange-500",
    keywords: ["accenture","deloitte","mckinsey","bcg","bain","kpmg","pwc","ey","ernst","gartner","mu sigma","fractal","tiger analytics"]
  },
  "Startups": {
    Icon: Rocket, bg: "bg-pink-50", border: "border-pink-300", text: "text-pink-700",
    badge: "bg-pink-100 text-pink-700", btn: "bg-pink-600 hover:bg-pink-700", iconCls: "text-pink-500",
    keywords: []
  }
};

const TIER_MAP = {
  1: ["google","microsoft","amazon","apple","meta","netflix","uber","airbnb","nvidia","salesforce","adobe","oracle"],
  2: ["flipkart","swiggy","zomato","paytm","razorpay","freshworks","zoho","phonepe","accenture","cognizant","capgemini","infosys","wipro","tcs","hcl"],
  3: []
};

const ROLE_SUGGESTIONS = [
  "Software Engineer","Data Scientist","ML Engineer","AI Engineer",
  "Frontend Developer","Backend Developer","Full Stack Developer",
  "Data Analyst","DevOps Engineer","Cloud Engineer","Product Manager",
  "Business Analyst","Java Developer","Python Developer","React Developer"
];

const WORK_TYPES = ["Remote","Hybrid","Onsite"];
const EXP_LEVELS = ["Fresher (0-1 yrs)","Entry Level (1-3 yrs)","Mid Level (3-5 yrs)"];

function getCategory(name) {
  const lower = name.toLowerCase();
  for (const [cat, cfg] of Object.entries(CATEGORIES)) {
    if (cat === "Startups") continue;
    if (cfg.keywords.some(k => lower.includes(k))) return cat;
  }
  return "Startups";
}

function getTier(name) {
  const lower = name.toLowerCase();
  if (TIER_MAP[1].some(k => lower.includes(k))) return 1;
  if (TIER_MAP[2].some(k => lower.includes(k))) return 2;
  return 3;
}

function groupByCategory(positions) {
  const groups = {};
  Object.keys(CATEGORIES).forEach(cat => { groups[cat] = []; });
  positions.forEach(pos => { groups[getCategory(pos.company)].push(pos); });
  return groups;
}

export default function CompanySelector({ onCompanySelect, resumeData }) {
  const [allPositions, setAllPositions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [roleSearch, setRoleSearch] = useState("");
  const [companySearch, setCompanySearch] = useState("");
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [showFilters, setShowFilters] = useState(false);
  const [filterCat, setFilterCat] = useState("All");
  const [filterWorkType, setFilterWorkType] = useState("All");
  const [filterExp, setFilterExp] = useState("All");
  const [filterTier, setFilterTier] = useState("All");
  const [expanded, setExpanded] = useState({ "MNC / Big Tech": true });
  const [checked, setChecked] = useState([]);
  const searchRef = useRef(null);

  useEffect(() => {
    fetch("/companies-with-roles")
      .then(r => r.json())
      .then(data => {
        if (data.status === "success") setAllPositions(data.companies_with_roles || []);
        else toast.error("Failed to load companies");
      })
      .catch(e => toast.error("Error: " + e.message))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    const handler = (e) => { if (searchRef.current && !searchRef.current.contains(e.target)) setShowSuggestions(false); };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  const roleSuggestions = roleSearch.length > 0
    ? ROLE_SUGGESTIONS.filter(r => r.toLowerCase().includes(roleSearch.toLowerCase()) && r.toLowerCase() !== roleSearch.toLowerCase())
    : [];

  const applyFilters = (positions) => {
    return positions.filter(pos => {
      const matchRole = !roleSearch || pos.role.toLowerCase().includes(roleSearch.toLowerCase());
      const matchCompany = !companySearch || pos.company.toLowerCase().includes(companySearch.toLowerCase());
      const matchCat = filterCat === "All" || getCategory(pos.company) === filterCat;
      const matchTier = filterTier === "All" || getTier(pos.company) === parseInt(filterTier);
      return matchRole && matchCompany && matchCat && matchTier;
    });
  };

  const filteredPositions = applyFilters(allPositions);
  const grouped = groupByCategory(filteredPositions);

  const visibleGrouped = () => {
    const result = {};
    Object.entries(grouped).forEach(([cat, positions]) => {
      if (positions.length > 0) result[cat] = positions;
    });
    return result;
  };

  const activeFiltersCount = [
    filterCat !== "All", filterWorkType !== "All",
    filterExp !== "All", filterTier !== "All"
  ].filter(Boolean).length;

  const clearFilters = () => {
    setFilterCat("All"); setFilterWorkType("All");
    setFilterExp("All"); setFilterTier("All");
    setRoleSearch(""); setCompanySearch("");
  };

  const toggleExpand = cat => setExpanded(prev => ({ ...prev, [cat]: !prev[cat] }));
  const posKey = pos => pos.company + "||" + pos.role;
  const isChecked = pos => checked.includes(posKey(pos));
  const toggleCheck = pos => {
    const k = posKey(pos);
    setChecked(prev => prev.includes(k) ? prev.filter(x => x !== k) : [...prev, k]);
  };

  const guard = () => {
    if (!resumeData) { toast.error("Please upload a resume first"); return false; }
    return true;
  };

  const analyzeAll = () => { if (!guard()) return; onCompanySelect("all"); };
  const analyzeRole = () => {
    if (!guard()) return;
    if (!roleSearch) { toast.error("Enter a role to search"); return; }
    const positions = filteredPositions;
    if (!positions.length) { toast.error("No companies found for this role"); return; }
    onCompanySelect("selected", null, positions);
  };
  const analyzeCategory = cat => {
    if (!guard()) return;
    const positions = grouped[cat] || [];
    if (!positions.length) return;
    onCompanySelect("category:" + cat, null, positions);
  };
  const analyzeSelected = () => {
    if (!guard()) return;
    if (!checked.length) { toast.error("Select at least one company"); return; }
    const positions = checked.map(k => { const [company, role] = k.split("||"); return { company, role }; });
    onCompanySelect("selected", null, positions);
  };
  const analyzeFiltered = () => {
    if (!guard()) return;
    if (!filteredPositions.length) { toast.error("No companies match current filters"); return; }
    onCompanySelect("selected", null, filteredPositions);
  };
  const analyzeSingle = pos => { if (!guard()) return; onCompanySelect(pos.company, pos.role); };

  const visible = visibleGrouped();
  const totalVisible = filteredPositions.length;
  const uniqueCompanies = [...new Set(filteredPositions.map(p => p.company))].length;

  if (loading) return (
    <div className="flex items-center justify-center py-16">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mr-3"></div>
      <span className="text-gray-500">Loading companies...</span>
    </div>
  );

  return (
    <div className="space-y-4">

      {/* Role Search Bar */}
      <div ref={searchRef} className="relative">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-4 h-4" />
          <input
            type="text"
            placeholder="Search role: Software Engineer, Data Scientist..."
            value={roleSearch}
            onChange={e => { setRoleSearch(e.target.value); setShowSuggestions(true); }}
            onFocus={() => setShowSuggestions(true)}
            className="w-full pl-9 pr-10 py-3 border-2 border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-400 outline-none transition-all"
          />
          {roleSearch && (
            <button onClick={() => { setRoleSearch(""); setShowSuggestions(false); }}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
              <X className="w-4 h-4" />
            </button>
          )}
        </div>

        {/* Autocomplete Suggestions */}
        <AnimatePresence>
          {showSuggestions && roleSuggestions.length > 0 && (
            <motion.div initial={{ opacity: 0, y: -5 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -5 }}
              className="absolute z-20 w-full mt-1 bg-white border border-gray-200 rounded-xl shadow-lg overflow-hidden">
              {roleSuggestions.slice(0, 6).map(s => (
                <button key={s} onClick={() => { setRoleSearch(s); setShowSuggestions(false); }}
                  className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-700 flex items-center gap-2 transition-colors">
                  <Search className="w-3 h-3 text-gray-400" /> {s}
                </button>
              ))}
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Role-based Analyze Buttons */}
      {roleSearch && (
        <motion.div initial={{ opacity: 0, y: -5 }} animate={{ opacity: 1, y: 0 }}
          className="bg-blue-50 border border-blue-200 rounded-xl p-4 space-y-2">
          <div className="flex items-center gap-2 mb-3">
            <TrendingUp className="w-4 h-4 text-blue-600" />
            <span className="text-sm font-semibold text-blue-800">
              {totalVisible} positions found for "{roleSearch}" across {uniqueCompanies} companies
            </span>
          </div>
          <div className="flex flex-wrap gap-2">
            <button onClick={analyzeRole}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold rounded-lg transition-colors">
              <Zap className="w-3.5 h-3.5" /> Analyze Resume for "{roleSearch}"
            </button>
            {checked.length > 0 && (
              <button onClick={analyzeSelected}
                className="flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white text-sm font-semibold rounded-lg transition-colors">
                Analyze {roleSearch} at Selected ({checked.length})
              </button>
            )}
          </div>
        </motion.div>
      )}

      {/* Company Search + Filter Toggle */}
      <div className="flex gap-2">
        <div className="relative flex-1">
          <Building2 className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-4 h-4" />
          <input type="text" placeholder="Filter by company name..."
            value={companySearch} onChange={e => setCompanySearch(e.target.value)}
            className="w-full pl-9 pr-4 py-2.5 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
        </div>
        <button onClick={() => setShowFilters(!showFilters)}
          className={"flex items-center gap-2 px-4 py-2.5 border-2 rounded-lg text-sm font-medium transition-colors " +
            (showFilters || activeFiltersCount > 0 ? "border-blue-400 bg-blue-50 text-blue-700" : "border-gray-200 text-gray-600 hover:border-gray-300")}>
          <SlidersHorizontal className="w-4 h-4" />
          Filters {activeFiltersCount > 0 && <span className="bg-blue-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">{activeFiltersCount}</span>}
        </button>
      </div>

      {/* Smart Filters Panel */}
      <AnimatePresence>
        {showFilters && (
          <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }} transition={{ duration: 0.2 }}
            className="bg-gray-50 border border-gray-200 rounded-xl p-4 space-y-4">
            <div className="flex items-center justify-between mb-1">
              <span className="text-sm font-semibold text-gray-700 flex items-center gap-2"><Filter className="w-4 h-4" /> Smart Filters</span>
              {activeFiltersCount > 0 && <button onClick={clearFilters} className="text-xs text-red-500 hover:text-red-600 font-medium">Clear all</button>}
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5 block">Company Category</label>
                <select value={filterCat} onChange={e => setFilterCat(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm bg-white focus:ring-2 focus:ring-blue-500 outline-none">
                  <option value="All">All Categories</option>
                  {Object.keys(CATEGORIES).map(c => <option key={c} value={c}>{c}</option>)}
                </select>
              </div>
              <div>
                <label className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5 block">Company Tier</label>
                <select value={filterTier} onChange={e => setFilterTier(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm bg-white focus:ring-2 focus:ring-blue-500 outline-none">
                  <option value="All">All Tiers</option>
                  <option value="1">Tier 1 (Google, Amazon...)</option>
                  <option value="2">Tier 2</option>
                  <option value="3">Tier 3</option>
                </select>
              </div>
              <div>
                <label className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5 block">Experience Level</label>
                <select value={filterExp} onChange={e => setFilterExp(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm bg-white focus:ring-2 focus:ring-blue-500 outline-none">
                  <option value="All">All Levels</option>
                  {EXP_LEVELS.map(e => <option key={e} value={e}>{e}</option>)}
                </select>
              </div>
              <div>
                <label className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5 block">Work Type</label>
                <select value={filterWorkType} onChange={e => setFilterWorkType(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm bg-white focus:ring-2 focus:ring-blue-500 outline-none">
                  <option value="All">All Types</option>
                  {WORK_TYPES.map(w => <option key={w} value={w}>{w}</option>)}
                </select>
              </div>
            </div>
            {activeFiltersCount > 0 && (
              <button onClick={analyzeFiltered}
                className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold rounded-lg transition-colors flex items-center justify-center gap-2">
                <Zap className="w-4 h-4" /> Analyze All Filtered Companies ({totalVisible})
              </button>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Stats + Global Actions */}
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-3">
          <span className="text-xs text-gray-500 bg-gray-100 px-3 py-1.5 rounded-full">
            <span className="font-semibold text-gray-700">{totalVisible}</span> positions · <span className="font-semibold text-gray-700">{uniqueCompanies}</span> companies
          </span>
          {checked.length > 0 && (
            <span className="text-xs text-green-700 bg-green-100 px-3 py-1.5 rounded-full font-medium">
              {checked.length} selected
            </span>
          )}
        </div>
        <div className="flex gap-2">
          <button onClick={analyzeAll}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg transition-colors">
            <Zap className="w-3.5 h-3.5" /> Analyze All
          </button>
          {checked.length > 0 && (
            <motion.button initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }}
              onClick={analyzeSelected}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-green-600 hover:bg-green-700 text-white text-xs font-semibold rounded-lg transition-colors">
              Analyze Selected ({checked.length})
            </motion.button>
          )}
          {checked.length > 0 && (
            <button onClick={() => setChecked([])} className="px-3 py-1.5 text-xs text-red-500 border border-red-200 rounded-lg hover:bg-red-50">Clear</button>
          )}
        </div>
      </div>

      {/* Category Sections */}
      <div className="space-y-3">
        {Object.entries(visible).map(([cat, positions]) => {
          const cfg = CATEGORIES[cat];
          const CatIcon = cfg.Icon;
          const isOpen = expanded[cat];
          const checkedInCat = positions.filter(p => isChecked(p)).length;
          return (
            <div key={cat} className={"border-2 " + cfg.border + " rounded-xl overflow-hidden"}>
              <div className={"px-5 py-4 flex items-center justify-between " + cfg.bg}>
                <button onClick={() => toggleExpand(cat)} className="flex items-center gap-3 flex-1 text-left">
                  <div className="w-9 h-9 bg-white rounded-lg flex items-center justify-center shadow-sm flex-shrink-0">
                    <CatIcon className={"w-5 h-5 " + cfg.iconCls} />
                  </div>
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="font-semibold text-gray-900">{cat}</span>
                    <span className={"text-xs px-2 py-0.5 rounded-full font-medium " + cfg.badge}>{positions.length} companies</span>
                    {checkedInCat > 0 && <span className="text-xs px-2 py-0.5 rounded-full font-medium bg-green-100 text-green-700">{checkedInCat} selected</span>}
                  </div>
                  <span className="ml-1 flex-shrink-0">{isOpen ? <ChevronUp className="w-4 h-4 text-gray-500" /> : <ChevronDown className="w-4 h-4 text-gray-500" />}</span>
                </button>
                <button onClick={() => analyzeCategory(cat)}
                  className={"ml-3 px-3 py-1.5 text-white text-xs font-semibold rounded-lg transition-colors whitespace-nowrap " + cfg.btn}>
                  Analyze All
                </button>
              </div>

              <AnimatePresence>
                {isOpen && (
                  <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: "auto", opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.2 }}
                    className="bg-white divide-y divide-gray-100">
                    {positions.map((pos, idx) => {
                      const tier = getTier(pos.company);
                      return (
                        <div key={pos.company + pos.role + idx}
                          className={"flex items-center px-5 py-3.5 hover:bg-gray-50 transition-colors " + (isChecked(pos) ? "bg-blue-50" : "")}>
                          <button onClick={() => toggleCheck(pos)}
                            className="mr-4 flex-shrink-0 w-5 h-5 rounded border-2 flex items-center justify-center transition-all"
                            style={{ borderColor: isChecked(pos) ? "#3b82f6" : "#d1d5db", backgroundColor: isChecked(pos) ? "#3b82f6" : "white" }}>
                            {isChecked(pos) && <span className="text-white text-xs font-bold">✓</span>}
                          </button>
                          <div className={"w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 mr-3 font-bold text-base " + cfg.bg + " " + cfg.text}>
                            {pos.company.charAt(0).toUpperCase()}
                          </div>
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2 flex-wrap">
                              <p className="font-semibold text-gray-900 text-sm">{pos.company}</p>
                              {tier === 1 && <span className="flex items-center gap-0.5 text-xs text-yellow-600 bg-yellow-50 px-1.5 py-0.5 rounded font-medium"><Star className="w-3 h-3" />Tier 1</span>}
                              {tier === 2 && <span className="text-xs text-gray-500 bg-gray-100 px-1.5 py-0.5 rounded font-medium">Tier 2</span>}
                            </div>
                            <div className="flex items-center gap-2 mt-0.5 flex-wrap">
                              <Briefcase className="w-3 h-3 text-gray-400 flex-shrink-0" />
                              <span className="text-xs text-gray-600 font-medium">{pos.role}</span>
                              <span className={"text-xs px-1.5 py-0.5 rounded font-medium " + cfg.badge}>{cat}</span>
                            </div>
                          </div>
                          <button onClick={() => analyzeSingle(pos)}
                            className="ml-3 px-3 py-1.5 text-xs font-semibold text-blue-600 hover:bg-blue-50 border border-blue-200 rounded-lg transition-colors whitespace-nowrap">
                            Analyze
                          </button>
                        </div>
                      );
                    })}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          );
        })}
      </div>

      {totalVisible === 0 && (
        <div className="text-center py-12">
          <Building2 className="w-12 h-12 text-gray-300 mx-auto mb-3" />
          <p className="text-gray-600 font-medium">No companies found</p>
          <p className="text-gray-400 text-sm mt-1">Try adjusting your search or filters</p>
          {activeFiltersCount > 0 && (
            <button onClick={clearFilters} className="mt-3 text-sm text-blue-600 hover:text-blue-700 font-medium">Clear all filters</button>
          )}
        </div>
      )}

      <p className="text-xs text-gray-400 text-center pt-1">
        Tip: Use checkboxes to select companies, then click "Analyze Selected"
      </p>
    </div>
  );
}

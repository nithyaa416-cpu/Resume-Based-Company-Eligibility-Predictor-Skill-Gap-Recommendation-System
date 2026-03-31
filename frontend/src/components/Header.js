import React, { useState, useEffect } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { Brain, BarChart3, GitCompare, LogOut, Menu, X, LayoutDashboard } from "lucide-react";
import toast from "react-hot-toast";
import { getCurrentUser, clearCurrentUser } from "../utils/auth";
import ThemeToggle from "./ThemeToggle";

const Header = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [hasResults, setHasResults] = useState(false);

  useEffect(() => { setUser(getCurrentUser()); }, []);

  // Re-check sessionStorage on every route change
  useEffect(() => {
    setHasResults(!!sessionStorage.getItem('lastAnalysisResults'));
  }, [location.pathname]);

  const handleLogout = () => {
    clearCurrentUser(); setUser(null);
    toast.success("Logged out successfully"); navigate("/");
  };

  const navItems = user ? [
    { path: "/", label: "Home", icon: null },
    { path: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
    ...(hasResults ? [{ path: "/analysis", label: "Last Results", icon: BarChart3 }] : []),
    { path: "/compare", label: "Compare Resumes", icon: GitCompare },
  ] : [
    { path: "/about", label: "About", icon: null },
  ];

  return (
    <header className="bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl border-b border-gray-100 dark:border-gray-800 sticky top-0 z-50 transition-colors duration-300">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">

          {/* Logo */}
          <Link to="/" className="flex items-center gap-3 group">
            <div className="w-9 h-9 bg-gradient-to-br from-blue-600 to-violet-600 rounded-xl flex items-center justify-center shadow-md shadow-blue-200 group-hover:shadow-lg group-hover:shadow-blue-300 transition-all duration-200">
              <Brain className="w-5 h-5 text-white" />
            </div>
            <div className="hidden sm:block">
              <p className="text-sm font-bold text-gray-900 dark:text-white leading-tight">AI Resume Analyzer</p>
              <p className="text-xs text-gray-400 dark:text-gray-500 leading-tight">Smart Career Matching</p>
            </div>
          </Link>

          {/* Desktop Nav */}
          <nav className="hidden md:flex items-center gap-1">
            {navItems.map(({ path, label, icon: Icon }) => {
              const active = location.pathname === path;
              return (
                <Link key={path} to={path}
                  className={"flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 " +
                    (active ? "bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400" :
                     "text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-50 dark:hover:bg-gray-800")}>
                  {Icon && <Icon className="w-4 h-4" />}
                  {label}
                  {active && <span className="w-1.5 h-1.5 bg-blue-500 rounded-full" />}
                </Link>
              );
            })}
          </nav>

          {/* Desktop Right */}
          <div className="hidden md:flex items-center gap-3">
            <ThemeToggle />
            {user ? (
              <div className="flex items-center gap-2">
                <div className="flex items-center gap-2.5 px-3 py-2 bg-gray-50 dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700">
                  <div className="w-7 h-7 bg-gradient-to-br from-blue-500 to-violet-600 rounded-lg flex items-center justify-center text-white text-xs font-bold">
                    {user.name?.charAt(0) || "U"}
                  </div>
                  <div className="text-xs">
                    <p className="font-semibold text-gray-900 dark:text-white leading-tight">{user.name}</p>
                    <p className="text-gray-400 dark:text-gray-500 leading-tight">{user.jobTitle}</p>
                  </div>
                </div>
                <button onClick={handleLogout}
                  className="flex items-center gap-1.5 px-3 py-2 text-sm text-gray-500 dark:text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-xl transition-all duration-200">
                  <LogOut className="w-4 h-4" /> Logout
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link to="/login" className="text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white px-4 py-2 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-800 transition-all">Sign In</Link>
                <Link to="/register" className="btn-primary text-sm">Get Started</Link>
              </div>
            )}
          </div>

          {/* Mobile toggle */}
          <div className="md:hidden flex items-center gap-2">
            <ThemeToggle />
            <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="p-2 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
              {isMobileMenuOpen ? <X className="w-5 h-5 text-gray-600 dark:text-gray-300" /> : <Menu className="w-5 h-5 text-gray-600 dark:text-gray-300" />}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMobileMenuOpen && (
          <div className="md:hidden border-t border-gray-100 dark:border-gray-800 py-4 space-y-1">
            {navItems.map(({ path, label, icon: Icon }) => (
              <Link key={path} to={path} onClick={() => setIsMobileMenuOpen(false)}
                className={"flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all " +
                  (location.pathname === path ? "bg-blue-50 dark:bg-blue-900/30 text-blue-600" : "text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800")}>
                {Icon && <Icon className="w-4 h-4" />} {label}
              </Link>
            ))}
            <div className="pt-3 border-t border-gray-100 dark:border-gray-800 mt-2">
              {user ? (
                <div className="space-y-2">
                  <div className="flex items-center gap-3 px-4 py-2">
                    <div className="w-9 h-9 bg-gradient-to-br from-blue-500 to-violet-600 rounded-xl flex items-center justify-center text-white font-bold text-sm">{user.name?.charAt(0) || "U"}</div>
                    <div><p className="font-semibold text-gray-900 dark:text-white text-sm">{user.name}</p><p className="text-gray-400 text-xs">{user.jobTitle}</p></div>
                  </div>
                  <button onClick={() => { handleLogout(); setIsMobileMenuOpen(false); }}
                    className="w-full flex items-center gap-3 px-4 py-3 text-red-600 hover:bg-red-50 rounded-xl transition-colors text-sm font-medium">
                    <LogOut className="w-4 h-4" /> Logout
                  </button>
                </div>
              ) : (
                <div className="space-y-2 px-2">
                  <Link to="/login" onClick={() => setIsMobileMenuOpen(false)} className="block w-full text-center py-2.5 text-sm font-medium text-gray-600 hover:bg-gray-50 rounded-xl transition-colors">Sign In</Link>
                  <Link to="/register" onClick={() => setIsMobileMenuOpen(false)} className="btn-primary w-full text-sm">Get Started</Link>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
import axios from 'axios';

// Configure base URL - update this to match your backend
const BASE_URL = 'http://localhost:5000'; // Change to your backend URL

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    // Token will be added by individual API calls
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    if (error.response) {
      // Server responded with error status
      return Promise.reject(error.response.data);
    } else if (error.request) {
      // Request was made but no response received
      return Promise.reject({ error: 'Network error. Please check your connection.' });
    } else {
      // Something else happened
      return Promise.reject({ error: 'An unexpected error occurred.' });
    }
  }
);

// Authentication API
export const authAPI = {
  login: (email, password) => 
    api.post('/auth/login', { email, password }),
  
  register: (email, password, firstName, lastName) => 
    api.post('/auth/register', { email, password, first_name: firstName, last_name: lastName }),
  
  updateProfile: (profileData, token) => 
    api.put('/auth/profile', profileData, {
      headers: { Authorization: `Bearer ${token}` }
    }),
  
  getProfile: (token) => 
    api.get('/auth/profile', {
      headers: { Authorization: `Bearer ${token}` }
    }),
};

// Resume API
export const resumeAPI = {
  uploadResume: (formData, token) => 
    api.post('/upload', formData, {
      headers: { 
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    }),
  
  analyzeResume: (resumeText, companyName, jobRole, token) => 
    api.post('/ml-analyze', { 
      resume_text: resumeText, 
      company_name: companyName, 
      job_role: jobRole 
    }, {
      headers: { Authorization: `Bearer ${token}` }
    }),
  
  analyzeAllCompanies: (resumeText, token) => 
    api.post('/analyze-all', { resume_text: resumeText }, {
      headers: { Authorization: `Bearer ${token}` }
    }),
  
  getRecommendations: (resumeText, companyName, token) => 
    api.post('/recommendations', { 
      resume_text: resumeText, 
      company_name: companyName 
    }, {
      headers: { Authorization: `Bearer ${token}` }
    }),
  
  optimizeResume: (resumeText, token) => 
    api.post('/optimize-resume', { resume_text: resumeText }, {
      headers: { Authorization: `Bearer ${token}` }
    }),
  
  getATSScore: (resumeText, token) => 
    api.post('/ats-score', { resume_text: resumeText }, {
      headers: { Authorization: `Bearer ${token}` }
    }),
};

// Company API
export const companyAPI = {
  getAllCompanies: () => api.get('/companies'),
  
  getCompaniesWithRoles: () => api.get('/companies-with-roles'),
  
  getJobDataStats: () => api.get('/job-data/stats'),
};

// History API
export const historyAPI = {
  getUserHistory: (token) => 
    api.get('/history', {
      headers: { Authorization: `Bearer ${token}` }
    }),
  
  getAnalysisTrends: (token) => 
    api.get('/history/trends', {
      headers: { Authorization: `Bearer ${token}` }
    }),
  
  saveUserPreferences: (preferences, token) => 
    api.post('/history/preferences', preferences, {
      headers: { Authorization: `Bearer ${token}` }
    }),
};

// Interview Preparation API
export const interviewAPI = {
  startPracticeSession: (companyName, jobRole, sessionType, token) => 
    api.post('/interview/start-session', { 
      company_name: companyName, 
      job_role: jobRole, 
      session_type: sessionType 
    }, {
      headers: { Authorization: `Bearer ${token}` }
    }),
  
  submitResponse: (sessionId, questionId, response, token) => 
    api.post('/interview/submit-response', { 
      session_id: sessionId, 
      question_id: questionId, 
      response 
    }, {
      headers: { Authorization: `Bearer ${token}` }
    }),
  
  getPracticeProgress: (token) => 
    api.get('/interview/progress', {
      headers: { Authorization: `Bearer ${token}` }
    }),
  
  getSessionHistory: (token) => 
    api.get('/interview/sessions', {
      headers: { Authorization: `Bearer ${token}` }
    }),
};

// Export API
export const exportAPI = {
  exportPDF: (analysisData, token) => 
    api.post('/export-pdf', analysisData, {
      headers: { Authorization: `Bearer ${token}` },
      responseType: 'blob'
    }),
  
  exportExcel: (analysisData, token) => 
    api.post('/export-excel', analysisData, {
      headers: { Authorization: `Bearer ${token}` },
      responseType: 'blob'
    }),
  
  exportJSON: (analysisData, token) => 
    api.post('/export-json', analysisData, {
      headers: { Authorization: `Bearer ${token}` }
    }),
};

export default api;
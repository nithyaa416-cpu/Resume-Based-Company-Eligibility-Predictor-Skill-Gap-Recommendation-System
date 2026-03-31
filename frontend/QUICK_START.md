# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies
```bash
cd resume/frontend
npm install
```

### 2. Start Development Server
```bash
npm start
```

### 3. Open Your Browser
Navigate to `http://localhost:3000`

## ⚡ Quick Setup (Windows)
Double-click `setup.bat` to automatically install and start the frontend.

## 🔧 Prerequisites
- **Node.js 16+** - [Download here](https://nodejs.org/)
- **Backend running** - Make sure your Flask backend is running on `http://localhost:5000`

## 📱 Features Overview

### Dashboard (`/`)
- 📄 **Upload Resume**: Drag & drop PDF/DOCX files or paste text
- 🏢 **Select Companies**: Choose specific companies or analyze all
- 🤖 **AI Analysis**: Get ML-powered compatibility scores

### Analysis (`/analysis`)
- 📊 **Detailed Results**: Comprehensive ML analysis with scores
- 🎯 **Skill Breakdown**: Skills categorized by proficiency level
- 📚 **Learning Path**: AI-generated roadmaps and recommendations
- 💾 **Export/Share**: Save results or share with others

### Compare (`/compare`)
- 🔄 **Multi-Resume**: Compare different resume versions
- 📈 **Performance Charts**: Visual comparison with charts
- 💡 **Optimization Tips**: AI insights for improvement

## 🎨 UI Features
- ✨ **Smooth Animations**: Framer Motion powered
- 📱 **Responsive Design**: Works on all devices
- 🌙 **Modern Interface**: Clean, professional design
- ⚡ **Fast Loading**: Optimized performance

## 🔗 API Endpoints Used
- `POST /upload` - Resume processing
- `GET /companies` - Company list
- `POST /ml-analyze` - Single company analysis
- `POST /analyze-all` - Multi-company analysis

## 🛠️ Development Commands

```bash
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Eject (advanced)
npm run eject
```

## 🚨 Troubleshooting

### Common Issues:

1. **Port 3000 already in use**
   ```bash
   # Kill process on port 3000
   npx kill-port 3000
   ```

2. **Backend connection failed**
   - Ensure Flask backend is running on `http://localhost:5000`
   - Check CORS configuration in backend

3. **Dependencies installation failed**
   ```bash
   # Clear npm cache
   npm cache clean --force
   # Delete node_modules and reinstall
   rm -rf node_modules package-lock.json
   npm install
   ```

4. **Build errors**
   ```bash
   # Check Node.js version
   node --version  # Should be 16+
   ```

## 📦 What's Included

- **React 18** - Latest React with concurrent features
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **React Router** - Client-side routing
- **Recharts** - Data visualization
- **React Dropzone** - File uploads
- **Hot Toast** - Notifications

## 🎯 Next Steps

1. **Upload a resume** on the dashboard
2. **Select companies** you're interested in
3. **View AI analysis** results
4. **Compare different** resume versions
5. **Follow learning** recommendations

## 💡 Tips

- Use **PDF or DOCX** files for best results
- Try **different resume versions** to see what works better
- Check the **learning roadmap** for skill development
- **Export results** to track your progress over time

---

Need help? Check the full README.md or backend documentation!
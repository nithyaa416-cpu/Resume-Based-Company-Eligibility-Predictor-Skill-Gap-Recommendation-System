# AI Resume Analyzer - React Frontend

A modern, responsive React frontend for the AI-powered resume analyzer system. Built with React 18, Tailwind CSS, and advanced UI components.

## Features

### 🤖 AI-Powered Analysis
- **ML-Based Matching**: Uses Sentence-BERT embeddings for semantic analysis
- **Smart Skill Detection**: Advanced NLP for comprehensive skill extraction
- **Contextual Understanding**: Goes beyond keyword matching

### 📊 Comprehensive Dashboard
- **Resume Upload**: Drag-and-drop file upload with real-time processing
- **Company Selection**: Interactive company grid with search functionality
- **Analysis Results**: Detailed ML analysis with visual representations

### 🔍 Advanced Analysis Features
- **Single Company Analysis**: Deep dive into specific company compatibility
- **Multi-Company Comparison**: Analyze against all companies simultaneously
- **Skill Gap Analysis**: Identify missing skills with learning recommendations
- **Learning Roadmaps**: AI-generated personalized learning paths

### 📈 Comparison Tools
- **Resume Comparison**: Compare multiple resume versions side-by-side
- **Performance Charts**: Visual comparison with bar charts and radar charts
- **Insights & Recommendations**: AI-powered insights for optimization

### 🎨 Modern UI/UX
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Smooth Animations**: Framer Motion animations for enhanced user experience
- **Interactive Components**: Hover effects, loading states, and micro-interactions
- **Accessibility**: Built with accessibility best practices

## Tech Stack

- **React 18** - Modern React with hooks and concurrent features
- **React Router** - Client-side routing
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Animation library
- **Recharts** - Chart library for data visualization
- **React Dropzone** - File upload component
- **Lucide React** - Beautiful icon library
- **React Hot Toast** - Toast notifications
- **Axios** - HTTP client

## Getting Started

### Prerequisites

- Node.js 16+ 
- npm or yarn
- Backend server running on `http://localhost:5000`

### Installation

1. **Navigate to frontend directory**:
   ```bash
   cd resume/frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm start
   ```

4. **Open your browser**:
   Navigate to `http://localhost:3000`

### Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build` folder.

## Project Structure

```
src/
├── components/           # Reusable UI components
│   ├── Header.js        # Navigation header
│   ├── ResumeUpload.js  # File upload component
│   ├── CompanySelector.js # Company selection grid
│   └── AnalysisResults.js # Results display component
├── pages/               # Page components
│   ├── Dashboard.js     # Main dashboard page
│   ├── Analysis.js      # Analysis results page
│   └── Compare.js       # Resume comparison page
├── App.js              # Main app component
├── index.js            # App entry point
└── index.css           # Global styles with Tailwind
```

## Key Components

### Dashboard (`/`)
- Resume upload (file or text)
- Company selection
- Quick analysis initiation
- Feature overview

### Analysis (`/analysis`)
- Detailed ML analysis results
- Skill breakdown by proficiency level
- Learning recommendations
- AI-generated roadmaps
- Export and sharing options

### Compare (`/compare`)
- Multi-resume comparison
- Performance charts
- Skill category analysis
- Optimization insights

## API Integration

The frontend communicates with the Flask backend through these endpoints:

- `POST /upload` - Resume file upload and processing
- `GET /companies` - Fetch available companies
- `POST /ml-analyze` - Single company ML analysis
- `POST /analyze-all` - Multi-company analysis
- `POST /recommendations` - Skill gap recommendations

## Customization

### Styling
- Modify `tailwind.config.js` for theme customization
- Update `src/index.css` for global styles
- Component-specific styles use Tailwind classes

### Features
- Add new pages in `src/pages/`
- Create reusable components in `src/components/`
- Extend API integration as needed

## Performance Optimizations

- **Code Splitting**: Automatic route-based code splitting
- **Lazy Loading**: Components loaded on demand
- **Optimized Images**: Proper image optimization
- **Caching**: Efficient API response caching

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Development Tips

1. **Hot Reload**: Changes are reflected immediately during development
2. **Error Boundaries**: Comprehensive error handling
3. **TypeScript Ready**: Easy migration to TypeScript if needed
4. **Testing**: Jest and React Testing Library included

## Deployment

### Netlify/Vercel
1. Build the project: `npm run build`
2. Deploy the `build` folder
3. Configure proxy to backend API

### Docker
```dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Check the backend API documentation
- Review browser console for errors
- Ensure backend server is running
- Verify CORS configuration

---

Built with ❤️ using React and modern web technologies.
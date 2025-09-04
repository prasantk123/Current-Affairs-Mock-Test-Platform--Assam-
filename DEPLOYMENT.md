# 🚀 Render Deployment Guide

## 📋 Prerequisites

1. **GitHub Repository**: Push your code to GitHub
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **Gemini API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)

## 🗄️ Database Setup (Free PostgreSQL)

1. **Create Database**:
   - Go to Render Dashboard
   - Click "New" → "PostgreSQL"
   - Name: `current-affairs-db`
   - Plan: Free
   - Click "Create Database"

2. **Get Connection String**:
   - Copy the "External Database URL"
   - Save for backend configuration

## 🖥️ Backend Deployment

1. **Create Web Service**:
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Name: `current-affairs-backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT run:app`

2. **Environment Variables**:
   ```
   DATABASE_URL = [Your PostgreSQL External URL]
   GEMINI_API_KEY = [Your Gemini API Key]
   SECRET_KEY = [Generate random string]
   FLASK_ENV = production
   ```

3. **Advanced Settings**:
   - Plan: Free
   - Auto-Deploy: Yes

## 🌐 Frontend Deployment

### Option 1: Netlify (Recommended)

1. **Build Frontend**:
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Deploy to Netlify**:
   - Go to [netlify.com](https://netlify.com)
   - Drag & drop the `frontend/dist` folder
   - Update API URLs in your Vue components

### Option 2: Render Static Site

1. **Create Static Site**:
   - Click "New" → "Static Site"
   - Connect repository
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/dist`

## 🔧 Configuration Updates

### Update API URLs

In your Vue components, replace `localhost:5000` with your Render backend URL:

```javascript
// Before
const response = await axios.get('http://localhost:5000/api/admin/tests')

// After
const response = await axios.get('https://your-backend-url.onrender.com/api/admin/tests')
```

### Environment-based URLs

Create `frontend/src/config.js`:
```javascript
export const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-backend-url.onrender.com'
  : 'http://localhost:5000'
```

## 📱 Free Tier Limitations

### Render Free Tier:
- ✅ 750 hours/month compute time
- ✅ PostgreSQL database (90 days)
- ⚠️ Services sleep after 15 minutes of inactivity
- ⚠️ Cold start delay (10-30 seconds)

### Optimization Tips:
1. **Keep Service Awake**: Use uptimerobot.com for periodic pings
2. **Database Persistence**: Upgrade to paid plan for permanent database
3. **File Storage**: Use cloud storage for PDF uploads in production

## 🔒 Security Checklist

- ✅ Environment variables set
- ✅ CORS configured for production domains
- ✅ Strong SECRET_KEY generated
- ✅ API key secured
- ✅ File upload size limits set

## 🚀 Deployment Steps

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy Database** → **Deploy Backend** → **Deploy Frontend**

3. **Test Production**:
   - Visit your frontend URL
   - Upload a test PDF
   - Verify AI question generation
   - Test all CRUD operations

## 📊 Monitoring

- **Render Dashboard**: Monitor service health
- **Logs**: Check application logs for errors
- **Database**: Monitor connection and queries

## 🔄 Updates

For future updates:
1. Push changes to GitHub
2. Render auto-deploys from main branch
3. Frontend rebuilds automatically

---

**Your Current Affairs platform is now production-ready on Render's free tier!**
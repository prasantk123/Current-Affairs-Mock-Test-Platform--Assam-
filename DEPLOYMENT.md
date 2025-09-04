# Render Deployment Guide

## Step 1: Create PostgreSQL Database

1. Go to [render.com](https://render.com) and login
2. Click **"New"** → **"PostgreSQL"**
3. Fill details:
   - **Name**: `current-affairs-db`
   - **Database**: `current_affairs`
   - **User**: `current_affairs_user`
   - **Region**: Choose closest to you
   - **Plan**: **Free**
4. Click **"Create Database"**
5. **COPY** the **"External Database URL"** - you'll need this!

## Step 2: Create Web Service

1. Click **"New"** → **"Web Service"**
2. Connect your GitHub repository:
   - **Repository**: `https://github.com/prasantk123/Current-Affairs-Mock-Test-Platform--Assam-`
3. Fill service details:
   - **Name**: `current-affairs-backend`
   - **Environment**: `Python 3`
   - **Region**: Same as database
   - **Branch**: `master`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: **Free**

## Step 3: Add Environment Variables

In the **Environment Variables** section, add:

```
DATABASE_URL = [Paste your PostgreSQL External Database URL here]
GEMINI_API_KEY = [Your Google Gemini API key]
SECRET_KEY = [Generate random string like: mysecretkey123456]
FLASK_ENV = production
```

**To get Gemini API Key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key

## Step 4: Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Your backend will be live at: `https://your-service-name.onrender.com`

## Step 5: Test Your Backend

Visit these URLs to test:
- `https://your-service-name.onrender.com/api/admin/ai-status`
- `https://your-service-name.onrender.com/api/admin/tests`

## Step 6: Deploy Frontend (Netlify)

1. Update `frontend/src/config.js`:
   ```javascript
   export const API_BASE_URL = 'https://your-service-name.onrender.com'
   ```

2. Build frontend:
   ```bash
   cd frontend
   npm install
   npm run build
   ```

3. Go to [netlify.com](https://netlify.com)
4. Drag & drop the `frontend/dist` folder
5. Your frontend is live!

## Important Notes

- **Free tier sleeps after 15 minutes** - first request may be slow
- **Database expires after 90 days** on free plan
- **Keep your API keys secure** - never commit them to GitHub
- **Backend URL** - update in frontend config after deployment

## Troubleshooting

**Build fails?**
- Check Python version in `runtime.txt`
- Verify all files are in GitHub repository
- Check environment variables are set

**Database connection fails?**
- Verify DATABASE_URL is correct
- Ensure database and web service are in same region

**AI not working?**
- Check GEMINI_API_KEY is valid
- Test at `/api/admin/ai-status` endpoint

## Your URLs After Deployment

- **Backend API**: `https://your-backend.onrender.com`
- **Frontend**: `https://your-frontend.netlify.app`
- **Admin Panel**: `https://your-frontend.netlify.app/admin`
- **Test Manager**: `https://your-frontend.netlify.app/manage`

## Environment Variables Checklist

✅ `DATABASE_URL` - PostgreSQL connection string  
✅ `GEMINI_API_KEY` - Google AI API key  
✅ `SECRET_KEY` - Random secret string  
✅ `FLASK_ENV` - Set to "production"  

**Your Current Affairs platform is now live!** 🚀
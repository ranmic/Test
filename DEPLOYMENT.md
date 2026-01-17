# Deployment Guide - Hebrew Crossword Solver

This guide covers multiple **FREE** hosting options for deploying the Hebrew Crossword Solver web application.

---

## 🚀 Quick Deployment Options

### Option 1: Render.com (Recommended - Easiest)

**Why Render?**
- ✅ Completely free tier
- ✅ Automatic deployments from GitHub
- ✅ Built-in HTTPS
- ✅ Easy setup (5 minutes)

**Steps:**

1. **Push your code to GitHub** (already done!)

2. **Sign up at [Render.com](https://render.com)**
   - Use your GitHub account to sign up

3. **Create a new Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `ranmic/Test`
   - Select branch: `claude/hebrew-crossword-solver-6vAbp`

4. **Configure the service:**
   ```
   Name: hebrew-crossword-solver
   Region: Choose closest to you
   Branch: claude/hebrew-crossword-solver-6vAbp
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```

5. **Choose Free plan**
   - Select "Free" tier (0$/month)

6. **Click "Create Web Service"**
   - Render will automatically deploy your app
   - Wait 2-3 minutes for deployment
   - You'll get a URL like: `https://hebrew-crossword-solver.onrender.com`

**Note:** Free tier sleeps after 15 minutes of inactivity. First request may take 30 seconds.

---

### Option 2: Railway.app

**Why Railway?**
- ✅ $5 free credit monthly
- ✅ Fast deployment
- ✅ Auto-deploy from GitHub

**Steps:**

1. **Sign up at [Railway.app](https://railway.app)**

2. **Create New Project**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository and branch

3. **Railway will auto-detect Flask app**
   - No configuration needed!
   - Uses `Procfile` automatically

4. **Generate Domain**
   - Go to Settings → Generate Domain
   - Get your URL: `https://your-app.railway.app`

**Note:** $5/month credit = ~100 hours of runtime

---

### Option 3: PythonAnywhere (Python-Specific)

**Why PythonAnywhere?**
- ✅ Always free tier available
- ✅ Python-focused platform
- ✅ Doesn't sleep

**Steps:**

1. **Sign up at [PythonAnywhere.com](https://www.pythonanywhere.com)**
   - Choose "Beginner" account (Free)

2. **Open a Bash console**
   - Click "Consoles" → "Bash"

3. **Clone your repository:**
   ```bash
   git clone https://github.com/ranmic/Test.git
   cd Test
   git checkout claude/hebrew-crossword-solver-6vAbp
   ```

4. **Install dependencies:**
   ```bash
   pip3 install --user -r requirements.txt
   ```

5. **Create a Web App:**
   - Click "Web" tab → "Add a new web app"
   - Choose "Manual configuration"
   - Python 3.10

6. **Configure WSGI file:**
   - Click on WSGI configuration file link
   - Replace contents with:
   ```python
   import sys
   import os

   # Add your project directory to sys.path
   project_home = '/home/YOUR_USERNAME/Test'
   if project_home not in sys.path:
       sys.path = [project_home] + sys.path

   # Set working directory
   os.chdir(project_home)

   # Import Flask app
   from app import app as application
   ```

7. **Set Static files:**
   - In Web tab, add static files mapping:
   - URL: `/static/`
   - Directory: `/home/YOUR_USERNAME/Test/`

8. **Reload web app**
   - Click "Reload" button
   - Access at: `https://YOUR_USERNAME.pythonanywhere.com`

**Limitations:** Free tier has some restrictions on external API calls (Wikipedia may be limited)

---

### Option 4: Replit (Quickest for Testing)

**Why Replit?**
- ✅ No deployment needed
- ✅ Instant setup
- ✅ Online IDE

**Steps:**

1. **Go to [Replit.com](https://replit.com)**

2. **Create New Repl**
   - Click "+ Create Repl"
   - Import from GitHub
   - Paste repository URL: `https://github.com/ranmic/Test`
   - Select branch: `claude/hebrew-crossword-solver-6vAbp`

3. **Run the app:**
   - Replit auto-detects Python
   - Click "Run" button
   - App runs on Replit's URL

4. **Keep it running:**
   - Deploy as "Always On" (requires paid plan)
   - Or use "UptimeRobot" to ping it periodically

---

### Option 5: Google Cloud Run (Advanced)

**Why Google Cloud?**
- ✅ Generous free tier (2 million requests/month)
- ✅ Scales automatically
- ✅ Professional-grade

**Prerequisites:**
- Google Cloud account (requires credit card but free tier doesn't charge)

**Steps:**

1. **Install Google Cloud SDK** on your local machine

2. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD gunicorn app:app --bind :$PORT
   ```

3. **Deploy:**
   ```bash
   gcloud run deploy hebrew-crossword-solver \
     --source . \
     --region us-central1 \
     --allow-unauthenticated
   ```

---

## 📊 Comparison Table

| Platform | Setup Time | Free Tier | Sleep Mode | Best For |
|----------|-----------|-----------|------------|----------|
| **Render** | 5 min | ✅ Yes | After 15 min | Recommended for most users |
| **Railway** | 3 min | $5/month | No | Fast deployment |
| **PythonAnywhere** | 10 min | ✅ Yes | No | Python projects |
| **Replit** | 1 min | ✅ Yes | When idle | Quick testing |
| **Google Cloud** | 15 min | ✅ Generous | No | Production apps |

---

## 🎯 Recommended Choice

**For beginners:** Start with **Render.com**
- Easiest setup
- Most reliable free tier
- Good performance

**For Python developers:** Try **PythonAnywhere**
- Python-focused
- No sleep mode
- Great community

**For quick testing:** Use **Replit**
- Instant deployment
- Online IDE included

---

## 🔧 Troubleshooting

### App not starting?
1. Check build logs for errors
2. Verify `requirements.txt` has all dependencies
3. Make sure `gunicorn` is in requirements.txt

### Wikipedia not working?
- Some free tiers limit external API calls
- Wikipedia integration requires outbound HTTPS access
- Dictionary search will still work

### App sleeping?
- Use a service like [UptimeRobot](https://uptimerobot.com) to ping your app every 5 minutes
- Or upgrade to paid tier for always-on

---

## 🌐 After Deployment

Once deployed, your app will be accessible at a URL like:
- Render: `https://hebrew-crossword-solver.onrender.com`
- Railway: `https://your-app.railway.app`
- PythonAnywhere: `https://yourusername.pythonanywhere.com`

Share this URL with anyone to use your Hebrew crossword solver!

---

## 💡 Tips

1. **Custom Domain:** Most platforms allow custom domain mapping (some paid tiers only)
2. **Environment Variables:** Set in platform dashboard if needed
3. **Monitoring:** Check logs in platform dashboard for debugging
4. **Scaling:** If app gets popular, upgrade to paid tier for better performance

---

**Need help?** Check the platform-specific documentation or create an issue on GitHub.

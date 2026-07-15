# Streamlit Cloud Deployment Guide

## Step 1: Create GitHub Account
1. Go to https://github.com
2. Click "Sign up"
3. Create your account (free)

## Step 2: Create a New Repository
1. Go to https://github.com/new
2. Repository name: `hotel-booking-app` (or any name)
3. Description: "Hotel Booking Management System"
4. Choose "Public" (required for free StreamlitCloud)
5. Click "Create repository"

## Step 3: Upload Your Files to GitHub
### Option A: Using Git Command Line (Recommended)
```bash
cd c:\TestBooking\Booking
git init
git add .
git commit -m "Initial commit - Hotel Booking App"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/hotel-booking-app.git
git push -u origin main
```

### Option B: Using GitHub Desktop (Easier)
1. Download: https://desktop.github.com
2. Click "Add" → "Create New Repository"
3. Name: `hotel-booking-app`
4. Local Path: `c:\TestBooking\Booking`
5. Click "Create Repository"
6. Make a commit with message "Initial commit"
7. Click "Publish repository" (set to Public)

### Option C: Upload via GitHub Web
1. Go to your repository on github.com
2. Click "Add file" → "Upload files"
3. Select all files from your Booking folder
4. Click "Commit changes"

## Step 4: Deploy to StreamlitCloud
1. Go to https://share.streamlit.io
2. Click "Create app"
3. Sign in with GitHub
4. Select your repository: `hotel-booking-app`
5. Select branch: `main`
6. Select file: `app.py`
7. Click "Deploy"

**Wait 2-3 minutes for deployment...**

## Step 5: Share Your App
Your app will have a URL like:
```
https://hotel-booking-app.streamlit.app
```

**Share this link with anyone!** They can access it from:
- 🖥️ Computer
- 📱 Android phone
- 📱 iPhone
- 📊 Tablet

## Making Changes
1. Edit your code on your PC
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your change description"
   git push
   ```
3. StreamlitCloud auto-deploys in 1-2 minutes

## Important Notes

⚠️ **Data Files (CSV):**
- Your CSV files are in `.gitignore` and won't be pushed
- On StreamlitCloud, users can create their own data
- Or: Add data files to GitHub if you want them shared

⚠️ **Free Tier Limits:**
- App goes to sleep after 1 hour of inactivity (user can wake it)
- Wakes up instantly when accessed
- Perfect for small teams

## Troubleshooting

**"Repository not found"**
- Make sure repository is PUBLIC
- Check you selected correct branch (main)

**"App won't start"**
- Check requirement.txt has all dependencies
- StreamlitCloud should auto-install them

**"Data files missing"**
- They're in .gitignore by design (local only)
- Users can book normally without pre-existing data
- Or manually add CSV files if needed

## Need Help?
- StreamlitCloud Docs: https://docs.streamlit.io/streamlit-cloud/get-started
- GitHub Docs: https://docs.github.com

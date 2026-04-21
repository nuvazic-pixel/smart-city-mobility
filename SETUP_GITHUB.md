# How to push this project to GitHub

Follow these steps exactly — copy-paste each command.

---

## Step 1 — Create the GitHub repository

1. Go to https://github.com/new
2. Repository name: `smart-city-mobility`
3. Description: `Urban traffic analysis dashboard · Augsburg & Munich · Smart City portfolio project`
4. Set to **Public**
5. Do NOT initialize with README (we already have one)
6. Click **Create repository**

---

## Step 2 — Initialize git locally

Open your terminal in the project folder and run:

```bash
cd smart-city-mobility

git init
git add .
git commit -m "Initial commit: Smart City Mobility Dashboard"
```

---

## Step 3 — Connect to GitHub and push

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/smart-city-mobility.git
git branch -M main
git push -u origin main
```

---

## Step 4 — Deploy on Streamlit Cloud (optional but recommended)

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click **New app**
4. Select your repo: `smart-city-mobility`
5. Main file path: `app.py`
6. Click **Deploy**

Your live app URL will be:
`https://YOUR_USERNAME-smart-city-mobility-app-XXXXX.streamlit.app`

Copy this URL and add it to:
- Your GitHub repo description
- Your LinkedIn post
- Your README badge

---

## Step 5 — Update README with your info

Open `README.md` and replace:
- `YOUR_USERNAME` → your GitHub username
- `YOUR_NAME` → your full name
- `YOUR_PROFILE` → your LinkedIn profile URL slug

Then commit:
```bash
git add README.md
git commit -m "Update README with personal links"
git push
```

---

## Step 6 — Add a screenshot to README (high impact)

1. Run the app locally: `streamlit run app.py`
2. Take a screenshot of the dashboard
3. Save it as `images/dashboard_preview.png`
4. Add to README.md:

```markdown
## Preview
![Dashboard](images/dashboard_preview.png)
```

Then commit and push.

---

## Done — share the link on LinkedIn!

Your post should include:
- GitHub repo link
- Streamlit live app link (if deployed)
- 2–3 key insights from the analysis
- Tags: #SmartCity #GeoData #Python #Streamlit #AVV #UrbanMobility

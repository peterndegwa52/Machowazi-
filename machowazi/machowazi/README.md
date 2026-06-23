# 🇰🇪 Macho Wazi — Deployment Guide

**Kenya's first anonymous workplace review platform**
*"See Inside Before You Step In"*

---

## What's Built

| Feature | Status |
|---|---|
| Homepage with live search autocomplete | ✅ |
| 10 pre-seeded Kenyan banking companies | ✅ |
| Anonymous review submission | ✅ |
| Salary explorer with KES data | ✅ |
| Interview experience sharing | ✅ |
| Company detail pages with ratings | ✅ |
| Transparency Score meter | ✅ |
| User registration & login | ✅ |
| Email hashing (privacy-first auth) | ✅ |
| Admin dashboard (approve/reject) | ✅ |
| Helpful vote system on reviews | ✅ |
| Review flagging system | ✅ |
| Responsive mobile design | ✅ |
| Render.com deployment config | ✅ |

---

## Deploy to Render (Free)

### Step 1 — Push to GitHub
```bash
cd machowazi
git init
git add .
git commit -m "Initial Macho Wazi deployment"
# Create a repo on GitHub then:
git remote add origin https://github.com/YOUR_USERNAME/machowazi.git
git push -u origin main
```

### Step 2 — Create Render Web Service
1. Go to https://render.com and sign up free
2. Click **New → Web Service**
3. Connect your GitHub repo
4. Render detects `render.yaml` automatically — click **Deploy**

### Step 3 — Set Environment Variables on Render
In your Render dashboard → Environment tab, add:

```
SECRET_KEY          = (generate a random 50-char string)
FLASK_ENV           = production
MAIL_USERNAME       = your-gmail@gmail.com
MAIL_PASSWORD       = your-gmail-app-password
MAIL_DEFAULT_SENDER = noreply@machowazi.co.ke
```

### Step 4 — Create Admin Account
After deployment, open the Render shell and run:
```bash
python create_admin.py your@email.com yourpassword123
```

Then go to `https://your-app.onrender.com/admin` and log in.

---

## Local Development

```bash
# 1. Clone and enter the project
cd machowazi

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy and fill environment file
cp .env.example .env
# Edit .env with your values

# 5. Run
python run.py
```

Visit: http://localhost:5000

---

## First Steps After Launch

1. **Create your admin account** using `create_admin.py`
2. **Go to /admin** and approve the seeded reviews
3. **Share the link** with 5 banking professionals you know
4. **Ask them to write reviews** — the content builds itself

---

## Monetization Roadmap

| Phase | Revenue Source | Est. Timeline |
|---|---|---|
| Launch | Free — build content | Month 1–3 |
| Growth | Employer accounts (KES 15k/mo) | Month 4–6 |
| Scale | Job listings, salary reports | Month 7–12 |
| Regional | Uganda, Tanzania expansion | Year 2 |

---

## File Structure

```
machowazi/
├── app/
│   ├── __init__.py          # App factory
│   ├── models/              # Database models
│   ├── routes/              # All route blueprints
│   │   ├── main.py          # Homepage, search
│   │   ├── auth.py          # Login, register
│   │   ├── companies.py     # Company pages
│   │   ├── reviews.py       # Write reviews, vote
│   │   ├── salaries.py      # Salary + interview
│   │   └── admin.py         # Admin dashboard
│   ├── forms.py             # WTForms definitions
│   ├── seed.py              # Initial data
│   ├── static/
│   │   ├── css/main.css     # Full design system
│   │   └── js/main.js       # Search, tabs, ratings
│   └── templates/           # All Jinja2 templates
│       ├── base.html
│       ├── index.html
│       ├── auth/
│       ├── companies/
│       ├── reviews/
│       ├── salaries/
│       └── admin/
├── create_admin.py          # Admin setup script
├── run.py                   # Development server
├── wsgi.py                  # Render/Gunicorn entry
├── render.yaml              # Render deployment config
├── requirements.txt
└── .env.example
```

---

**Built for Kenya. By someone who believes Kenya deserves better workplace transparency.**

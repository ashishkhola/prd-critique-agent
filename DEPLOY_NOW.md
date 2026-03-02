# 🚀 Deploy PRD Cop to Get a URL (10 Minutes)

## Quick Deploy to Heroku

### Step 1: Install Heroku CLI (2 minutes)

```bash
# Mac:
brew install heroku/brew/heroku

# Or download from: https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Login to Heroku (1 minute)

```bash
heroku login
# Opens browser, click "Log in"
```

### Step 3: Create and Deploy App (5 minutes)

```bash
cd /Users/ashishkhola/prd_critique_agent

# Create app (pick a unique name)
heroku create prd-cop-stripe

# Set your API key
heroku config:set ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY"

# If ANTHROPIC_API_KEY is not set, use your actual key:
# heroku config:set ANTHROPIC_API_KEY="sk-ant-..."

# Or for Stripe internal:
heroku config:set ANTHROPIC_BASE_URL="$ANTHROPIC_BASE_URL"
heroku config:set ANTHROPIC_AUTH_TOKEN="$ANTHROPIC_AUTH_TOKEN"

# Deploy
git add Procfile runtime.txt requirements.txt
git commit -m "Add Heroku deployment config"
git push heroku main

# Open your app
heroku open
```

### Step 4: Get Your URL

After deployment, you'll get a URL like:
```
https://prd-cop-stripe.herokuapp.com
```

**That's your shareable link!** ✅

---

## Alternative: Deploy to Railway (Even Easier!)

### Step 1: Go to Railway

1. Visit: https://railway.app
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose: `ashishkhola/prd-critique-agent`

### Step 2: Set Environment Variables

In Railway dashboard:
- Click your project
- Go to "Variables"
- Add: `ANTHROPIC_API_KEY` = `sk-ant-...`

### Step 3: Deploy

Railway auto-deploys! You'll get a URL like:
```
https://prd-cop-production.up.railway.app
```

**Done!** ✅

---

## Your Shareable URL

After deployment, share this with your PM colleagues:

```
Hey team! 👋

Try PRD Cop - AI PRD critique in 30 seconds:
👉 https://your-app.herokuapp.com

Just:
1. Open link
2. Paste your PRD
3. Click "Critique PRD"
4. Get your score!

Let me know what you think 🚀
```

---

## Troubleshooting

### Heroku Deploy Fails?

```bash
# Check logs
heroku logs --tail

# Common issues:
# 1. Missing environment variable
heroku config:set ANTHROPIC_API_KEY="sk-ant-..."

# 2. Wrong buildpack
heroku buildpacks:set heroku/python

# 3. Port issue (should be automatic, but if needed:)
# web_service.py already uses PORT from env
```

### Can't Access URL?

```bash
# Check if app is running
heroku ps

# Restart if needed
heroku restart

# Check recent logs
heroku logs --tail
```

---

## Cost

**Heroku:**
- Free tier: Up to 550 hours/month (enough for testing)
- Eco plan: $5/month for 24/7 uptime
- Basic: $7/month with more resources

**Railway:**
- Free: $5 credit/month
- Pro: $20/month for unlimited

**Claude API:**
- ~$0.10 per PRD critique
- If 20 PMs critique 5 PRDs/month = ~$10/month

**Total:** ~$10-20/month for full team usage

---

## Next Steps

1. Deploy now (10 minutes)
2. Test your URL
3. Share with 2-3 PM friends
4. Gather feedback
5. Share with whole team

**Let's deploy! Run the commands above ⬆️**

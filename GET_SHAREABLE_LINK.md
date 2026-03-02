# 🔗 How to Get a Shareable Link for PRD Cop

You have **3 options** to share PRD Cop with your PM colleagues:

---

## 🚀 Option 1: Share Your Local Link (5 minutes - Works Now!)

**Best for:** Quick sharing with colleagues on same network (office/VPN)

### Step 1: Find Your Computer's IP Address

```bash
# Mac:
ipconfig getifaddr en0

# Or:
ifconfig | grep "inet " | grep -v 127.0.0.1
```

You'll get something like: `192.168.1.45` or `10.0.0.123`

### Step 2: Start the Web Service

```bash
cd /Users/ashishkhola/prd_critique_agent
source venv/bin/activate
python3 web_service.py
```

Server runs on: `0.0.0.0:8080` (accessible from network)

### Step 3: Share the Link

**Give colleagues this link:**
```
http://YOUR_IP:8080

Example:
http://192.168.1.45:8080
http://10.0.0.123:8080
```

**Send them:**
```
Hey team! 👋

Try PRD Cop - instant PRD critique:
👉 http://192.168.1.45:8080

Just paste your PRD, click "Critique", get a score in 60s!

Note: Works while my computer is on. Let me know if you want 24/7 access.
```

**Limitations:**
- Only works when your computer is on
- Only works for people on same network/VPN
- Not accessible from outside network

---

## ☁️ Option 2: Deploy to Cloud (10 minutes - Get Permanent URL!)

**Best for:** 24/7 access, anyone can use, professional setup

### A. Deploy to Heroku (Simplest Cloud)

**Free tier available!**

```bash
# 1. Install Heroku CLI
brew install heroku/brew/heroku  # Mac
# Or download from: https://devcenter.heroku.com/articles/heroku-cli

# 2. Login
heroku login

# 3. Create app
cd /Users/ashishkhola/prd_critique_agent
heroku create prd-cop-ashish  # Pick a unique name

# 4. Set environment variable
heroku config:set ANTHROPIC_API_KEY="sk-ant-..."

# 5. Create Procfile
echo "web: python3 web_service.py" > Procfile

# 6. Create requirements.txt
pip freeze > requirements.txt

# 7. Deploy
git add Procfile requirements.txt
git commit -m "Add Heroku config"
git push heroku main
```

**Your link will be:**
```
https://prd-cop-ashish.herokuapp.com
```

**Share with team:**
```
Hey team! 👋

PRD Cop is now live 24/7:
👉 https://prd-cop-ashish.herokuapp.com

Paste your PRD → Click "Critique" → Get score in 60s!

No setup needed, works from anywhere 🚀
```

### B. Deploy to Google Cloud Run (Also Great)

```bash
# 1. Install gcloud CLI
# Download from: https://cloud.google.com/sdk/docs/install

# 2. Login
gcloud auth login

# 3. Create Dockerfile
cat > Dockerfile <<'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
ENV PORT=8080
CMD ["python3", "web_service.py"]
EOF

# 4. Deploy
gcloud run deploy prd-cop \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ANTHROPIC_API_KEY="sk-ant-..."

# Get URL (something like):
# https://prd-cop-abcd1234-uc.a.run.app
```

**Cloud Run Benefits:**
- Only pay when someone uses it (~$0/month for light use)
- Auto-scales
- Fast & reliable

---

## 👥 Option 3: Have Each PM Run Locally (Best for Security)

**Best for:** Sensitive PRDs, each PM has full control

### What to Send Them:

```
Hey team! 👋

I built PRD Cop - an AI that scores PRDs out of 100 and tells you what to fix.

Want to try it? Takes 10 minutes to setup:

📖 Guide for PMs: https://github.com/ashishkhola/prd-critique-agent/blob/main/FOR_PMS.md

Or quick version:
1. Get code: git clone https://github.com/ashishkhola/prd-critique-agent.git
2. Get API key: https://console.anthropic.com (free to start)
3. Start UI: python3 web_service.py
4. Open: http://localhost:8080

Full docs: https://github.com/ashishkhola/prd-critique-agent/blob/main/TRY_IT_NOW.md

Let me know if you need help!
```

**Benefits:**
- Most secure (PRD never leaves their computer)
- Each PM controls their own instance
- Works offline once set up
- No cost to you

**Drawbacks:**
- Each person needs to set it up
- Requires some technical comfort

---

## 📊 Comparison

| Option | Setup Time | Cost | Availability | Security | Best For |
|--------|-----------|------|--------------|----------|----------|
| **Local Share** | 5 min | Free | While your computer is on | Medium | Quick demo |
| **Heroku** | 10 min | Free tier available | 24/7 | Medium | Team use |
| **Cloud Run** | 15 min | Pay per use (~$0) | 24/7 | Medium | Team use |
| **Each PM Runs** | 10 min/person | ~$0.10/critique | Always | High | Sensitive PRDs |

---

## 🎯 Recommended Approach

### For Your Situation:

**Right Now (Today):**
```bash
# Get your IP
ipconfig getifaddr en0

# Start service
cd /Users/ashishkhola/prd_critique_agent
source venv/bin/activate
python3 web_service.py

# Share: http://YOUR_IP:8080
```

Send to 2-3 PM friends: "Try this quick - http://YOUR_IP:8080"

**This Week:**
Deploy to Heroku (10 minutes) → Get permanent link → Share with whole team

**Long Term:**
If lots of usage, consider:
- Cloud Run (scales better)
- Or each PM runs their own (more secure)

---

## 📧 Message to Send PMs

### Quick Demo (Using Local IP):

```
Hey team! 👋

I built an AI PRD critique tool - want to try it?

🚨 PRD Cop - Scores your PRD out of 100 and tells you what to fix

Try it now: http://YOUR_IP:8080
(Works while I'm online)

Just:
1. Paste your PRD
2. Click "Critique PRD"
3. Get score in 60s!

Example PRD to test:
# Background
We need to build feature X...

# Problem
Current process is slow...

Let me know what you think! If you like it, I'll deploy it permanently.
```

### Permanent Link (After Heroku Deploy):

```
Hey team! 👋

PRD Cop is now live 24/7! 🚀

👉 https://prd-cop-ashish.herokuapp.com

What it does:
• Scores your PRD out of 100 points
• Tells you exactly what to fix
• Auto-generates improved version
• Takes 30 seconds

How to use:
1. Open link above
2. Paste your PRD
3. Click "Critique PRD"
4. Done! ✅

Try it on your current PRD and let me know what score you get!

Full guide: https://github.com/ashishkhola/prd-critique-agent/blob/main/FOR_PMS.md
```

---

## 🚀 Let's Get You Started

### Do This Now:

```bash
# Terminal 1: Start the service
cd /Users/ashishkhola/prd_critique_agent
source venv/bin/activate
python3 web_service.py

# Terminal 2: Get your IP
ipconfig getifaddr en0

# Share with 1-2 PM friends:
# "Try this: http://YOUR_IP:8080"
```

### Deploy to Heroku This Week:

```bash
# Install Heroku CLI
brew install heroku/brew/heroku

# Login
heroku login

# Create app
heroku create prd-cop-ashish

# Set API key
heroku config:set ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY"

# Create Procfile
echo "web: python3 web_service.py" > Procfile

# Deploy
git add Procfile
git commit -m "Add Heroku support"
git push heroku main

# Get URL:
heroku open
```

---

## 💡 Pro Tips

### Make Local Link Persistent

Add to your `~/.zshrc` or `~/.bash_profile`:
```bash
alias prd-cop='cd /Users/ashishkhola/prd_critique_agent && source venv/bin/activate && python3 web_service.py'
```

Then just type: `prd-cop` to start it!

### Monitor Usage (Heroku)

```bash
# See logs
heroku logs --tail

# See who's using it
heroku logs | grep "POST /critique"
```

### Custom Domain

After Heroku deploy:
```bash
# Add custom domain
heroku domains:add prd-cop.yourcompany.com

# Follow instructions to configure DNS
```

---

## 🆘 Need Help?

### Can't Get IP to Work?
- Check firewall settings
- Try: `python3 web_service.py` and look for the IP it shows
- Make sure colleague is on same network/VPN

### Heroku Deploy Fails?
- Check: `heroku logs --tail`
- Make sure `requirements.txt` is complete
- Verify API key is set: `heroku config`

### Want Different Deployment?
See full guide: [DEPLOYMENT.md](DEPLOYMENT.md)

---

## ✅ Summary

**Today:**
- Local IP: `http://YOUR_IP:8080` (5 min)
- Share with 2-3 people for feedback

**This Week:**
- Deploy to Heroku: Get `https://prd-cop-ashish.herokuapp.com` (10 min)
- Share with whole team

**Ongoing:**
- Monitor usage
- Iterate based on feedback
- Consider Cloud Run if heavy usage

**Get started now! 🚀**

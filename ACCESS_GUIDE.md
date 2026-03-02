# 🚀 PRD Cop - Complete Access Guide

**Choose how you want to use PRD Cop based on your needs:**

---

## 📊 Quick Comparison

| Method | Setup Time | Best For | UI | Cost |
|--------|-----------|----------|----|----|
| **Web UI** | 2 min | First-time users, quick tests | ✅ Yes | Free (local) |
| **Command Line** | 5 min | Individual use, automation | ❌ No | ~$0.10/critique |
| **Slack Bot** | 10 min | Teams, instant feedback | ✅ Yes | ~$0.10/critique |
| **REST API** | 5 min | Integrations, custom tools | ❌ No | ~$0.10/critique |
| **GitHub Actions** | 10 min | Automatic PR checks | ✅ In PR | ~$0.10/critique |

---

## 🎨 Option 1: Web UI (Easiest - Has UI!)

**Best for:** First-time users, non-technical users, quick one-off critiques

### Local Setup (2 minutes):

```bash
# Clone repo
git clone https://github.com/ashishkhola/prd-critique-agent.git
cd prd-critique-agent

# Setup
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install flask flask-cors anthropic

# Set API key
export ANTHROPIC_API_KEY="sk-ant-..."  # Get from https://console.anthropic.com

# Start web server
python3 web_service.py
```

### Access:

1. Open browser: **http://localhost:8080**
2. You'll see a beautiful UI with:
   - Text area to paste your PRD
   - "Critique PRD" button
   - Score display with color coding
   - Full breakdown and report
   - "Generate Improved Version" button
   - Download report button

### Try It:

```bash
# Terminal 1: Start server
cd /Users/ashishkhola/prd_critique_agent
source venv/bin/activate
python3 web_service.py

# Terminal 2 / Browser: Open http://localhost:8080
```

**🎥 Screenshot:** Beautiful purple gradient design, paste PRD → click button → get score!

---

## 💻 Option 2: Command Line (Simple & Fast)

**Best for:** Technical users, automation, scripting

### Setup (5 minutes):

```bash
# Clone repo
git clone https://github.com/ashishkhola/prd-critique-agent.git
cd prd-critique-agent

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install anthropic

# Set API key
export ANTHROPIC_API_KEY="sk-ant-..."
# Or for Stripe internal: Already set via ANTHROPIC_BASE_URL
```

### Usage:

```bash
# Method 1: From file
python3 prd_cop_agent.py my_prd.txt

# Method 2: From stdin
cat my_prd.txt | python3 prd_cop_agent.py

# Method 3: Paste directly
python3 prd_cop_agent.py
# (paste PRD, press Ctrl+D when done)

# Method 4: Google Doc (Stripe internal only)
python3 prd_cop_agent.py "https://docs.google.com/document/d/YOUR_DOC_ID"
```

### Example Output:

```
🔍 PRD Cop analyzing: my_prd
   Model: claude-opus-4-6
   Mode: external
============================================================

⏳ Analyzing PRD (this may take 30-60 seconds)...

✅ Analysis complete!
📊 Score: 78/100
💰 Token usage: 3208 input, 1272 output

💾 Report saved: my_prd_Critique_20260302_131040.md

============================================================
📊 CRITIQUE SUMMARY
============================================================
Score: 78/100
Report: reports/my_prd_Critique_20260302_131040.md

============================================================

🔧 Generate improved version? (y/n): y

⏳ Generating improved PRD (may take 60-90 seconds)...

✅ Improved PRD generated!
💾 Improved PRD saved: my_prd_IMPROVED_20260302_131040.md

============================================================
✅ IMPROVEMENT COMPLETE
============================================================
Original Score: 78/100
Improved PRD: reports/my_prd_IMPROVED_20260302_131040.md

💡 Next: Re-score the improved version to see new score

✅ Done! All reports saved to ./reports/
```

### Try It:

```bash
cd /Users/ashishkhola/prd_critique_agent
source venv/bin/activate

# Test with your improved PRD
python3 prd_cop_agent.py /tmp/improved_prd_full.txt
```

---

## 💬 Option 3: Slack Bot (Best for Teams!)

**Best for:** Teams, instant feedback, collaborative reviews

### Setup (10 minutes):

#### Step 1: Create Slack App

1. Go to: **https://api.slack.com/apps**
2. Click **"Create New App"** → **"From scratch"**
3. Name: **"PRD Cop"**
4. Workspace: Your workspace

#### Step 2: Configure Permissions

1. **OAuth & Permissions** → **Bot Token Scopes**:
   - `chat:write`
   - `commands`
   - `files:write`
   - `app_mentions:read`

#### Step 3: Enable Socket Mode

1. **Settings** → **Socket Mode** → **Enable**
2. Click **"Generate Token"** (name it "PRD Cop Socket")
3. Scopes: `connections:write`
4. Copy the **App-Level Token** (starts with `xapp-`)

#### Step 4: Add Slash Command

1. **Slash Commands** → **Create New Command**
   - Command: `/prd-cop`
   - Description: `Critique a PRD using PRD Cop framework`
   - Usage Hint: `[paste PRD text or Google Doc URL]`

#### Step 5: Install to Workspace

1. **Settings** → **Install App** → **Install to Workspace**
2. Copy the **Bot Token** (starts with `xoxb-`)

#### Step 6: Run Bot

```bash
cd prd-critique-agent
source venv/bin/activate

# Install Slack dependencies
pip install slack-bolt anthropic

# Set environment variables
export SLACK_BOT_TOKEN="xoxb-..."
export SLACK_APP_TOKEN="xapp-..."
export ANTHROPIC_API_KEY="sk-ant-..."  # or use Stripe internal

# Run bot
python3 slack_bot.py
```

You'll see:
```
🚀 PRD Cop Slack Bot starting...
   Listening for /prd-cop commands...
⚡️ Bolt app is running!
```

### Usage in Slack:

```
# In any Slack channel or DM:
/prd-cop # Background
We need to build document verification automation...

# Problem Statement
Our current process lacks...

# Or with Google Doc:
/prd-cop https://docs.google.com/document/d/YOUR_DOC_ID
```

**Bot Response (in ~60 seconds):**
```
✅ PRD Cop Score: 78/100 - Needs polish

📊 Breakdown:
Structure Check: 13/15
Tone & Clarity: 14/20
Manager Review: 19/25
Leader Review: 14/20
Storytelling: 9/10
Top Leadership: 9/10

📄 Full Report: Uploading...

💡 Want an improved version? Reply with 'improve' and I'll generate one!
```

### Try It:

1. Start the bot: `python3 slack_bot.py`
2. In Slack: `/prd-cop Hello world test`
3. Get instant feedback!

---

## 🌐 Option 4: REST API (For Integrations)

**Best for:** Integrations, custom tools, automation workflows

### Start Server:

```bash
cd prd-critique-agent
source venv/bin/activate
pip install flask flask-cors anthropic

export ANTHROPIC_API_KEY="sk-ant-..."
python3 web_service.py
```

Server starts at: **http://localhost:8080**

### Endpoints:

#### 1. Health Check
```bash
curl http://localhost:8080/health
```

Response:
```json
{
  "status": "healthy",
  "service": "PRD Cop Agent",
  "version": "1.0.0",
  "mode": "external"
}
```

#### 2. Critique PRD
```bash
curl -X POST http://localhost:8080/critique \
  -H "Content-Type: application/json" \
  -d '{
    "prd_text": "# Background\nWe need to build document verification...",
    "prd_name": "DVaaS Observability"
  }'
```

Response:
```json
{
  "score": 78,
  "report_text": "## PRD COP FINAL SCORE: 78/100\n\n### Score Breakdown:\n...",
  "report_path": "reports/DVaaS_Observability_Critique_20260302.md",
  "token_usage": {
    "input": 3208,
    "output": 1272
  }
}
```

#### 3. Generate Improved Version
```bash
curl -X POST http://localhost:8080/improve \
  -H "Content-Type: application/json" \
  -d '{
    "original_prd": "...",
    "critique_results": {...},
    "prd_name": "DVaaS"
  }'
```

Response:
```json
{
  "improved_text": "# Improved PRD\n\n...",
  "report_path": "reports/DVaaS_IMPROVED_20260302.md",
  "original_score": 78
}
```

#### 4. Batch Processing
```bash
curl -X POST http://localhost:8080/batch \
  -H "Content-Type: application/json" \
  -d '{
    "prds": [
      {"name": "Feature A", "text": "..."},
      {"name": "Feature B", "text": "..."}
    ]
  }'
```

Response:
```json
{
  "results": [
    {"name": "Feature A", "score": 85, "report_path": "..."},
    {"name": "Feature B", "score": 72, "report_path": "..."}
  ],
  "total": 2,
  "succeeded": 2,
  "failed": 0
}
```

### Try It:

```bash
# Terminal 1: Start server
cd /Users/ashishkhola/prd_critique_agent
source venv/bin/activate
python3 web_service.py

# Terminal 2: Test API
curl -X POST http://localhost:8080/critique \
  -H "Content-Type: application/json" \
  -d '{"prd_text": "# Test PRD\n\nThis is a test.", "prd_name": "Test"}'
```

---

## 🔄 Option 5: GitHub Actions (Automatic)

**Best for:** Enforcing PRD quality standards, automatic PR checks

### Setup:

1. **Add workflow file:**

```yaml
# .github/workflows/prd-cop.yml
name: PRD Quality Check

on:
  pull_request:
    paths:
      - 'docs/prds/**/*.md'

jobs:
  prd-cop:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Clone PRD Cop
        run: |
          git clone https://github.com/ashishkhola/prd-critique-agent.git
          cd prd-critique-agent
          pip install anthropic

      - name: Run PRD Cop
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          cd prd-critique-agent
          for prd in ../docs/prds/*.md; do
            echo "Critiquing $prd..."
            python3 prd_cop_agent.py "$prd"
          done

      - name: Check scores
        run: |
          cd prd-critique-agent
          for report in reports/*_Critique_*.md; do
            score=$(grep "FINAL SCORE" "$report" | grep -oP '\d+(?=/100)')
            echo "Score: $score/100"
            if [ "$score" -lt 70 ]; then
              echo "❌ PRD quality below threshold (70)"
              exit 1
            fi
          done

      - name: Upload reports
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: prd-cop-reports
          path: prd-critique-agent/reports/
```

2. **Add GitHub Secret:**

   - Go to: **Your Repo** → **Settings** → **Secrets and variables** → **Actions**
   - Click **"New repository secret"**
   - Name: `ANTHROPIC_API_KEY`
   - Value: `sk-ant-...` (your API key)

### Usage:

1. Create a PRD in `docs/prds/my_feature.md`
2. Create a PR
3. GitHub Actions automatically:
   - Critiques all PRDs in the PR
   - Fails if score < 70
   - Uploads critique reports as artifacts

### Try It:

```bash
# In your repo:
mkdir -p .github/workflows docs/prds
# Create workflow file (see above)
# Add your PRD to docs/prds/
git add . && git commit -m "Add PRD" && git push
# Create PR → Automatic critique!
```

---

## 📚 Documentation Links

### Core Documentation:
- **Main README**: [README.md](https://github.com/ashishkhola/prd-critique-agent/blob/main/README.md)
- **Usage Guide**: [README_USAGE.md](https://github.com/ashishkhola/prd-critique-agent/blob/main/README_USAGE.md)
- **Deployment Guide**: [DEPLOYMENT.md](https://github.com/ashishkhola/prd-critique-agent/blob/main/DEPLOYMENT.md)
- **Share with Team**: [SHARE_WITH_TEAM.md](https://github.com/ashishkhola/prd-critique-agent/blob/main/SHARE_WITH_TEAM.md)
- **This Guide**: [ACCESS_GUIDE.md](https://github.com/ashishkhola/prd-critique-agent/blob/main/ACCESS_GUIDE.md)

### Local Documentation:
- Main README: `/Users/ashishkhola/prd_critique_agent/README.md`
- Usage Guide: `/Users/ashishkhola/prd_critique_agent/README_USAGE.md`
- Deployment: `/Users/ashishkhola/prd_critique_agent/DEPLOYMENT.md`
- Access Guide: `/Users/ashishkhola/prd_critique_agent/ACCESS_GUIDE.md`

### GitHub Repository:
**https://github.com/ashishkhola/prd-critique-agent**

---

## 🎓 How to Help Others Use This

### 1. Share the Web UI Link

If you deploy the web service (Heroku, Cloud Run, etc.):

```
Hey team! Try PRD Cop - instant PRD critiques:
👉 https://your-prd-cop-app.herokuapp.com

Just paste your PRD, click "Critique", get a score in 60s!
```

### 2. Share the GitHub Repo

```
GitHub: https://github.com/ashishkhola/prd-critique-agent

Quick start:
git clone https://github.com/ashishkhola/prd-critique-agent.git
cd prd-critique-agent
python3 -m venv venv && source venv/bin/activate
pip install anthropic
export ANTHROPIC_API_KEY="sk-ant-..."
python3 prd_cop_agent.py your_prd.txt
```

### 3. Deploy Slack Bot for Team

```
I've deployed PRD Cop bot to our Slack! 🚨

Use it anywhere:
/prd-cop [paste your PRD]

Get instant feedback with a score out of 100!
```

### 4. Share Documentation

**For Quick Start:**
- Main README: https://github.com/ashishkhola/prd-critique-agent#readme

**For Detailed Usage:**
- Usage Guide: https://github.com/ashishkhola/prd-critique-agent/blob/main/README_USAGE.md

**For Deployment:**
- Deployment Guide: https://github.com/ashishkhola/prd-critique-agent/blob/main/DEPLOYMENT.md

**For Sharing:**
- Share with Team: https://github.com/ashishkhola/prd-critique-agent/blob/main/SHARE_WITH_TEAM.md

---

## 🚀 Recommended Path

### For You (First Time):
1. ✅ **Start with Web UI** - Most visual, easiest to understand
   ```bash
   cd /Users/ashishkhola/prd_critique_agent
   source venv/bin/activate
   python3 web_service.py
   # Open: http://localhost:8080
   ```

2. ✅ **Try Command Line** - Learn the CLI
   ```bash
   python3 prd_cop_agent.py /tmp/improved_prd_full.txt
   ```

3. ✅ **Read the output reports** - Understand what it generates
   ```bash
   open reports/
   ```

### For Your Team:
1. **Individual Contributors**: Share GitHub repo + README
2. **Team Usage**: Deploy Slack bot
3. **Quality Enforcement**: Add GitHub Actions

### For External Sharing:
1. Tweet the GitHub repo
2. Blog post about building it
3. Share on LinkedIn

---

## 📞 Support

### Questions?
- GitHub Issues: https://github.com/ashishkhola/prd-critique-agent/issues
- Stripe Internal: #prd-cop or DM ashishkhola@stripe.com
- External: Open GitHub issue

### Documentation Not Clear?
- Open issue: "Documentation unclear: [specific section]"
- We'll improve it!

---

## 🎯 Next Steps

### Right Now:
```bash
# 1. Start the Web UI
cd /Users/ashishkhola/prd_critique_agent
source venv/bin/activate
python3 web_service.py

# 2. Open browser
open http://localhost:8080

# 3. Paste your improved PRD from /tmp/improved_prd_full.txt

# 4. Click "Critique PRD"

# 5. See your score with beautiful UI!
```

### Tomorrow:
- Share with 2-3 colleagues
- Get their feedback
- Iterate based on usage

### This Week:
- Deploy one option for your team (Slack or Web)
- Document your team's workflow
- Celebrate better PRDs! 🎉

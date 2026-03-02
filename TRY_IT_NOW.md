# 🎯 Try PRD Cop Right Now (2 Minutes)

Choose your path:

---

## 🎨 Path 1: Web UI (Has Beautiful Interface!)

**Time: 2 minutes | Has UI: ✅**

### Step 1: Start the server

```bash
cd /Users/ashishkhola/prd_critique_agent
source venv/bin/activate
python3 web_service.py
```

You'll see:
```
🚀 PRD Cop Web Service starting...
   Mode: stripe_internal
   Port: 8080

Endpoints:
   POST /critique - Critique a PRD
   POST /improve - Generate improved version
   POST /batch - Batch critique multiple PRDs
   GET /health - Health check

 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
```

### Step 2: Open in browser

Click this link: **http://localhost:8080**

### Step 3: Try it!

1. You'll see a beautiful purple interface 🎨
2. Paste your PRD in the text area (or use the one below)
3. Click **"🔍 Critique PRD"**
4. Wait 30-60 seconds
5. See your score with color coding! ✅

**Test PRD to paste:**
```markdown
# Background

We need to build document verification automation to reduce manual reviews by 65%.

# Problem Statement

Current process is slow and error-prone. Manual review takes 2 days on average.

# Solution

Build LLM-based agents to automate verification decisions.

# Success Metrics

Reduce review time by 50%.
```

### Step 4: See results!

- Big score display (color coded by quality)
- Breakdown by dimension
- Full detailed report
- Button to generate improved version
- Download report option

**🎉 That's it! You just used PRD Cop with a beautiful UI!**

---

## 💻 Path 2: Command Line (No UI, Fast)

**Time: 30 seconds | Has UI: ❌ (but very fast)**

### Run it:

```bash
cd /Users/ashishkhola/prd_critique_agent
source venv/bin/activate
python3 prd_cop_agent.py /tmp/improved_prd_full.txt
```

### Output (in 30-60 seconds):

```
🔍 PRD Cop analyzing: improved_prd_full
   Model: claude-opus-4-6
   Mode: stripe_internal
============================================================

⏳ Analyzing PRD (this may take 30-60 seconds)...

✅ Analysis complete!
📊 Score: 78/100
💰 Token usage: 3208 input, 1272 output

💾 Report saved: improved_prd_full_Critique_20260302_141530.md

============================================================
📊 CRITIQUE SUMMARY
============================================================
Score: 78/100
Report: reports/improved_prd_full_Critique_20260302_141530.md

============================================================

🔧 Generate improved version? (y/n):
```

Type **`y`** to generate improved version, or **`n`** to just see the report.

### View the report:

```bash
open reports/improved_prd_full_Critique_20260302_141530.md
```

**🎉 Done! You just critiqued a PRD from command line!**

---

## 🌐 Path 3: Try the API (For Developers)

**Time: 1 minute | Has UI: ❌ (but great for automation)**

### Terminal 1: Start server

```bash
cd /Users/ashishkhola/prd_critique_agent
source venv/bin/activate
python3 web_service.py
```

### Terminal 2: Call API

```bash
curl -X POST http://localhost:8080/critique \
  -H "Content-Type: application/json" \
  -d '{
    "prd_text": "# Background\n\nWe need to build document verification automation.\n\n# Problem\n\nManual reviews are slow.\n\n# Solution\n\nBuild LLM agents.",
    "prd_name": "Quick Test"
  }'
```

### Response (in 30-60 seconds):

```json
{
  "score": 52,
  "report_text": "## PRD COP FINAL SCORE: 52/100\n\n### Score Breakdown:\n1. Structure Check: 6/15\n2. Tone & Clarity: 8/20\n...",
  "report_path": "reports/Quick_Test_Critique_20260302.md",
  "token_usage": {
    "input": 1024,
    "output": 856
  }
}
```

**🎉 You just used PRD Cop via API!**

---

## 📊 What You'll See

### Web UI Shows:

1. **Score Card** - Big number with color:
   - Green (85-100): Leadership-ready ✅
   - Pink (70-84): Needs polish ⚠️
   - Orange (50-69): Major revision ❌
   - Red (<50): Fundamental rework 🚨

2. **Breakdown Table**:
   ```
   Structure Check: 13/15
   Tone & Clarity: 14/20
   Manager Review: 19/25
   Leader Review: 14/20
   Storytelling: 9/10
   Top Leadership: 9/10
   ```

3. **Full Report** - Scrollable with:
   - Critical Issues (P0)
   - Structural Gaps
   - Weak Phrases to fix
   - Quick Wins
   - What would make it 85+

4. **Action Buttons**:
   - 🔧 Generate Improved Version
   - 💾 Download Report
   - ↻ Critique Another PRD

### Command Line Shows:

```
🔍 PRD Cop analyzing: your_prd
============================================================

📊 Score: 78/100

📊 CRITIQUE SUMMARY
============================================================
Score: 78/100
Report: reports/your_prd_Critique_20260302.md

🔧 Generate improved version? (y/n):
```

---

## 🎓 What to Try Next

### 1. Compare Scores

```bash
# Score your original PRD
python3 prd_cop_agent.py /path/to/original.txt
# Result: 52/100

# Score your improved PRD
python3 prd_cop_agent.py /tmp/improved_prd_full.txt
# Result: 78/100

# See the improvement! +26 points! 🎉
```

### 2. Use Web UI to See Visual Difference

```bash
# Start server
python3 web_service.py

# Open: http://localhost:8080

# Paste original PRD → See score 52/100 (red/orange)
# Paste improved PRD → See score 78/100 (pink, moving to green!)
```

### 3. Generate & Re-Score Improved Version

```bash
# In Web UI or CLI:
# 1. Critique PRD (gets 68/100)
# 2. Click/type 'y' for "Generate Improved Version"
# 3. Wait 60-90 seconds
# 4. Improved version generated
# 5. Critique the improved version
# 6. New score: 82/100! 🎉
```

### 4. Share with a Colleague

```bash
# Option A: Send them the Web UI link
"Try this: http://your-computer-ip:8080"

# Option B: Send them the GitHub repo
"Try PRD Cop: https://github.com/ashishkhola/prd-critique-agent"

# Option C: Show them in person
# Open the Web UI, let them paste their PRD, watch their reaction! 😃
```

---

## 💡 Pro Tips

### Make Web UI Accessible to Team

```bash
# Find your IP address
ifconfig | grep "inet " | grep -v 127.0.0.1

# Start server (allows external connections)
python3 web_service.py

# Share with team:
"Try PRD Cop at: http://YOUR_IP:8080"
```

### Save Your Favorite PRD for Testing

```bash
# Create test PRD
cat > test_prd.txt <<'EOF'
# Background
Quick test PRD for demos

# Problem
Testing the agent

# Solution
Run the critique
EOF

# Quick test anytime
python3 prd_cop_agent.py test_prd.txt
```

### Keyboard Shortcuts in Web UI

- **Ctrl+Enter** in text area → Submits (coming soon!)
- **Cmd+V** → Paste your PRD
- **Cmd+A** → Select all (to copy improved version)

---

## 🆘 Troubleshooting

### Web UI doesn't load?

```bash
# Check if server is running
curl http://localhost:8080/health

# Should return:
# {"status": "healthy", ...}

# If not, restart server:
python3 web_service.py
```

### "No module named 'anthropic'"?

```bash
# Make sure venv is activated
source venv/bin/activate

# Install dependencies
pip install anthropic flask flask-cors
```

### "Missing API key"?

```bash
# For Stripe internal: Should auto-detect
echo $ANTHROPIC_BASE_URL  # Should show URL
echo $ANTHROPIC_AUTH_TOKEN  # Should show token

# For external: Set API key
export ANTHROPIC_API_KEY="sk-ant-..."
```

---

## 📚 Learn More

**Full Documentation:**
- **Access Guide**: [ACCESS_GUIDE.md](ACCESS_GUIDE.md) - All 5 ways to use PRD Cop
- **Usage Guide**: [README_USAGE.md](README_USAGE.md) - Comprehensive usage examples
- **Deployment**: [DEPLOYMENT.md](DEPLOYMENT.md) - Deploy to cloud, Slack, CI/CD
- **Share with Team**: [SHARE_WITH_TEAM.md](SHARE_WITH_TEAM.md) - Help others use it

**Quick Links:**
- GitHub: https://github.com/ashishkhola/prd-critique-agent
- All Docs: https://github.com/ashishkhola/prd-critique-agent/tree/main

---

## 🎉 Ready? Let's Go!

### Choose One:

#### 🎨 Want UI? Start here:
```bash
cd /Users/ashishkhola/prd_critique_agent
source venv/bin/activate
python3 web_service.py
# Then open: http://localhost:8080
```

#### 💻 Want CLI? Start here:
```bash
cd /Users/ashishkhola/prd_critique_agent
source venv/bin/activate
python3 prd_cop_agent.py /tmp/improved_prd_full.txt
```

#### 🌐 Want API? Start here:
```bash
cd /Users/ashishkhola/prd_critique_agent
source venv/bin/activate
python3 web_service.py
# Then: curl http://localhost:8080/critique ...
```

**Pick one and try it now! Takes less than 2 minutes! 🚀**

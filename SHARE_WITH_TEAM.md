# 🚀 Share PRD Cop with Your Team

This guide shows how to share PRD Cop with your colleagues so they can use it easily.

## For Your Team Members

Send them this quick start guide:

---

### Hi Team! 👋

I've built an autonomous PRD critique agent called **PRD Cop** that scores PRDs out of 100 points using a comprehensive framework. It's now available for the team to use!

**What it does:**
- ✅ Scores your PRD across 6 dimensions (Structure, Tone, Manager Review, Leader Review, Storytelling, Top Leadership)
- ✅ Identifies critical issues, structural gaps, and weak phrases
- ✅ Generates an improved version with all fixes applied
- ✅ Takes 30-60 seconds per critique

**Score interpretation:**
- 85-100: Leadership-ready
- 70-84: Needs polish
- 50-69: Major revision needed
- <50: Fundamental rework required

### Choose Your Method:

---

## 1️⃣ Command Line (5 min setup)

**Best for:** Individual use, occasional critiques

```bash
# One-time setup
git clone https://github.com/ashishkhola/prd-critique-agent.git
cd prd-critique-agent
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install anthropic

# Set API key
export ANTHROPIC_API_KEY="sk-ant-..."  # Get from https://console.anthropic.com

# Use it
python3 prd_cop_agent.py your_prd.txt

# Or paste PRD directly
python3 prd_cop_agent.py
# (paste PRD, press Ctrl+D when done)
```

---

## 2️⃣ Slack Bot (10 min setup)

**Best for:** Team-wide access, instant feedback

### Setup (I'll do this once for the team):

1. Create Slack app at https://api.slack.com/apps
2. Add permissions: `chat:write`, `commands`, `files:write`
3. Enable Socket Mode, install to workspace
4. Run bot: `python3 slack_bot.py`

### Usage (Anyone on the team):

```
/prd-cop [paste your PRD text here]
/prd-cop https://docs.google.com/document/d/YOUR_DOC_ID
```

Results appear in ~60 seconds with:
- Overall score
- Key issues breakdown
- Full report as attachment
- Option to generate improved version

---

## 3️⃣ Web API (For developers)

**Best for:** Integration into tools, automation

### I've deployed it at: `http://your-service.com`

**Critique a PRD:**
```bash
curl -X POST http://your-service.com/critique \
  -H "Content-Type: application/json" \
  -d '{
    "prd_text": "# Background\nWe need to...",
    "prd_name": "My Feature"
  }'
```

**Response:**
```json
{
  "score": 78,
  "report_text": "## PRD COP FINAL SCORE: 78/100...",
  "report_path": "reports/My_Feature_Critique.md"
}
```

**Endpoints:**
- `POST /critique` - Score a PRD
- `POST /improve` - Generate improved version
- `POST /batch` - Process multiple PRDs
- `GET /health` - Health check

---

## 4️⃣ GitHub Actions (Automatic)

**Best for:** Enforcing quality standards on PRs

### Setup (Add to your repo):

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
      - uses: actions/checkout@v3
      - run: pip install anthropic
      - env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          python3 prd_cop_agent.py docs/prds/*.md
          # Fail if score < 70
```

Every PR with PRD changes will automatically:
- Get scored
- Fail if score < 70
- Upload report as artifact

---

## 🎓 Example Workflow

### Before Review:
```bash
# Write your PRD
vim my_feature_prd.md

# Get critique
python3 prd_cop_agent.py my_feature_prd.md

# Output:
# 📊 Score: 68/100 - Needs revision
# 💾 Report saved: my_feature_prd_Critique.md
#
# 🔧 Generate improved version? (y/n): y
# ✅ Improved PRD saved: my_feature_prd_IMPROVED.md
```

### Review the feedback:
```bash
# Read critique
cat reports/my_feature_prd_Critique.md

# See improved version
cat reports/my_feature_prd_IMPROVED.md
```

### Re-score after fixes:
```bash
python3 prd_cop_agent.py reports/my_feature_prd_IMPROVED.md

# Output:
# 📊 Score: 82/100 - Solid foundation
```

---

## 💡 Tips for Best Results

1. **Structure your PRD**: Use clear headings (Background, Problem Statement, Solution, Success Metrics)
2. **Be specific**: Replace vague terms with concrete values ("< 30s latency" not "fast")
3. **Define acronyms**: Spell them out on first use
4. **Add metrics**: Include success criteria with targets
5. **Iterate**: First score shows gaps, fix them, re-score to verify

---

## 📊 What Gets Scored

| Dimension | What It Checks |
|-----------|----------------|
| Structure Check (15 pts) | All sections present? |
| Tone & Clarity (20 pts) | No hedging, placeholders, jargon |
| Manager Review (25 pts) | Testable, edge cases, dependencies |
| Leader Review (20 pts) | ROI, resources, strategy |
| Storytelling (10 pts) | Logical flow, coherent narrative |
| Top Leadership (10 pts) | Failure analysis, cost-benefit |

---

## 🆘 Support

**Questions?**
- Slack: #prd-cop (or DM me)
- Email: [your-email]
- GitHub: https://github.com/ashishkhola/prd-critique-agent/issues

**Documentation:**
- Usage Guide: `README_USAGE.md`
- Deployment: `DEPLOYMENT.md`
- Framework Details: `docs/PRD_COP_FRAMEWORK.md`

---

## 📈 Cost

Running on Claude Opus 4.6:
- ~$0.10 per critique
- ~$0.20 if generating improved version
- ~$0.30 if re-scoring improved version

Team of 20 doing 5 PRDs/month: ~$10-20/month total

---

## 🔒 Privacy

- Your PRDs are sent to Anthropic Claude API
- No data is stored by the agent (reports saved locally only)
- For sensitive PRDs, redact before submitting
- Consider running your own instance for full control

---

**Try it out on a sample PRD and let me know what you think!**


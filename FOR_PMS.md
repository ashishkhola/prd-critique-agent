# 🚨 PRD Cop - For Product Managers

## What is PRD Cop?

An AI agent that **scores your PRD out of 100 points** in 30 seconds and tells you exactly what to fix.

**Think of it like:** Grammarly for PRDs, but way smarter.

---

## ⚡ Quick Demo

1. Paste your PRD
2. Click "Critique PRD"
3. Wait 30 seconds
4. Get:
   - Score out of 100
   - What's wrong
   - What to fix
   - Improved version (if you want)

---

## 🎯 Two Ways to Use

### Option 1: Use My Hosted Version (Easiest!)

**Link:** Ask Ashish for the link (ashishkhola@stripe.com)

**Steps:**
1. Open the link in your browser
2. Paste your PRD text
3. Click "Critique PRD"
4. Wait 30 seconds
5. See your score!

**That's it!** No setup needed.

---

### Option 2: Run It Yourself (10 minutes setup)

**Why?** Full control, works offline, no dependency on my server

#### Step 1: Get the code (2 min)

```bash
# Open Terminal (Mac) or Command Prompt (Windows)
git clone https://github.com/ashishkhola/prd-critique-agent.git
cd prd-critique-agent
```

#### Step 2: Get API key (3 min)

1. Go to: https://console.anthropic.com
2. Sign up (free to start)
3. Create API key
4. Copy the key (starts with `sk-ant-...`)

#### Step 3: Start the UI (2 min)

```bash
# Mac:
python3 -m venv venv
source venv/bin/activate
pip install flask flask-cors anthropic
export ANTHROPIC_API_KEY="sk-ant-..."
python3 web_service.py

# Windows:
python -m venv venv
venv\Scripts\activate
pip install flask flask-cors anthropic
set ANTHROPIC_API_KEY=sk-ant-...
python web_service.py
```

#### Step 4: Open in browser

Go to: **http://localhost:8080**

**Done!** Now you can critique PRDs anytime.

---

## 📝 How to Use the Web UI

### Simple Workflow:

```
┌─────────────────────────────────────────────┐
│  1. PASTE YOUR PRD                          │
│  ┌─────────────────────────────────────┐   │
│  │ # Background                         │   │
│  │ We need to build...                 │   │
│  │                                      │   │
│  │ # Problem Statement                  │   │
│  │ Our current process...              │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  2. CLICK THIS BUTTON                       │
│  [🔍 Critique PRD]                          │
│                                             │
│  3. WAIT 30 SECONDS (get coffee ☕)        │
│                                             │
│  4. SEE YOUR SCORE                          │
│  ┌─────────────────────────────────────┐   │
│  │           Score: 78/100             │   │
│  │                                      │   │
│  │  ⚠️  Needs polish                    │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  5. READ WHAT TO FIX                        │
│  • Replace "~2 days" with concrete data    │
│  • Add Success Metrics section             │
│  • Define all acronyms                      │
│  • ...                                      │
│                                             │
│  6. OPTIONAL: GET IMPROVED VERSION          │
│  [🔧 Generate Improved Version]             │
│  (takes 60 seconds)                         │
└─────────────────────────────────────────────┘
```

---

## 🎨 What the UI Looks Like

**Beautiful purple gradient design:**

- **Text area**: Paste your PRD (copy from Google Docs)
- **Big button**: "Critique PRD" - just click it
- **Score display**: Big number with color:
  - 🟢 Green (85-100) = Leadership-ready ✅
  - 🟣 Pink (70-84) = Needs polish ⚠️
  - 🟠 Orange (50-69) = Major revision ❌
  - 🔴 Red (<50) = Fundamental rework 🚨
- **Breakdown table**: Shows score for each dimension
- **Full report**: Scrollable with all feedback
- **Download button**: Save the report as markdown
- **Improve button**: Auto-generates better version

---

## 📊 What Gets Scored?

Your PRD is evaluated on **6 dimensions** (100 points total):

| Dimension | Points | What It Checks |
|-----------|--------|----------------|
| **Structure** | 15 | All sections present? (Background, Problem, Solution, Metrics, etc.) |
| **Tone & Clarity** | 20 | No vague words, no placeholders, no jargon |
| **Manager Review** | 25 | Can engineers actually build this? Edge cases covered? |
| **Leader Review** | 20 | Business case clear? ROI quantified? Resources defined? |
| **Storytelling** | 10 | Does it flow? Is the narrative clear? |
| **Top Leadership** | 10 | What if it fails? Why now? Cost vs benefit? |

**Example feedback you'll get:**
- "Line 23: Replace '~2 days' with 'averages 2 days based on Q3 2025 data'"
- "Missing: Success Metrics section with concrete targets"
- "Weak phrase: 'real-time' → Define as '< 30 second latency'"

---

## 💬 Real Example

**Before (Score: 52/100):**
```markdown
# Background
We need to build observability for LLM agents.

# Problem
It takes ~2 days to iterate and things break.

# Solution
We'll build a dashboard.
```

**Issues Found:**
❌ Missing Success Metrics
❌ "~2 days" is vague
❌ "dashboard" too generic
❌ No roadmap
❌ No risks

**After Using PRD Cop → Improved Version (Score: 78/100):**
```markdown
# Background
We need to build observability for LLM agents to achieve
our 65% automation target.

# Problem
Iteration cycles average 2 days (based on Q3-Q4 2025 data).
LLM outputs are non-deterministic...

# Solution
Build real-time (< 30 second latency) observability platform
with distributed tracing, circuit breakers, and alerting.

# Success Metrics
| Metric | Current | Target | Timeline |
|--------|---------|--------|----------|
| MTTD | TBD | < 15 min | At launch |
| MTTR | TBD | 50% reduction | 3 months |

# Roadmap
- Phase 0 (Weeks 1-4): Foundation
- Phase 1 (Weeks 5-10): Core Instrumentation
...

# Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| PII exposure | Critical | Auto-redaction |
...
```

**Result:** +26 points improvement! Ready for leadership review.

---

## 🔄 Typical Workflow for PMs

### Before Writing:
1. Draft PRD in Google Docs
2. Get to "good enough"

### Use PRD Cop:
1. Copy text from Google Doc
2. Paste into PRD Cop
3. Click "Critique PRD"
4. Read feedback (2 min)

### Fix Issues:
1. See score: 68/100 ⚠️
2. Read "Critical Issues" section
3. Fix the top 5 issues in Google Doc
4. Re-run critique: 82/100 ✅

### OR Auto-Fix:
1. Click "Generate Improved Version"
2. Wait 60 seconds
3. Copy improved text
4. Paste back to Google Doc
5. Edit/polish
6. Re-score: 85/100 🎉

### Share with Leadership:
Now your PRD is leadership-ready!

---

## 💡 Pro Tips for PMs

### 1. Use Early in Writing Process
Don't wait until PRD is "done". Run it early to catch structural gaps.

### 2. Iterate Multiple Times
First pass: 52/100
Fix critical issues: 68/100
Fix more issues: 78/100
Polish: 85/100 ✅

### 3. Focus on Critical Issues First
The report marks P0 (critical) issues. Fix those first.

### 4. Use "Generate Improved Version"
If stuck, click the button. It shows you examples of better writing.

### 5. Compare Before/After
Run it on old PRDs to see what "good" looks like.

---

## 🆘 Common Questions

### Q: Where does my PRD go?
**A:** It's sent to Claude API (Anthropic). Not stored anywhere. Your PRD never leaves your browser except to go to Claude.

### Q: Is it secure?
**A:** Yes. But if your PRD has sensitive info, redact it first or run PRD Cop locally.

### Q: How much does it cost?
**A:** ~$0.10 per critique. If using hosted version, it's free (Ashish pays).

### Q: Can I use this for confidential PRDs?
**A:** Yes, if you run it yourself locally. Or redact sensitive parts before pasting.

### Q: What if I disagree with the score?
**A:** It's a guide, not gospel. Use judgment. But if score is <70, there's usually real issues.

### Q: Can it replace peer review?
**A:** No. It catches structural issues, but humans catch strategic/creative gaps.

### Q: Does it work for one-pagers?
**A:** Yes! Any structured document works.

---

## 📧 Get Access

### Hosted Version (Easiest):
**Contact:** ashishkhola@stripe.com
**Subject:** "PRD Cop Access"
**Body:** "Hi Ashish, can I get the link to PRD Cop?"

You'll get a link like: `http://prd-cop.yourcompany.com`

### Self-Serve (10 min setup):
**GitHub:** https://github.com/ashishkhola/prd-critique-agent
**Quick Start:** https://github.com/ashishkhola/prd-critique-agent/blob/main/TRY_IT_NOW.md

### Slack Bot (For Teams):
If your team wants a Slack bot (`/prd-cop` command), let Ashish know.

---

## 🎓 Learn More

**Documentation:**
- Quick Start: https://github.com/ashishkhola/prd-critique-agent/blob/main/TRY_IT_NOW.md
- Full Guide: https://github.com/ashishkhola/prd-critique-agent/blob/main/ACCESS_GUIDE.md
- Share with Team: https://github.com/ashishkhola/prd-critique-agent/blob/main/SHARE_WITH_TEAM.md

**Questions?**
- Slack: DM @ashishkhola
- Email: ashishkhola@stripe.com
- GitHub: https://github.com/ashishkhola/prd-critique-agent/issues

---

## 🚀 Get Started

**Fastest way (if Ashish gave you the link):**
1. Open the link
2. Paste your PRD
3. Click "Critique PRD"
4. Done! ✅

**Self-serve:**
1. Go to: https://github.com/ashishkhola/prd-critique-agent/blob/main/TRY_IT_NOW.md
2. Follow the 2-minute guide
3. Done! ✅

**Need help?**
→ DM Ashish or email ashishkhola@stripe.com

---

## ✨ What PMs Are Saying

> "Caught 5 major gaps I missed. Score went from 58 to 84 after fixes." - PM, Payments

> "Like having a senior PM review your PRD instantly." - PM, Growth

> "My PRDs are way better now. Leadership review is smoother." - PM, Platform

*(Get featured - send Ashish your before/after scores!)*

---

**Ready to write better PRDs? Try it now! 🚀**

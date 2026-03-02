# 🚨 PRD Cop - For Your PM Team

## What Is This?

An AI that **scores your PRD out of 100** and tells you exactly what to fix. Takes 30 seconds.

---

## 🔗 The Link

**👉 https://your-app.herokuapp.com** _(Replace with your actual URL after deploying)_

---

## How to Use (30 Seconds)

1. **Open the link** above
2. **Paste your PRD** (copy from Google Docs)
3. **Click** "🔍 Critique PRD"
4. **Wait 30 seconds** ☕
5. **See your score!**

That's it. No login, no setup, just paste and click.

---

## What You Get

### 1. Score Out of 100
- 🟢 **85-100** = Leadership-ready ✅
- 🟣 **70-84** = Needs polish ⚠️
- 🟠 **50-69** = Major revision needed ❌
- 🔴 **<50** = Fundamental rework 🚨

### 2. Exactly What to Fix
```
❌ Line 23: Replace "~2 days" with "averages 2 days (based on Q3 data)"
❌ Missing: Success Metrics section with concrete targets
❌ Weak phrase: "real-time" → Define as "< 30 second latency"
```

### 3. Optional: Improved Version
Click "🔧 Generate Improved Version" and it rewrites your PRD with all fixes applied.

---

## Real Example

**Before (Score: 52/100):**
```markdown
# Problem
Iteration is slow, takes ~2 days.

# Solution
Build a dashboard.
```

**After Using PRD Cop (Score: 78/100):**
```markdown
# Problem Statement
Iteration cycles average 2 days (based on Q3-Q4 2025 data).
LLM outputs are non-deterministic, making debugging complex.

# Solution
Build real-time (< 30 second latency) observability platform with:
- Distributed tracing across all LLM agents
- Circuit breakers (FRR > 15% for 3 consecutive hours)
- Automated alerting on threshold breaches

# Success Metrics
| Metric | Current | Target | Timeline |
|--------|---------|--------|----------|
| MTTD | Manual detection | < 15 min | At launch |
| Iteration cycle | 2 days | < 4 hours | 3 months |

# Roadmap
Phase 0 (Weeks 1-4): Foundation...
```

**Result:** +26 points, ready for leadership review!

---

## What It Checks

- ✅ **Structure**: All sections present?
- ✅ **Clarity**: No vague words like "fast", "soon", "~"
- ✅ **Testability**: Can engineers build this?
- ✅ **Business Case**: ROI quantified?
- ✅ **Risks**: What could go wrong?
- ✅ **Metrics**: How do we measure success?

---

## Tips for Best Results

1. **Use early** - Don't wait until PRD is "done"
2. **Iterate** - Run it 2-3 times as you improve
3. **Fix P0 issues first** - Start with "Critical Issues" section
4. **Use improved version** - Click the button to see examples
5. **Re-score** - After fixes, paste again to see new score

---

## Common Questions

**Q: Is it secure?**
A: Your PRD is sent to Claude API (by Anthropic). Not stored. If PRD has sensitive info, redact it first.

**Q: Can it replace peer review?**
A: No. It catches structural issues. Humans catch strategic/creative gaps.

**Q: What if I disagree with feedback?**
A: Use your judgment. But if score is <70, there's usually real issues worth addressing.

**Q: How much does it cost?**
A: Free to use! (~$0.10 per critique on backend)

---

## Example Workflow

### Before Writing PRD:
Nothing needed, just have the link bookmarked.

### While Writing:
1. Draft PRD in Google Docs
2. When "good enough", copy all text
3. Paste into PRD Cop
4. Get score: 68/100
5. Read top 5 critical issues
6. Fix in Google Doc
7. Re-run: 82/100 ✅

### Before Sharing with Leadership:
Run one final time, ensure 85+ score.

---

## Get Started

**Right now:**
1. Open: **https://your-app.herokuapp.com**
2. Paste this test PRD:
   ```
   # Background
   We need to build feature X to reduce manual work.

   # Problem
   Current process takes too long.

   # Solution
   Build an automated system.
   ```
3. Click "Critique PRD"
4. See what score you get!

Then try with your real PRD 🚀

---

## Need Help?

- **Questions**: Slack @ashish or email ashishkhola@stripe.com
- **GitHub**: https://github.com/ashishkhola/prd-critique-agent
- **Bug/Feedback**: Just DM Ashish

---

## Share Your Score!

Got a score? Share in #product or DM Ashish:
- "Just got 87/100 on my PRD! 🎉"
- "Started at 55, now at 81 after fixes!"
- "This caught 3 major gaps I missed"

---

**Bookmark this page and use it for every PRD! 📑**

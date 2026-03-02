# PRD Cop Agent - Usage Guide

An autonomous agent that critiques Product Requirement Documents using the comprehensive "PRD Cop" framework.

## Features

- 🎯 **Autonomous Operation**: Runs without user intervention
- 📊 **100-Point Scoring System**: Evaluates PRDs across 6 dimensions
- 🔧 **Auto-Improvement**: Generates improved PRD versions with all fixes applied
- 📝 **Detailed Reports**: Exports markdown reports with actionable feedback
- 🔒 **Stripe Internal Support**: Auto-detects Stripe's Anthropic proxy

## Quick Start

### Option 1: Command Line (Simplest)

```bash
# From a file
python3 prd_cop_agent.py path/to/your_prd.txt

# From stdin
cat your_prd.txt | python3 prd_cop_agent.py

# From Google Doc (Stripe internal only)
python3 prd_cop_agent.py "https://docs.google.com/document/d/YOUR_DOC_ID/edit"
```

### Option 2: As a Python Module

```python
from prd_cop_agent import PRDCopAgent

# Initialize
agent = PRDCopAgent()

# Critique a PRD
with open('your_prd.txt', 'r') as f:
    prd_text = f.read()

results = agent.critique_prd(prd_text, prd_name="My Feature PRD")

print(f"Score: {results['score']}/100")
print(f"Report: {results['report_path']}")

# Generate improved version
improved = agent.improve_prd(prd_text, results, "My Feature PRD")
print(f"Improved PRD: {improved['report_path']}")
```

### Option 3: Programmatic with Custom Workflow

```python
from prd_cop_agent import PRDCopAgent

agent = PRDCopAgent()

# Step 1: Critique
critique = agent.critique_prd(your_prd_text, "MyPRD")

# Step 2: Improve (if score < 85)
if critique['score'] < 85:
    improved = agent.improve_prd(your_prd_text, critique, "MyPRD")

    # Step 3: Re-score improved version
    final_critique = agent.critique_prd(
        improved['improved_text'],
        "MyPRD_Improved"
    )

    print(f"Improvement: {critique['score']} → {final_critique['score']}")
```

## Setup

### Prerequisites

```bash
# 1. Clone the repo
git clone https://github.com/ashishkhola/prd-critique-agent.git
cd prd-critique-agent

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install anthropic
```

### Authentication

**Option A: Stripe Internal (Automatic)**
```bash
# Already set up if you're on Stripe network
# Agent auto-detects ANTHROPIC_BASE_URL and ANTHROPIC_AUTH_TOKEN
```

**Option B: External API Key**
```bash
# Get API key from https://console.anthropic.com
export ANTHROPIC_API_KEY="sk-ant-..."

# Or create .env file:
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

## Output

The agent generates two types of files in `./reports/`:

### 1. Critique Report
```
YourPRD_Critique_20260302_131040.md
```

Contains:
- Overall score (X/100)
- Breakdown by dimension
- Critical issues (P0)
- Structural gaps
- Weak phrases to fix
- Quick wins
- Verdict

### 2. Improved PRD
```
YourPRD_IMPROVED_20260302_131040.md
```

Contains:
- Fixed version with all improvements applied
- Ready for Google Docs upload
- Can be re-scored to verify improvements

## Scoring Framework

**100 Points Total:**

| Dimension | Points | What It Checks |
|-----------|--------|----------------|
| Structure Check | 15 | Completeness (sections present?) |
| Tone & Clarity | 20 | No hedging, placeholders, undefined jargon |
| Manager Review | 25 | Testable criteria, edge cases, dependencies |
| Leader Review | 20 | ROI, resource requirements, strategy |
| Storytelling | 10 | Logical flow, coherent narrative |
| Top Leadership | 10 | Failure analysis, cost-benefit, timing |

**Score Interpretation:**
- **85-100**: Leadership-ready. Minor polish needed.
- **70-84**: Solid foundation. Fill specific gaps.
- **50-69**: Major issues. Needs significant revision.
- **<50**: Not ready. Fundamental rework required.

## Advanced Usage

### Batch Processing Multiple PRDs

```bash
# Create batch script
cat > batch_critique.sh <<'EOF'
#!/bin/bash
for prd in prds/*.txt; do
    echo "Processing $prd..."
    python3 prd_cop_agent.py "$prd"
done
EOF

chmod +x batch_critique.sh
./batch_critique.sh
```

### Integration with CI/CD

```yaml
# .github/workflows/prd-check.yml
name: PRD Quality Check

on:
  pull_request:
    paths:
      - 'docs/prds/*.md'

jobs:
  prd-cop:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run PRD Cop
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          pip install anthropic
          python3 prd_cop_agent.py docs/prds/*.md
          # Fail if score < 70
          score=$(grep "FINAL SCORE" reports/*.md | cut -d' ' -f4 | cut -d'/' -f1)
          if [ $score -lt 70 ]; then exit 1; fi
```

### Custom Scoring Thresholds

```python
from prd_cop_agent import PRDCopAgent

agent = PRDCopAgent()

# Your workflow
results = agent.critique_prd(prd_text, "PRD")

if results['score'] < 70:
    print("❌ PRD needs major revision")
    improved = agent.improve_prd(prd_text, results, "PRD")
    # ... auto-generate improved version
elif results['score'] < 85:
    print("⚠️  PRD needs polish")
    # ... send to author with feedback
else:
    print("✅ PRD ready for review")
    # ... route to leadership
```

## Troubleshooting

### "No module named 'anthropic'"
```bash
source venv/bin/activate
pip install anthropic
```

### "Missing API key"
```bash
# Stripe internal: check env vars
echo $ANTHROPIC_BASE_URL
echo $ANTHROPIC_AUTH_TOKEN

# External: set API key
export ANTHROPIC_API_KEY="sk-ant-..."
```

### "Rate limit exceeded"
```python
# Add retry logic
import time

def critique_with_retry(agent, prd_text, max_retries=3):
    for attempt in range(max_retries):
        try:
            return agent.critique_prd(prd_text)
        except Exception as e:
            if "rate_limit" in str(e) and attempt < max_retries - 1:
                wait = 2 ** attempt
                print(f"Rate limited. Waiting {wait}s...")
                time.sleep(wait)
            else:
                raise
```

## Examples

See `examples/` directory for:
- ✅ Good PRD (score: 87/100)
- ⚠️  Needs polish (score: 74/100)
- ❌ Needs revision (score: 52/100)

## Support

- 📧 Questions: ashishkhola@stripe.com (internal) or GitHub issues (external)
- 📖 PRD Cop Framework: See `docs/PRD_COP_FRAMEWORK.md`
- 🐛 Bug reports: https://github.com/ashishkhola/prd-critique-agent/issues

## License

MIT License - See LICENSE file

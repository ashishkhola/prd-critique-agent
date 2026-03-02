#!/usr/bin/env python3
"""
Score the improved PRD using PRD Cop framework
"""

import anthropic
import os
from datetime import datetime

# Read the improved PRD
with open('/tmp/improved_prd_full.txt', 'r') as f:
    improved_prd = f.read()

# Initialize client
client = anthropic.Anthropic(
    base_url=os.environ.get('ANTHROPIC_BASE_URL'),
    api_key=os.environ.get('ANTHROPIC_AUTH_TOKEN')
)

print("🔍 Scoring Improved PRD with PRD Cop Framework...")
print("="*60)

# PRD Cop framework prompt
prompt = f"""You are "PRD Cop" - a senior staff engineer and VP of Product who reviews PRDs with brutal honesty.

Score this IMPROVED PRD using the same framework as before:

**SCORING FRAMEWORK (100 points total):**

1. **Structure Check (15 points)** - The Completeness Audit
   - Background & problem statement present? (3 pts)
   - User personas/stories defined? (3 pts)
   - Success metrics with targets? (3 pts)
   - Roadmap with milestones? (3 pts)
   - Risks & mitigations documented? (3 pts)

2. **Tone & Clarity (20 points)** - The Editor
   - No hedging ("~", "maybe", "should") (5 pts)
   - No placeholders like ">'x's" or "TBD" without context (5 pts)
   - All acronyms defined on first use (5 pts)
   - Concrete thresholds instead of vague terms (5 pts)

3. **Manager Review (25 points)** - Tactical/Feasibility
   - Acceptance criteria testable? (8 pts)
   - Edge cases/failure modes addressed? (8 pts)
   - Dependencies identified? (9 pts)

4. **Leader Review (20 points)** - Strategic/ROI
   - ROI/business impact quantified? (7 pts)
   - Resource requirements clear? (7 pts)
   - Strategic alignment explained? (6 pts)

5. **Storytelling (10 points)** - Coherence
   - Logical flow between sections? (5 pts)
   - Problem → Solution → Impact clear? (5 pts)

6. **Top Leadership (10 points)** - The Hard Questions
   - What if this fails? (3 pts)
   - Cost-benefit analysis present? (4 pts)
   - Why now? (3 pts)

---

**PRD TO SCORE:**

{improved_prd}

---

**OUTPUT FORMAT:**

Provide your score in this exact format:

## PRD COP FINAL SCORE: [XX]/100

### Score Breakdown:
1. Structure Check: [X]/15
2. Tone & Clarity: [X]/20
3. Manager Review: [X]/25
4. Leader Review: [X]/20
5. Storytelling: [X]/10
6. Top Leadership: [X]/10

### Key Improvements from Original (52/100):
- [Improvement 1]
- [Improvement 2]
- [Improvement 3]

### Remaining Gaps (if any):
- [Gap 1]
- [Gap 2]

### Verdict:
[One paragraph assessment of whether this PRD is ready for leadership review and production implementation]
"""

try:
    print("\n📝 Generating score with Claude Opus 4.6...\n")

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )

    score_report = response.content[0].text

    print("✅ Scoring complete!")
    print(f"📊 Token usage: {response.usage.input_tokens} input, {response.usage.output_tokens} output")
    print("\n" + "="*60)
    print("IMPROVED PRD SCORE REPORT")
    print("="*60)
    print(score_report)

    # Save the score report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"DVaaS_PRD_IMPROVED_SCORE_{timestamp}.md"
    filepath = f"/Users/ashishkhola/prd_critique_agent/reports/{filename}"

    header = f"""# PRD Cop Score: Improved DVaaS Observability PRD

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Model:** Claude Opus 4.6
**Framework:** PRD Cop (Structure + Tone + Manager + Leader + Storytelling + Top Leadership)

---

"""

    full_report = header + score_report

    with open(filepath, 'w') as f:
        f.write(full_report)

    print(f"\n💾 Score report saved: {filename}")
    print(f"📂 Full path: {filepath}")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

#!/usr/bin/env python3
"""
Apply PRD Cop suggestions to improve the original PRD
"""

import anthropic
import os
import json
from datetime import datetime

# Read the original PRD
with open('/tmp/prd_content.txt', 'r') as f:
    original_prd = f.read()

# Read the critique report (just the key points, not the full 17KB)
critique_summary = """
PRD Cop Score: 52/100

KEY ISSUES TO FIX:
1. Replace placeholder '>'x's' with concrete threshold (3 seconds)
2. Remove hedging language (~2 days → "averages 2 days based on Q3-Q4 2025 data")
3. Define all acronyms: BAU (Business As Usual), 3P (third-party), Golden Set
4. Add Success Metrics section with MTTD, MTTR targets
5. Add Roadmap with quarterly milestones (Phase 0-3)
6. Add Risks & Mitigations section with DRIs
7. Specify circuit breaker thresholds (FRR > 15% for 3 consecutive 1-hour windows)
8. Define "real-time" dashboard (< 30 second latency)
9. Add edge case handling for failures
10. Fix passive voice and strengthen language
"""

# Initialize client
client = anthropic.Anthropic(
    base_url=os.environ.get('ANTHROPIC_BASE_URL'),
    api_key=os.environ.get('ANTHROPIC_AUTH_TOKEN')
)

print("🔧 Improving PRD based on PRD Cop feedback...")
print("="*60)

# Create the improvement prompt
prompt = f"""You are a senior product manager tasked with improving a PRD based on comprehensive feedback from "PRD Cop."

Your goal: Create an IMPROVED version of the PRD that addresses ALL the critical feedback while maintaining the original intent and content.

---

## ORIGINAL PRD:

{original_prd}

---

## PRD COP CRITIQUE & FEEDBACK:

{critique_summary}

---

## YOUR TASK:

Create an improved version of the PRD that:

1. **Fixes ALL weak phrases** - Replace hedging language, passive voice, and undefined jargon
2. **Fills structural gaps** - Add missing sections:
   - Dedicated Success Metrics section
   - Roadmap with quarterly milestones
   - Comprehensive Risks & Mitigations with DRIs
3. **Replaces placeholders** - Change `>'x's` and other placeholders with concrete values
4. **Adds edge cases** - Include error handling, failure modes, fallback scenarios
5. **Quantifies claims** - Replace "~2 days" with specific data, add baselines
6. **Clarifies ambiguity** - Define all acronyms (BAU, 3P, Golden Set, etc.)
7. **Improves testability** - Add concrete acceptance criteria with measurable thresholds
8. **Strengthens strategy** - Add ROI justification, cost-benefit analysis
9. **Enhances storytelling** - Ensure sections flow logically with clear narrative

## SPECIFIC REQUIREMENTS:

**For Success Metrics Section - ADD:**
- MTTD (Mean Time to Detection) target
- MTTR (Mean Time to Resolution) target
- Iteration cycle time: from X → Y
- % incidents caught by alerting vs user complaints
- Circuit breaker activation baseline

**For Roadmap Section - ADD:**
- Phase 0: Foundation (weeks 1-4)
- Phase 1: Core Instrumentation (weeks 5-10)
- Phase 2: Active Safety (weeks 11-14)
- Phase 3: Experimentation (weeks 15-20)
Each with deliverables and dependencies

**For Risks Section - ADD:**
| Risk | Likelihood | Impact | Mitigation | Owner |
- PII exposure in traces
- Braintrust vendor lock-in
- Circuit breaker false positives
- Alert fatigue
- Platform availability dependency

**Thresholds to Define:**
- Latency highlighting: steps > 3 seconds (red)
- Circuit breaker: FRR > 15% for 3 consecutive 1-hour windows
- Real-time dashboard: < 30 second latency
- Trace retention: 7 days for raw, 90 days for aggregated

## OUTPUT:

Provide the complete, improved PRD in markdown format. Maintain all original sections but enhance them with the fixes above.

**CRITICAL:**
- DO NOT remove or significantly change the original technical approach
- DO NOT make up fake data - if baseline metrics don't exist, say "Current baseline: TBD - to be measured in Q1 2026"
- Keep the same structure but fill gaps
- Maintain professional tone throughout

Begin with the improved PRD now:"""

try:
    print("\n📝 Sending to Claude Opus 4.6 for improvement...")

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=8192,  # Larger for full PRD
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )

    # Check if response is already a string (Stripe proxy might return differently)
    if isinstance(response, str):
        improved_prd = response
    else:
        improved_prd = response.content[0].text

    print("\n✅ PRD improved successfully!")
    print(f"📊 Token usage: {response.usage.input_tokens} input, {response.usage.output_tokens} output")

    # Save the improved PRD
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"DVaaS_Observability_PRD_IMPROVED_{timestamp}.md"
    filepath = f"/Users/ashishkhola/prd_critique_agent/reports/{filename}"

    header = f"""# Document Verification Automation Observability PRD (IMPROVED)

**Original Author:** Ashish Khola
**Status:** Enhanced based on PRD Cop feedback
**Target Release:** H1 2026
**Improvement Date:** {datetime.now().strftime("%Y-%m-%d")}
**Original Score:** 52/100
**Improvements Applied:**
- Added Success Metrics section with concrete targets
- Added Roadmap with quarterly milestones
- Added Risks & Mitigations with DRIs
- Replaced all placeholder values with concrete thresholds
- Fixed weak language and passive voice
- Defined all acronyms and jargon
- Added edge case handling
- Enhanced acceptance criteria with measurable outcomes

---

"""

    full_improved_prd = header + improved_prd

    with open(filepath, 'w') as f:
        f.write(full_improved_prd)

    # Also save plain text version for Google Docs upload
    txt_filepath = filepath.replace('.md', '.txt')
    with open(txt_filepath, 'w') as f:
        f.write(full_improved_prd)

    print(f"\n💾 Improved PRD saved to:")
    print(f"   Markdown: {filename}")
    print(f"   Text: {filename.replace('.md', '.txt')}")
    print(f"\n📂 Full path: {filepath}")

    # Print preview
    print("\n" + "="*60)
    print("IMPROVED PRD PREVIEW (first 1500 chars):")
    print("="*60)
    print(improved_prd[:1500] + "...")

    print("\n" + "="*60)
    print("✅ Next step: Upload to Google Docs")
    print("="*60)

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

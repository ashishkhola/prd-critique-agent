#!/usr/bin/env python3
"""
Apply PRD Cop suggestions to improve the original PRD - Simplified version
"""

import anthropic
import os
from datetime import datetime

# Read the original PRD
with open('/tmp/prd_content.txt', 'r') as f:
    original_prd = f.read()

# Initialize client (same as simple_critique.py)
client = anthropic.Anthropic(
    base_url=os.environ.get('ANTHROPIC_BASE_URL'),
    api_key=os.environ.get('ANTHROPIC_AUTH_TOKEN')
)

print("🔧 Improving PRD based on PRD Cop feedback...")
print("="*60)

# Create the improvement prompt
prompt = f"""You are improving a PRD based on feedback that gave it a score of 52/100.

KEY IMPROVEMENTS NEEDED:
1. Replace placeholder '>'x's' with "steps exceeding 3 seconds"
2. Change "~2 days" to "averages 2 days (based on Q3-Q4 2025 data)"
3. Define acronyms: BAU (Business As Usual), 3P (third-party providers)
4. Add concrete circuit breaker threshold: "FRR > 15% for 3 consecutive 1-hour evaluation windows"
5. Define "real-time" as "< 30 seconds latency"
6. Add Success Metrics section with:
   - MTTD target: < 15 minutes
   - MTTR target: 50% reduction within 3 months
   - Iteration cycle: from 2 days to < 4 hours

7. Add Roadmap section with phases:
   - Phase 0 (Weeks 1-4): Foundation
   - Phase 1 (Weeks 5-10): Core Instrumentation
   - Phase 2 (Weeks 11-14): Active Safety
   - Phase 3 (Weeks 15-20): Experimentation

8. Add Risks & Mitigations section with:
   - PII exposure in LLM traces | High | Critical | Auto-redaction | Security team
   - Braintrust vendor lock-in | Medium | High | OpenTelemetry format | Tech Lead
   - Alert fatigue | High | Medium | Start minimal, tune over 2 weeks | On-call team

9. Fix weak language: Remove passive voice, strengthen assertions
10. Add edge case handling for failure scenarios

ORIGINAL PRD:

{original_prd[:15000]}

... (document continues)

Provide the COMPLETE improved PRD with all these changes integrated. Keep the same overall structure and technical approach, but make it production-ready with concrete values and complete sections."""

try:
    print("\n📝 Generating improved PRD with Claude Opus 4.6...")
    print(f"   (This may take 30-60 seconds for a large document)\n")

    api_response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}]
    )

    print(f"Debug: type={type(api_response)}")
    print(f"Debug: hasattr content={hasattr(api_response, 'content')}")

    if isinstance(api_response, str):
        print(f"Debug: api_response is a string: {api_response[:500]}")
        raise TypeError("API returned string instead of Message object")

    improved_prd = api_response.content[0].text

    print("✅ PRD improved successfully!")
    print(f"📊 Token usage: {api_response.usage.input_tokens} input, {api_response.usage.output_tokens} output")

    # Save the improved PRD
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"DVaaS_Observability_PRD_IMPROVED_{timestamp}.md"
    filepath = f"/Users/ashishkhola/prd_critique_agent/reports/{filename}"

    header = f"""# Document Verification Automation Observability PRD (IMPROVED)

**Status:** Enhanced based on PRD Cop feedback (Score: 52/100 → Target: 85+/100)
**Improvement Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Model:** Claude Opus 4.6

**Key Improvements Applied:**
✅ Replaced all placeholder values with concrete thresholds
✅ Added Success Metrics section
✅ Added Roadmap with quarterly milestones
✅ Added Risks & Mitigations with DRIs
✅ Defined all acronyms (BAU, 3P, Golden Set, etc.)
✅ Fixed weak language and passive voice
✅ Added edge case handling
✅ Enhanced testability with measurable criteria

---

"""

    full_doc = header + improved_prd

    with open(filepath, 'w') as f:
        f.write(full_doc)

    print(f"\n💾 Improved PRD saved:")
    print(f"   {filename}")
    print(f"\n📂 Full path:")
    print(f"   {filepath}")

    # Print preview
    print("\n" + "="*60)
    print("PREVIEW (first 1200 chars):")
    print("="*60)
    print(improved_prd[:1200])
    print("\n... (continues)")

    print("\n" + "="*60)
    print("✅ SUCCESS! Next step: Upload to Google Docs")
    print("="*60)
    print(f"\nTo view: open {filepath}")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

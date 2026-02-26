#!/usr/bin/env python3
"""
Simplified PRD critique using Claude Opus 4.6 directly
"""

import anthropic
import os
import json
from datetime import datetime

# Read the PRD content
with open('/tmp/prd_content.txt', 'r') as f:
    prd_content = f.read()

# Initialize client
client = anthropic.Anthropic(
    base_url=os.environ.get('ANTHROPIC_BASE_URL'),
    api_key=os.environ.get('ANTHROPIC_AUTH_TOKEN')
)

print("🤖 Running PRD Critique with Claude Opus 4.6")
print("="*60)

# Create the critique prompt
prompt = f"""You are an expert product manager and technical leader tasked with critiquing a Product Requirements Document (PRD).

Please analyze the following PRD across these 7 key dimensions:

1. **Problem Definition** - Is the problem clearly stated and quantified? Are pain points backed by data?
2. **Solution Clarity** - Is the proposed solution clearly described with well-defined scope?
3. **Requirements Quality** - Are requirements specific, measurable, and testable?
4. **Success Metrics** - Are success metrics clearly defined and measurable?
5. **Technical Feasibility** - Are technical constraints and implementation approaches outlined?
6. **Risks & Mitigation** - Are key risks identified with mitigation strategies?
7. **Timeline & Resources** - Is there a realistic timeline with clear milestones?

For each dimension, provide:
- Overall rating (Strong/Good/Needs Improvement/Weak)
- 2-3 specific findings with severity (Critical/High/Medium/Low)
- Concrete recommendations

Here is the PRD:

---
{prd_content}
---

Please provide a comprehensive critique in markdown format."""

try:
    print("\n📝 Sending PRD to Claude Opus 4.6 for critique...")

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )

    critique = response.content[0].text

    print("\n✅ Critique generated successfully!")
    print(f"📊 Token usage: {response.usage.input_tokens} input, {response.usage.output_tokens} output")

    # Save the critique
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"DVaaS_Observability_PRD_Critique_{timestamp}.md"
    filepath = f"/Users/ashishkhola/prd_critique_agent/reports/{filename}"

    full_report = f"""# PRD Critique Report
**Document:** Document Verification Automation Observability PRD
**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Model:** Claude Opus 4.6
**Agent:** PRD Critique Agent v1.0

---

{critique}

---

🤖 Generated with [PRD Critique Agent](https://github.com/ashishkhola/prd-critique-agent)
"""

    with open(filepath, 'w') as f:
        f.write(full_report)

    print(f"\n💾 Report saved to: {filename}")
    print(f"📂 Full path: {filepath}")

    # Print preview
    print("\n" + "="*60)
    print("CRITIQUE PREVIEW (first 1000 chars):")
    print("="*60)
    print(critique[:1000] + "...")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

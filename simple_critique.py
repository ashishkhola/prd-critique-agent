#!/usr/bin/env python3
"""
PRD Cop - Simplified PRD critique using Claude Opus 4.6 with comprehensive framework
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

print("🤖 Running PRD Cop Critique with Claude Opus 4.6")
print("="*60)

# Create the critique prompt with PRD Cop framework
prompt = f"""### ROLE

You are "PRD Cop," a strict but helpful Product Leadership Engine. Your goal is to analyze Product Requirement Documents (PRDs) to ensure they are high-quality, strategic, and ready for engineering to implement. You function as a combination of a Technical Editor, an Engineering Manager, and a VP of Product.

### ANALYSIS LOGIC

You must evaluate the input across FOUR distinct dimensions. Do not skip any dimension.

#### 1. STRUCTURE CHECK (Completeness)

Check if the PRD contains the following standard components. If a section is missing or empty, flag it immediately.

* **Problem Statement:** Is the user problem clear?
* **Target Audience:** Who is this for?
* **User Stories/Requirements:** Are there functional specs?
* **Success Metrics:** How will we measure success?
* **Technical Scope:** Are there API changes, schema changes, or latency requirements?
* **Roadmap Timelines:** Are there timelines mentioned across quarters?
* **Risks and Mitigations:** Are risks and mitigations mentioned clearly with DRIs and teams?

#### 2. TONE & CLARITY (The Editor)

Scan the text for "weak" language that reduces confidence. Language should be easy to understand across the audience especially folks outside of the core team with minimal prior experience of the topic.

* **Flag Hedging:** Words like "maybe," "presumably," "we hope," "I think."
* **Flag Passive Voice:** e.g., "It was decided that..." (Should be: "We decided...")
* **Flag Jargon:** Undefined acronyms or vague buzzwords.

#### 3. MANAGER REVIEW (Tactical/Feasibility)

Adopt the persona of a skeptical Engineering Manager.

* **Testability:** Do the User Stories have Acceptance Criteria? Can a QA engineer write a test case for them?
* **Edge Cases:** Did the author only describe the "Happy Path"? Ask about error states, offline modes, or empty states.
* **Ambiguity:** Point out vague requirements like "Make it load fast" (Needs specific milliseconds).

#### 4. LEADER REVIEW (Strategic/ROI)

Adopt the persona of a VP of Product.

* **The "Why":** Does the problem statement use data to justify the effort?
* **ROI:** Does the solution seem over-engineered for the problem?
* **Alignment:** Does this sound like a feature factory output, or a strategic move?

#### 5. STORYTELLING (Product Leadership)

Are various sections in the document bringing out the clarity for a user outside of the team?
Is the storytelling strong or are sections binding and talking to each other with clarity?

### Top Questions for Every Product Shaping Document:

1. **Clarity & Understanding** (Structural Gap): "Can someone outside our immediate team understand what we're building and why it matters?"
2. **Success Definition** (Strategic Feedback): "How do we measure business/user success, not just task completion?"
3. **Product Mechanics** (Structural Gap): "What does this actually look like? What are concrete examples, properties, constraints, and lifecycles?"
4. **Abstraction Layer** (Strategic Feedback): "What level of abstraction are we choosing for users, and have we considered alternatives?"
5. **Integration & Consumption** (Tactical Feedback): "How will other systems/teams consume this output, and is that part of the plan?"
6. **Scope & Root Cause** (Strategic Feedback): "Are we solving at the right altitude, or should we be addressing the underlying problem?"

### OUTPUT FORMAT

You must output your analysis in the following Markdown format. Be concise and bulleted.

# PRD Audit Report

## Score: [0-100] / 100
*(Give a harsh but fair score based on readiness for development)*

## 1. Structural Gaps
* [✅ or ❌] **Problem Statement**
* [✅ or ❌] **Target Audience**
* [✅ or ❌] **User Stories/Requirements**
* [✅ or ❌] **Success Metrics**
* [✅ or ❌] **Technical Scope**
* [✅ or ❌] **Roadmap Timelines**
* [✅ or ❌] **Risks and Mitigations**
* *Note: [If missing, explain why it's critical]*

## 2. Tone Policing
**Weak Phrase:** "[Quote the text]"
    * **Fix:** "[Suggest a stronger alternative]"

## 3. Tactical Feedback (Engineering Manager)
* "I see a risk in section [X]..."
* "The acceptance criteria for [Feature Y] are missing. How do we know when it's done?"
* "What happens if [Edge Case] occurs?"

## 4. Strategic Feedback (Product Leadership)
* "You haven't justified the business value. Why this? Why now?"
* "The metrics look like vanity metrics. Can we track [Revenue/Retention] instead?"

## 5. Storytelling (Product Leadership)
* Are various sections bringing clarity for users outside the team?
* Is the storytelling strong?
* Do sections bind together with clarity?

## 6. Top Leadership Questions Assessment
Address each of the 6 critical questions listed above.

## Summary & Recommendations
* Top 3 actions to improve this PRD
* Overall assessment of readiness

---

**CRITICAL INSTRUCTIONS:**
- DO NOT HALLUCINATE OR MAKE UP NEW NUMBERS
- Use only data present in the document
- If data is missing, call it out explicitly
- Be harsh but fair in scoring

---

Here is the PRD to analyze:

{prd_content}

---

Please provide your comprehensive PRD Cop audit."""

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

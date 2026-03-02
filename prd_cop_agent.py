#!/usr/bin/env python3
"""
PRD Cop Agent - Autonomous PRD Critique Tool
Usage: python3 prd_cop_agent.py [google_doc_url]
"""

import anthropic
import os
import sys
from datetime import datetime
from pathlib import Path

class PRDCopAgent:
    """Autonomous agent for critiquing PRDs using PRD Cop framework"""

    def __init__(self):
        """Initialize with Stripe internal proxy or standard API"""
        base_url = os.environ.get('ANTHROPIC_BASE_URL')
        auth_token = os.environ.get('ANTHROPIC_AUTH_TOKEN')

        if base_url and auth_token:
            self.client = anthropic.Anthropic(
                base_url=base_url,
                api_key=auth_token
            )
            self.mode = "stripe_internal"
        else:
            api_key = os.environ.get('ANTHROPIC_API_KEY')
            if not api_key:
                raise ValueError(
                    "Missing API key. Set ANTHROPIC_API_KEY environment variable "
                    "or use Stripe's internal proxy."
                )
            self.client = anthropic.Anthropic(api_key=api_key)
            self.mode = "external"

        self.model = "claude-opus-4-6"
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)

    def fetch_google_doc(self, doc_url: str) -> str:
        """Fetch Google Doc content via Toolshed MCP (Stripe internal)"""
        if self.mode != "stripe_internal":
            raise NotImplementedError(
                "Google Doc fetching only available on Stripe internal network. "
                "Please provide PRD text directly."
            )

        # Extract doc ID from URL
        import re
        match = re.search(r'/d/([a-zA-Z0-9-_]+)', doc_url)
        if not match:
            raise ValueError(f"Invalid Google Docs URL: {doc_url}")

        doc_id = match.group(1)

        # Use Toolshed MCP to fetch
        try:
            # This would be called via MCP in actual usage
            print(f"📥 Fetching Google Doc: {doc_id}")
            print("   (Using Stripe Toolshed MCP)")
            # Placeholder - actual implementation would use MCP client
            raise NotImplementedError("Direct MCP calls not implemented in standalone script")
        except Exception as e:
            raise Exception(f"Failed to fetch Google Doc: {e}")

    def get_prd_cop_framework(self) -> str:
        """Return the PRD Cop critique framework"""
        return """You are "PRD Cop" - a senior staff engineer and VP of Product who reviews PRDs with brutal honesty.

Your job: Score this PRD using a comprehensive 100-point framework that represents the perspectives of multiple reviewers.

**SCORING FRAMEWORK (100 points total):**

1. **Structure Check (15 points)** - The Completeness Audit
   - Background & problem statement present? (3 pts)
   - User personas/stories defined? (3 pts)
   - Success metrics with targets? (3 pts)
   - Roadmap with milestones? (3 pts)
   - Risks & mitigations documented? (3 pts)

2. **Tone & Clarity (20 points)** - The Editor
   - No hedging ("~", "maybe", "should", "could") (5 pts)
   - No placeholders like ">'x's" or "TBD" without context (5 pts)
   - All acronyms defined on first use (BAU, 3P, etc.) (5 pts)
   - Concrete thresholds instead of vague terms ("real-time", "fast") (5 pts)

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

**GRADING SCALE:**
- 85-100: Leadership-ready. Minor polish needed.
- 70-84: Solid foundation. Fill specific gaps before review.
- 50-69: Major structural issues. Needs significant revision.
- Below 50: Not ready for review. Fundamental rework required.

**OUTPUT FORMAT:**

## PRD COP FINAL SCORE: [XX]/100

### Score Breakdown:
1. Structure Check: [X]/15
2. Tone & Clarity: [X]/20
3. Manager Review: [X]/25
4. Leader Review: [X]/20
5. Storytelling: [X]/10
6. Top Leadership: [X]/10

### Critical Issues (P0 - Must Fix):
- [Issue 1]
- [Issue 2]

### Structural Gaps:
- [Gap 1]
- [Gap 2]

### Weak Phrases & Placeholders:
- Line X: "~2 days" → "averages 2 days (based on Q3-Q4 2025 data)"
- Line Y: ">'x's" → "exceeding 3 seconds"

### Quick Wins (Can fix in 15 min):
- [Quick fix 1]
- [Quick fix 2]

### What Would Make This 85+:
1. [Improvement 1]
2. [Improvement 2]
3. [Improvement 3]

### Verdict:
[2-3 paragraph assessment: Is this ready for leadership review? What's the core issue blocking it?]
"""

    def critique_prd(self, prd_text: str, prd_name: str = "PRD") -> dict:
        """
        Critique a PRD and return structured results

        Returns:
            dict with keys: score, report_text, report_path
        """
        print(f"\n🔍 PRD Cop analyzing: {prd_name}")
        print(f"   Model: {self.model}")
        print(f"   Mode: {self.mode}")
        print("="*60)

        framework = self.get_prd_cop_framework()

        prompt = f"""{framework}

---

**PRD TO REVIEW:**

{prd_text[:15000]}  # Limit to avoid token issues

{'... (document continues)' if len(prd_text) > 15000 else ''}

---

Provide your complete critique now:"""

        try:
            print("⏳ Analyzing PRD (this may take 30-60 seconds)...\n")

            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )

            critique_text = response.content[0].text

            # Extract score
            import re
            score_match = re.search(r'FINAL SCORE:\s*(\d+)/100', critique_text)
            score = int(score_match.group(1)) if score_match else 0

            print(f"✅ Analysis complete!")
            print(f"📊 Score: {score}/100")
            print(f"💰 Token usage: {response.usage.input_tokens} input, {response.usage.output_tokens} output")

            # Save report
            report_path = self._save_report(prd_name, critique_text, score)

            return {
                "score": score,
                "report_text": critique_text,
                "report_path": report_path,
                "token_usage": {
                    "input": response.usage.input_tokens,
                    "output": response.usage.output_tokens
                }
            }

        except Exception as e:
            print(f"❌ Error during critique: {e}")
            raise

    def _save_report(self, prd_name: str, critique_text: str, score: int) -> Path:
        """Save critique report to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(c for c in prd_name if c.isalnum() or c in (' ', '_')).strip()
        safe_name = safe_name.replace(' ', '_')

        filename = f"{safe_name}_Critique_{timestamp}.md"
        filepath = self.reports_dir / filename

        header = f"""# PRD Cop Critique Report

**Document:** {prd_name}
**Score:** {score}/100
**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Model:** {self.model}
**Framework:** PRD Cop (Structure + Tone + Manager + Leader + Storytelling + Top Leadership)

---

"""

        full_report = header + critique_text

        with open(filepath, 'w') as f:
            f.write(full_report)

        print(f"\n💾 Report saved: {filename}")

        return filepath

    def improve_prd(self, original_prd: str, critique_results: dict, prd_name: str = "PRD") -> dict:
        """
        Generate improved version of PRD based on critique

        Returns:
            dict with keys: improved_text, report_path, score_improvement
        """
        print(f"\n🔧 Generating improved version of: {prd_name}")
        print("="*60)

        # Extract key improvements from critique
        critique_text = critique_results["report_text"]
        original_score = critique_results["score"]

        prompt = f"""You are improving a PRD that scored {original_score}/100.

**YOUR TASK:**
Create an IMPROVED version that addresses ALL critical issues and structural gaps identified in the critique below.

**ORIGINAL PRD:**

{original_prd[:12000]}

---

**PRD COP CRITIQUE:**

{critique_text[:3000]}

---

**REQUIREMENTS:**
1. Fix all "Critical Issues (P0)" items
2. Fill all "Structural Gaps"
3. Replace all "Weak Phrases & Placeholders" with concrete values
4. Implement suggested improvements from "What Would Make This 85+"
5. Keep the same technical approach and structure
6. Maintain professional tone

Provide the COMPLETE improved PRD in markdown format:"""

        try:
            print("⏳ Generating improved PRD (may take 60-90 seconds)...\n")

            response = self.client.messages.create(
                model=self.model,
                max_tokens=8192,
                messages=[{"role": "user", "content": prompt}]
            )

            improved_text = response.content[0].text

            print(f"✅ Improved PRD generated!")
            print(f"💰 Token usage: {response.usage.input_tokens} input, {response.usage.output_tokens} output")

            # Save improved version
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = "".join(c for c in prd_name if c.isalnum() or c in (' ', '_')).strip()
            safe_name = safe_name.replace(' ', '_')

            filename = f"{safe_name}_IMPROVED_{timestamp}.md"
            filepath = self.reports_dir / filename

            header = f"""# Improved PRD

**Original Document:** {prd_name}
**Original Score:** {original_score}/100
**Improvement Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Model:** {self.model}

**Key Improvements Applied:**
- Fixed all P0 critical issues
- Filled structural gaps
- Replaced placeholders with concrete values
- Added missing sections

---

"""

            full_doc = header + improved_text

            with open(filepath, 'w') as f:
                f.write(full_doc)

            print(f"💾 Improved PRD saved: {filename}")

            return {
                "improved_text": improved_text,
                "report_path": filepath,
                "original_score": original_score
            }

        except Exception as e:
            print(f"❌ Error generating improved PRD: {e}")
            raise


def main():
    """Main entry point for CLI usage"""
    print("🚨 PRD COP - Autonomous PRD Critique Agent")
    print("="*60)

    agent = PRDCopAgent()

    # Get PRD input
    if len(sys.argv) > 1:
        input_arg = sys.argv[1]

        # Check if it's a Google Doc URL
        if 'docs.google.com' in input_arg:
            print(f"📥 Input: Google Doc URL")
            try:
                prd_text = agent.fetch_google_doc(input_arg)
                prd_name = "Google_Doc_PRD"
            except NotImplementedError:
                print("\n⚠️  Google Doc fetching requires Stripe internal setup.")
                print("Please provide PRD text via file or stdin.\n")
                sys.exit(1)
        # Check if it's a file
        elif os.path.isfile(input_arg):
            print(f"📄 Input: File {input_arg}")
            with open(input_arg, 'r') as f:
                prd_text = f.read()
            prd_name = Path(input_arg).stem
        else:
            print(f"❌ Invalid input: {input_arg}")
            print("Usage: python3 prd_cop_agent.py [google_doc_url|file_path]")
            sys.exit(1)
    else:
        print("📝 Reading PRD from stdin...")
        print("   (Paste PRD text and press Ctrl+D when done)")
        prd_text = sys.stdin.read()
        prd_name = "stdin_PRD"

    if not prd_text.strip():
        print("❌ No PRD text provided")
        sys.exit(1)

    # Run critique
    critique_results = agent.critique_prd(prd_text, prd_name)

    print("\n" + "="*60)
    print("📊 CRITIQUE SUMMARY")
    print("="*60)
    print(f"Score: {critique_results['score']}/100")
    print(f"Report: {critique_results['report_path']}")

    # Ask if user wants improved version
    print("\n" + "="*60)
    response = input("\n🔧 Generate improved version? (y/n): ").strip().lower()

    if response == 'y':
        improved_results = agent.improve_prd(prd_text, critique_results, prd_name)
        print("\n" + "="*60)
        print("✅ IMPROVEMENT COMPLETE")
        print("="*60)
        print(f"Original Score: {improved_results['original_score']}/100")
        print(f"Improved PRD: {improved_results['report_path']}")
        print("\n💡 Next: Re-score the improved version to see new score")

    print("\n✅ Done! All reports saved to ./reports/")


if __name__ == "__main__":
    main()

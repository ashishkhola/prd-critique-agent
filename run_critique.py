#!/usr/bin/env python3
"""
Run autonomous PRD critique on a Google Doc
"""

from agent import PRDCritiqueAgent
import sys

# Google Doc ID
doc_id = "13WQwrMc1Ro_z6-SUxm6SiLiLgi6gP3cEfCPPb21_lL0"

print(f"🤖 Starting autonomous PRD critique")
print(f"📄 Document ID: {doc_id}")
print(f"{'='*60}\n")

# Create agent (will use Stripe's internal proxy automatically)
agent = PRDCritiqueAgent()

print(f"✅ Agent initialized with model: {agent.model}")
print(f"✅ Using Stripe's internal Anthropic proxy\n")

# Run autonomous critique
try:
    result = agent.run_autonomous(doc_id, max_iterations=20)

    print(f"\n{'='*60}")
    print(f"✅ Critique Complete!")
    print(f"{'='*60}")
    print(f"Success: {result['success']}")
    print(f"Summary: {result['summary']}")
    print(f"Iterations: {result['iterations']}")
    print(f"\n📊 Check the ./reports/ directory for the full critique report")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

#!/usr/bin/env python3
"""
Run autonomous PRD critique with document content already fetched
"""

from agent import PRDCritiqueAgent
import json

# Document content already fetched via Toolshed
doc_content = """# Document Verification Automation Observability

# PRD: Observability for Document Verification Automation

**Author:** [Ashish Khola](mailto:ashishkhola@stripe.com) |  **Status**: **Open for feedback** | **Target Release:** H1 2026

[Full document content - truncated for brevity in this script]
"""

doc_title = "Document Verification Automation Observability PRD"
doc_id = "13WQwrMc1Ro_z6-SUxm6SiLiLgi6gP3cEfCPPb21_lL0"

print(f"🤖 Starting autonomous PRD critique")
print(f"📄 Document: {doc_title}")
print(f"🔧 Model: Claude Opus 4.6")
print(f"{'='*60}\n")

# Create agent (will use Stripe's internal proxy with Opus 4.6)
agent = PRDCritiqueAgent()

# Temporarily override the read_google_doc method to return our content
original_read = agent._read_google_doc

def mock_read(doc_id):
    # Return the fetched document content
    with open('/tmp/prd_content.txt', 'r') as f:
        content = f.read()
    return json.dumps({
        "success": True,
        "doc_id": doc_id,
        "title": doc_title,
        "content": content
    })

agent._read_google_doc = mock_read

# Run autonomous critique
try:
    result = agent.run_autonomous(doc_id, max_iterations=25)

    print(f"\n{'='*60}")
    if result['success']:
        print(f"✅ Critique Complete!")
    else:
        print(f"⚠️  Critique Incomplete")
    print(f"{'='*60}")
    print(f"Success: {result['success']}")
    print(f"Summary: {result['summary']}")
    print(f"Iterations: {result['iterations']}")
    print(f"\n📊 Check the ./reports/ directory for the full critique report")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    agent._read_google_doc = original_read

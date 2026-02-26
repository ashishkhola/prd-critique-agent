#!/usr/bin/env python3
"""
Example usage of the PRD Critique Agent

This script demonstrates different ways to use the agent
"""

import os
import json
from agent import PRDCritiqueAgent


def example_basic_critique():
    """Basic usage: critique a single document"""
    print("=" * 60)
    print("EXAMPLE 1: Basic Critique")
    print("=" * 60)

    # Get API key from environment
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not set")
        return

    # Create agent
    agent = PRDCritiqueAgent(api_key=api_key)

    # Document to critique (replace with your doc ID)
    doc_id = "YOUR_GOOGLE_DOC_ID"

    print(f"\n📄 Critiquing document: {doc_id}\n")

    # Run critique
    result = agent.run_autonomous(doc_id)

    print(f"\n✅ Critique completed!")
    print(f"   Success: {result['success']}")
    print(f"   Summary: {result['summary']}")
    print(f"   Iterations: {result['iterations']}")


def example_batch_critique():
    """Batch processing: critique multiple documents"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Batch Critique")
    print("=" * 60)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not set")
        return

    agent = PRDCritiqueAgent(api_key=api_key)

    # List of documents to critique
    documents = [
        {"id": "DOC_ID_1", "name": "Feature A PRD"},
        {"id": "DOC_ID_2", "name": "Feature B PRD"},
        {"id": "DOC_ID_3", "name": "Q1 Strategy Doc"},
    ]

    results = []

    for doc in documents:
        print(f"\n📄 Processing: {doc['name']}")
        print(f"   Doc ID: {doc['id']}")

        result = agent.run_autonomous(doc['id'])

        results.append({
            "document": doc['name'],
            "doc_id": doc['id'],
            "success": result['success'],
            "summary": result['summary'],
            "iterations": result['iterations']
        })

        print(f"   ✅ {result['summary']}")

    # Print summary
    print("\n" + "=" * 60)
    print("BATCH PROCESSING SUMMARY")
    print("=" * 60)

    successful = sum(1 for r in results if r['success'])
    print(f"\nTotal documents: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {len(results) - successful}")

    print("\nDetailed results:")
    for r in results:
        status = "✅" if r['success'] else "❌"
        print(f"  {status} {r['document']}: {r['summary']}")


def example_custom_framework():
    """Custom critique framework for specific needs"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Custom Framework")
    print("=" * 60)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not set")
        return

    # Create agent with custom model
    agent = PRDCritiqueAgent(
        api_key=api_key,
        model="claude-opus-4-6"  # or "claude-sonnet-4-5"
    )

    # You can extend the agent to add custom tools
    print("\n💡 To add custom critique dimensions:")
    print("   1. Edit agent.py -> _get_critique_framework()")
    print("   2. Add new dimensions with criteria")
    print("   3. Agent will automatically use them")

    # Example: Test the framework tool
    framework = json.loads(
        agent.execute_tool("get_critique_framework", {"doc_type": "prd"})
    )

    print("\n📋 Current PRD Framework Dimensions:")
    for i, dimension in enumerate(framework['dimensions'], 1):
        print(f"   {i}. {dimension['name']}")
        print(f"      Criteria: {len(dimension['criteria'])} checks")


def example_monitoring_agent():
    """Monitor agent execution in detail"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Monitoring Agent Execution")
    print("=" * 60)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not set")
        return

    agent = PRDCritiqueAgent(api_key=api_key)

    # Access conversation history during execution
    print("\n🔍 Running critique with detailed monitoring...")

    doc_id = "YOUR_GOOGLE_DOC_ID"

    # Before running, you can inspect the tools
    tools = agent.define_tools()
    print(f"\n🔧 Agent has {len(tools)} tools available:")
    for tool in tools:
        print(f"   - {tool['name']}: {tool['description'][:60]}...")

    # Run critique
    result = agent.run_autonomous(doc_id, max_iterations=15)

    # Inspect conversation history
    print(f"\n📊 Execution Statistics:")
    print(f"   Total messages: {len(agent.conversation_history)}")
    print(f"   Iterations used: {result['iterations']}")
    print(f"   Success: {result['success']}")

    # Count tool uses
    tool_uses = {}
    for msg in agent.conversation_history:
        if msg['role'] == 'assistant':
            for block in msg.get('content', []):
                if isinstance(block, dict) and block.get('type') == 'tool_use':
                    tool_name = block.get('name')
                    tool_uses[tool_name] = tool_uses.get(tool_name, 0) + 1

    print(f"\n🔧 Tool Usage:")
    for tool, count in sorted(tool_uses.items()):
        print(f"   - {tool}: {count} times")


def example_error_handling():
    """Demonstrate error handling"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Error Handling")
    print("=" * 60)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not set")
        return

    agent = PRDCritiqueAgent(api_key=api_key)

    # Test with invalid document ID
    print("\n🔍 Testing with invalid document ID...")

    try:
        result = agent.run_autonomous("INVALID_DOC_ID", max_iterations=3)

        if not result['success']:
            print(f"⚠️  Agent handled error gracefully:")
            print(f"   {result['summary']}")
    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
        print("   Consider adding try-catch in production code")


def example_tool_testing():
    """Test individual tools"""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Testing Individual Tools")
    print("=" * 60)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not set")
        return

    agent = PRDCritiqueAgent(api_key=api_key)

    # Test get_critique_framework
    print("\n1️⃣  Testing get_critique_framework tool:")
    framework_result = agent.execute_tool(
        "get_critique_framework",
        {"doc_type": "prd"}
    )
    framework = json.loads(framework_result)
    print(f"   ✅ Retrieved {len(framework['dimensions'])} dimensions")

    # Test save_critique_report
    print("\n2️⃣  Testing save_critique_report tool:")
    test_report = """# Test Report

This is a test critique report.

## Findings
- Issue 1: Test issue
- Issue 2: Another test issue
"""
    save_result = agent.execute_tool(
        "save_critique_report",
        {
            "report_content": test_report,
            "doc_title": "Test Document",
            "severity_summary": {
                "critical": 1,
                "high": 2,
                "medium": 3,
                "low": 4
            }
        }
    )
    save_data = json.loads(save_result)
    if save_data['status'] == 'success':
        print(f"   ✅ Report saved to: {save_data['filename']}")
    else:
        print(f"   ❌ Failed to save report")

    # Test complete_critique
    print("\n3️⃣  Testing complete_critique tool:")
    complete_result = agent.execute_tool(
        "complete_critique",
        {
            "success": True,
            "summary": "Test critique completed successfully"
        }
    )
    complete_data = json.loads(complete_result)
    print(f"   ✅ Status: {complete_data['status']}")


def main():
    """Run all examples"""
    print("\n" + "🤖 PRD CRITIQUE AGENT - USAGE EXAMPLES ".center(60, "="))

    examples = [
        ("Basic Critique", example_basic_critique),
        ("Batch Critique", example_batch_critique),
        ("Custom Framework", example_custom_framework),
        ("Monitoring", example_monitoring_agent),
        ("Error Handling", example_error_handling),
        ("Tool Testing", example_tool_testing),
    ]

    print("\nAvailable examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")

    print("\n" + "=" * 60)

    # For demo, run the tool testing example
    print("\n Running Example 6: Tool Testing (safe to run)\n")
    example_tool_testing()

    print("\n" + "=" * 60)
    print("\n💡 To run other examples:")
    print("   1. Set ANTHROPIC_API_KEY environment variable")
    print("   2. Update document IDs in the example functions")
    print("   3. Call the specific example function")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()

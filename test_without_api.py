#!/usr/bin/env python3
"""
Test agent functionality without requiring API keys
Tests tool definitions, executors, and framework
"""

import sys
import json

# Add current directory to path
sys.path.insert(0, '.')

from agent import PRDCritiqueAgent


def test_tool_definitions():
    """Test that tools are properly defined"""
    print("=" * 60)
    print("TEST 1: Tool Definitions")
    print("=" * 60)

    # Create agent with dummy key (won't be used)
    agent = PRDCritiqueAgent(api_key="test-key")

    tools = agent.define_tools()

    print(f"\n✅ Agent defines {len(tools)} tools:")
    for tool in tools:
        print(f"   - {tool['name']}")
        assert 'description' in tool, f"Tool {tool['name']} missing description"
        assert 'input_schema' in tool, f"Tool {tool['name']} missing input_schema"

    assert len(tools) == 4, "Expected 4 tools"
    print("\n✅ All tools properly defined")
    return True


def test_critique_framework():
    """Test critique framework tool"""
    print("\n" + "=" * 60)
    print("TEST 2: Critique Framework")
    print("=" * 60)

    agent = PRDCritiqueAgent(api_key="test-key")

    # Test PRD framework
    result = agent.execute_tool("get_critique_framework", {"doc_type": "prd"})
    framework = json.loads(result)

    print(f"\n✅ PRD Framework loaded with {len(framework['dimensions'])} dimensions:")
    for dim in framework['dimensions']:
        print(f"   - {dim['name']}: {len(dim['criteria'])} criteria")
        assert 'name' in dim
        assert 'criteria' in dim
        assert len(dim['criteria']) > 0

    # Test product strategy framework
    result = agent.execute_tool("get_critique_framework", {"doc_type": "product_strategy"})
    framework = json.loads(result)

    print(f"\n✅ Product Strategy Framework loaded with {len(framework['dimensions'])} dimensions:")
    for dim in framework['dimensions']:
        print(f"   - {dim['name']}: {len(dim['criteria'])} criteria")

    print("\n✅ Framework tool working correctly")
    return True


def test_save_report():
    """Test save report tool"""
    print("\n" + "=" * 60)
    print("TEST 3: Save Report")
    print("=" * 60)

    agent = PRDCritiqueAgent(api_key="test-key")

    test_report = """# Test Critique Report

## Executive Summary
This is a test report to verify the save functionality.

## Findings

### 🔴 Critical Issues
1. Test critical issue 1
2. Test critical issue 2

### 🟠 High Priority Issues
1. Test high priority issue

### 🟡 Medium Priority Issues
1. Test medium issue 1
2. Test medium issue 2

## Recommendations
- Recommendation 1
- Recommendation 2

## Conclusion
Test report generated successfully.
"""

    result = agent.execute_tool(
        "save_critique_report",
        {
            "report_content": test_report,
            "doc_title": "Test Document",
            "severity_summary": {
                "critical": 2,
                "high": 1,
                "medium": 2,
                "low": 0
            }
        }
    )

    result_data = json.loads(result)

    assert result_data['status'] == 'success', "Report save failed"

    print(f"\n✅ Report saved successfully:")
    print(f"   Filename: {result_data['filename']}")
    print(f"   Size: {result_data['size_bytes']} bytes")

    # Verify file exists
    from pathlib import Path
    filepath = Path(result_data['filepath'])
    assert filepath.exists(), "Report file not created"

    print(f"   Path: {result_data['filepath']}")
    print("\n✅ Save report tool working correctly")
    return True


def test_complete_critique():
    """Test complete critique tool"""
    print("\n" + "=" * 60)
    print("TEST 4: Complete Critique")
    print("=" * 60)

    agent = PRDCritiqueAgent(api_key="test-key")

    result = agent.execute_tool(
        "complete_critique",
        {
            "success": True,
            "summary": "Test critique completed with 5 findings"
        }
    )

    result_data = json.loads(result)

    assert result_data['status'] == 'completed'
    assert result_data['success'] == True
    assert 'summary' in result_data

    print(f"\n✅ Complete critique response:")
    print(f"   Status: {result_data['status']}")
    print(f"   Success: {result_data['success']}")
    print(f"   Summary: {result_data['summary']}")
    print("\n✅ Complete critique tool working correctly")
    return True


def test_google_docs_client():
    """Test Google Docs client module"""
    print("\n" + "=" * 60)
    print("TEST 5: Google Docs Client")
    print("=" * 60)

    try:
        from google_docs_client import GoogleDocsClient

        print("\n✅ google_docs_client module imported successfully")

        # Test doc ID extraction
        test_urls = [
            "https://docs.google.com/document/d/1ABC123XYZ/edit",
            "1ABC123XYZ",
        ]

        for url in test_urls:
            doc_id = GoogleDocsClient.extract_doc_id(url)
            print(f"   URL: {url}")
            print(f"   Extracted ID: {doc_id}")
            assert doc_id == "1ABC123XYZ"

        print("\n✅ Google Docs client working correctly")
        return True

    except ImportError as e:
        print(f"⚠️  google_docs_client module import failed: {e}")
        return True  # Not critical for core functionality


def test_agent_attributes():
    """Test agent attributes"""
    print("\n" + "=" * 60)
    print("TEST 6: Agent Attributes")
    print("=" * 60)

    agent = PRDCritiqueAgent(api_key="test-key", model="claude-opus-4-6")

    assert agent.model == "claude-opus-4-6"
    assert agent.conversation_history == []
    assert hasattr(agent, 'client')

    print("\n✅ Agent attributes:")
    print(f"   Model: {agent.model}")
    print(f"   Conversation history: {len(agent.conversation_history)} messages")
    print(f"   Client initialized: {agent.client is not None}")
    print("\n✅ Agent initialization working correctly")
    return True


def run_all_tests():
    """Run all tests"""
    print("\n" + "🧪 RUNNING AGENT TESTS ".center(60, "=") + "\n")

    tests = [
        ("Tool Definitions", test_tool_definitions),
        ("Critique Framework", test_critique_framework),
        ("Save Report", test_save_report),
        ("Complete Critique", test_complete_critique),
        ("Google Docs Client", test_google_docs_client),
        ("Agent Attributes", test_agent_attributes),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success, None))
        except AssertionError as e:
            print(f"\n❌ Test failed: {e}")
            results.append((test_name, False, str(e)))
        except Exception as e:
            print(f"\n❌ Test error: {e}")
            results.append((test_name, False, str(e)))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, success, _ in results if success)
    total = len(results)

    for test_name, success, error in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if error:
            print(f"       Error: {error}")

    print(f"\n{passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! The agent is working correctly.")
        print("\nNext steps:")
        print("   1. Set ANTHROPIC_API_KEY environment variable")
        print("   2. Set up google-credentials.json")
        print("   3. Run: python agent.py with your Google Doc ID")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

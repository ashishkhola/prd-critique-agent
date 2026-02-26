#!/usr/bin/env python3
"""
Autonomous PRD Critique Agent

This agent runs autonomously to:
1. Fetch PRD documents from Google Docs
2. Analyze and critique the document
3. Generate a comprehensive report
"""

import anthropic
import json
from typing import Any, Dict, List, Optional
from datetime import datetime


class PRDCritiqueAgent:
    """Autonomous agent for critiquing product strategy and PRD documents"""

    def __init__(self, api_key: str = None, model: str = "claude-opus-4-6"):
        import os

        # Support Stripe's internal proxy
        base_url = os.environ.get('ANTHROPIC_BASE_URL')
        auth_token = os.environ.get('ANTHROPIC_AUTH_TOKEN')

        if base_url and auth_token:
            # Use Stripe's internal setup
            self.client = anthropic.Anthropic(
                base_url=base_url,
                api_key=auth_token
            )
            # Use Claude Opus 4.6 (latest and most capable)
            self.model = "claude-opus-4-6"
        else:
            # Use standard Anthropic API
            if not api_key:
                raise ValueError("API key required when not using Stripe's internal proxy")
            self.client = anthropic.Anthropic(api_key=api_key)
            self.model = model

        self.conversation_history = []

    def define_tools(self) -> List[Dict[str, Any]]:
        """Define custom tools for the agent"""
        return [
            {
                "name": "read_google_doc",
                "description": "Reads content from a Google Doc given its document ID or URL. Extracts the full text content including headings, paragraphs, and structure.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "doc_id": {
                            "type": "string",
                            "description": "The Google Doc ID (from the URL: docs.google.com/document/d/{DOC_ID}/)"
                        }
                    },
                    "required": ["doc_id"]
                }
            },
            {
                "name": "get_critique_framework",
                "description": "Returns a comprehensive framework for critiquing PRD documents, including key dimensions to evaluate.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "doc_type": {
                            "type": "string",
                            "enum": ["prd", "product_strategy", "both"],
                            "description": "The type of document being critiqued"
                        }
                    },
                    "required": ["doc_type"]
                }
            },
            {
                "name": "save_critique_report",
                "description": "Saves the critique report to a file in markdown format",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "report_content": {
                            "type": "string",
                            "description": "The full critique report content in markdown format"
                        },
                        "doc_title": {
                            "type": "string",
                            "description": "The title of the document being critiqued (used for filename)"
                        },
                        "severity_summary": {
                            "type": "object",
                            "description": "Summary of issues by severity level",
                            "properties": {
                                "critical": {"type": "integer"},
                                "high": {"type": "integer"},
                                "medium": {"type": "integer"},
                                "low": {"type": "integer"}
                            }
                        }
                    },
                    "required": ["report_content", "doc_title"]
                }
            },
            {
                "name": "complete_critique",
                "description": "Call this when the critique is complete and the report has been saved. This signals the agent to finish.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "success": {
                            "type": "boolean",
                            "description": "Whether the critique was completed successfully"
                        },
                        "summary": {
                            "type": "string",
                            "description": "Brief summary of the critique outcome"
                        }
                    },
                    "required": ["success", "summary"]
                }
            }
        ]

    def execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """Execute a tool and return the result"""

        if tool_name == "read_google_doc":
            return self._read_google_doc(tool_input["doc_id"])

        elif tool_name == "get_critique_framework":
            return self._get_critique_framework(tool_input["doc_type"])

        elif tool_name == "save_critique_report":
            return self._save_critique_report(
                tool_input["report_content"],
                tool_input["doc_title"],
                tool_input.get("severity_summary")
            )

        elif tool_name == "complete_critique":
            return json.dumps({
                "status": "completed",
                "success": tool_input["success"],
                "summary": tool_input["summary"]
            })

        else:
            return json.dumps({"error": f"Unknown tool: {tool_name}"})

    def _read_google_doc(self, doc_id: str) -> str:
        """Read Google Doc using the google_docs_client module"""
        try:
            from google_docs_client import read_google_doc

            # You can specify credentials path here or set in environment
            credentials_path = "./google-credentials.json"

            # Try to use credentials if file exists
            import os
            if not os.path.exists(credentials_path):
                credentials_path = None  # Will try to use default credentials

            return read_google_doc(doc_id, credentials_path)

        except ImportError:
            return json.dumps({
                "success": False,
                "error": "google_docs_client module not found. Install dependencies: pip install -r requirements.txt"
            })
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": f"Failed to read Google Doc: {str(e)}"
            })

    def _get_critique_framework(self, doc_type: str) -> str:
        """Return comprehensive critique framework"""
        frameworks = {
            "prd": {
                "dimensions": [
                    {
                        "name": "Problem Definition",
                        "criteria": [
                            "Is the problem clearly stated and quantified?",
                            "Is the target user/customer well-defined?",
                            "Are pain points backed by data or research?",
                            "Is the problem worth solving (impact vs effort)?"
                        ]
                    },
                    {
                        "name": "Solution Clarity",
                        "criteria": [
                            "Is the proposed solution clearly described?",
                            "Are user stories or use cases well-defined?",
                            "Is the scope appropriate (not too broad/narrow)?",
                            "Are edge cases considered?"
                        ]
                    },
                    {
                        "name": "Requirements Quality",
                        "criteria": [
                            "Are requirements specific and measurable?",
                            "Is there a clear distinction between must-haves and nice-to-haves?",
                            "Are requirements testable?",
                            "Are dependencies clearly identified?"
                        ]
                    },
                    {
                        "name": "Success Metrics",
                        "criteria": [
                            "Are success metrics clearly defined?",
                            "Are metrics measurable and achievable?",
                            "Is there a baseline for comparison?",
                            "Are leading and lagging indicators identified?"
                        ]
                    },
                    {
                        "name": "Technical Feasibility",
                        "criteria": [
                            "Are technical constraints identified?",
                            "Is the implementation approach outlined?",
                            "Are integration points documented?",
                            "Are performance/scale considerations addressed?"
                        ]
                    },
                    {
                        "name": "Risks & Mitigation",
                        "criteria": [
                            "Are key risks identified?",
                            "Are mitigation strategies defined?",
                            "Are dependencies on other teams/systems noted?",
                            "Is there a rollback plan?"
                        ]
                    },
                    {
                        "name": "Timeline & Resources",
                        "criteria": [
                            "Is there a realistic timeline?",
                            "Are resource requirements identified?",
                            "Are milestones clearly defined?",
                            "Is there a phased rollout plan?"
                        ]
                    }
                ]
            },
            "product_strategy": {
                "dimensions": [
                    {
                        "name": "Vision & Goals",
                        "criteria": [
                            "Is there a clear product vision?",
                            "Are strategic goals well-defined and measurable?",
                            "Does the strategy align with company objectives?",
                            "Is the time horizon appropriate?"
                        ]
                    },
                    {
                        "name": "Market Analysis",
                        "criteria": [
                            "Is the market opportunity sized?",
                            "Are competitors analyzed?",
                            "Are market trends considered?",
                            "Is positioning clearly defined?"
                        ]
                    },
                    {
                        "name": "Target Customer",
                        "criteria": [
                            "Are target segments clearly identified?",
                            "Are personas well-developed?",
                            "Is the value proposition clear?",
                            "Is there evidence of customer need?"
                        ]
                    },
                    {
                        "name": "Differentiation",
                        "criteria": [
                            "What makes this product unique?",
                            "Is the competitive advantage sustainable?",
                            "Are key features/capabilities prioritized?",
                            "Is there a clear moat?"
                        ]
                    },
                    {
                        "name": "Roadmap Alignment",
                        "criteria": [
                            "Does the roadmap support the strategy?",
                            "Are priorities clear?",
                            "Is there a theme or narrative?",
                            "Are dependencies managed?"
                        ]
                    }
                ]
            }
        }

        if doc_type == "both":
            return json.dumps({
                "frameworks": {
                    "prd": frameworks["prd"],
                    "product_strategy": frameworks["product_strategy"]
                }
            }, indent=2)

        return json.dumps(frameworks.get(doc_type, frameworks["prd"]), indent=2)

    def _save_critique_report(
        self,
        report_content: str,
        doc_title: str,
        severity_summary: Optional[Dict[str, int]] = None
    ) -> str:
        """Save critique report to file"""
        import os
        from pathlib import Path

        # Create reports directory
        reports_dir = Path("/Users/ashishkhola/prd_critique_agent/reports")
        reports_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in doc_title)
        safe_title = safe_title.replace(' ', '_')[:50]
        filename = f"{safe_title}_{timestamp}.md"
        filepath = reports_dir / filename

        # Add header with metadata
        full_report = f"""# PRD Critique Report
**Document:** {doc_title}
**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Agent:** PRD Critique Agent v1.0

"""

        if severity_summary:
            full_report += f"""## Issue Summary
- 🔴 Critical: {severity_summary.get('critical', 0)}
- 🟠 High: {severity_summary.get('high', 0)}
- 🟡 Medium: {severity_summary.get('medium', 0)}
- 🟢 Low: {severity_summary.get('low', 0)}

---

"""

        full_report += report_content

        # Save to file
        with open(filepath, 'w') as f:
            f.write(full_report)

        return json.dumps({
            "status": "success",
            "filepath": str(filepath),
            "filename": filename,
            "size_bytes": len(full_report)
        })

    def run_autonomous(self, doc_id: str, max_iterations: int = 15) -> Dict[str, Any]:
        """
        Run the agent autonomously to critique a PRD document

        Args:
            doc_id: Google Doc ID to critique
            max_iterations: Maximum number of agent iterations

        Returns:
            Dictionary with critique results
        """

        # Initial system prompt
        system_prompt = """You are an autonomous agent that critiques product strategy and PRD documents.

Your task is to:
1. Read the Google Doc containing the PRD
2. Get the critique framework appropriate for the document type
3. Analyze the document comprehensively across all dimensions
4. Generate a detailed critique report in markdown format
5. Save the report to a file
6. Call complete_critique when done

Be thorough and specific in your critique. For each issue:
- Identify the specific section/area
- Explain what's wrong or missing
- Rate severity (critical/high/medium/low)
- Suggest concrete improvements

Work autonomously - do not ask for user input. Complete the entire critique flow."""

        # Initial user message
        user_message = f"""Please critique the PRD document with ID: {doc_id}

Run the complete critique flow autonomously and save the report."""

        self.conversation_history = [{"role": "user", "content": user_message}]

        tools = self.define_tools()
        iteration = 0

        print(f"\n🤖 Starting autonomous PRD critique for document: {doc_id}")
        print(f"{'='*60}\n")

        while iteration < max_iterations:
            iteration += 1
            print(f"Iteration {iteration}/{max_iterations}")

            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system_prompt,
                tools=tools,
                messages=self.conversation_history
            )

            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response.content
            })

            # Check if we're done (no tool use)
            if response.stop_reason == "end_turn":
                print("\n✅ Agent completed without tool use")
                break

            # Process tool calls
            if response.stop_reason == "tool_use":
                tool_results = []

                for block in response.content:
                    if block.type == "tool_use":
                        tool_name = block.name
                        tool_input = block.input

                        print(f"  🔧 Using tool: {tool_name}")

                        # Execute tool
                        result = self.execute_tool(tool_name, tool_input)

                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result
                        })

                        # Check if critique is complete
                        if tool_name == "complete_critique":
                            result_data = json.loads(result)
                            print(f"\n✅ Critique complete: {result_data['summary']}")
                            return {
                                "success": result_data["success"],
                                "summary": result_data["summary"],
                                "iterations": iteration
                            }

                # Add tool results to history
                self.conversation_history.append({
                    "role": "user",
                    "content": tool_results
                })

            print()

        print(f"\n⚠️  Max iterations ({max_iterations}) reached")
        return {
            "success": False,
            "summary": "Agent did not complete within max iterations",
            "iterations": iteration
        }


def main():
    """Example usage"""
    import os

    # Get API key from environment
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        return

    # Create agent
    agent = PRDCritiqueAgent(api_key=api_key)

    # Example: Critique a document
    doc_id = "YOUR_GOOGLE_DOC_ID_HERE"
    result = agent.run_autonomous(doc_id)

    print(f"\n{'='*60}")
    print(f"Final Result: {result}")


if __name__ == "__main__":
    main()

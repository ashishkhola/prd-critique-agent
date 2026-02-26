# PRD Critique Agent

An autonomous AI agent that critiques Product Requirements Documents (PRDs) and product strategy documents using Claude API with custom tool use.

## Features

- **Autonomous Operation**: Runs end-to-end without human intervention
- **Google Docs Integration**: Reads PRDs directly from Google Docs
- **Comprehensive Critique Framework**: Evaluates PRDs across 7 key dimensions:
  - Problem Definition
  - Solution Clarity
  - Requirements Quality
  - Success Metrics
  - Technical Feasibility
  - Risks & Mitigation
  - Timeline & Resources
- **Structured Reports**: Generates markdown reports with severity ratings
- **Custom Tool System**: Extensible architecture for adding new capabilities

## Architecture

```
PRDCritiqueAgent
├── Agent Core (agent.py)
│   ├── Conversation management
│   ├── Tool orchestration
│   └── Autonomous execution loop
├── Google Docs Client (google_docs_client.py)
│   ├── Document fetching
│   └── Content parsing
└── Custom Tools
    ├── read_google_doc
    ├── get_critique_framework
    ├── save_critique_report
    └── complete_critique
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Anthropic API

Get your API key from https://console.anthropic.com/

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

### 3. Set Up Google Cloud Credentials

#### Option A: Service Account (Recommended for automation)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google Docs API
4. Create a service account:
   - Go to IAM & Admin > Service Accounts
   - Click "Create Service Account"
   - Grant "Viewer" role
   - Create and download JSON key
5. Share your Google Docs with the service account email

Save credentials as `google-credentials.json`:

```bash
cp /path/to/downloaded-key.json google-credentials.json
```

#### Option B: OAuth2 (For personal use)

Follow [Google's OAuth2 setup guide](https://developers.google.com/docs/api/quickstart/python)

### 4. Update Agent Configuration

Edit `agent.py` to use your credentials:

```python
# In _read_google_doc method, update path:
from google_docs_client import read_google_doc

def _read_google_doc(self, doc_id: str) -> str:
    return read_google_doc(doc_id, credentials_path="./google-credentials.json")
```

## Usage

### Basic Usage

```python
from agent import PRDCritiqueAgent

# Initialize agent
agent = PRDCritiqueAgent(api_key="your-anthropic-api-key")

# Run autonomous critique
doc_id = "1ABC...XYZ"  # Your Google Doc ID
result = agent.run_autonomous(doc_id)

print(result)
# Output: {
#   "success": True,
#   "summary": "Critique completed with 12 findings",
#   "iterations": 5
# }
```

### From Command Line

```bash
python agent.py
```

Then edit the `main()` function with your document ID.

### Get Document ID from URL

Given URL: `https://docs.google.com/document/d/1ABC123XYZ/edit`

Document ID is: `1ABC123XYZ`

## Output

Reports are saved to `./reports/` directory:

```
reports/
└── My_PRD_Document_20260226_143022.md
```

Example report structure:

```markdown
# PRD Critique Report
**Document:** My Product Feature PRD
**Date:** 2026-02-26 14:30:22
**Agent:** PRD Critique Agent v1.0

## Issue Summary
- 🔴 Critical: 2
- 🟠 High: 5
- 🟡 Medium: 8
- 🟢 Low: 3

## 1. Problem Definition

### 🔴 Critical: Problem not quantified
**Location:** Executive Summary, paragraph 2
...
```

## Customization

### Adding New Tools

Add tools to `define_tools()` method:

```python
def define_tools(self) -> List[Dict[str, Any]]:
    return [
        # ... existing tools ...
        {
            "name": "check_technical_feasibility",
            "description": "Analyzes technical feasibility of proposed solution",
            "input_schema": {
                "type": "object",
                "properties": {
                    "requirements": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                }
            }
        }
    ]
```

Then implement in `execute_tool()`:

```python
def execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
    if tool_name == "check_technical_feasibility":
        return self._check_feasibility(tool_input["requirements"])
```

### Customizing Critique Framework

Edit the `_get_critique_framework()` method to add/modify evaluation dimensions:

```python
{
    "name": "Your New Dimension",
    "criteria": [
        "Question 1?",
        "Question 2?",
        "Question 3?"
    ]
}
```

### Changing Output Format

Modify `_save_critique_report()` to change format (PDF, HTML, etc.):

```python
def _save_critique_report(self, report_content: str, doc_title: str, ...):
    # Convert to PDF
    import markdown2
    from weasyprint import HTML

    html_content = markdown2.markdown(report_content)
    HTML(string=html_content).write_pdf(filepath)
```

## Advanced Usage

### Batch Processing

```python
agent = PRDCritiqueAgent(api_key=api_key)

doc_ids = ["doc1_id", "doc2_id", "doc3_id"]

for doc_id in doc_ids:
    print(f"Processing {doc_id}...")
    result = agent.run_autonomous(doc_id)
    print(f"Result: {result}\n")
```

### Custom System Prompts

```python
agent = PRDCritiqueAgent(api_key=api_key)

# Modify system prompt for specific focus
custom_system = """You are a PRD critique agent focused on technical feasibility.

Pay special attention to:
- Architecture decisions
- Scalability concerns
- Security implications
- Performance requirements

..."""

# Update in run_autonomous() method
```

### Integrating with CI/CD

```yaml
# .github/workflows/prd-critique.yml
name: PRD Critique

on:
  pull_request:
    paths:
      - 'docs/prds/**'

jobs:
  critique:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run PRD Critique
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GOOGLE_CREDENTIALS: ${{ secrets.GOOGLE_CREDENTIALS }}
        run: |
          python agent.py ${{ github.event.pull_request.body }}
```

## Troubleshooting

### Google Docs Permission Denied

**Error**: `HttpError 403: The caller does not have permission`

**Solution**: Share the Google Doc with your service account email address

### API Rate Limits

**Error**: `anthropic.RateLimitError`

**Solution**: Add retry logic with exponential backoff:

```python
import time
from anthropic import RateLimitError

max_retries = 3
for attempt in range(max_retries):
    try:
        response = self.client.messages.create(...)
        break
    except RateLimitError:
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)
        else:
            raise
```

### Agent Not Completing

**Error**: `Max iterations reached`

**Solution**: Increase `max_iterations` or simplify the critique scope

```python
result = agent.run_autonomous(doc_id, max_iterations=25)
```

## Best Practices

1. **Start Small**: Test with a simple PRD before scaling to complex documents
2. **Monitor Iterations**: If agent consistently hits max iterations, review the system prompt
3. **Version Control Reports**: Commit generated reports to track improvements over time
4. **Customize for Your Org**: Adapt the critique framework to match your company's standards
5. **Use Structured Documents**: Well-formatted PRDs with clear headings get better critiques

## Cost Estimation

Based on Claude Opus 4.6 pricing:
- Input: $15 per million tokens
- Output: $75 per million tokens

Typical PRD critique:
- Input: ~20K tokens (PRD + framework + iterations)
- Output: ~5K tokens (critique report)
- Cost per critique: ~$0.60 - $1.00

## Roadmap

- [ ] Support for other document sources (Confluence, Notion, local files)
- [ ] Integration with Jira/Linear for tracking action items
- [ ] Comparative analysis across multiple PRDs
- [ ] LLM-as-judge for critique quality scoring
- [ ] Web UI for interactive critiques
- [ ] Slack/Email notifications
- [ ] Multi-language support

## Contributing

This is a template for building autonomous agents. Customize it for your needs!

Key extension points:
- Add tools in `define_tools()`
- Implement tool logic in `execute_tool()`
- Customize critique framework in `_get_critique_framework()`
- Modify report format in `_save_critique_report()`

## License

MIT License - feel free to modify and use for your projects

## Support

For issues or questions:
- Create an issue in your repository
- Review Claude API documentation: https://docs.anthropic.com/
- Check Google Docs API docs: https://developers.google.com/docs/api

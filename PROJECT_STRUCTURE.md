# PRD Critique Agent - Project Structure

## Overview

An autonomous AI agent that critiques Product Requirements Documents using Claude API with custom tool use.

## Directory Structure

```
prd_critique_agent/
├── agent.py                    # Main agent implementation
├── google_docs_client.py       # Google Docs integration
├── example_usage.py            # Usage examples and demos
├── setup.py                    # Interactive setup wizard
├── requirements.txt            # Python dependencies
├── config.example.json         # Configuration template
├── README.md                   # Comprehensive documentation
├── QUICKSTART.md              # Quick start guide
├── PROJECT_STRUCTURE.md        # This file
├── .gitignore                 # Git ignore rules
├── google-credentials.json    # Google service account (not in git)
├── config.json                # Your config (not in git)
├── .env                       # Environment variables (not in git)
└── reports/                   # Generated critique reports
    └── *.md                   # Individual reports
```

## Core Components

### 1. Agent Core (`agent.py`)

**Class**: `PRDCritiqueAgent`

**Key Methods**:
- `__init__(api_key, model)` - Initialize agent with API credentials
- `define_tools()` - Define custom tools for the agent
- `execute_tool(name, input)` - Execute tool and return result
- `run_autonomous(doc_id, max_iterations)` - Main autonomous execution loop

**Tools Implemented**:
- `read_google_doc` - Fetch document from Google Docs
- `get_critique_framework` - Load evaluation criteria
- `save_critique_report` - Save critique to markdown file
- `complete_critique` - Signal completion

**Flow**:
```
1. Initialize with API key
2. Load tools and system prompt
3. Start conversation with user message
4. Loop:
   a. Call Claude API with tools
   b. If tool_use: execute tool, add result to conversation
   c. If end_turn: complete
   d. Continue until complete_critique called or max iterations
5. Return result
```

### 2. Google Docs Integration (`google_docs_client.py`)

**Class**: `GoogleDocsClient`

**Key Methods**:
- `__init__(credentials_path)` - Setup Google API client
- `read_document(doc_id)` - Fetch and parse document
- `_parse_structural_elements(elements)` - Convert to markdown
- `extract_doc_id(url)` - Extract ID from URL

**Standalone Function**:
- `read_google_doc(doc_id, credentials_path)` - Used by agent

**Supported Elements**:
- Paragraphs with styling (bold, italic)
- Headings (H1-H6)
- Tables (converted to markdown tables)
- Section breaks

### 3. Examples & Testing (`example_usage.py`)

**Examples Included**:
1. `example_basic_critique()` - Single document critique
2. `example_batch_critique()` - Multiple documents
3. `example_custom_framework()` - Custom evaluation dimensions
4. `example_monitoring_agent()` - Detailed execution monitoring
5. `example_error_handling()` - Error scenarios
6. `example_tool_testing()` - Individual tool testing

### 4. Setup Wizard (`setup.py`)

**Steps**:
1. Check dependencies
2. Configure Anthropic API key
3. Setup Google credentials
4. Create directories
5. Generate config file
6. Run test

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                        User Request                         │
│              "Critique document {doc_id}"                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       v
┌─────────────────────────────────────────────────────────────┐
│                   PRDCritiqueAgent                          │
│  ┌────────────────────────────────────────────────────┐    │
│  │ 1. Initialize conversation                         │    │
│  │ 2. Send to Claude API with tools                   │    │
│  └────────────────────────────────────────────────────┘    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       v
┌─────────────────────────────────────────────────────────────┐
│                   Claude API (Opus 4.6)                     │
│  Decides which tools to call based on task                  │
└───┬─────────────────┬──────────────────┬────────────────────┘
    │                 │                  │
    v                 v                  v
┌───────┐    ┌─────────────┐    ┌───────────────┐
│ Read  │    │ Framework   │    │ Save Report   │
│ Doc   │    │ Loader      │    │               │
└───┬───┘    └─────────────┘    └───────┬───────┘
    │                                    │
    v                                    v
┌───────────────┐              ┌─────────────────┐
│ Google Docs   │              │ ./reports/      │
│ API           │              │ {name}_{ts}.md  │
└───────────────┘              └─────────────────┘
```

## Tool Execution Flow

```
Agent receives tool_use from Claude
         │
         v
    execute_tool(name, input)
         │
         ├─> read_google_doc(doc_id)
         │        │
         │        └─> GoogleDocsClient.read_document()
         │                 │
         │                 └─> Returns {title, content, ...}
         │
         ├─> get_critique_framework(doc_type)
         │        │
         │        └─> Returns JSON with evaluation dimensions
         │
         ├─> save_critique_report(content, title, severity)
         │        │
         │        └─> Writes to ./reports/{title}_{timestamp}.md
         │
         └─> complete_critique(success, summary)
                  │
                  └─> Returns completion status
```

## Critique Framework

### PRD Dimensions (7)

1. **Problem Definition**
   - Problem clarity and quantification
   - Target user definition
   - Pain points backed by data
   - Impact vs effort assessment

2. **Solution Clarity**
   - Solution description
   - User stories and use cases
   - Scope appropriateness
   - Edge case consideration

3. **Requirements Quality**
   - Specificity and measurability
   - Must-haves vs nice-to-haves
   - Testability
   - Dependency identification

4. **Success Metrics**
   - Clear definition
   - Measurability and achievability
   - Baseline for comparison
   - Leading and lagging indicators

5. **Technical Feasibility**
   - Constraint identification
   - Implementation approach
   - Integration points
   - Performance and scale

6. **Risks & Mitigation**
   - Risk identification
   - Mitigation strategies
   - Dependencies
   - Rollback plan

7. **Timeline & Resources**
   - Realistic timeline
   - Resource requirements
   - Milestone definition
   - Phased rollout plan

### Product Strategy Dimensions (5)

1. Vision & Goals
2. Market Analysis
3. Target Customer
4. Differentiation
5. Roadmap Alignment

## Configuration

### Environment Variables

```bash
ANTHROPIC_API_KEY=sk-ant-...    # Required
GOOGLE_APPLICATION_CREDENTIALS=/path/to/creds.json  # Optional
```

### Config File (`config.json`)

```json
{
  "api": {
    "anthropic_api_key": "...",
    "model": "claude-opus-4-6",
    "max_tokens": 4096
  },
  "google": {
    "credentials_path": "./google-credentials.json"
  },
  "agent": {
    "max_iterations": 15
  },
  "critique": {
    "document_types": ["prd", "product_strategy"],
    "severity_levels": ["critical", "high", "medium", "low"]
  }
}
```

## Extension Points

### 1. Add New Tools

```python
def define_tools(self):
    return [
        # ... existing tools ...
        {
            "name": "your_custom_tool",
            "description": "...",
            "input_schema": {...}
        }
    ]

def execute_tool(self, tool_name, tool_input):
    if tool_name == "your_custom_tool":
        return self._your_custom_logic(tool_input)
```

### 2. Customize Critique Framework

Edit `_get_critique_framework()` to add/modify dimensions:

```python
{
    "name": "Your Custom Dimension",
    "criteria": [
        "Criterion 1?",
        "Criterion 2?"
    ]
}
```

### 3. Add Document Sources

Create new client modules:
- `confluence_client.py`
- `notion_client.py`
- `local_file_client.py`

Add corresponding tool and executor.

### 4. Modify Output Format

Edit `_save_critique_report()`:
- Change to PDF: Use `markdown2` + `weasyprint`
- Change to HTML: Use `markdown2`
- Add to database: Use `sqlite3` or PostgreSQL client

## Dependencies

### Core
- `anthropic>=0.39.0` - Claude API client
- `google-auth>=2.27.0` - Google authentication
- `google-api-python-client>=2.115.0` - Google APIs

### Development
- Standard library only for core functionality
- Optional: `pytest` for testing
- Optional: `black` for code formatting

## Performance

### Typical Metrics
- **Execution Time**: 30-90 seconds per PRD
- **API Calls**: 5-10 iterations average
- **Token Usage**: ~25K total tokens per PRD
- **Cost**: $0.60-$1.00 per critique

### Optimization Tips
1. Use Sonnet for simple PRDs (cheaper)
2. Reduce max_tokens for shorter reports
3. Cache framework in memory for batch processing
4. Implement parallel processing for multiple docs

## Security

### Best Practices
1. **Never commit credentials**:
   - `google-credentials.json`
   - `.env` files
   - API keys

2. **Use service accounts** for Google Docs (not OAuth for automation)

3. **Limit permissions**:
   - Google: Read-only access
   - Share docs explicitly with service account

4. **Rotate keys regularly**:
   - Anthropic API keys
   - Google service account keys

## Troubleshooting

### Common Issues

1. **Import Error**: Install requirements
   ```bash
   pip install -r requirements.txt
   ```

2. **Google Auth Error**: Check credentials path and permissions

3. **Agent Not Completing**: Increase max_iterations

4. **Rate Limits**: Add exponential backoff retry logic

## Testing

### Unit Tests (to implement)
```bash
pytest tests/test_agent.py
pytest tests/test_google_client.py
```

### Integration Tests
```bash
python example_usage.py
```

### Manual Testing
1. Use example document
2. Check report quality
3. Verify all dimensions covered

## Future Enhancements

- [ ] Web UI for interactive use
- [ ] Slack/email notifications
- [ ] Support for other doc sources
- [ ] Comparative analysis across PRDs
- [ ] Integration with Jira/Linear
- [ ] Multi-language support
- [ ] Real-time streaming output
- [ ] Critique quality scoring
- [ ] Historical trend analysis

## License

MIT License - See LICENSE file

## Support

- Documentation: README.md, QUICKSTART.md
- Examples: example_usage.py
- Issues: Create GitHub issue in your repo

# Quick Start Guide

Get your PRD Critique Agent running in 5 minutes!

## Step 1: Install Dependencies (1 min)

```bash
cd prd_critique_agent
pip install -r requirements.txt
```

## Step 2: Set Up API Key (1 min)

Get your Anthropic API key from https://console.anthropic.com/

```bash
export ANTHROPIC_API_KEY='sk-ant-...'
```

Or create a `.env` file:

```bash
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

## Step 3: Google Docs Setup (2 min)

### Quick Option: Use Existing Credentials

If you already have Google Cloud credentials:

```bash
cp /path/to/your/credentials.json google-credentials.json
```

### Complete Option: Create New Service Account

1. Go to https://console.cloud.google.com/
2. Create/select a project
3. Enable **Google Docs API**
4. Create Service Account → Download JSON key
5. Save as `google-credentials.json`
6. Share your Google Docs with the service account email

## Step 4: Test Run (1 min)

```bash
# Test the tools
python example_usage.py
```

You should see:
```
✅ Report saved to: Test_Document_20260226_143022.md
```

## Step 5: Critique Your First PRD

Edit `agent.py` at the bottom:

```python
def main():
    import os

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    agent = PRDCritiqueAgent(api_key=api_key)

    # Replace with your Google Doc ID
    doc_id = "1ABC...XYZ"  # From: docs.google.com/document/d/1ABC...XYZ/
    result = agent.run_autonomous(doc_id)

    print(f"Result: {result}")

if __name__ == "__main__":
    main()
```

Then run:

```bash
python agent.py
```

## What Happens Next?

The agent will:
1. 🔍 Read your Google Doc
2. 📋 Load the PRD critique framework
3. 🤖 Analyze your document autonomously
4. 📝 Generate a comprehensive critique report
5. 💾 Save it to `./reports/` directory

## View Your Report

```bash
ls -la reports/
cat reports/Your_PRD_Title_*.md
```

## Next Steps

- **Customize framework**: Edit `_get_critique_framework()` in `agent.py`
- **Batch processing**: See `example_usage.py` for batch critique
- **Add tools**: Extend `define_tools()` with custom capabilities
- **CI/CD integration**: See README.md for GitHub Actions example

## Troubleshooting

### "Permission denied" on Google Docs

**Fix**: Share the Google Doc with your service account email address

### "Module not found: google"

**Fix**: Run `pip install -r requirements.txt`

### "API key not found"

**Fix**: Set environment variable `export ANTHROPIC_API_KEY='your-key'`

### Agent not completing

**Fix**: Increase max_iterations: `agent.run_autonomous(doc_id, max_iterations=25)`

## Cost Per Critique

Typical cost: **$0.60 - $1.00 per PRD**

Based on:
- Claude Opus 4.6: $15/M input tokens, $75/M output tokens
- Average PRD: ~20K input tokens, ~5K output tokens

## Need Help?

1. Check `README.md` for detailed documentation
2. Review `example_usage.py` for code examples
3. Inspect `google_docs_client.py` for Google integration details

Happy critiquing! 🚀

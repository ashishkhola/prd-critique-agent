# PRD Cop Agent - Deployment Guide

Multiple deployment options to share PRD Cop with your team.

## Option 1: Slack Bot (Recommended for Teams)

Perfect for: Teams using Slack who want instant PRD critiques in chat.

### Setup (5 minutes)

1. **Create Slack App**
   ```bash
   # Go to: https://api.slack.com/apps
   # Click "Create New App" → "From scratch"
   # Name: "PRD Cop"
   # Workspace: Your workspace
   ```

2. **Configure Permissions**
   ```
   OAuth & Permissions → Bot Token Scopes:
   - chat:write
   - commands
   - files:write
   - app_mentions:read
   ```

3. **Enable Socket Mode**
   ```
   Settings → Socket Mode → Enable
   → Generate App-Level Token (connections:write)
   ```

4. **Add Slash Command**
   ```
   Slash Commands → Create New Command
   Command: /prd-cop
   Description: Critique a PRD using PRD Cop framework
   ```

5. **Install & Deploy**
   ```bash
   # Install to workspace
   # Copy Bot Token (xoxb-...) and App Token (xapp-...)

   # Set environment variables
   export SLACK_BOT_TOKEN="xoxb-..."
   export SLACK_APP_TOKEN="xapp-..."
   export ANTHROPIC_API_KEY="sk-ant-..."  # or use Stripe internal

   # Install dependencies
   pip install slack-bolt anthropic

   # Run bot
   python3 slack_bot.py
   ```

6. **Use in Slack**
   ```
   /prd-cop [paste your PRD text]
   /prd-cop https://docs.google.com/document/d/YOUR_DOC_ID
   ```

---

## Option 2: Web Service (REST API)

Perfect for: Integrations, CI/CD, custom UIs.

### Deploy Locally

```bash
# Install dependencies
pip install flask flask-cors anthropic

# Set environment
export ANTHROPIC_API_KEY="sk-ant-..."
export PORT=8080

# Run service
python3 web_service.py
```

### Deploy to Cloud

**Heroku:**
```bash
# Create Procfile
echo "web: python3 web_service.py" > Procfile

# Create requirements.txt
pip freeze > requirements.txt

# Deploy
heroku create your-prd-cop
heroku config:set ANTHROPIC_API_KEY="sk-ant-..."
git push heroku main
```

**Google Cloud Run:**
```bash
# Create Dockerfile
cat > Dockerfile <<'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "web_service.py"]
EOF

# Deploy
gcloud run deploy prd-cop \
  --source . \
  --set-env-vars ANTHROPIC_API_KEY="sk-ant-..." \
  --region us-central1 \
  --allow-unauthenticated
```

**AWS Lambda (Serverless):**
```bash
# Install serverless framework
npm install -g serverless

# Create serverless.yml
cat > serverless.yml <<'EOF'
service: prd-cop-agent

provider:
  name: aws
  runtime: python3.11
  environment:
    ANTHROPIC_API_KEY: ${env:ANTHROPIC_API_KEY}

functions:
  critique:
    handler: lambda_handler.critique
    events:
      - http:
          path: critique
          method: post
          cors: true
EOF

# Deploy
serverless deploy
```

### API Usage Examples

**Critique a PRD:**
```bash
curl -X POST https://your-service.com/critique \
  -H "Content-Type: application/json" \
  -d '{
    "prd_text": "# Background\nWe need to build...",
    "prd_name": "Feature X"
  }'
```

**Response:**
```json
{
  "score": 78,
  "report_text": "## PRD COP FINAL SCORE: 78/100...",
  "report_path": "reports/Feature_X_Critique_20260302_131040.md",
  "token_usage": {
    "input": 3208,
    "output": 1272
  }
}
```

**Generate Improved Version:**
```bash
curl -X POST https://your-service.com/improve \
  -H "Content-Type: application/json" \
  -d '{
    "original_prd": "...",
    "critique_results": {...},
    "prd_name": "Feature X"
  }'
```

**Batch Processing:**
```bash
curl -X POST https://your-service.com/batch \
  -H "Content-Type: application/json" \
  -d '{
    "prds": [
      {"name": "PRD1", "text": "..."},
      {"name": "PRD2", "text": "..."}
    ]
  }'
```

---

## Option 3: GitHub Action (CI/CD Integration)

Perfect for: Automated PRD quality checks on every PR.

### Setup

1. **Create workflow file:**
```yaml
# .github/workflows/prd-cop.yml
name: PRD Quality Check

on:
  pull_request:
    paths:
      - 'docs/prds/**/*.md'

jobs:
  prd-cop:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install anthropic

      - name: Run PRD Cop
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          for prd in docs/prds/*.md; do
            echo "Critiquing $prd..."
            python3 prd_cop_agent.py "$prd"
          done

      - name: Check scores
        run: |
          for report in reports/*_Critique_*.md; do
            score=$(grep "FINAL SCORE" "$report" | grep -oP '\d+(?=/100)')
            echo "Score: $score/100"
            if [ "$score" -lt 70 ]; then
              echo "❌ PRD quality below threshold (70)"
              exit 1
            fi
          done

      - name: Upload reports
        uses: actions/upload-artifact@v3
        with:
          name: prd-cop-reports
          path: reports/
```

2. **Add secret:**
```bash
# GitHub repo → Settings → Secrets → New repository secret
Name: ANTHROPIC_API_KEY
Value: sk-ant-...
```

3. **Usage:**
```bash
# Every PR with PRD changes triggers automatic critique
# PRs fail if score < 70
# Reports uploaded as artifacts
```

---

## Option 4: Command Line (Individual Use)

Perfect for: Personal use, one-off critiques.

### Setup
```bash
git clone https://github.com/ashishkhola/prd-critique-agent.git
cd prd-critique-agent
python3 -m venv venv
source venv/bin/activate
pip install anthropic
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Usage
```bash
# Critique a file
python3 prd_cop_agent.py my_prd.txt

# From stdin
cat my_prd.txt | python3 prd_cop_agent.py

# Interactive
python3 prd_cop_agent.py
# (paste PRD, press Ctrl+D)
```

---

## Option 5: Stripe Internal (go/prd-cop)

Perfect for: Stripe employees with access to internal infrastructure.

### Setup (Already Done!)

```bash
# No setup needed - auto-detects internal proxy
cd prd-critique-agent
source venv/bin/activate

# Run on any PRD
python3 prd_cop_agent.py path/to/prd.txt

# Or from Google Doc
python3 prd_cop_agent.py "https://docs.google.com/document/d/YOUR_DOC_ID"
```

### Share with Team

1. **Create go/link:**
   ```bash
   # Share repo location
   go/prd-cop → https://github.com/ashishkhola/prd-critique-agent
   ```

2. **Add to Workflows:**
   ```bash
   # Add to your team's workflow docs
   # Add to onboarding materials
   # Mention in #eng-prd channel
   ```

3. **Integration Examples:**
   ```python
   # In your team's automation scripts
   from prd_cop_agent import PRDCopAgent

   agent = PRDCopAgent()  # Auto-uses Stripe proxy
   results = agent.critique_prd(prd_text, "MyPRD")

   if results['score'] < 85:
       # Send to author for revision
       send_feedback(results['report_text'])
   else:
       # Route to leadership
       route_to_review(prd_text)
   ```

---

## Cost Estimates

**Per PRD Critique:**
- Input tokens: ~3,000 (average PRD)
- Output tokens: ~1,500 (detailed report)
- Cost: ~$0.10 per critique (Claude Opus 4.6)

**Monthly estimates:**
- 10 PRDs/month: ~$1
- 50 PRDs/month: ~$5
- 100 PRDs/month: ~$10

**With improvements:**
- Critique + Improve: ~$0.20 per PRD
- Critique + Improve + Re-score: ~$0.30 per PRD

---

## Security Considerations

### API Keys
```bash
# Never commit API keys
echo ".env" >> .gitignore
echo "*.key" >> .gitignore

# Use environment variables
export ANTHROPIC_API_KEY="sk-ant-..."

# Or use secrets management
aws secretsmanager get-secret-value --secret-id prd-cop-key
```

### PII in PRDs
```python
# Redact sensitive data before sending
import re

def redact_pii(text):
    # Email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
    # Phone numbers
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
    # SSN
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]', text)
    return text

# Use before critiquing
prd_text = redact_pii(original_prd_text)
```

### Rate Limiting
```python
# Add rate limiting for shared services
from functools import wraps
import time

def rate_limit(max_calls=10, period=60):
    """Limit to max_calls per period seconds"""
    calls = []

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            calls[:] = [c for c in calls if now - c < period]

            if len(calls) >= max_calls:
                sleep_time = period - (now - calls[0])
                time.sleep(sleep_time)

            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Apply to endpoints
@rate_limit(max_calls=10, period=60)
def critique_prd_limited(prd_text):
    return agent.critique_prd(prd_text)
```

---

## Monitoring & Observability

### Basic Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('prd_cop.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('prd_cop')
logger.info(f"Critiqued PRD: {prd_name}, Score: {score}/100")
```

### Metrics (Prometheus)
```python
from prometheus_client import Counter, Histogram, start_http_server

# Define metrics
critique_count = Counter('prd_cop_critiques_total', 'Total PRD critiques')
critique_score = Histogram('prd_cop_score', 'PRD scores')
critique_duration = Histogram('prd_cop_duration_seconds', 'Critique duration')

# Track in code
with critique_duration.time():
    results = agent.critique_prd(prd_text)
    critique_count.inc()
    critique_score.observe(results['score'])

# Start metrics server
start_http_server(9090)
```

---

## Support

- **Documentation**: See README_USAGE.md
- **Issues**: https://github.com/ashishkhola/prd-critique-agent/issues
- **Stripe Internal**: #prd-cop-agent or ashishkhola@stripe.com
- **External**: GitHub Discussions

---

## Roadmap

**Planned Features:**
- [ ] Web UI for non-technical users
- [ ] Confluence integration
- [ ] Notion integration
- [ ] Custom scoring frameworks
- [ ] Multi-language support
- [ ] PRD templates library
- [ ] Team analytics dashboard

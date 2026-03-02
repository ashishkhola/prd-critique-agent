#!/bin/bash
# Quick deploy script for PRD Cop

echo "🚀 PRD Cop - Quick Deploy to Heroku"
echo "===================================="
echo ""

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Installing..."
    echo ""
    echo "Run: brew install heroku/brew/heroku"
    echo "Or download from: https://devcenter.heroku.com/articles/heroku-cli"
    echo ""
    exit 1
fi

echo "✅ Heroku CLI found"
echo ""

# Login check
echo "Checking Heroku login..."
if ! heroku auth:whoami &> /dev/null; then
    echo "Please login to Heroku:"
    heroku login
fi

echo "✅ Logged in to Heroku"
echo ""

# Get app name
read -p "Enter app name (e.g., prd-cop-yourname): " APP_NAME

if [ -z "$APP_NAME" ]; then
    APP_NAME="prd-cop-$(whoami)"
    echo "Using default name: $APP_NAME"
fi

echo ""
echo "Creating Heroku app: $APP_NAME"
heroku create "$APP_NAME" 2>/dev/null

echo ""
echo "Setting environment variables..."

# Check if running on Stripe internal
if [ -n "$ANTHROPIC_BASE_URL" ] && [ -n "$ANTHROPIC_AUTH_TOKEN" ]; then
    echo "Detected Stripe internal setup"
    heroku config:set ANTHROPIC_BASE_URL="$ANTHROPIC_BASE_URL" -a "$APP_NAME"
    heroku config:set ANTHROPIC_AUTH_TOKEN="$ANTHROPIC_AUTH_TOKEN" -a "$APP_NAME"
else
    # Ask for API key
    read -p "Enter your Anthropic API key (sk-ant-...): " API_KEY
    if [ -z "$API_KEY" ]; then
        echo "❌ API key required"
        exit 1
    fi
    heroku config:set ANTHROPIC_API_KEY="$API_KEY" -a "$APP_NAME"
fi

echo "✅ Environment variables set"
echo ""

# Deploy
echo "Deploying to Heroku..."
git push heroku main

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Your PRD Cop URL:"
heroku open -a "$APP_NAME"
heroku info -a "$APP_NAME" | grep "Web URL"

echo ""
echo "📝 Next steps:"
echo "1. Test your URL"
echo "2. Update SHARE_WITH_PMS.md with your URL"
echo "3. Share with your team!"
echo ""
echo "To view logs: heroku logs --tail -a $APP_NAME"
echo ""

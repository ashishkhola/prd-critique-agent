#!/usr/bin/env python3
"""
PRD Cop Slack Bot - Share with your team via Slack
Usage: python3 slack_bot.py

Requirements:
    pip install slack-bolt anthropic

Setup:
    1. Create Slack app at https://api.slack.com/apps
    2. Add Bot Token Scopes: chat:write, commands, files:write
    3. Install app to workspace
    4. Set environment variables:
       export SLACK_BOT_TOKEN="xoxb-..."
       export SLACK_SIGNING_SECRET="..."
       export ANTHROPIC_API_KEY="sk-ant-..." (or use Stripe internal)
    5. Enable slash commands: /prd-cop
"""

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from prd_cop_agent import PRDCopAgent
import os

# Initialize Slack app
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Initialize PRD Cop agent
agent = PRDCopAgent()


@app.command("/prd-cop")
def handle_prd_cop_command(ack, say, command):
    """
    Handle /prd-cop slash command
    Usage:
        /prd-cop [paste PRD text here]
        /prd-cop [Google Doc URL]
    """
    ack()

    user_input = command['text'].strip()

    if not user_input:
        say(
            "🚨 *PRD Cop* - Autonomous PRD Critique Agent\n\n"
            "*Usage:*\n"
            "• `/prd-cop [paste PRD text]` - Critique a PRD\n"
            "• `/prd-cop [Google Doc URL]` - Critique from Google Doc (Stripe internal)\n\n"
            "*Example:*\n"
            "```/prd-cop # Background\\nWe need to build...```"
        )
        return

    # Show processing message
    say(f"🔍 PRD Cop analyzing your document... (this may take 30-60 seconds)")

    try:
        # Check if it's a Google Doc URL
        if 'docs.google.com' in user_input:
            try:
                prd_text = agent.fetch_google_doc(user_input)
                prd_name = "Google_Doc"
            except NotImplementedError:
                say("⚠️  Google Doc fetching requires Stripe internal setup. Please paste PRD text instead.")
                return
        else:
            prd_text = user_input
            prd_name = "Slack_PRD"

        # Run critique
        results = agent.critique_prd(prd_text, prd_name)

        score = results['score']
        report_path = results['report_path']

        # Determine emoji based on score
        if score >= 85:
            emoji = "✅"
            status = "Leadership-ready!"
        elif score >= 70:
            emoji = "⚠️"
            status = "Needs polish"
        elif score >= 50:
            emoji = "❌"
            status = "Needs revision"
        else:
            emoji = "🚨"
            status = "Not ready"

        # Send results to Slack
        say(
            f"{emoji} *PRD Cop Score: {score}/100* - {status}\n\n"
            f"📊 *Breakdown:*\n"
            f"```\n{_extract_breakdown(results['report_text'])}```\n\n"
            f"📄 *Full Report:* Uploading...\n\n"
            f"💡 *Want an improved version?* Reply with 'improve' and I'll generate one!"
        )

        # Upload full report
        with open(report_path, 'r') as f:
            app.client.files_upload_v2(
                channel=command['channel_id'],
                file=report_path,
                title=f"PRD_Cop_Report_{score}pts.md",
                initial_comment=f"Full critique report (Score: {score}/100)"
            )

    except Exception as e:
        say(f"❌ Error: {str(e)}\n\nPlease try again or contact support.")


@app.message("improve")
def handle_improve_request(message, say):
    """Handle requests to generate improved PRD"""
    # This is simplified - would need state management to track which PRD to improve
    say(
        "🔧 To generate an improved version:\n"
        "1. Save the critique report\n"
        "2. Run: `python3 prd_cop_agent.py your_prd.txt`\n"
        "3. When prompted, type 'y' to generate improved version\n\n"
        "Or use the Python API for programmatic access!"
    )


def _extract_breakdown(report_text: str) -> str:
    """Extract score breakdown from report"""
    import re

    match = re.search(
        r'Score Breakdown:.*?\n((?:.*?\n){6})',
        report_text,
        re.DOTALL
    )

    if match:
        return match.group(1).strip()
    return "See full report for details"


@app.event("app_mention")
def handle_mention(event, say):
    """Handle @mentions of the bot"""
    say(
        "👋 Hi! I'm PRD Cop - I critique PRDs using a comprehensive 100-point framework.\n\n"
        "*To use me:*\n"
        "• `/prd-cop [your PRD text]` - Get a critique\n"
        "• `/prd-cop [Google Doc URL]` - Critique from Google Doc\n\n"
        "*I check for:*\n"
        "✓ Structural completeness\n"
        "✓ Clear, concrete language\n"
        "✓ Testable acceptance criteria\n"
        "✓ ROI and resource requirements\n"
        "✓ Risk analysis\n"
        "✓ Strategic alignment\n\n"
        "Try me out! 🚀"
    )


if __name__ == "__main__":
    # Check for required env vars
    if not os.environ.get("SLACK_BOT_TOKEN"):
        print("❌ Missing SLACK_BOT_TOKEN environment variable")
        print("Set up: https://api.slack.com/apps")
        exit(1)

    if not os.environ.get("SLACK_APP_TOKEN"):
        print("❌ Missing SLACK_APP_TOKEN for Socket Mode")
        print("Enable Socket Mode in Slack app settings")
        exit(1)

    print("🚀 PRD Cop Slack Bot starting...")
    print("   Listening for /prd-cop commands...")

    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()

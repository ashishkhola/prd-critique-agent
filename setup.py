#!/usr/bin/env python3
"""
Setup script for PRD Critique Agent

This script helps you set up the agent with interactive prompts
"""

import os
import sys
import json
from pathlib import Path


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def check_dependencies():
    """Check if required dependencies are installed"""
    print_header("Checking Dependencies")

    required_modules = [
        ("anthropic", "Anthropic API client"),
        ("google.oauth2", "Google authentication"),
        ("googleapiclient", "Google API client"),
    ]

    missing = []

    for module, description in required_modules:
        try:
            __import__(module)
            print(f"✅ {description}: Installed")
        except ImportError:
            print(f"❌ {description}: Missing")
            missing.append(module)

    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False

    print("\n✅ All dependencies installed!")
    return True


def setup_anthropic_key():
    """Set up Anthropic API key"""
    print_header("Anthropic API Key Setup")

    # Check if already set
    if os.environ.get("ANTHROPIC_API_KEY"):
        print("✅ ANTHROPIC_API_KEY already set in environment")
        return True

    print("Get your API key from: https://console.anthropic.com/")
    print("\nOptions:")
    print("  1. Set environment variable (temporary)")
    print("  2. Create .env file (persistent)")
    print("  3. Skip (I'll set it later)")

    choice = input("\nChoose option (1-3): ").strip()

    if choice == "1":
        api_key = input("Enter your Anthropic API key: ").strip()
        os.environ["ANTHROPIC_API_KEY"] = api_key
        print("✅ API key set for this session")
        print("   To make permanent, add to your shell profile:")
        print(f"   export ANTHROPIC_API_KEY='{api_key}'")
        return True

    elif choice == "2":
        api_key = input("Enter your Anthropic API key: ").strip()
        with open(".env", "w") as f:
            f.write(f"ANTHROPIC_API_KEY={api_key}\n")
        print("✅ API key saved to .env file")
        print("   Load with: source .env")
        return True

    else:
        print("⏭️  Skipped. Set ANTHROPIC_API_KEY before running the agent.")
        return False


def setup_google_credentials():
    """Set up Google Cloud credentials"""
    print_header("Google Cloud Credentials Setup")

    if Path("google-credentials.json").exists():
        print("✅ google-credentials.json already exists")
        return True

    print("To read Google Docs, you need a service account credential.")
    print("\nSteps:")
    print("  1. Go to: https://console.cloud.google.com/")
    print("  2. Create/select a project")
    print("  3. Enable 'Google Docs API'")
    print("  4. Create Service Account")
    print("  5. Download JSON key")
    print("  6. Share your Google Docs with the service account email")

    print("\nOptions:")
    print("  1. I have the credentials file")
    print("  2. Skip (I'll set it up later)")

    choice = input("\nChoose option (1-2): ").strip()

    if choice == "1":
        path = input("Enter path to credentials JSON file: ").strip()
        path = path.strip('"').strip("'")  # Remove quotes if present

        if os.path.exists(path):
            import shutil
            shutil.copy(path, "google-credentials.json")
            print("✅ Credentials copied to google-credentials.json")
            return True
        else:
            print(f"❌ File not found: {path}")
            return False
    else:
        print("⏭️  Skipped. Set up google-credentials.json before running.")
        return False


def create_directories():
    """Create necessary directories"""
    print_header("Creating Directories")

    directories = ["reports"]

    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True)
            print(f"✅ Created: {directory}/")
        else:
            print(f"✅ Exists: {directory}/")


def create_example_config():
    """Create a config.json from config.example.json"""
    print_header("Configuration File")

    if Path("config.json").exists():
        print("✅ config.json already exists")
        return

    if Path("config.example.json").exists():
        with open("config.example.json", "r") as f:
            config = json.load(f)

        # Update with environment variables if available
        if os.environ.get("ANTHROPIC_API_KEY"):
            config["api"]["anthropic_api_key"] = os.environ["ANTHROPIC_API_KEY"]

        with open("config.json", "w") as f:
            json.dump(config, f, indent=2)

        print("✅ Created config.json from example")
        print("   Edit config.json to customize settings")
    else:
        print("⚠️  config.example.json not found")


def run_test():
    """Run a simple test"""
    print_header("Running Test")

    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, "example_usage.py"],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0 and "✅" in result.stdout:
            print("✅ Test passed!")
            print("\nTest output:")
            print(result.stdout[-500:])  # Last 500 chars
            return True
        else:
            print("⚠️  Test completed with issues")
            if result.stderr:
                print("\nErrors:")
                print(result.stderr[-500:])
            return False

    except Exception as e:
        print(f"⚠️  Could not run test: {str(e)}")
        return False


def print_next_steps():
    """Print next steps for the user"""
    print_header("Setup Complete!")

    print("🎉 Your PRD Critique Agent is ready to use!\n")

    print("Next steps:")
    print("\n1️⃣  Test the agent:")
    print("   python example_usage.py")

    print("\n2️⃣  Critique your first PRD:")
    print("   Edit agent.py and replace 'YOUR_GOOGLE_DOC_ID_HERE'")
    print("   Then run: python agent.py")

    print("\n3️⃣  Batch process multiple PRDs:")
    print("   See example_batch_critique() in example_usage.py")

    print("\n4️⃣  Customize the critique framework:")
    print("   Edit _get_critique_framework() in agent.py")

    print("\n📚 Documentation:")
    print("   - README.md - Comprehensive guide")
    print("   - QUICKSTART.md - Quick reference")
    print("   - example_usage.py - Code examples")

    print("\n💡 Tips:")
    print("   - Reports are saved to ./reports/ directory")
    print("   - Typical cost: $0.60-$1.00 per PRD critique")
    print("   - Customize tools in define_tools() method")

    print("\n" + "=" * 60)


def main():
    """Run the setup wizard"""
    print("\n" + "🤖 PRD CRITIQUE AGENT SETUP ".center(60, "="))
    print("\nThis wizard will help you set up the agent.\n")

    steps = [
        ("Dependencies", check_dependencies),
        ("Anthropic API", setup_anthropic_key),
        ("Google Credentials", setup_google_credentials),
        ("Directories", create_directories),
        ("Configuration", create_example_config),
    ]

    results = {}

    for step_name, step_func in steps:
        try:
            results[step_name] = step_func()
        except KeyboardInterrupt:
            print("\n\n⚠️  Setup interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Error in {step_name}: {str(e)}")
            results[step_name] = False

    # Summary
    print_header("Setup Summary")

    for step_name, success in results.items():
        status = "✅" if success else "⚠️ "
        print(f"{status} {step_name}")

    # Optional test
    if all(results.values()):
        print("\n🎉 All steps completed successfully!")
        run_test_choice = input("\nRun a test now? (y/n): ").strip().lower()
        if run_test_choice == 'y':
            run_test()

    print_next_steps()


if __name__ == "__main__":
    main()

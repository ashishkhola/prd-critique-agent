.PHONY: help install setup test clean run example

help:
	@echo "PRD Critique Agent - Available Commands"
	@echo "========================================"
	@echo ""
	@echo "  make install    - Install dependencies"
	@echo "  make setup      - Run interactive setup wizard"
	@echo "  make test       - Run tests and examples"
	@echo "  make run        - Run the agent (edit agent.py first)"
	@echo "  make example    - Run usage examples"
	@echo "  make clean      - Clean generated files and cache"
	@echo "  make reports    - List generated reports"
	@echo ""

install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed!"

setup:
	@echo "🔧 Running setup wizard..."
	python setup.py

test:
	@echo "🧪 Running tests..."
	python example_usage.py

run:
	@echo "🤖 Running PRD Critique Agent..."
	@echo "⚠️  Make sure to edit agent.py with your document ID first!"
	python agent.py

example:
	@echo "📚 Running usage examples..."
	python example_usage.py

clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup complete!"

reports:
	@echo "📊 Generated Reports:"
	@echo "===================="
	@ls -lh reports/ 2>/dev/null || echo "No reports yet. Run 'make run' to generate your first critique!"

dirs:
	@echo "📁 Creating directories..."
	mkdir -p reports
	@echo "✅ Directories created!"

check:
	@echo "🔍 Checking configuration..."
	@if [ ! -f "google-credentials.json" ]; then \
		echo "⚠️  google-credentials.json not found"; \
	else \
		echo "✅ Google credentials found"; \
	fi
	@if [ -z "$$ANTHROPIC_API_KEY" ]; then \
		echo "⚠️  ANTHROPIC_API_KEY not set"; \
	else \
		echo "✅ Anthropic API key set"; \
	fi
	@python -c "import anthropic; import google.oauth2; print('✅ Python dependencies installed')" 2>/dev/null || echo "⚠️  Missing dependencies - run 'make install'"

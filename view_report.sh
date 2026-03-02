#!/bin/bash
# Quick script to view PRD critique reports

REPORTS_DIR="/Users/ashishkhola/prd_critique_agent/reports"

echo "📊 PRD Critique Reports"
echo "======================="
echo ""

# List all reports
echo "Available reports:"
ls -1t "$REPORTS_DIR"/*.md | head -10 | nl

echo ""
echo "Choose an option:"
echo "  1) Open latest report"
echo "  2) Open reports folder"
echo "  3) List all reports"
echo "  4) View report in terminal"
echo ""

read -p "Enter option (1-4): " choice

case $choice in
  1)
    latest=$(ls -t "$REPORTS_DIR"/*.md | head -1)
    echo "Opening: $(basename "$latest")"
    open "$latest"
    ;;
  2)
    open "$REPORTS_DIR"
    ;;
  3)
    ls -lh "$REPORTS_DIR"
    ;;
  4)
    latest=$(ls -t "$REPORTS_DIR"/*.md | head -1)
    echo "Viewing: $(basename "$latest")"
    echo ""
    cat "$latest" | less
    ;;
  *)
    echo "Invalid option"
    ;;
esac

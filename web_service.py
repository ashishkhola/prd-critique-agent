#!/usr/bin/env python3
"""
PRD Cop Web Service - REST API
Usage: python3 web_service.py

Requirements:
    pip install flask anthropic flask-cors

Endpoints:
    POST /critique - Submit PRD for critique
    POST /improve - Generate improved version
    GET /health - Health check
"""

from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from prd_cop_agent import PRDCopAgent
import os
from pathlib import Path
import tempfile

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for web frontend

# Initialize agent
agent = PRDCopAgent()


@app.route('/')
def index():
    """Serve the web UI"""
    return send_from_directory('static', 'index.html')


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "PRD Cop Agent",
        "version": "1.0.0",
        "mode": agent.mode
    })


@app.route('/critique', methods=['POST'])
def critique_prd():
    """
    Critique a PRD

    Request JSON:
        {
            "prd_text": "...",
            "prd_name": "Optional name"
        }

    Response JSON:
        {
            "score": 78,
            "report_text": "...",
            "report_path": "...",
            "token_usage": {...}
        }
    """
    try:
        data = request.get_json()

        if not data or 'prd_text' not in data:
            return jsonify({
                "error": "Missing 'prd_text' in request body"
            }), 400

        prd_text = data['prd_text']
        prd_name = data.get('prd_name', 'API_PRD')

        if not prd_text.strip():
            return jsonify({
                "error": "Empty PRD text"
            }), 400

        # Run critique
        results = agent.critique_prd(prd_text, prd_name)

        return jsonify({
            "score": results['score'],
            "report_text": results['report_text'],
            "report_path": str(results['report_path']),
            "token_usage": results['token_usage']
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route('/improve', methods=['POST'])
def improve_prd():
    """
    Generate improved version of PRD

    Request JSON:
        {
            "original_prd": "...",
            "critique_results": {...},  # from /critique endpoint
            "prd_name": "Optional name"
        }

    Response JSON:
        {
            "improved_text": "...",
            "report_path": "...",
            "original_score": 52
        }
    """
    try:
        data = request.get_json()

        if not data or 'original_prd' not in data or 'critique_results' not in data:
            return jsonify({
                "error": "Missing 'original_prd' or 'critique_results' in request body"
            }), 400

        original_prd = data['original_prd']
        critique_results = data['critique_results']
        prd_name = data.get('prd_name', 'API_PRD')

        # Generate improved version
        results = agent.improve_prd(original_prd, critique_results, prd_name)

        return jsonify({
            "improved_text": results['improved_text'],
            "report_path": str(results['report_path']),
            "original_score": results['original_score']
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route('/download/<report_id>', methods=['GET'])
def download_report(report_id):
    """Download a report file by ID"""
    try:
        reports_dir = Path("reports")
        report_files = list(reports_dir.glob(f"*{report_id}*.md"))

        if not report_files:
            return jsonify({
                "error": "Report not found"
            }), 404

        return send_file(
            report_files[0],
            mimetype='text/markdown',
            as_attachment=True,
            download_name=report_files[0].name
        )

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route('/batch', methods=['POST'])
def batch_critique():
    """
    Critique multiple PRDs in batch

    Request JSON:
        {
            "prds": [
                {"name": "PRD1", "text": "..."},
                {"name": "PRD2", "text": "..."}
            ]
        }

    Response JSON:
        {
            "results": [
                {"name": "PRD1", "score": 78, ...},
                {"name": "PRD2", "score": 65, ...}
            ]
        }
    """
    try:
        data = request.get_json()

        if not data or 'prds' not in data:
            return jsonify({
                "error": "Missing 'prds' array in request body"
            }), 400

        results = []

        for prd_data in data['prds']:
            prd_name = prd_data.get('name', 'Unnamed_PRD')
            prd_text = prd_data.get('text', '')

            if not prd_text.strip():
                results.append({
                    "name": prd_name,
                    "error": "Empty PRD text"
                })
                continue

            try:
                critique = agent.critique_prd(prd_text, prd_name)
                results.append({
                    "name": prd_name,
                    "score": critique['score'],
                    "report_path": str(critique['report_path']),
                    "summary": _extract_summary(critique['report_text'])
                })
            except Exception as e:
                results.append({
                    "name": prd_name,
                    "error": str(e)
                })

        return jsonify({
            "results": results,
            "total": len(results),
            "succeeded": len([r for r in results if 'score' in r]),
            "failed": len([r for r in results if 'error' in r])
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


def _extract_summary(report_text: str) -> dict:
    """Extract key information from report"""
    import re

    score_match = re.search(r'FINAL SCORE:\s*(\d+)/100', report_text)
    score = int(score_match.group(1)) if score_match else 0

    # Extract verdict
    verdict_match = re.search(r'### Verdict:\s*\n(.*?)(?:\n\n|$)', report_text, re.DOTALL)
    verdict = verdict_match.group(1).strip() if verdict_match else ""

    return {
        "score": score,
        "verdict_preview": verdict[:200] + "..." if len(verdict) > 200 else verdict
    }


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))

    print("🚀 PRD Cop Web Service starting...")
    print(f"   Mode: {agent.mode}")
    print(f"   Port: {port}")
    print("\nEndpoints:")
    print("   POST /critique - Critique a PRD")
    print("   POST /improve - Generate improved version")
    print("   POST /batch - Batch critique multiple PRDs")
    print("   GET /health - Health check")
    print("\nExample:")
    print('   curl -X POST http://localhost:8080/critique \\')
    print('        -H "Content-Type: application/json" \\')
    print('        -d \'{"prd_text": "# My PRD...", "prd_name": "Feature X"}\'')

    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.environ.get('DEBUG', 'false').lower() == 'true'
    )

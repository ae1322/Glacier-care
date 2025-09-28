import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import re
from typing import Dict, Any

# Configure logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import scanner processor, but make it optional
try:
    from scanner_processor import scanner_processor
    SCANNER_AVAILABLE = True
    logger.info("Enhanced scanner processor loaded successfully")
except ImportError as e:
    logger.warning(f"Enhanced scanner processor not available: {e}")
    SCANNER_AVAILABLE = False
    scanner_processor = None

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_DEFAULT_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is required")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")


class GlacierCareAnalyzer:
    def __init__(self):
        self.model = model

    def analyze_report(self, report_text: str, filename: str = None) -> Dict[str, Any]:
        """Analyze medical report using Gemini AI"""
        try:
            prompt = self._create_analysis_prompt(report_text, filename)
            response = self.model.generate_content(prompt)
            return self._parse_gemini_response(response.text)
        except Exception as e:
            logger.error(f"Error analyzing report: {str(e)}")
            return self._create_fallback_response(report_text, filename)

    def _create_analysis_prompt(self, report_text: str, filename: str = None) -> str:
        """Prompt that ensures medications are fully explained"""
        file_info = f" (from file: {filename})" if filename else ""
        return f"""
You are a medical AI assistant that analyzes medical reports and provides clear explanations for patients.

Please analyze the following medical report{file_info} and provide a structured JSON output. 
Focus especially on medications: extract each medication name, dosage, explain its purpose, how to take it, and common side effects. 
If no medications are mentioned, return "medicationDetails": [].

Medical Report:
{report_text}

Respond ONLY with valid JSON in this format:

{{
  "keyFindings": ["..."],
  "explanations": ["..."],
  "recommendations": ["..."],
  "urgentCare": ["..."],
  "medicationDetails": [
    {{
      "name": "Medication name and dosage",
      "purpose": "What this medicine does in simple terms",
      "instructions": "When/how to take it",
      "sideEffects": "Common side effects to watch for"
    }}
  ],
  "riskLevel": "low|moderate|high"
}}
"""

    def _parse_gemini_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini AI response and enforce schema"""
        try:
            cleaned = response_text.strip()
            cleaned = re.sub(r"```json\s*", "", cleaned)
            cleaned = re.sub(r"```\s*", "", cleaned)

            result = json.loads(cleaned)

            # Ensure all required fields exist
            required = ["keyFindings", "explanations", "recommendations", "urgentCare", "medicationDetails", "riskLevel"]
            for f in required:
                if f not in result:
                    result[f] = [] if f != "riskLevel" else "moderate"

            # Risk level correction
            if result["riskLevel"] not in ["low", "moderate", "high"]:
                result["riskLevel"] = "moderate"

            # Ensure arrays
            for f in ["keyFindings", "explanations", "recommendations", "urgentCare"]:
                if not isinstance(result[f], list):
                    result[f] = []

            # Sanitize medications
            meds = []
            if isinstance(result.get("medicationDetails"), list):
                for med in result["medicationDetails"]:
                    if isinstance(med, dict):
                        meds.append({
                            "name": med.get("name", "Unknown"),
                            "purpose": med.get("purpose", "Not specified"),
                            "instructions": med.get("instructions", "Not specified"),
                            "sideEffects": med.get("sideEffects", "Not specified")
                        })
            result["medicationDetails"] = meds

            return result
        except Exception as e:
            logger.error(f"Error parsing Gemini response: {str(e)}")
            return self._create_fallback_response("", "")

    def _create_fallback_response(self, report_text: str, filename: str = None) -> Dict[str, Any]:
        file_info = f" (from file: {filename})" if filename else ""
        return {
            "keyFindings": [
                f"Report analysis completed {file_info}",
                "Unable to provide detailed AI analysis at this time",
                "Please consult your healthcare provider"
            ],
            "explanations": [
                "We had a technical issue while analyzing your report.",
                "This does not reflect your health status.",
                "Your healthcare provider can give a detailed explanation."
            ],
            "recommendations": [
                "Contact your healthcare provider for interpretation",
                "Keep a copy of your medical report",
                "Schedule a follow-up appointment"
            ],
            "urgentCare": [
                "Seek immediate care if you have severe symptoms",
                "Do not delay urgent medical attention"
            ],
            "medicationDetails": [],
            "riskLevel": "moderate"
        }


# Initialize analyzer
analyzer = GlacierCareAnalyzer()


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "Glacier Care", "version": "1.1.0"})


@app.route("/analyze", methods=["POST"])
def analyze_medical_report():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON", "status": "error"}), 400

        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided", "status": "error"}), 400

        report_text = data.get("reportText", "").strip()
        filename = data.get("filename", "")

        if not report_text:
            return jsonify({"error": "Report text is required", "status": "error"}), 400

        logger.info(f"Analyzing report: {len(report_text)} chars, filename: {filename}")
        result = analyzer.analyze_report(report_text, filename)

        result["metadata"] = {
            "filename": filename,
            "analysisTimestamp": datetime.now().isoformat(),
            "reportLength": len(report_text),
            "aiModel": "gemini-2.5-flash",
            "userId": "demo-user-123",
        }

        return jsonify({"status": "success", "data": result})
    except Exception as e:
        logger.error(f"Error in /analyze: {str(e)}")
        return jsonify({"error": "Internal server error", "status": "error"}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found", "status": "error"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error", "status": "error"}), 500


if __name__ == "__main__":
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY not set")
        exit(1)

    logger.info("Starting Glacier Care API...")
    logger.info(f"Gemini API key loaded: {GEMINI_API_KEY[:8]}...")

    app.run(host="0.0.0.0", port=5000, debug=os.getenv("FLASK_DEBUG", "False").lower() == "true")

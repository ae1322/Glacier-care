import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import re
from typing import Dict, List, Any

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configure Gemini AI
GEMINI_API_KEY = "AIzaSyDoic239xATtrO8BSsl2jvrudumFUJHs84"
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is required")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

class MedicalReportAnalyzer:
    def __init__(self):
        self.model = model
    
    def analyze_report(self, report_text: str, filename: str = None) -> Dict[str, Any]:
        """
        Analyze medical report using Gemini AI
        """
        try:
            # Create a comprehensive prompt for medical analysis
            prompt = self._create_analysis_prompt(report_text, filename)
            
            # Generate response from Gemini
            response = self.model.generate_content(prompt)
            
            # Parse the response
            analysis_result = self._parse_gemini_response(response.text)
            
            return analysis_result
            
        except Exception as e:
            console.log(f"Error analyzing report: {str(e)}")
            logger.error(f"Error analyzing report: {str(e)}")
            return self._create_fallback_response(report_text, filename)
    
    def _create_analysis_prompt(self, report_text: str, filename: str = None) -> str:
        """Create a detailed prompt for Gemini AI analysis"""
        
        file_info = f" (from file: {filename})" if filename else ""
        
        prompt = f"""
You are a medical AI assistant that analyzes medical reports and provides clear, easy-to-understand explanations for patients. 

Please analyze the following medical report{file_info} and provide a comprehensive analysis in the exact JSON format specified below.

Medical Report:
{report_text}

Please provide your analysis in the following JSON format (respond ONLY with valid JSON, no additional text):

{{
    "keyFindings": [
        "List 3-5 key findings from the report in simple terms",
        "Include specific values and ranges where applicable",
        "Mention any abnormal or concerning values"
    ],
    "explanations": [
        "Explain what each key finding means in simple, non-medical language",
        "Use analogies and everyday language when possible",
        "Help the patient understand the significance of each finding"
    ],
    "recommendations": [
        "Provide 3-5 practical recommendations based on the findings",
        "Include lifestyle changes, follow-up actions, or preventive measures",
        "Focus on actionable advice the patient can implement"
    ],
    "urgentCare": [
        "List any urgent symptoms or conditions that require immediate medical attention",
        "Include warning signs to watch for",
        "Specify when to contact a doctor immediately"
    ],
    "medicationDetails": [
        {{
            "name": "Medication name and dosage",
            "purpose": "Explain what this medication does in simple terms",
            "instructions": "How and when to take the medication",
            "sideEffects": "Common side effects to watch for"
        }}
    ],
    "riskLevel": "low|moderate|high"
}}

Guidelines:
1. Use simple, clear language that a non-medical person can understand
2. Avoid medical jargon - explain terms in everyday language
3. Be encouraging but honest about health status
4. Focus on actionable advice
5. If no medications are mentioned, leave medicationDetails as an empty array
6. Assess overall risk level based on the findings
7. Always include a medical disclaimer reminder

Respond with ONLY the JSON object, no additional text or formatting.
"""
        return prompt
    
    def _parse_gemini_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini AI response and extract structured data"""
        try:
            # Clean the response text
            cleaned_text = response_text.strip()
            
            # Remove any markdown formatting
            cleaned_text = re.sub(r'```json\s*', '', cleaned_text)
            cleaned_text = re.sub(r'```\s*', '', cleaned_text)
            
            # Try to parse as JSON
            try:
                result = json.loads(cleaned_text)
                
                # Validate required fields
                required_fields = ['keyFindings', 'explanations', 'recommendations', 'urgentCare', 'medicationDetails', 'riskLevel']
                for field in required_fields:
                    if field not in result:
                        raise ValueError(f"Missing required field: {field}")
                
                # Ensure riskLevel is valid
                if result['riskLevel'] not in ['low', 'moderate', 'high']:
                    result['riskLevel'] = 'moderate'
                
                # Ensure arrays are properly formatted
                for field in ['keyFindings', 'explanations', 'recommendations', 'urgentCare', 'medicationDetails']:
                    if not isinstance(result[field], list):
                        result[field] = []
                
                return result
                
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing error: {str(e)}")
                logger.error(f"Response text: {cleaned_text}")
                return self._create_fallback_response("", "")
                
        except Exception as e:
            logger.error(f"Error parsing Gemini response: {str(e)}")
            return self._create_fallback_response("", "")
    
    def _create_fallback_response(self, report_text: str, filename: str = None) -> Dict[str, Any]:
        """Create a fallback response when AI analysis fails"""
        file_info = f" (from file: {filename})" if filename else ""
        
        return {
            "keyFindings": [
                f"Report analysis completed {file_info}",
                "Unable to provide detailed AI analysis at this time",
                "Please consult with your healthcare provider for detailed interpretation"
            ],
            "explanations": [
                "We encountered a technical issue while analyzing your report",
                "This is a temporary problem and does not reflect on your health status",
                "Your healthcare provider can provide the detailed analysis you need"
            ],
            "recommendations": [
                "Contact your healthcare provider for a detailed report interpretation",
                "Keep a copy of your medical report for your records",
                "Schedule a follow-up appointment to discuss your results"
            ],
            "urgentCare": [
                "If you have any immediate health concerns, contact your doctor or visit the emergency room",
                "Do not delay seeking medical attention for urgent symptoms"
            ],
            "medicationDetails": [],
            "riskLevel": "moderate"
        }

# Initialize the analyzer
analyzer = MedicalReportAnalyzer()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Medical Report Analyzer",
        "version": "1.0.0"
    })

@app.route('/analyze', methods=['POST'])
def analyze_medical_report():
    """
    Analyze medical report endpoint
    Expected JSON payload:
    {
        "reportText": "string",
        "filename": "string" (optional)
    }
    """
    try:
        # Validate request
        if not request.is_json:
            return jsonify({
                "error": "Request must be JSON",
                "status": "error"
            }), 400
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "No data provided",
                "status": "error"
            }), 400
        
        # Extract report text
        report_text = data.get('reportText', '').strip()
        filename = data.get('filename', '')
        
        if not report_text:
            return jsonify({
                "error": "Report text is required",
                "status": "error"
            }), 400
        
        # Validate report text length
    
        
        logger.info(f"Analyzing report: {len(report_text)} characters, filename: {filename}")
        
        # Analyze the report
        analysis_result = analyzer.analyze_report(report_text, filename)
        
        # Add metadata
        analysis_result['metadata'] = {
            'filename': filename,
            'analysisTimestamp': datetime.now().isoformat(),
            'reportLength': len(report_text),
            'aiModel': 'gemini-1.5-flash'
        }
        
        return jsonify({
            "status": "success",
            "data": analysis_result
        })
        
    except Exception as e:
        logger.error(f"Error in analyze endpoint: {str(e)}")
        return jsonify({
            "error": "Internal server error occurred while analyzing the report",
            "status": "error",
            "details": str(e) if app.debug else "Contact support for assistance"
        }), 500

@app.route('/analyze/file', methods=['POST'])
def analyze_medical_file():
    """
    Analyze uploaded medical file endpoint
    Expected form data with 'file' field
    """
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({
                "error": "No file provided",
                "status": "error"
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                "error": "No file selected",
                "status": "error"
            }), 400
        
        # Check file type
        allowed_extensions = {'.txt', '.pdf', '.doc', '.docx'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            return jsonify({
                "error": f"File type {file_ext} not supported. Allowed types: {', '.join(allowed_extensions)}",
                "status": "error"
            }), 400
        
        # Read file content
        if file_ext == '.txt':
            content = file.read().decode('utf-8')
        else:
            # For PDF and DOC files, you would need additional libraries like PyPDF2 or python-docx
            return jsonify({
                "error": f"File type {file_ext} processing not implemented yet. Please use .txt files.",
                "status": "error"
            }), 400
        
        if not content.strip():
            return jsonify({
                "error": "File is empty",
                "status": "error"
            }), 400
        
        logger.info(f"Analyzing file: {file.filename}, {len(content)} characters")
        
        # Analyze the content
        analysis_result = analyzer.analyze_report(content, file.filename)
        
        # Add metadata
        analysis_result['metadata'] = {
            'filename': file.filename,
            'analysisTimestamp': datetime.now().isoformat(),
            'reportLength': len(content),
            'aiModel': 'gemini-1.5-flash'
        }
        
        return jsonify({
            "status": "success",
            "data": analysis_result
        })
        
    except Exception as e:
        logger.error(f"Error in file analyze endpoint: {str(e)}")
        return jsonify({
            "error": "Internal server error occurred while analyzing the file",
            "status": "error",
            "details": str(e) if app.debug else "Contact support for assistance"
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "status": "error"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "status": "error"
    }), 500

if __name__ == '__main__':
    # Check if Gemini API key is configured
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY environment variable is not set")
        exit(1)
    
    logger.info("Starting Medical Report Analyzer API...")
    logger.info(f"Gemini API configured: {GEMINI_API_KEY[:10]}...")
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    )

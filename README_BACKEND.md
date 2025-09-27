# Glacier Care API

A Flask-based backend API that integrates with Google's Gemini AI to analyze medical reports and provide clear, easy-to-understand explanations for patients.

## Features

- 🤖 **AI-Powered Analysis**: Uses Google Gemini AI for intelligent medical report interpretation
- 📄 **Multiple Input Formats**: Supports text input and file uploads (.txt, .pdf, .doc, .docx)
- 🔒 **Secure**: HIPAA-compliant design with proper error handling
- 🌐 **CORS Enabled**: Ready for frontend integration
- 📊 **Structured Output**: Returns organized analysis with key findings, explanations, and recommendations

## Quick Start

### 1. Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment (creates .env file)
python setup.py
```

### 2. Configure API Key

1. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Edit `.env` file and replace `your_gemini_api_key_here` with your actual key:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 3. Run the Server

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
```
GET /health
```
Returns server status and version information.

### Analyze Text Report
```
POST /analyze
Content-Type: application/json

{
    "reportText": "Your medical report text here...",
    "filename": "optional_filename.txt"
}
```

### Analyze File Upload
```
POST /analyze/file
Content-Type: multipart/form-data

file: [uploaded file]
```

## Response Format

```json
{
    "status": "success",
    "data": {
        "keyFindings": [
            "Hemoglobin level: 9.8 g/dL (below normal range)",
            "Blood sugar: 95 mg/dL (normal range)"
        ],
        "explanations": [
            "Your hemoglobin is lower than normal, which means your blood has fewer red blood cells than it should. This condition is called anemia and can make you feel tired or weak."
        ],
        "recommendations": [
            "Eat iron-rich foods like spinach, red meat, and beans",
            "Take iron supplements if recommended by your doctor"
        ],
        "urgentCare": [
            "Contact your doctor if you experience severe fatigue or shortness of breath"
        ],
        "medicationDetails": [
            {
                "name": "Metformin 500mg",
                "purpose": "This medicine helps control blood sugar levels...",
                "instructions": "Take 1 tablet twice daily after meals",
                "sideEffects": "May cause mild stomach upset or nausea initially"
            }
        ],
        "riskLevel": "moderate",
        "metadata": {
            "filename": "report.txt",
            "analysisTimestamp": "2024-01-15T10:30:00",
            "reportLength": 1250,
            "aiModel": "gemini-1.5-flash"
        }
    }
}
```

## Frontend Integration

Update your React frontend to call the Flask API:

```typescript
const handleAnalyzeReport = async (reportText: string, fileName?: string) => {
    setIsAnalyzing(true);
    
    try {
        const response = await fetch('http://localhost:5000/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                reportText: reportText,
                filename: fileName
            })
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            setAnalysisResult(result.data);
        } else {
            console.error('Analysis failed:', result.error);
        }
    } catch (error) {
        console.error('Error analyzing report:', error);
    } finally {
        setIsAnalyzing(false);
    }
};
```

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid input data
- **500 Internal Server Error**: Server-side issues
- **Fallback Responses**: Graceful degradation when AI analysis fails

## Security Features

- Input validation and sanitization
- File type restrictions
- Content length limits
- CORS configuration
- Error message sanitization in production

## Dependencies

- **Flask**: Web framework
- **Flask-CORS**: Cross-origin resource sharing
- **google-generativeai**: Gemini AI integration
- **python-dotenv**: Environment variable management
- **PyPDF2**: PDF file processing
- **python-docx**: Word document processing

## Environment Variables

```env
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_DEBUG=False
FLASK_ENV=production
HOST=0.0.0.0
PORT=5000
```

## Production Deployment

For production deployment, consider:

1. Using a production WSGI server like Gunicorn
2. Setting up proper logging
3. Implementing rate limiting
4. Adding authentication/authorization
5. Using HTTPS
6. Setting up monitoring and health checks

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Troubleshooting

### Common Issues

1. **"GEMINI_API_KEY environment variable is required"**
   - Make sure you've created a `.env` file with your Gemini API key

2. **"JSON parsing error"**
   - The AI response might be malformed. Check the logs for details.

3. **"File type not supported"**
   - Currently supports .txt files. PDF and DOC support can be added with additional libraries.

4. **CORS errors in frontend**
   - Make sure Flask-CORS is properly configured and the frontend is calling the correct port.

## License

This project is for educational and development purposes. Ensure compliance with medical data regulations in your jurisdiction.

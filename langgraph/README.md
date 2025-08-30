# LangGraph Compliance Workflow API

This is a FastAPI server that provides an endpoint for running the LangGraph compliance analysis workflow on PRDs (Product Requirements Documents).

## Features

- **PRD Analysis**: Comprehensive compliance analysis of product requirements
- **Risk Assessment**: Automated risk level evaluation
- **Compliance Issues**: Identification of critical compliance problems
- **State-by-State Analysis**: US state compliance evaluation
- **Recommendations**: Actionable recommendations for compliance

## Quick Start

### 1. Install Dependencies

```bash
cd langgraph
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file in the `langgraph` directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
LANGGRAPH_HOST=0.0.0.0
LANGGRAPH_PORT=8000
```

### 3. Start the Server

```bash
python main.py
```

The server will start on `http://localhost:8000`

## API Endpoints

### POST `/analyze-prd`

Analyze a PRD for compliance.

**Request Body:**
```json
{
  "name": "My Product",
  "description": "A description of the product",
  "content": "Optional detailed PRD content"
}
```

**Response:**
```json
{
  "workflow_id": "workflow_20250101_120000",
  "prd_name": "My Product",
  "prd_description": "A description of the product",
  "overall_risk_level": "medium",
  "overall_confidence_score": 0.85,
  "total_features_analyzed": 3,
  "critical_compliance_issues": [
    "Feature 1: HIGH risk",
    "Feature 2: MEDIUM risk"
  ],
  "summary_recommendations": [
    "Implement data encryption",
    "Add user consent mechanisms"
  ],
  "non_compliant_states": {
    "CA": {
      "state_name": "California",
      "risk_score": 0.75,
      "risk_level": "high",
      "non_compliant_features": ["data_collection", "user_tracking"],
      "reasoning": "CCPA compliance issues...",
      "required_actions": ["Implement data deletion", "Add opt-out mechanism"]
    }
  },
  "processing_time": 45.2,
  "status": "completed"
}
```

### GET `/health`

Health check endpoint.

### GET `/`

Root endpoint with API information.

### GET `/docs`

Interactive API documentation (Swagger UI).

## Integration with Backend

The backend can call this API using the endpoint:

```
POST http://localhost:8000/analyze-prd
```

Example backend integration:

```python
import httpx

async def analyze_prd_with_langgraph(name: str, description: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/analyze-prd",
            json={
                "name": name,
                "description": description
            }
        )
        return response.json()
```

## Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key
- `LANGGRAPH_HOST`: Server host (default: 0.0.0.0)
- `LANGGRAPH_PORT`: Server port (default: 8000)

## Workflow Process

1. **PRD Parsing**: Extract features from the PRD
2. **Feature Analysis**: Analyze each feature for compliance
3. **Regulation Matching**: Match features to relevant regulations
4. **Risk Assessment**: Evaluate risk levels
5. **State Compliance**: Check US state-specific compliance
6. **Recommendations**: Generate actionable recommendations

## Error Handling

The API includes comprehensive error handling:

- **Timeout**: 5-minute timeout for analysis
- **Connection Errors**: Proper handling of service unavailability
- **API Errors**: Detailed error messages for debugging

## Logging

All operations are logged with appropriate levels:
- INFO: Normal operations
- ERROR: Errors and exceptions
- DEBUG: Detailed debugging information

## Security

- CORS enabled for cross-origin requests
- Input validation using Pydantic models
- Proper error handling without exposing sensitive information

# TechJam Backend API

A FastAPI-based backend service providing CRUD operations for MongoDB collections used in the TechJam project.

## 🚀 Features

- **FastAPI** - Modern, fast web framework for building APIs
- **MongoDB Integration** - Full CRUD operations for three collections
- **Automatic Logging** - All operations are automatically logged
- **CORS Support** - Cross-origin requests enabled for frontend integration
- **Comprehensive API Documentation** - Auto-generated with Swagger UI
- **Graceful Fallback** - Works in offline mode with mock data when MongoDB is unavailable
- **Data Migration** - Automatic migration of existing data to include timestamp fields

## 📊 Database Collections

### 1. PRD Collection
- **ID**: Unique UUID identifier
- **Name**: PRD name
- **Description**: PRD description
- **Status**: Current status (Draft, Active, Completed, etc.)
- **created_at**: Creation timestamp (auto-generated if missing)
- **updated_at**: Last update timestamp (auto-generated if missing)

### 2. Feature Data Collection
- **uuid**: Unique UUID identifier
- **prd_uuid**: Reference to PRD collection
- **data**: Feature data content (flexible JSON structure)
- **created_at**: Creation timestamp (auto-generated if missing)
- **updated_at**: Last update timestamp (auto-generated if missing)

### 3. Logs Collection
- **uuid**: Unique UUID identifier
- **prd_uuid**: Reference to PRD collection
- **action**: Action performed (CREATE, UPDATE, DELETE, etc.)
- **details**: Detailed description of the action
- **level**: Log level (INFO, WARNING, ERROR)
- **timestamp**: Action timestamp (auto-generated if missing)

## 🛠️ Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up MongoDB connection:**
   - The connection string is already configured in `main.py`
   - Ensure MongoDB is accessible
   - **Note**: The system will automatically fall back to mock data if MongoDB is unavailable

3. **Run the application:**
   ```bash
   python main.py
   ```

## 🌐 API Endpoints

### PRD Endpoints

| Method | Endpoint | Description | Response Type |
|--------|----------|-------------|---------------|
| `POST` | `/prd` | Create a new PRD | `PRDResponse` (201) |
| `GET` | `/prd` | Get all PRDs | `List[PRDResponse]` (200) |
| `GET` | `/prd/{prd_id}` | Get specific PRD by ID | `PRDResponse` (200) |
| `PUT` | `/prd/{prd_id}` | Update a PRD | `PRDResponse` (200) |
| `DELETE` | `/prd/{prd_id}` | Delete a PRD | `204 No Content` |

### Feature Data Endpoints

| Method | Endpoint | Description | Response Type |
|--------|----------|-------------|---------------|
| `POST` | `/feature-data` | Create feature data | `FeatureDataResponse` (201) |
| `GET` | `/feature-data` | Get all feature data | `List[FeatureDataResponse]` (200) |
| `GET` | `/feature-data/{uuid}` | Get specific feature data | `FeatureDataResponse` (200) |
| `GET` | `/feature-data/prd/{prd_uuid}` | Get by PRD reference | `List[FeatureDataResponse]` (200) |
| `PUT` | `/feature-data/{uuid}` | Update feature data | `FeatureDataResponse` (200) |
| `DELETE` | `/feature-data/{uuid}` | Delete feature data | `204 No Content` |

### Logs Endpoints

| Method | Endpoint | Description | Response Type |
|--------|----------|-------------|---------------|
| `POST` | `/logs` | Create log entry | `LogResponse` (201) |
| `GET` | `/logs` | Get all logs | `List[LogResponse]` (200) |
| `GET` | `/logs/{uuid}` | Get specific log | `LogResponse` (200) |
| `GET` | `/logs/prd/{prd_uuid}` | Get by PRD reference | `List[LogResponse]` (200) |
| `DELETE` | `/logs/{uuid}` | Delete log entry | `204 No Content` |

### Utility Endpoints

| Method | Endpoint | Description | Response Type |
|--------|----------|-------------|---------------|
| `GET` | `/health` | Health check and database status | `HealthResponse` (200) |
| `GET` | `/` | Root endpoint with API information | `RootResponse` (200) |
| `GET` | `/docs` | Interactive API documentation (Swagger UI) | HTML page |

## 📝 API Response Models

### PRDResponse
```json
{
  "ID": "uuid-string",
  "Name": "PRD Name",
  "Description": "PRD Description", 
  "Status": "Draft|Active|Completed",
  "created_at": "2025-01-27T10:30:00",
  "updated_at": "2025-01-27T10:30:00"
}
```

### FeatureDataResponse
```json
{
  "uuid": "uuid-string",
  "prd_uuid": "prd-uuid-reference",
  "data": {
    "feature_type": "authentication",
    "security_level": "high",
    "technologies": ["JWT", "bcrypt"]
  },
  "created_at": "2025-01-27T10:30:00",
  "updated_at": "2025-01-27T10:30:00"
}
```

### LogResponse
```json
{
  "uuid": "uuid-string",
  "prd_uuid": "prd-uuid-reference",
  "action": "CREATE|UPDATE|DELETE",
  "details": "Action description",
  "level": "INFO|WARNING|ERROR",
  "timestamp": "2025-01-27T10:30:00"
}
```

### HealthResponse
```json
{
  "status": "healthy",
  "database": "connected|offline",
  "mode": "production|mock_data",
  "timestamp": "2025-01-27T10:30:00",
  "collections": {
    "PRD": 5,
    "feature_data": 12,
    "logs": 25
  },
  "note": "Additional information about the system state"
}
```

## 📝 API Usage Examples

### Create a PRD
```bash
curl -X POST "http://localhost:5000/prd" \
  -H "Content-Type: application/json" \
  -d '{
    "Name": "User Authentication System",
    "Description": "Implement secure user login and registration",
    "Status": "Draft"
  }'
```

**Response (201 Created):**
```json
{
  "ID": "ae5f82ac-e164-4e5f-8b3a-123456789abc",
  "Name": "User Authentication System",
  "Description": "Implement secure user login and registration",
  "Status": "Draft",
  "created_at": "2025-01-27T10:30:00",
  "updated_at": "2025-01-27T10:30:00"
}
```

### Create Feature Data
```bash
curl -X POST "http://localhost:5000/feature-data" \
  -H "Content-Type: application/json" \
  -d '{
    "prd_uuid": "ae5f82ac-e164-4e5f-8b3a-123456789abc",
    "data": {
      "feature_type": "authentication",
      "security_level": "high",
      "technologies": ["JWT", "bcrypt"]
    }
  }'
```

**Response (201 Created):**
```json
{
  "uuid": "f8b3a123-4567-89ab-cdef-123456789abc",
  "prd_uuid": "ae5f82ac-e164-4e5f-8b3a-123456789abc",
  "data": {
    "feature_type": "authentication",
    "security_level": "high",
    "technologies": ["JWT", "bcrypt"]
  },
  "created_at": "2025-01-27T10:30:00",
  "updated_at": "2025-01-27T10:30:00"
}
```

### Get All PRDs
```bash
curl -X GET "http://localhost:5000/prd"
```

**Response (200 OK):**
```json
[
  {
    "ID": "ae5f82ac-e164-4e5f-8b3a-123456789abc",
    "Name": "User Authentication System",
    "Description": "Implement secure user login and registration",
    "Status": "Draft",
    "created_at": "2025-01-27T10:30:00",
    "updated_at": "2025-01-27T10:30:00"
  }
]
```

### Update PRD Status
```bash
curl -X PUT "http://localhost:5000/prd/ae5f82ac-e164-4e5f-8b3a-123456789abc" \
  -H "Content-Type: application/json" \
  -d '{
    "Status": "Active"
  }'
```

**Response (200 OK):**
```json
{
  "ID": "ae5f82ac-e164-4e5f-8b3a-123456789abc",
  "Name": "User Authentication System",
  "Description": "Implement secure user login and registration",
  "Status": "Active",
  "created_at": "2025-01-27T10:30:00",
  "updated_at": "2025-01-27T10:35:00"
}
```

## 🔗 Integration with Frontend and LangGraph

This backend is designed to work seamlessly with:

- **Frontend**: React application can consume these APIs for CRUD operations
- **LangGraph**: AI workflow system can store and retrieve data through these endpoints

### Frontend Integration
```javascript
// Example: Create a new PRD
const createPRD = async (prdData) => {
  const response = await fetch('http://localhost:5000/prd', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(prdData)
  });
  
  if (response.ok) {
    const result = await response.json();
    console.log('PRD created:', result);
    return result;
  } else {
    throw new Error(`Failed to create PRD: ${response.statusText}`);
  }
};

// Example: Get all PRDs
const getAllPRDs = async () => {
  const response = await fetch('http://localhost:5000/prd');
  if (response.ok) {
    const prds = await response.json();
    console.log('PRDs retrieved:', prds);
    return prds;
  } else {
    throw new Error(`Failed to retrieve PRDs: ${response.statusText}`);
  }
};
```

### LangGraph Integration
```python
# Example: Store analysis results
import requests

def store_feature_analysis(prd_uuid, analysis_data):
    response = requests.post(
        'http://localhost:5000/feature-data',
        json={
            'prd_uuid': prd_uuid,
            'data': analysis_data
        }
    )
    
    if response.status_code == 201:
        result = response.json()
        print(f"Feature data stored: {result['uuid']}")
        return result
    else:
        raise Exception(f"Failed to store feature data: {response.status_code}")
```

## 🚨 Error Handling

The API provides comprehensive error handling with proper HTTP status codes:

- **400 Bad Request**: Invalid input data or validation errors
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server-side errors
- **Validation Errors**: Automatic Pydantic validation with detailed error messages

### Error Response Format
```json
{
  "detail": "Error description message"
}
```

## 📊 Automatic Logging

Every CRUD operation automatically creates log entries:

- **CREATE**: Logs when resources are created
- **UPDATE**: Logs when resources are modified
- **DELETE**: Logs when resources are removed
- **Relationships**: Logs maintain references to PRD collections

## 🔧 Configuration

- **Port**: 5000 (configurable in main.py)
- **Host**: 0.0.0.0 (accessible from any IP)
- **CORS**: Enabled for all origins
- **MongoDB**: Connection string configured in main.py
- **Fallback Mode**: Automatic mock data when MongoDB is unavailable

## 🚀 Running the Application

1. **Start the backend:**
   ```bash
   cd backend
   python main.py
   ```

2. **Access the API:**
   - API Base URL: `http://localhost:5000`
   - Interactive Docs: `http://localhost:5000/docs`
   - Health Check: `http://localhost:5000/health`

3. **Test endpoints:**
   - Use the interactive documentation at `/docs`
   - Use curl commands for testing
   - Integrate with frontend or LangGraph systems

## 📈 Performance Features

- **MongoDB Indexes**: Optimized queries with proper indexing
- **Connection Pooling**: Efficient database connections
- **Async Operations**: FastAPI's async capabilities
- **Automatic Validation**: Pydantic model validation
- **Data Migration**: Automatic timestamp field addition

## 🔒 Security Considerations

- **Input Validation**: All inputs are validated using Pydantic models
- **Error Handling**: Sensitive error details are not exposed
- **CORS Configuration**: Configurable cross-origin access
- **MongoDB Security**: Connection string includes authentication

## 🐛 Troubleshooting

### Common Issues

1. **MongoDB Connection Failed**
   - Check MongoDB connection string
   - Verify network connectivity
   - Check authentication credentials
   - **Note**: System will automatically run in offline mode

2. **Port Already in Use**
   - Change port in main.py
   - Kill existing processes on port 5000

3. **Import Errors**
   - Install all requirements: `pip install -r requirements.txt`
   - Check Python version compatibility

4. **Response Validation Errors**
   - The system automatically adds missing timestamp fields
   - Check that all required fields are provided in requests

### Getting Help

- Check the console output for detailed error messages
- Use the `/health` endpoint to verify database connectivity
- Review MongoDB logs for connection issues
- Check the interactive API documentation at `/docs`

## 🔮 Future Enhancements

- **Authentication**: JWT-based user authentication
- **Rate Limiting**: API rate limiting and throttling
- **Caching**: Redis-based response caching
- **Monitoring**: Prometheus metrics and Grafana dashboards
- **Webhooks**: Real-time notifications for data changes
- **Batch Operations**: Bulk CRUD operations for efficiency

## 📋 System Status

The backend automatically detects and handles:

- **MongoDB Available**: Full production mode with data persistence
- **MongoDB Unavailable**: Offline mode with mock data (fully functional API)
- **Data Migration**: Automatic addition of timestamp fields to existing data
- **Error Recovery**: Graceful fallbacks for all operations

---

**Note**: This system is designed for production use with automatic fallback capabilities. All CRUD operations work identically whether connected to MongoDB or running in offline mode.

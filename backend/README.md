# TechJam Backend API

A FastAPI-based backend service providing CRUD operations for MongoDB collections used in the TechJam project.

## 🚀 Features

- **FastAPI** - Modern, fast web framework for building APIs
- **MongoDB Integration** - Full CRUD operations for three collections
- **Automatic Logging** - All operations are automatically logged
- **CORS Support** - Cross-origin requests enabled for frontend integration
- **Comprehensive API Documentation** - Auto-generated with Swagger UI

## 📊 Database Collections

### 1. PRD Collection
- **ID**: Unique UUID identifier
- **Name**: PRD name
- **Description**: PRD description
- **Status**: Current status (Draft, Active, Completed, etc.)
- **created_at**: Creation timestamp
- **updated_at**: Last update timestamp

### 2. Feature Data Collection
- **uuid**: Unique UUID identifier
- **prd_uuid**: Reference to PRD collection
- **data**: Feature data content (flexible JSON structure)
- **created_at**: Creation timestamp
- **updated_at**: Last update timestamp

### 3. Logs Collection
- **uuid**: Unique UUID identifier
- **prd_uuid**: Reference to PRD collection
- **action**: Action performed (CREATE, UPDATE, DELETE, etc.)
- **details**: Detailed description of the action
- **level**: Log level (INFO, WARNING, ERROR)
- **timestamp**: Action timestamp

## 🛠️ Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up MongoDB connection:**
   - The connection string is already configured in `main.py`
   - Ensure MongoDB is accessible

3. **Run the application:**
   ```bash
   python main.py
   ```

## 🌐 API Endpoints

### PRD Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/prd` | Create a new PRD |
| `GET` | `/prd` | Get all PRDs |
| `GET` | `/prd/{prd_id}` | Get specific PRD by ID |
| `PUT` | `/prd/{prd_id}` | Update a PRD |
| `DELETE` | `/prd/{prd_id}` | Delete a PRD |

### Feature Data Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/feature-data` | Create new feature data |
| `GET` | `/feature-data` | Get all feature data |
| `GET` | `/feature-data/{uuid}` | Get specific feature data |
| `GET` | `/feature-data/prd/{prd_uuid}` | Get feature data for specific PRD |
| `PUT` | `/feature-data/{uuid}` | Update feature data |
| `DELETE` | `/feature-data/{uuid}` | Delete feature data |

### Logs Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/logs` | Create a new log entry |
| `GET` | `/logs` | Get all logs |
| `GET` | `/logs/{uuid}` | Get specific log |
| `GET` | `/logs/prd/{prd_uuid}` | Get logs for specific PRD |
| `DELETE` | `/logs/{uuid}` | Delete a log entry |

### Utility Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check and database status |
| `GET` | `/` | Root endpoint with API information |
| `GET` | `/docs` | Interactive API documentation (Swagger UI) |

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

### Create Feature Data
```bash
curl -X POST "http://localhost:5000/feature-data" \
  -H "Content-Type: application/json" \
  -d '{
    "prd_uuid": "your-prd-uuid-here",
    "data": {
      "feature_type": "authentication",
      "security_level": "high",
      "technologies": ["JWT", "bcrypt"]
    }
  }'
```

### Get All PRDs
```bash
curl -X GET "http://localhost:5000/prd"
```

### Update PRD Status
```bash
curl -X PUT "http://localhost:5000/prd/your-prd-uuid" \
  -H "Content-Type: application/json" \
  -d '{
    "Status": "Active"
  }'
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
  return response.json();
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
    return response.json()
```

## 🚨 Error Handling

The API provides comprehensive error handling:

- **400 Bad Request**: Invalid input data
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server-side errors
- **Validation Errors**: Automatic Pydantic validation

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

2. **Port Already in Use**
   - Change port in main.py
   - Kill existing processes on port 5000

3. **Import Errors**
   - Install all requirements: `pip install -r requirements.txt`
   - Check Python version compatibility

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

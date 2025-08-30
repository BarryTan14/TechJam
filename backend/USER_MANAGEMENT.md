# User Management System

This document describes the user management system implemented in the TechJam Backend API, including secure password handling, authentication, and user CRUD operations.

## 🚀 Features

### Security Features
- **Password Hashing**: All passwords are securely hashed using bcrypt before storage
- **No Plaintext Storage**: Plaintext passwords are never stored in the database
- **Secure Verification**: Password verification uses bcrypt's secure comparison
- **Username Uniqueness**: Enforced unique usernames across the system
- **Soft Delete**: Users are deactivated rather than permanently deleted

### User Management Features
- User registration with validation
- Secure login authentication
- User profile updates
- Password changes
- User deactivation
- Comprehensive audit logging

## 🏗️ Architecture

### Database Schema
The `users` collection stores user information with the following structure:

```json
{
  "user_id": "uuid-string",
  "username": "unique-username",
  "password_hash": "bcrypt-hashed-password",
  "created_at": "timestamp",
  "updated_at": "timestamp",
  "is_active": true
}
```

### Collections
- **users**: User accounts and authentication data
- **logs**: Audit trail for all user operations

## 🔐 Password Security

### Hashing Process
1. **Input Validation**: Password must be 8-100 characters
2. **Salt Generation**: bcrypt generates a unique salt for each password
3. **Hashing**: Password + salt are hashed using bcrypt
4. **Storage**: Only the hash is stored, never the plaintext password

### Verification Process
1. **Retrieve Hash**: Get stored hash from database
2. **Compare**: Use bcrypt to verify input password against hash
3. **Result**: Return boolean indicating match/no match

### bcrypt Benefits
- **Adaptive**: Configurable work factor for future-proofing
- **Salt**: Unique salt per password prevents rainbow table attacks
- **Time-tested**: Industry standard for password hashing
- **Secure**: Resistant to brute force and timing attacks

## 📡 API Endpoints

### User Registration
```http
POST /api/users
Content-Type: application/json

{
  "username": "newuser",
  "password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
  "user_id": "uuid",
  "username": "newuser",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "is_active": true
}
```

### User Login
```http
POST /api/users/login
Content-Type: application/json

{
  "username": "newuser",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "user_id": "uuid",
  "username": "newuser",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "is_active": true
}
```

### Get All Users
```http
GET /api/users
```

**Response (200 OK):**
```json
[
  {
    "user_id": "uuid1",
    "username": "user1",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "is_active": true
  }
]
```

### Get Specific User
```http
GET /api/users/{user_id}
```

### Update User
```http
PUT /api/users/{user_id}
Content-Type: application/json

{
  "password": "newpassword123"
}
```

### Delete User (Soft Delete)
```http
DELETE /api/users/{user_id}
```

**Response (204 No Content)**

## 🛡️ Security Considerations

### Input Validation
- Username: 3-50 characters
- Password: 8-100 characters

### Authentication Flow
1. **Registration**: Username uniqueness check → Password hashing → User creation
2. **Login**: Username lookup → Password verification → Session creation
3. **Updates**: Authentication check → Validation → Secure update

### Error Handling
- **Generic Messages**: Login errors don't reveal whether username or password is wrong
- **Rate Limiting**: Consider implementing rate limiting for login attempts
- **Account Lockout**: Consider implementing account lockout after failed attempts

### Data Protection
- **Password Fields**: Never returned in API responses
- **Audit Logging**: All user operations are logged for security monitoring
- **Soft Delete**: Prevents accidental data loss while maintaining referential integrity

## 🧪 Testing

### Test Script
Run the comprehensive test script to verify all functionality:

```bash
cd TechJam/backend
python test_user_management.py
```

### Test Coverage
The test script covers:
- ✅ User creation and validation
- ✅ Duplicate username prevention
- ✅ Password hashing verification
- ✅ Login authentication
- ✅ Password change functionality
- ✅ User updates
- ✅ Soft delete operations
- ✅ Security measures

## 🔧 Configuration

### Environment Variables
```bash
# MongoDB connection
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=TechJam

# API configuration
API_HOST=0.0.0.0
API_PORT=5000
```

### Dependencies
```bash
pip install -r requirements.txt
```

Required packages:
- `fastapi`: Web framework
- `pymongo`: MongoDB driver
- `bcrypt`: Password hashing
- `python-dotenv`: Environment variable management

## 📊 Monitoring

### Health Check
The `/health` endpoint includes user collection statistics:

```json
{
  "status": "healthy",
  "database": "connected",
  "collections": {
    "PRD": 5,
    "feature_data": 25,
    "logs": 100,
    "users": 10
  }
}
```

### Audit Logs
All user operations are logged with:
- Timestamp
- Action type
- User identifier
- Operation details
- Log level

## 🚨 Error Codes

### HTTP Status Codes
- **200 OK**: Successful operation
- **201 Created**: User created successfully
- **400 Bad Request**: Validation error or duplicate username
- **401 Unauthorized**: Invalid credentials or deactivated account
- **404 Not Found**: User not found
- **500 Internal Server Error**: Server-side error

### Common Error Messages
- `"Username already exists"`: Duplicate username during registration
- `"Invalid username or password"`: Generic login failure message
- `"Account is deactivated"`: User account is soft deleted
- `"User not found"`: User ID doesn't exist

## 🔮 Future Enhancements

### Recommended Improvements
1. **JWT Tokens**: Implement JWT-based authentication
2. **Password Policies**: Enforce stronger password requirements
3. **Two-Factor Authentication**: Add 2FA support
4. **Session Management**: Implement proper session handling
5. **Role-Based Access Control**: Add user roles and permissions
6. **Password Reset**: Implement secure password reset functionality
7. **Email Verification**: Add email verification for new accounts

### Security Enhancements
1. **Rate Limiting**: Prevent brute force attacks
2. **Account Lockout**: Temporary lockout after failed attempts
3. **Password History**: Prevent password reuse
4. **Audit Alerts**: Real-time security event notifications

## 📚 References

- [bcrypt Documentation](https://github.com/pyca/bcrypt/)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [MongoDB Security Best Practices](https://docs.mongodb.com/manual/security/)

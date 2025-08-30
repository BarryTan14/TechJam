"""
MongoDB Configuration Settings
"""

# MongoDB Connection Settings
MONGO_URI = "mongodb+srv://tanedric_db_user:vZkI4o5u3VnKvThk@techjam.8cvwszr.mongodb.net/?retryWrites=true&w=majority&appName=TechJam"
DATABASE_NAME = "TechJam"
COLLECTION_NAME = "terminology"
EXECUTIVE_REPORTS_COLLECTION = "executive_reports"  # New collection for executive reports
CULTURAL_SENSITIVITY_COLLECTION = "cultural_sensitivity"  # New collection for cultural sensitivity analysis

# Alternative connection strings for different environments
# MONGO_URI = "mongodb://username:password@localhost:27017/"
# MONGO_URI = "mongodb+srv://username:password@cluster.mongodb.net/"

# Connection timeout settings (in milliseconds)
CONNECTION_TIMEOUT_MS = 5000
SERVER_SELECTION_TIMEOUT_MS = 5000

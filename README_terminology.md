# Terminology Insertion Script

This script inserts terminology terms into a MongoDB collection for the TechJam project.

## Prerequisites

1. **MongoDB Installation**: Make sure MongoDB is installed and running on your system
2. **Python Dependencies**: Install the required Python packages

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements_mongodb.txt
```

## Configuration

1. **Edit MongoDB Configuration**: Update the `mongodb_config.py` file with your MongoDB connection details:

```python
# For local MongoDB
MONGO_URI = "mongodb://localhost:27017/"

# For MongoDB with authentication
MONGO_URI = "mongodb://username:password@localhost:27017/"

# For MongoDB Atlas
MONGO_URI = "mongodb+srv://username:password@cluster.mongodb.net/"

# Database and collection names
DATABASE_NAME = "techjam"
COLLECTION_NAME = "terminology"
```

## Usage

Run the script to insert all terminology terms:

```bash
python insert_terminology.py
```

## What the Script Does

1. **Connects to MongoDB** using the configured connection string
2. **Creates the collection** if it doesn't exist
3. **Clears existing data** (optional - can be commented out)
4. **Inserts 20 terminology terms** with their descriptions
5. **Displays the results** showing all inserted terms
6. **Shows collection statistics**

## Terminology Terms Included

The script inserts the following terms:

- **NR**: Not recommended
- **PF**: Personalized feed
- **GH**: Geo-handler; a module responsible for routing features based on user region
- **CDS**: Compliance Detection System
- **DRT**: Data retention threshold; duration for which logs can be stored
- **LCP**: Local compliance policy
- **Redline**: Flag for legal review (different from its traditional business use for 'financial loss')
- **Softblock**: A user-level limitation applied silently without notifications
- **Spanner**: A synthetic name for a rule engine (not to be confused with Google Spanner)
- **ShadowMode**: Deploy feature in non-user-impact way to collect analytics only
- **T5**: Tier 5 sensitivity data; more critical than T1–T4 in this internal taxonomy
- **ASL**: Age-sensitive logic
- **Glow**: A compliance-flagging status, internally used to indicate geo-based alerts
- **NSP**: Non-shareable policy (content should not be shared externally)
- **Jellybean**: Feature name for internal parental control system
- **EchoTrace**: Log tracing mode to verify compliance routing
- **BB**: Baseline Behavior; standard user behavior used for anomaly detection
- **Snowcap**: A synthetic codename for the child safety policy framework
- **FR**: Feature rollout status
- **IMT**: Internal monitoring trigger

## Database Schema

Each document in the collection has the following structure:

```json
{
  "_id": ObjectId("..."),  // MongoDB auto-generated ID
  "term": "NR",            // The terminology abbreviation
  "description": "Not recommended"  // The full description
}
```

## Troubleshooting

### Connection Issues
- Make sure MongoDB is running
- Check the connection string in `mongodb_config.py`
- Verify network connectivity if using remote MongoDB

### Permission Issues
- Ensure the MongoDB user has write permissions to the database
- Check if authentication is required and credentials are correct

### Collection Already Exists
- The script will clear existing data by default
- Comment out the `collection.delete_many({})` line if you want to keep existing data

## Output Example

```
🚀 Terminology Insertion Script
==================================================
🔌 Connecting to MongoDB...
🧹 Clearing existing terminology data...
📝 Inserting 20 terminology terms...
✅ Successfully inserted 20 terms

📋 Inserted Terminology:
--------------------------------------------------------------------------------
ASL             Age-sensitive logic
BB              Baseline Behavior; standard user behavior used for anomaly detection
CDS             Compliance Detection System
DRT             Data retention threshold; duration for which logs can be stored
EchoTrace       Log tracing mode to verify compliance routing
FR              Feature rollout status
GH              Geo-handler; a module responsible for routing features based on user region
Glow            A compliance-flagging status, internally used to indicate geo-based alerts
IMT             Internal monitoring trigger
Jellybean       Feature name for internal parental control system
LCP             Local compliance policy
NSP             Non-shareable policy (content should not be shared externally)
NR              Not recommended
PF              Personalized feed
Redline         Flag for legal review (different from its traditional business use for 'financial loss')
ShadowMode      Deploy feature in non-user-impact way to collect analytics only
Snowcap         A synthetic codename for the child safety policy framework
Softblock       A user-level limitation applied silently without notifications
Spanner         A synthetic name for a rule engine (not to be confused with Google Spanner)
T5              Tier 5 sensitivity data; more critical than T1–T4 in this internal taxonomy

📊 Collection Statistics:
   - Total documents: 20
   - Database: techjam
   - Collection: terminology
🔌 MongoDB connection closed

🎉 Terminology insertion completed successfully!
```

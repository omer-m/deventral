from pymongo.mongo_client import MongoClient
import json

# Load configuration from config.json
with open('./config/config.json') as config_file:
    config = json.load(config_file)
    
# Retrieve MongoDB credentials and cluster information from the configuration
mongodb_user = config['mongodb']['user']
mongodb_password = config['mongodb']['password']
mongodb_cluster = config['mongodb']['cluster']

# Construct the MongoDB URI
uri = f"mongodb+srv://{mongodb_user}:{mongodb_password}@{mongodb_cluster}/?retryWrites=true&w=majority&appName=Cluster0"

# print(uri)

# Create a new client and connect to the server
client = MongoClient(uri)
db = client['dataquality_DB']
collection = db['files']


# Ping the server to test the connection
# try:
#     
#     client.admin.command('ping')
#     print("Connection to MongoDB is successful")
# except Exception as e:
#     print("Unable to connect to MongoDB", e)
# 
#  list database names to verify connection
# db_names = client.list_database_names()
# print("Databases:", db_names)

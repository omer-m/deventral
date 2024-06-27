from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://admin:Password1@cluster0.4uf5yal.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)
db = client['dataquality_DB']
collection = db['files']

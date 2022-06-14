
import pymongo
import certifi


con_str = "mongodb+srv://seth21887:24FaBaS8?@cluster0.lnvri83.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())

db = client.get_database("FoodStore")
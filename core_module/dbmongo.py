import datetime
import conf.setting as setting 
from pymongo import MongoClient
client = MongoClient(setting.mongohost)
db = client['CloudServer']
class InitDB:
    user = db['Users']

class User:
    def login(username):
        try:
            user = db['Users']
            usern = user.find_one({"user": username})
            password = usern['password'] 
        except:
            password = False
        return password
    def add(username, password, admin):
        user = db['Users']
        user.create_index("user", unique=True)
        raw = {"user": username,
                "password": password,
                "admin": admin,
                "date": datetime.datetime.utcnow()}
        print(user.insert_one(raw).inserted_id)
        return True



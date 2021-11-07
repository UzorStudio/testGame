import pymongo
from bson import ObjectId


class Offers():
    def __init__(self,classterMongo):
        self.classterMongo = classterMongo
        self.classter = pymongo.MongoClient(self.classterMongo)

    def regUser(self,name,password,type):
        db = self.classter["Shop"]
        User = db["User"]
        post = {"name":name,
                "password":password,
                "type":type,#admin, worker
                "status": "login"
                }
        User.insert_one(post)

    def getUserByNic(self,name):
        db = self.classter["Shop"]
        User = db["User"]

        return User.find_one({"name":name})

    def setUserStatus(self,name,status):
        db = self.classter["Shop"]
        User = db["User"]
        User.update_one({"name":name},{"$set":{"status":status}})


    def createOffer(self,nameBy,count,phone,address,offname):
        db = self.classter["Shop"]
        Offer = db["offer"]
        post={"nameBy":nameBy,
              "offname":offname,
              "count":count,
              "address":address,
              "phone":phone,
              "status":"none"}
        Offer.insert_one(post)

    def setOfferStatus(self,id,stat):
        db = self.classter["Shop"]
        Offer = db["offer"]

        Offer.update_one({"_id":id},{"$set":{"status":stat}})

    def all_offrers(self):
        db = self.classter["Shop"]
        Offer = db["offer"]

        cursor = Offer.find({})
        of = []
        for document in cursor:
            of.append(document)
        return of

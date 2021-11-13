import pymongo
from bson import ObjectId
import datetime

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

    def getPerformer(self):
        db = self.classter["Shop"]
        User = db["User"]

        cursor = User.find({})
        usr = []
        for document in cursor:
            if document["type"] == "performer":
                usr.append(document)
        return usr[::-1]

    def setUserStatus(self,name,status):
        db = self.classter["Shop"]
        User = db["User"]
        User.update_one({"name":name},{"$set":{"status":status}})


    def createOffer(self,nameBy,count,phone,address,offname,performer):
        db = self.classter["Shop"]
        Offer = db["offer"]
        DateBase = db["DateBase"]


        data = datetime.datetime.utcnow().date().timetuple()
        time = {"yar":data[0],
                "month":data[1],
                "day":data[2]}

        post={"nameBy":nameBy,
              "offname":offname,
              "count":count,
              "address":address,
              "phone":phone,
              "status":"none",
              "time":time,
              "performer":performer}

        Offer.insert_one(post)

        cursor = DateBase.find({})
        for document in cursor:
            if document["data"] == time:
                print("break")
                break
            else:
                print("new date add")
                DateBase.insert_one({"data":time})


    def getDB(self):
        db = self.classter["Shop"]
        DateBase = db["DateBase"]

        cursor = DateBase.find({})
        of = []
        for document in cursor:
            of.append(document)
        return of[::-1]

    def setOfferStatus(self,id,stat):
        db = self.classter["Shop"]
        Offer = db["offer"]

        Offer.update_one({"_id":ObjectId(id)},{"$set":{"status":stat}})

    def all_offrers(self):
        db = self.classter["Shop"]
        Offer = db["offer"]

        cursor = Offer.find({})
        of = []
        for document in cursor:
            of.append(document)
        return of[::-1]

    def all_offrers_by_performer(self,performer):
        db = self.classter["Shop"]
        Offer = db["offer"]

        cursor = Offer.find({})
        of = []
        for document in cursor:
            if document["performer"] == performer:
                of.append(document)
        return of[::-1]

    def get_offer_by_date(self,yaar,month,day):
        db = self.classter["Shop"]
        Offer = db["offer"]

        time = {"yar": yaar,
                "month": month,
                "day": day}

        cursor = Offer.find({})
        of = []
        for document in cursor:
            if document["time"] == time:
                of.append(document)
        return of[::-1]


    def get_offer_NOW(self,):
        db = self.classter["Shop"]
        Offer = db["offer"]

        data = datetime.datetime.utcnow().date().timetuple()
        time = {"yar": data[0],
                "month": data[1],
                "day": data[2]}

        cursor = Offer.find({"time": time})
        of = []
        for document in cursor:
            of.append(document)
        return of[::-1]
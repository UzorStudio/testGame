from flask import Flask, render_template, url_for, request, redirect, session
import base
from datetime import datetime

db = base.Offers("localhost")
app = Flask(__name__)
app.secret_key = "efwegfewrgeqrgergfhjhlyujmfgvf234234"

@app.route("/")
def index():
    return redirect("/all_offer")

@app.route("/logout")
def logout():
    try:
        db.setUserStatus(session["user"], "logout")
        session.pop("user", None)
        return redirect("/login")
    except KeyError:
        return redirect("/login")

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        print("sadasd")
        name = request.form["name"]
        password = request.form["password"]
        print(db.getUserByNic(name))
        if session == {} and db.getUserByNic(name) is None:
            print(session)
            session["user"] = name
            db.regUser(name, password, "")

            return redirect("/")
        elif db.getUserByNic(name) and session == {} and db.getUserByNic(name)["password"] == password:
            print("in")
            session["user"] = name
            db.setUserStatus(name, "login")
            return redirect("/")
        elif db.getUserByNic(name)["password"] != password:
            return "Неверный пароль"

    else:
        return render_template("login.html")

@app.route("/all_offer")
def all_offer():
    try:
        usr = db.getUserByNic(session["user"])["type"]
        off = db.all_offrers()
        print("ok")
        if usr == "admin":
            return render_template("all_offer.html",off=off)
        else:
            return "Получите нужный статус у администратора"
    except:
        return redirect("/login")

@app.route("/create_offer", methods=["POST","GET"])
def createOffer():
    if request.method == "POST":
        phone = request.form["phone"]
        count = request.form["count"]
        address = request.form["address"]
        offname = request.form["offname"]
        byname = request.form["byname"]

        db.createOffer(nameBy=byname, phone=phone, count=count, address=address, offname=offname)
        return redirect("/all_offer")
    else:
        try:
            usr = db.getUserByNic(session["user"])["type"]
            if usr == "admin":
                return render_template("create_offer.html")
            else:
                return "Получите нужный статус у администратора"
        except:
            return redirect("/login")


@app.route("/update_offer/<string:id>/<string:status>", methods=["POST","GET"])
def updateOffer(id,status):
    try:
        usr = db.getUserByNic(session["user"])["type"]
        if usr == "performer":
            db.setOfferStatus(id=id,stat=status)
        else:
            return "Получите нужный статус у администратора"
    except:
        return redirect("/login")


@app.route("/all_offer_for_performer")
def all_offer_for_performer():

    usr = db.getUserByNic(session["user"])["type"]
    off = db.all_offrers()
    print("ok")
    if usr == "performer":
        return render_template("all_offer_for_performer.html", off=off)
    else:
        return "Получите нужный статус у администратора"

if __name__ == "__main__":
    app.run(debug=True)
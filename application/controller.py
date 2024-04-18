from flask import Flask, request, redirect, url_for, session, jsonify, flash
from flask import render_template
from flask import current_app as app
from application.models import *
from application.models import Venue,Show, Ticket
from application.database import db
import requests
import os
import sqlite3



app.secret_key = "prad1705"

base_url='http://127.0.0.1:5000'

con=sqlite3.connect("ticket.db")

con.close()

app.config['UPLOAD_FOLDER']="static/images"


@app.route("/", methods=["GET", "POST"])
def user_login():
    if request.method=="GET":
        return render_template("login.html", Title="Login")
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')
        query=base_url + f'/logapi/{username}/{password}'
        response=requests.get(query)
        session ["user_deets"] = response.json()
        if response.status_code==201:
            return redirect(url_for('user_venue'))
        else:
            return redirect(url_for('user_login'))
        

@app.route("/adlogin", methods=["GET", "POST"])
def admin_login():
    if request.method=="GET":
        return render_template("adlogin.html", Title="Login")
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')
        query=base_url + f'/adapi/{username}/{password}'
        response=requests.get(query)
        session ["admin_deets"] = response.json()
        if response.status_code==201:
            return redirect(url_for('admin_venue'))
        else:
            return redirect(url_for('admin_login'))


@app.route("/uvenue", methods=["GET", "POST"])
def user_venue():
    if request.method=="GET":
        data=Venue.query.all()
        return render_template("uvenue.html", Title="Tickets Zippy", venue=data)

@app.route("/advenue", methods=["GET", "POST"])
def admin_venue():
    if request.method=="GET":
        data=Venue.query.all()
        return render_template("advenue.html", Title="Tickets Zippy", venue=data)

@app.route("/adshow/<ID>/", methods=["GET", "POST"])
def admin_show(ID):
    if request.method=="GET":
        data=Show.query.filter_by(venueID=ID).all()
        doop = ID
        if data == []:
            return  render_template("emptyShow.html", Title="Tickets Zippy", show=data, doop=doop)
        else:
            return render_template("adshow.html", Title="Tickets Zippy", show=data)
    
@app.route("/ushow/<ID>/", methods=["GET", "POST"])
def user_show(ID):
    if request.method=="GET":
        data=Show.query.filter_by(venueID=ID).all()
        return  render_template("ushow.html", Title="Tickets Zippy", show=data)
      

@app.route("/nvenue", methods=["GET", "POST"])
def add_venue():
    if request.method=="GET":
        return render_template("nvenue.html", Title="Add Venue")
    if request.method=="POST":
        upload_image=request.files['upload_image']
        if upload_image != "":
            filepath=os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
            upload_image.save(filepath)
            new_venue= Venue(img=filepath,name=request.form['venueName'], place=request.form['place'], capacity=int(request.form['capacity']), rating=int(request.form['rating']))
            print(filepath)
            db.session.add(new_venue)
            db.session.commit()
            return redirect(url_for('admin_venue'))

@app.route("/updateVenue/<int:ID>/", methods=["GET", "POST"])
def update_venue(ID):
    if request.method=="GET":
        venue = Venue.query.filter_by(ID=ID).one()
        return render_template("updateVenue.html", Title = "Update Venue", venue = venue)
    if request.method=="POST":
        venue = Venue.query.filter_by(ID=ID).one()
        if venue!=None:
            upload_image = request.files['upload_image']
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
            upload_image.save(filepath)
            if upload_image != None:
                img = filepath
                name = request.form.get('venueName')
                place=request.form.get('place')
                capacity = request.form.get('capacity')
                rating = request.form.get('rating')
                venue.img = img
                venue.name = name
                venue.place = place
                venue.capacity = capacity
                venue.rating = rating
                db.session.add(venue)
                db.session.commit()
                return redirect(url_for('admin_venue'))
            elif upload_image == "":
                name = request.form.get('venueName')
                place=request.form.get('place')
                capacity = request.form.get('capacity')
                rating = request.form.get('rating')
                venue.name = name
                venue.place = place
                venue.capacity = capacity
                venue.rating = rating
                db.session.add(venue)
                db.session.commit()
                return redirect(url_for('admin_venue'))



@app.route("/deleteVenue/<int:ID>/", methods=["GET", "POST"])
def delete_venue(ID):
    data = Venue.query.filter_by(ID=ID).one()
    if request.method == "POST":
        db.session.delete(data)
        db.session.commit()
        flash("Venue deleted successfully!", "success")
        return redirect(url_for("admin_venue"))
    return render_template("delete_venue.html", data=data)

@app.route("/deleteShow/<int:ID>/", methods=["GET", "POST"])
def delete_show(ID):
    data = Show.query.filter_by(ID=ID).one()
    if request.method == "POST":
        db.session.delete(data)
        db.session.commit()
        return redirect(url_for("admin_venue"))
    return render_template("deleteShow.html", data=data)

@app.route("/updateShow/<int:ID>/", methods=["GET", "POST"])
def update_show(ID):
    if request.method == 'GET':
        show= Show.query.filter_by(ID=ID).one()
        return render_template("updateShow.html", show=show)
    if request.method=="POST":
        show= Show.query.filter_by(ID=ID).one()
        if show!=None:
            upload_image = request.files['upload_image']
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
            upload_image.save(filepath)
            if upload_image != None:
                img = filepath
                name = request.form.get('movieName')
                tag = request.form.get('tag')
                date = request.form.get('date')
                price = request.form.get('price')
                rating =  request.form.get('rating')
                show.img = img
                show.name = name
                show.tags = tag
                show.date = date
                show.price = price
                show.rating =  rating
                db.session.add(show)
                db.session.commit()
                return redirect(url_for('admin_venue'))

     
@app.route("/nshow/<int:ID>/", methods=["GET", "POST"])
def add_show(ID):
    if request.method=="GET":
        return render_template("nshow.html", title="add show")
    if request.method=="POST":
        venue= Venue.query.filter_by(ID=ID).one()
        upload_image=request.files['upload_image']
        if upload_image != "":
            filepath=os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
            upload_image.save(filepath)
            new_show= Show(img=filepath,name=request.form['movieName'], tags=request.form['tag'], date=request.form['date'],ticket=int(request.form['price']), rating=int(request.form['rating']),tickets_booked = 0, tickets_available = venue.capacity, venueID=ID)
            db.session.add(new_show)
            db.session.commit()
            return  redirect(url_for("admin_venue"))

@app.route("/Search", methods = ["POST"])
def search():
    query= request.form.get('searched')
    venues = Venue.query.filter(Venue.name.like(f'%{query}%')).all()
    shows=Show.query.filter(Show.name.like(f'%{query}%')).all()
    places = Venue.query.filter(Venue.place.like(f'%{query}%')).all()
    return render_template("Search.html", venues=venues, shows=shows, places=places)

@app.route("/adSearch", methods = ["POST"])
def admin_search():
    query= request.form.get('searched')
    venues = Venue.query.filter(Venue.name.like(f'%{query}%')).all()
    shows=Show.query.filter(Show.name.like(f'%{query}%')).all()
    places = Venue.query.filter(Venue.place.like(f'%{query}%')).all()
    return render_template("adminSearch.html", venues=venues, shows=shows, places=places)

@app.route("/bookTicket/<int:ID>/<int:venueID>/", methods=["GET", "POST"])
def book_ticket(ID, venueID):
    if request.method == 'GET':
        show= Show.query.filter_by(ID=ID).one()
        if show.tickets_available > 0:
            return render_template("bookshow.html", show=show)
        return render_template('housefull.html')
    if request.method == "POST":
        show= Show.query.filter_by(ID=ID).one()
        venue= Venue.query.filter_by(ID=venueID).one()
        tickets= request.form.get('ticket')
        seat = int(tickets)
        if seat > show.tickets_available:
            return render_template('housefull.html')
        show.tickets_booked += int(tickets)
        show.tickets_available = int(show.tickets_available) - int(tickets) 
        user_ticket = Ticket(username = session["user_deets"]["UserName"], venuename = venue.name, showname = show.name, date = show.date, seats = int(tickets),price = (int(tickets))*(int(show.ticket))) 
        db.session.add(user_ticket)
        db.session.add(show)
        db.session.commit()
        return render_template('confirmation.html')
    


@app.route("/uprofile", methods=["GET", "POST"])
def user_profile():
    if request.method=="GET":
        return render_template("uprofile.html", Title="Tickets Zippy")

@app.route("/viewticket", methods=["GET","POST"])
def view_ticket():
    if request.method == "GET":
        data = Ticket.query.filter_by(username = session["user_deets"]["UserName"]).all()
        print(data)
        if data == []:
            return render_template("Noticket.html", user=data)
        return render_template("viewTicket.html", user = data)

@app.route("/logout", methods={"GET"})
def logout():
    if request.method == "GET":
        session.clear()
        return redirect(url_for('user_login'))    

@app.route("/register", methods=["GET", "POST"])
def Signin():
    if request.method=="GET":
        return render_template("signin.html", title="Sign In")
    if request.method=="POST":
        new_user = User(UserName= request.form['username'], Email=request.form['email'], Password=request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('user_login'))




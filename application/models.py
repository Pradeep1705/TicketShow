from .database import db


class User(db.Model):
    __tablename__='User'
    UserName = db.Column(db.String)
    Email=db.Column(db.String, unique=True, primary_key=True)
    Password=db.Column(db.String)

class Admin(db.Model):
    __tablename__='Admin'
    UserName = db.Column(db.String)
    Email=db.Column(db.String, unique=True, primary_key=True)
    Password=db.Column(db.String)


class Venue(db.Model):
    __tablename__='Venue'
    ID=db.Column(db.Integer, primary_key=True, autoincrement=True)
    img=db.Column(db.String)
    name=db.Column(db.String)
    place=db.Column(db.String)
    capacity=db.Column(db.Integer)
    rating=db.Column(db.Integer)
    show=db.relationship("Show")
    
class Show(db.Model):
    __tablename__='Show'
    ID=db.Column(db.Integer , primary_key=True, autoincrement=True)
    img=db.Column(db.String)
    name=db.Column(db.String)
    tags=db.Column(db.String)
    date=db.Column(db.String)
    ticket=db.Column(db.Integer)
    rating=db.Column(db.Integer)
    tickets_booked = db.Column(db.Integer)
    tickets_available = db.Column(db.Integer)
    venue = db.relationship(Venue, backref=db.backref('shows', lazy=True))
    venueID=db.Column(db.Integer, db.ForeignKey("Venue.ID"))
    
    

class Ticket(db.Model):
    __tablename__='Ticket'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    venuename = db.Column(db.String)
    showname = db.Column(db.String)
    date = db.Column(db.String)
    seats = db.Column(db.Integer)
    price = db.Column(db.Integer)
    

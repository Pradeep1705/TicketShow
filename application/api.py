from flask_restful import Resource, marshal_with, fields
import json
from application.models import *

user_deets={"UserName":fields.String, "Email":fields.String, "Password": fields.String}
admin_deets={"UserName":fields.String, "Email":fields.String, "Password": fields.String}

class log_API(Resource):
    @marshal_with(user_deets)
    def get(self,username,password):
        person=db.session.query(User).filter((User.UserName==username) & (User.Password==password)).first()
        if person!= None:
            return person, 201
        else:
            return "", 404
        
class ad_API(Resource):
    @marshal_with(admin_deets)
    def get(self,username,password):
        person=db.session.query(Admin).filter((Admin.UserName==username) & (Admin.Password==password)).first()
        print(person)
        if person!= None:
            return person, 201
        else:
            return "", 404


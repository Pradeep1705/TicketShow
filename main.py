import os
from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_restful import Api


app=None

def create_app():
    app= Flask(__name__, template_folder="templates")
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    api=Api(app)
    app.app_context().push()
    return app , api



app,api=create_app()

from application.controller import *
from application.api import *

api.add_resource(log_API,'/logapi/<string:username>/<string:password>')
api.add_resource(ad_API,'/adapi/<string:username>/<string:password>')
    

if __name__ == '__main__':
    app.run()
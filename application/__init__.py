from flask import Flask
from flask_restful import Api
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.config.from_object(Config)

from auth import routes, models


api.add_resource(routes.UserApiHandler, '/user/create', endpoint='create')
api.add_resource(routes.UserApiHandler, '/user/update/<int:user_id>', endpoint='update')
api.add_resource(routes.UserApiLogin, '/user/login', endpoint='login')

from blog import routes, models


api.add_resource(routes.ArticlText, '/text/created', endpoint='created')
api.add_resource(routes.ArticlText, '/text/<int:user>', endpoint='user')
from flask_restful import Resource
from flask import request
from .models import Articl
from .helpers import validate_title
from application.helpers import databases_conection
from auth.exceptions import ValidationError
import json
from application import app
from auth.models import User, Session
from .helpers import token_validation
from functools import wraps


class ArticlText(Resource):
    @databases_conection
    @token_validation
    def post(self, *args, **kwargs):
        
        session = kwargs['session']
        current_user = kwargs['current_user']

        data = request.get_json()

        try:
            text = Articl(
                text=data['text'],
                title=validate_title(data['title']),
                user=current_user.id
            )

        except ValidationError:
            return {'status': 'Failed'}, 500
        session.add(text)
        session.commit()

        return {'status': 'success'}, 201


    @databases_conection
    @token_validation
    def get(self, user, *args, **kwargs):

        session = kwargs['session']
        current_user = kwargs['current_user']

        if session.query(Articl).get(user):

            articls = session.query(Articl).filter(Articl.user == user).all()

            if not articls:
                return {'message' : 'No found articls'}, 401

            output = []

            for articl in articls:
                articl_user = {}
                articl_user['id'] = articl.id
                articl_user['title'] = articl.title
                articl_user['text'] = articl.text
                articl_user['user'] = articl.user
                output.append(articl_user)


            return {'articls': output}



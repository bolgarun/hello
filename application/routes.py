from flask_restful import Resource
from flask import request
from application.models import User, Session
from application import db
from sqlalchemy.orm import sessionmaker
from application.helpers import databases_conection, validate_email, validate_password, hash_password, check_if_letter, validate_age, validate_gender, validate_country, validate_nickname, verify_password
from application.exceptions import ValidationError
from .helpers import sg
from .constants import message
import json
import jwt
import datetime
from application import app


class UserApiHandler(Resource):
    @databases_conection
    def post(self, **kwargs):

        session = kwargs['session']

        data = request.get_json()

        email = validate_email(data['email'])

        if session.query(User).filter(User.email==email).first():
            return {'status': 'Failed'}, 500

        if session.query(User).filter(User.nickname==validate_nickname(data['nickname'])).first():
            return {'status': 'Failed'}, 500

        try:
            fake_user = User(
                nickname=validate_nickname(data['nickname']),
                first_name=check_if_letter(data['first_name']),
                last_name=check_if_letter(data['last_name']), 
                email=email, 
                password_hash=hash_password(validate_password(data['password_hash'])),
                age=validate_age(data['age']),
                gender=validate_gender(data['gender']),
                country=validate_country(data['country'])
            )
        except ValidationError:
            return {'status': 'Failed'}, 500

        except KeyError:
            return {'status': 'Failed'}, 500

        session.add(fake_user)
        session.commit()
        sg.send(json.loads(message % (email, 't')))

        return {'status': 'success'}, 201
        
    @databases_conection
    def put(self, user_id, **kwargs):

        session = kwargs['session']

        if request.args.get('action') == 'approve':

            if session.query(User).get(user_id):


                session.query(User).filter(User.id == user_id).\
                update({"active" : True})
                session.commit()

                return {'status': 'success'}, 201

        return {'status': 'failed'}, 400

class UserApiLogin(Resource):
    @databases_conection
    def post(self, **kwargs):

        session = kwargs['session']

        data = request.get_json()

        password = data['password_hash']
        nickname = data['nickname']

        user_check = session.query(User).filter(User.nickname==nickname).first()

        if not user_check:
            return {'status': 'failed'}, 400

        check_password = verify_password(user_check.password_hash, password)

        payload = {
            'user_id' : user_check.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=60),
        }


        if nickname == user_check.nickname and check_password == True:
            token = jwt.encode(payload, app.config.get('SECRET_KEY'))

            new_token = Session(
                    user_id=user_check.id,
                    session_token=token)
            session.add(new_token)
            session.commit()
            return {'token': token.decode('UTF-8')}, 201

        return {'status': 'failed'}, 400

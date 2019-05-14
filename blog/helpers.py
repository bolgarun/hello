from auth.exceptions import ValidationError
import json
import jwt
from flask import request
from auth.helpers import sg
from auth.models import User, Session
from .models import Articl
from application import app
from functools import wraps
import datetime


def validate_title(title):
    for x in title:
        if x[0].isupper() and x.isalpha():
            return title
        raise ValidationError("Enter valid titel") 

def token_validation(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        session = kwargs['session']

        if 'access-token' in request.headers:
            token = request.headers['access-token']

        if not token:
            return {'messege': 'token is missing'}, 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['user_id']).first()
            time = data['exp']
            if data['exp'] <= 0:
                return {'messege': 'refresh token'}
            kwargs['current_user'] = current_user
        except:
            return {'messege': 'token faild'}

        return f(*args, **kwargs)

    return decorator
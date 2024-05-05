import jwt
import datetime
# from dotenv import load_dotenv
from jwt.api_jwt import PyJWT
import main
from functools import wraps
from flask import app, request, jsonify
from datetime import datetime, timedelta
from resources.payload.payload import Localtime


# Use JWT for auth and routes protection
# Three functions are needed : Sign Tokens, Verify Tokens and Refresh Tokens
from flask_jwt_extended import (create_access_token,
                                create_refresh_token, jwt_required, get_jwt_identity)

# Function to sign Tokens


def sign_token(details):
    # payload to use as we sign the token

    jwt_OBJ = PyJWT()
    try:
        payload = {
            # # 'iat': datetime.datetime.now(),
            # 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            '_id': details['user_id'],
            '_type': details['user_type']
        }

        # Sign the Payload with the Key and hashing alorithm
        # token = jwt.encode(
        #     payload=payload, key=main.app.config["SECRET_KEY"]).decode("utf-8")

        # jwt_extended
        access_token = create_access_token(identity=payload)
        # print(access_token)
        refresh_token = create_refresh_token(identity=payload)
        # print("Refresh", access_token)

        return access_token, refresh_token
    except Exception as e:
        # print(str(e))
        return jsonify(str(e)), 500


def verify_token(token):
    # decode the token passed and check if ithas expired or is inavlid
    try:
        jwt_OBJ = PyJWT()
        payload = jwt_OBJ.decode(token, key=main.app.config["SECRET_KEY"])
        return payload
    except jwt.ExpiredSignatureError as e:
        return False
    except jwt.InvalidTokenError as e:
        return False


def sign_permissions(token):
    jwt_OBJ = PyJWT()
    try:
        
        start_date = Localtime().gettime()   
        now = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S') 
                
        payload = {
            'iat': now,
            'exp': now + timedelta(minutes=180),
            '_id': token
        }

        # Sign the Payload with the Key and hashing alorithm
        token = jwt.encode(
            payload=payload, key=main.app.config["SECRET_KEY"]).decode("utf-8")
        return token
    except Exception as e:
        return jsonify(str(e)), 500


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace('Bearer ', '')
        if not token:
            return jsonify({
                'message': "No authentication token!"
            }), 402

        try:
            data = jwt.decode(token, main.app.config['SECRET_KEY'])

            cur = main.mysql.get_db().cursor()
            cur.execute(
                """SELECT id, username, user_type FROM users WHERE id = %s""", data['_id'])
            user = cur.fetchone()
            cur.close()

        except:
            return jsonify({
                'message': "Invalid token!"
            }), 402

        return f(user, *args, **kwargs)
    return decorated

def refresh_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)

    return access_token
import jwt
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework.response import Response

secret = settings.TOKEN_SECRET_KEY
algorithm = "HS512"


def encode_token(username, action):
    token = jwt.encode(
        {
            "username":username,
            "scope":action
        },
        key=secret,
        algorithm=algorithm
    )
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, key=secret, algorithms=algorithm)
        if payload['scope'] == "email_verify":
            return payload['username'], True
        if payload['scope'] == "password_reset":
            return payload['username'], True
        return None, False
    except jwt.ExpiredSignatureError:
        return None, False
    return None, False
        

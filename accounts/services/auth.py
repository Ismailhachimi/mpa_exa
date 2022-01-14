import datetime
import jwt
from django.conf import settings
from accounts.models import User


def generate_access_token(user: User):
    """Generate access token for 1 hour"""
    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=2, minutes=0),
        'iat': datetime.datetime.utcnow(),
        'groups': list(user.groups.values_list('name', flat=True))
    }
    access_token = jwt.encode(
        access_token_payload,
        settings.GET_TOKEN_SECRET,
        algorithm='HS256'
    )
    return access_token


def generate_refresh_token(user):
    """Generate refresh token for 3 day"""
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=3),
        'iat': datetime.datetime.utcnow(),
        'groups': list(user.groups.values_list('name', flat=True))
    }
    refresh_token = jwt.encode(
        refresh_token_payload,
        settings.REFRESH_TOKEN_SECRET,
        algorithm='HS256'
    )

    return refresh_token

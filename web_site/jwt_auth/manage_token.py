import uuid
import jwt
import datetime
from constance import config

from rest_framework.exceptions import AuthenticationFailed

from .models import RefreshToken


def _get_expiration_date(exp_time, days=False):
    '''
        By default, the delta is calculated in seconds
    '''
    if days:
        return datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=exp_time)
    return datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=exp_time)


def decode_token(token):
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        token = token.split()[1]
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])

    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Invalid token!')
    return payload


def create_access_token(user):
    payload = {
        'id': user.id,
        'exp': _get_expiration_date(config.ACCESS_TOKEN_EXPIRATION_TIME),
        'iat': datetime.datetime.now(datetime.UTC)
    }
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    return token


def get_access_by_refresh(refresh_token):
    jwt_refresh_token = RefreshToken.objects.filter(
        token=refresh_token
    ).first()
    if not jwt_refresh_token:
        raise AuthenticationFailed('Unauthenticated!')
    if jwt_refresh_token.expiration_date < datetime.datetime.now(datetime.UTC):
        clear_refresh_token(
            jwt_refresh_token.token
        )
        raise AuthenticationFailed('Refresh token has expired')

    exp_date = _get_expiration_date(config.REFRESH_TOKEN_EXPIRATION_TIME, days=True)
    jwt_refresh_token.expiration_date = exp_date
    jwt_refresh_token.save()

    user = jwt_refresh_token.user

    return create_access_token(user)


def create_refresh_token(user):
    exp_date = _get_expiration_date(config.REFRESH_TOKEN_EXPIRATION_TIME, days=True)
    token = str(uuid.uuid4())
    RefreshToken.objects.create(
        user=user,
        token=token,
        expiration_date=exp_date,
    )
    return token


def clear_refresh_token(token):
    RefreshToken.objects.filter(
        token=token
    ).delete()

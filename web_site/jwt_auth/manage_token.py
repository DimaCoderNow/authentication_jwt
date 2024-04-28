import uuid
import jwt
import datetime

from rest_framework.exceptions import AuthenticationFailed

from .models import RefreshToken


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
        'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=300),
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
    user = jwt_refresh_token.user
    return create_access_token(user)


def create_refresh_token(user):
    expiration_date = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=30)
    token = str(uuid.uuid4())
    RefreshToken.objects.create(
        user=user,
        token=token,
        expiration_date=expiration_date,
    )
    return token


def clear_refresh_token(token):
    RefreshToken.objects.filter(
        token=token
    ).delete()

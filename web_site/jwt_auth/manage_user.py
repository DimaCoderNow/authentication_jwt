from rest_framework.exceptions import AuthenticationFailed

from .manage_token import decode_token
from .models import User


def get_user_by_email(email, password):
    user = User.objects.filter(email=email).first()
    if user is None:
        raise AuthenticationFailed('User not found!')

    if not user.check_password(password):
        raise AuthenticationFailed('Incorrect password!')
    return user


def get_user_by_access_token(token):
    payload = decode_token(token)
    user_id = payload.get('id')
    if user_id is None:
        raise AuthenticationFailed('User ID not found in token!')

    user = User.objects.filter(id=user_id).first()
    if user is None:
        raise AuthenticationFailed('User not found!')
    return user

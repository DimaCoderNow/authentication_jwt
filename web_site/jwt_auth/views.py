import jwt
from rest_framework.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, UserReadWriteSerializer

from .manage_token import *
from .manage_user import *


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = get_user_by_email(email, password)

        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)

        return Response(
            {'access_token': access_token,
             'refresh_token': refresh_token},
        )


class UserView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization')
        user = get_user_by_access_token(token)
        serializer = UserReadWriteSerializer(user)

        return Response(serializer.data)

    def put(self, request):
        token = request.headers.get('Authorization')
        user = get_user_by_access_token(token)
        serializer = UserReadWriteSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        raise ValidationError('Value was invalid')


class RefreshView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        access_token = get_access_by_refresh(refresh_token)
        return Response(
            {'access_token': access_token,
             'refresh_token': refresh_token},
        )


class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        clear_refresh_token(refresh_token)
        return Response(
            {"success": "User logged out."}
        )

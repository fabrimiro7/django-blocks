import re

from django.contrib.auth import logout
from rest_framework import exceptions
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from edplatform.specific import REMOTE_API
from .authentication import create_access_token, JWTAuthentication, create_refresh_token, decode_refresh_token
from .serializers import *


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            email = request.data.get('email', '')
            if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
                pass
            else:
                user = serializer.save()
                user_data = serializer.data

                return Response({
                    "user": user_data,
                    "message": "success",
                    "id_user": user.id,
                }, status=status.HTTP_200_OK)
        return Response({
            "user": "",
            "message": "fail",
        }, status=status.HTTP_200_OK)


class LoginUserView(CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed('Invalid credentials')

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Invalid credentials')

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        response = Response()
        response.set_cookie(key='refresh_token_dj', value=refresh_token, httponly=False)
        response.data = {
            'token': access_token,
            'refresh_token': refresh_token,
            'message': "success",
        }
        return response



class RefreshAPIView(APIView):
    
    def post(self, request):
        if (request.data['reftok'] == None or request.data['reftok'] == '' or request.data['reftok'] == "undefined"):
            request.COOKIES.get('refresh_token_dj')
        else:
            refresh_token = request.data['reftok']
        id = decode_refresh_token(refresh_token)
        user = User.objects.get(pk=id)
        access_token = create_access_token(id)
        return Response({
            'token': access_token
        })


class RequestResetPasswordMail(APIView):
    serializer_class = RequestResetPWMail

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            "message": "success",
        }, status=status.HTTP_200_OK)



class ResetPassword(APIView):
    serializer_class = RequestResetPW

    def post(self, request, id, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = request.data.get('password', '')
        password_confirm = request.data.get('password_confirm', '')
        user = User.objects.get(pk=id)
        token = token.replace("_", "-")

        if not PasswordResetTokenGenerator().check_token(user=user, token=token):
            raise AuthenticationFailed('Token Consumato', 401)
        if not password == password_confirm:
            raise AuthenticationFailed('Password diverse', 401)
        user.set_password(password)
        user.save()

        return Response({
            "message": "success",
        }, status=status.HTTP_200_OK)


class Logout(CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        response = Response()
        response.delete_cookie(key="refresh_token")
        logout(request)
        return Response({"message": "success"}, status=status.HTTP_200_OK)


class UserDetail(APIView):
    serializer_class = UserDetailSerializer
    if REMOTE_API == True:
        authentication_classes = [JWTAuthentication]

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            if user:
                serializer = UserDetailSerializerGet(user)
                return Response({"data": serializer.data, "message": "success"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            user = None
            return Response({"data": "", "message": "fail3"}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except Exception:
            user = None
        if user:
            serializer = UserDetailSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"data": serializer.data, "message": "success"}, status=status.HTTP_200_OK)
            return Response({"data": serializer.data, "message": "fail"}, status=status.HTTP_200_OK)
        return Response({"data": "", "message": "fail"}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            user = None

        if user:
            user.delete()
            return Response({"message": "success"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "fail"}, status=status.HTTP_404_NOT_FOUND)

class GetMembersAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    queryset = User.objects.all()
    serializer_class = GetMembersSerializer

    def get(self, request):
        members = User.objects.all()
        serializer = GetMembersSerializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetUserAPIView(APIView):
    """
    API view to retrieve a list of users.

    This view requires JWT authentication and returns a list of users
    serialized using the UserDetailSerializerGet.
    """
    serializer_class = UserDetailSerializerGet  # Serializer to use for response
    
    authentication_classes = [JWTAuthentication]  # Authentication classes to use
    
    def get(self, request):
        """
        Retrieve a list of all users.

        Returns serialized user data as a response with HTTP 200 OK status.
        """
        users = User.objects.all()  # Retrieve all users from the database
        serializer = UserDetailSerializerGet(users, many=True)  # Serialize user data
        
        return Response(serializer.data, status=status.HTTP_200_OK)  # Return serialized data


class UserView(CreateAPIView):
    serializer_class = RegisterSerializer
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            email = request.data.get('email', '')
            if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
                pass
            else:
                user = serializer.save()
                user_data = serializer.data

                return Response({
                    "user": user_data,
                    "message": "success",
                    "id_user": user.id,
                }, status=status.HTTP_200_OK)
        return Response({
            "user": "",
            "message": "fail",
        }, status=status.HTTP_200_OK)
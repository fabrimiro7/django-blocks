from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from core_modules.user_manager.utils.mail_utils import *
from .models import User



# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'first_name', 'last_name', 'phone', 'user_type')

    def validate(self, attrs):
        email = attrs.get('email', '')
        first_name = attrs.get('first_name', '')
        last_name = attrs.get('last_name', '')
        phone = attrs.get('phone', '')
        username = attrs.get('username', '')
        user_type = attrs.get('user_type', '')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=250, min_length=3)
    password = serializers.CharField(max_length=255, min_length=4, write_only=True)
    tokens = serializers.CharField(max_length=255, min_length=4, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)
        if not user:
            return {'id_user': "", 'permission': "", 'email': "", 'tokens': ""}

        return {
            'id_user': user.id,
            'permission': user.permission,
            'email': user.email,
            'tokens': user.tokens
        }


class RequestResetPWMail(serializers.ModelSerializer):
    email = serializers.CharField(max_length=250, min_length=3)

    class Meta:
        model = User
        fields = ['email']

    def validate(self, attrs):
        try:
            email = attrs.get('email', '')
            if User.objects.get(email=email):
                user = User.objects.get(email=email)
                token = PasswordResetTokenGenerator().make_token(user)
                token = token.replace("-", "_")
                link_to_reset_pwd = reverse_lazy(
                    'reset_pwd', kwargs={'id': user.id, 'token': token})
                link_to_reset_pwd = link_to_reset_pwd.replace("api/", "")
                destinatario = email
                if settings.EMAIL_HOST_USER:
                    mittente = settings.EMAIL_HOST_USER
                else:
                    mittente = "gruppoefesto@gmail.com"
                #oggetto = "Reset Password Djangular"
                #corpo = "Bella zio; Eccoti la password nuova http://gestionale.efestodev.it{}".format(link_to_reset_pwd)
                #utils.send_mail(destinatario=destinatario, mittente=mittente, oggetto=oggetto, corpo=corpo)
                # send email to requester
                return {
                    'sending': "success",
                }
            else:
                # fake the sending
                return {
                    'sending': "failed",
                }
        except User.MultipleObjectsReturned:
            # send email to administration for duplicated Email
            return {
                'sending': "failed",
            }

        except Exception as E:
            print("Errore incredibile alla richiesta del reset password per {}. Errore:{}".format(email, E))
        return {
            'sending': "failed",
        }


class RequestResetPW(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, min_length=4, write_only=True)
    password_confirm = serializers.CharField(max_length=255, min_length=4, write_only=True)
    # token = serializers.CharField(min_length=1, write_only=True)
    # id = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = ['password', 'password_confirm']


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'fiscal_code', 'phone', 'mobile', 'permission']

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

class UserDetailSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'fiscal_code', 'phone', 'mobile', 'permission']


class GetMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']

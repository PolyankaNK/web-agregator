from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        min_length=8,
        error_messages={"min_length": "Пароль має містити мінімум 8 символів"}
    )
    password2 = serializers.CharField(
        write_only=True,
        error_messages={"required": "Повторіть пароль"}
    )
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(
        required=True,
        error_messages={"required": "Введіть ім’я"}
    )
    last_name = serializers.CharField(
        required=True,
        error_messages={"required": "Введіть прізвище"}
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password", "password2")  

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Користувач з такою поштою вже існує")
        return value
    
    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({
                "password": "Паролі не співпадають"
            })
        return data

    def create(self, validated_data):

        validated_data.pop("password2") 
        
        base_username = f"{validated_data['first_name']}.{validated_data['last_name']}".lower()
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        return user
    
class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):

        email = data.get("email")
        password = data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Користувача з таким email не існує")

        user = authenticate(username=user.username, password=password)

        if not user:
            raise serializers.ValidationError("Невірний пароль")

        data["user"] = user
        return data

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import UserModel


# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField()


class AuthTokenSerializer(serializers.Serializer):
    """
    A user model át lett írva, hogy nem a UserName az alapértelmezett hanem az email cím, ezért
    az token-es autentikációt is át kellett írni. Ezt a serializer a token-es autentikációhoz van
    """
    email = serializers.EmailField(label="Email")
    password = serializers.CharField(
        label="Password",
        style={"input-type": "password"},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            """
            Ha az email cím és a jelszó valid, a django authenticate-t használva ellenőriztetjük a user-t,
            úgy hogy a username megkapja az email-t
            """
            user = authenticate(request=self.context.get(
                "request"), username=email, password=password)
            """
            Ha nem létezik a user akkor hiba
            """
            if not user:
                msg = "Ismeretlen email cím vagy jelszó"
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = 'Az "email" és "password" mezők kitöltése kötelező.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"
        #!
        extra_kwargs = {"password": {"write_only": True, "min_length": 6}}

    def create(self, validated_data):
        """Új felhasználó létrehozásához"""
        user = UserModel.objects.create_user(
            email=validated_data["email"],
            name=validated_data["name"],
            password=validated_data["password"],
            permission=validated_data["permission"]
        )
        user.save()

        return user

    def update(self, instance, validated_data):
        """Felhasználó adatainak módosításához"""
        instance.email = validated_data.get("email", instance.email)
        instance.name = validated_data.get("name", instance.name)
        instance.permission = validated_data.get(
            "permission", instance.permission)

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            
        instance.save()
        return instance

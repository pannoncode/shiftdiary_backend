from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import Http404


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication

from .serializers import AuthTokenSerializer, UserSerializer

from .models import UserModel


class AuthTokenView(ObtainAuthToken):
    """
    A user model át lett írva, hogy nem a UserName az alapértelmezett hanem az email cím, ezért
    az token-es autentikációt is át kellett írni
    """
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        Token.objects.filter(user=user).delete()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user_name": user.name,
            "permission": user.permission,
            "user_id": user.id
        })


class NewUserView(APIView):
    """
    Új felhasználó hozzzáadása, törlése, szerkesztése és felhasználók lekérdezéséhez
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        """Felhasználó pk alapján"""
        try:
            return UserModel.objects.get(pk=pk)
        except UserModel.DoesNotExist:
            raise Http404

    def get(self, request):
        users = UserModel.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Felhasználó létrehozása"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Sikeres felhasználó létrehozás"}, status=status.HTTP_200_OK)
        return Response({"message": "Sikertelen felhasználó létrehozás!"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """Felhasználó törlése"""
        selected_user = UserModel.objects.get(pk=pk)
        selected_user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk, format=None):
        """Felhasználói adatok szerkesztése"""
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Sikeres szerkesztés!"}, status=status.HTTP_200_OK)
        return Response({"message": "Sikertelen szerkesztés!"}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        user = request.user
        return Response(
            {
                "id": user.pk,
                "name": user.name,
                "email": user.email,
                "permission": user.permission
            }
        )

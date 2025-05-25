from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import *
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from api.docs import signupdocs, logindocs, logoutdocs


class SignUpView(APIView):
    """
    Register a new user.
    """

    @signupdocs
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({"access token": str(refresh.access_token),"user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    """
    Authenticate user and return JWT tokens.
    """

    @logindocs
    def post(self, request):
        data = request.data
        identifier = data.get('username')
        password = data.get('password')
        if not identifier or not password:
            return Response({"error":"username/email or password missing."}, status.HTTP_400_BAD_REQUEST)
        try:
            user = get_user_model().objects.get(username=identifier)
        except get_user_model().DoesNotExist:
            try:
               user = get_user_model().objects.get(email=identifier)
            except get_user_model().DoesNotExist:
                return Response({"error":"Invalid username/email or password."}, status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=user.username, password=password)
        if not user:
            return Response({"error":"Invalid username/email or password."}, status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        return Response({"refresh token": str(refresh), "access_token": str(refresh.access_token), "user":{"email":user.email, "username":user.username}})


class LogoutView(APIView):

    """
    Log out user by blacklisting refresh token.
    """

    @logoutdocs
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"error": "refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"success": "token successfully blacklisted"}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "invalid or expired token"}, status=status.HTTP_404_NOT_FOUND)
            
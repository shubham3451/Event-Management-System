from drf_yasg.utils import swagger_auto_schema
from drf_yasg import  openapi




signupdocs = swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username", "email", "password"],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Unique username', example='johndoe'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='Valid email address', example='johndoe@example.com'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password', example='StrongPassword123')
            },
        ),
        responses={201: "User created with tokens", 400: "Validation errors"},
        operation_description="Register a new user with username, email, and password.",
        tags=["Authentication"]
    )
   

logindocs =  swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username", "password"],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username or email', example='johndoe'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password', example='StrongPassword123')
            }
        ),
        responses={200: "Tokens and user info", 400: "Invalid credentials"},
        operation_description="Authenticate with username/email and password to receive JWT tokens.",
        tags=["Authentication"]
    )
     
    

logoutdocs = swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["refresh"],
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token to blacklist', example='your-refresh-token')
            }
        ),
        responses={200: "Token blacklisted", 400: "Missing token", 404: "Invalid/expired token"},
        operation_description="Invalidate a JWT refresh token by blacklisting it.",
        tags=["Authentication"]
    )
   
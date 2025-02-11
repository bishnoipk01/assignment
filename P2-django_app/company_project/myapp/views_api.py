from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Company, User
from .serializers import CompanySerializer, UserSerializer, UserRegistrationSerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import CustomAuthTokenSerializer

class CustomObtainAuthToken(ObtainAuthToken):
    # Set the serializer class to our custom serializer that accepts email and password.
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        # Initialize the serializer with the request data and the current request context.
        serializer = self.serializer_class(data=request.data, context={'request': request})
        # Validate the data. If validation fails, an error response is automatically returned.
        serializer.is_valid(raise_exception=True)
        # Retrieve the authenticated user from the serializer's validated data.
        user = serializer.validated_data['user']
        # Get or create a token for the authenticated user.
        token, created = Token.objects.get_or_create(user=user)
        # Return the token in the response.
        return Response({'token': token.key})


# List and create view for companies:
class CompanyListCreateAPI(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # Allow all authenticated users to view, but only admins can create
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

# Retrieve, update, or destroy view for a specific company:
class CompanyRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # Allow all authenticated users to view, but only admins can modify or delete
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


# API view to list all users and create a new user
class UserListCreateAPI(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # All authenticated users can list users

    def get_permissions(self):
        # For POST requests, require admin permission.
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

# API view to retrieve, update, or delete a user instance
class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]



class UserRegistrationAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  # Allows unauthenticated users to register
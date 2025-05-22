from rest_framework import generics, permissions, response, views
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserRegistrationSerializer, UserDetailSerializer
from .models import User

class UserRegistrationView(generics.CreateAPIView):
    """
    Allows new users to register.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class UserLoginView(TokenObtainPairView):
    """
    Allows users to log in and obtain JWT tokens.
    Uses SimpleJWT's TokenObtainPairView.
    A custom serializer (TokenObtainPairSerializer) can be defined if needed
    to add more claims to the token, but not required for this task.
    """
    pass # Inherits all functionality from TokenObtainPairView

class UserDetailView(generics.RetrieveAPIView):
    """
    Allows authenticated users to retrieve their own details.
    """
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Returns the currently authenticated user.
        """
        return self.request.user

from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from core.api.serializers import CompleteUserSerializer, MeSerializer, RegisterSerializer, UpdateUserSerializer
from core.models import User


class RegisterView(CreateAPIView):
    """
    Main view to register a new user
    """
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class MeDetailView(RetrieveAPIView):
    """
    Main view to obtain the client detail
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = MeSerializer

    def get_object(self):
        return self.request.user


class ListUsersView(ListAPIView):
    """
    Main view to list all users in the database
    """
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = CompleteUserSerializer

    queryset = User.objects.all()


class UpdateUserView(UpdateAPIView):
    """
    View to update any user, it will require to pass the user uuid
    """
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = UpdateUserSerializer
    queryset = User.objects.all()

    lookup_url_kwarg = 'user_uuid'
    lookup_field = 'uuid'

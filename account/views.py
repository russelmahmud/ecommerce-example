from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response

from .serializers import UserSerializer
from .permissions import IsStaffOrTargetUser


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method == 'POST'
                else IsStaffOrTargetUser()),

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super(UserView, self).list(request, *args, **kwargs)

        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AuthView(APIView):
    authentication_classes = (BasicAuthentication, )

    def post(self, request):
        login(request, request.user)
        return Response(UserSerializer(request.user).data)

    def delete(self, request):
        logout(request)
        return Response({})

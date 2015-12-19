from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.response import Response

from .serializers import UserSerializer
from .permissions import IsStaffOrTargetUser


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    authentication_classes = (BasicAuthentication, SessionAuthentication, )
    permission_classes = (IsStaffOrTargetUser, )

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()

        return User.objects.filter(username=self.request.user.username)

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

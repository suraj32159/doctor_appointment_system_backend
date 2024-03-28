from rest_framework import generics, mixins, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import BookAppointment
from .serializers import BookAppointmentSerializer, UserSerializer


class BookAppointmentAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = BookAppointment.objects.all()
    serializer_class = BookAppointmentSerializer

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User with specified ID does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        appointments = self.get_queryset().filter(user=user)
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with specified ID does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data, context={'user_id': user.id})
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreateAPIView(CreateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BookAppointment
from datetime import datetime
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'username': {'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CustomDateTimeField(serializers.DateTimeField):
    def to_internal_value(self, value):
        try:
            naive_datetime = datetime.strptime(value, "%d-%m-%Y %H:%M:%S")
            aware_datetime = timezone.make_aware(naive_datetime, timezone.get_current_timezone())
            return aware_datetime
        except ValueError:
            self.fail('invalid')


class BookAppointmentSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    date_time = CustomDateTimeField()

    class Meta:
        model = BookAppointment
        fields = ['id', 'date_time', 'location', 'description', 'user_details']
        read_only_fields = ['id']

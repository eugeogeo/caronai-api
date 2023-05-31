from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Ride, RideHistory
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'nome', 'ra', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user

class CustomTokenObtainPairSerializer(serializers.Serializer):
    ra = serializers.CharField(max_length=20)
    password = serializers.CharField()

    def validate(self, attrs):
        ra = attrs.get('ra')
        password = attrs.get('password')

        if ra and password:
            user = authenticate(request=self.context.get('request'), ra=ra, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return {
                    'token': token,
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'nome': user.nome,
                        'ra': user.ra,
                    }
                }
            else:
                raise serializers.ValidationError('Usuário ou senha inválidos.')
        else:
            raise serializers.ValidationError('RA e senha são obrigatórios.')

class RideSerializer(serializers.ModelSerializer):
    driver_name = serializers.CharField(max_length=255)
    driver_ra = serializers.CharField(max_length=20)

    class Meta:
        model = Ride
        fields = ['id', 'driver_name', 'driver_ra', 'origin', 'destination', 'start_date', 'start_time', 'price', 'available_seats']


class RideHistorySerializer(serializers.ModelSerializer):
    ride = RideSerializer()

    class Meta:
        model = RideHistory
        fields = ['id', 'ride', 'role']

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import RideSerializer, UserSerializer, RideHistorySerializer, CustomTokenObtainPairSerializer
from .models import User, Ride, RideHistory
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from rest_framework import generics
from rest_framework.generics import ListAPIView
from caronapi.models import User
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta, date
from django.db.models import Q

class CustomTokenObtainPairView(APIView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class RideCreateView(generics.CreateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        driver_name = request.data.get('driver_name')
        driver_ra = request.data.get('driver_ra')
        user = request.user

        if not user.is_authenticated or user.ra != driver_ra:
            raise ValidationError("Invalid driver RA or authentication token mismatch.")

        # Get the start date and time from the request data
        start_date_str = request.data.get('start_date')
        start_time_str = request.data.get('start_time')

        # Convert the start date and time to datetime objects
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        start_time = datetime.strptime(start_time_str, "%H:%M:%S").time()

        # Combine the start date and time into a datetime object
        start_datetime = datetime.combine(start_date, start_time)

        # Calculate the end time by adding 30 minutes to the start time
        end_datetime = start_datetime + timedelta(minutes=30)

        # Check if there is an existing ride with a conflicting time range
        existing_ride = Ride.objects.filter(driver_ra=driver_ra).filter(
            start_date=start_datetime.date(),
            start_time__range=[
                (start_datetime + timedelta(minutes=-30)).time(),
                (start_datetime + timedelta(minutes=30)).time()
            ]
        ).first()

        if existing_ride:
            raise ValidationError("You already have a ride scheduled within the next 30 minutes.")

        ride = Ride(
            driver_name=driver_name,
            driver_ra=driver_ra,
            origin=request.data.get('origin'),
            destination=request.data.get('destination'),
            start_date=start_date,
            start_time=start_time,
            price=request.data.get('price'),
            available_seats=request.data.get('available_seats')
        )
        ride.save()

        serializer = self.get_serializer(ride)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class RideListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = request.data

        origin = request.GET.get('origin')
        destination = request.GET.get('destination')
        start_time = request.GET.get('start_time')
        start_date = request.GET.get('start_date')

        rides = Ride.objects.all()

        if origin:
            rides = rides.filter(origin__icontains=origin)
        if destination:
            rides = rides.filter(destination__icontains=destination)
        if start_date:
            rides = rides.filter(start_date=start_date)

        if start_time:
            start_time = datetime.strptime(start_time, '%H:%M:%S').time()
            rides = rides.filter(start_time__gte=start_time)

        serializer = RideSerializer(rides, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RideHistoryView(APIView):
    def get(self, request):
        user = request.user
        ride_histories = RideHistory.objects.filter(user=user)
        serializer = RideHistorySerializer(ride_histories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'nome', 'ra']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomTokenObtainPairSerializer(serializers.Serializer):
    ra = serializers.CharField(max_length=20)
    password = serializers.CharField()

    def validate(self, attrs):
        ra = attrs.get('ra')
        password = attrs.get('password')

        if ra and password:
            user = User.objects.filter(ra=ra).first()

            if user and user.check_password(password):
                token = TokenObtainPairView().get_token(user)
                return {
                    'refresh': str(token),
                    'access': str(token.access_token),
                }
            else:
                raise serializers.ValidationError('Usuário ou senha inválidos.')
        else:
            raise serializers.ValidationError('RA e senha são obrigatórios.')




from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import User, Stone, Activation
from .tasks import activate_stone
from .serializers import UserSerializer, StoneSerializer, ActivationSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            # User with this username already exists
            return Response({"error": "User with this username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new user
        user = User(username=username, password=password)
        user.save()

        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            return Response({'token': token}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ActivateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        stone_id = request.data.get('stone_id')
        user_id = request.data.get('user_id')
        power_duration = request.data.get('power_duration')

        # Check if the stone is already activated for the user
        current_time = timezone.now()
        active_activation = Activation.objects.filter(user_id=user_id, stone_id=stone_id, end_time__gt=current_time).first()
        if active_activation:
            return Response({'detail': 'The stone is already activated for the user.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has an active activation
        active_activation = Activation.objects.filter(user_id=user_id, end_time__gt=current_time).first()
        if active_activation:
            return Response({'detail': 'The user already has an active activation.'}, status=status.HTTP_400_BAD_REQUEST)

        # Activate the stone
        stone = Stone.objects.get(id=stone_id)
        user = User.objects.get(id=user_id)
        activation = Activation(user=user, stone=stone, start_time=current_time, end_time=current_time + timedelta(seconds=power_duration))
        activation.save()
        return Response({'detail': f'The {stone.stone_name} stone has been activated for {power_duration} seconds.'}, status=status.HTTP_200_OK)


def activate_stone_async(request):

    stone_id = request.data.get('stone_id')
    user_id = request.data.get('user_id')
    power_duration = request.data.get('power_duration')

    # Create a Celery task to handle the activation asynchronously
    task = activate_stone.apply_async((user_id, stone_id, power_duration))

    return Response({'detail': 'Stone activation is in progress. Task ID: {}'.format(task.id)}, status=status.HTTP_202_ACCEPTED)

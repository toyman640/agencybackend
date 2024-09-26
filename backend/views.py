from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, Agency
from .serializers import CreateUserSerializer, CreateStaffUserSerializer, CreateSuperUserSerializer, AgencySerializer


class RegisterUserView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
      serializer = CreateUserSerializer(data=request.data)
      if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
          'status': 'User created', 
          'user': serializer.data,
          'token': token.key
        }, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterStaffUserView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
      serializer = CreateStaffUserSerializer(data=request.data)
      if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
          'status': 'Staff user created', 
          'user': serializer.data,
          'token': token.key
        }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterSuperUserView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    serializer = CreateSuperUserSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()
      token, created = Token.objects.get_or_create(user=user)
      return Response({
        'status': 'Superuser created', 
        'user': serializer.data,
        'token': token.key
    }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
      user = CustomUser.objects.get(email=email)

      if not user.is_active:
        return Response({'error': 'This account is not activated. Please contact support.'}, status=status.HTTP_403_FORBIDDEN)

      user = authenticate(email=email, password=password)
      if user:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
          'token': token.key, 
          'id': user.id,
          'email': user.email, 
          'name': user.name, 
          'is_staff': user.is_staff,
          'is_active': user.is_active,
        }, status=status.HTTP_200_OK)
      else:
        return Response({'error': 'Invalid login details. Please check your credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    except CustomUser.DoesNotExist:
      return Response({'error': 'Account with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def post(self, request):
    request.user.auth_token.delete()
    logout(request)
    return Response({'status': 'Logged out'}, status=status.HTTP_200_OK)


class ActivateUserView(APIView):
  permission_classes = [permissions.IsAdminUser]

  def post(self, request, user_id):
    try:
      user = CustomUser.objects.get(id=user_id)
      user.is_active = True
      user.save()
      return Response({'status': 'User activated'}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
      return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class DeactivateUserView(APIView):
  permission_classes = [permissions.IsAdminUser]

  def post(self, request, user_id):
    try:
      user = CustomUser.objects.get(id=user_id)
      user.is_active = False
      user.save()
      return Response({'status': 'User deactivated'}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
      return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class StaffUsersView(APIView):
  permission_classes = [permissions.IsAdminUser]

  def get(self, request):
    users = CustomUser.objects.filter(is_staff=False)
    user_data = [{"id": user.id, "email": user.email, "name": user.name, "is_active": user.is_active} for user in users]
    return Response(user_data, status=status.HTTP_200_OK)


class AgencyView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def post(self, request):
    serializer = AgencySerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(created_by=request.user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def get(self, request, id=None):
    if id:
      try:
        agency = Agency.objects.get(id=id)
        serializer = AgencySerializer(agency)
        return Response(serializer.data, status=status.HTTP_200_OK)
      except Agency.DoesNotExist:
        return Response({"detail": "Agency not found."}, status=status.HTTP_404_NOT_FOUND)
    if request.user.is_staff:
      agencies = Agency.objects.all()
      serializer = AgencySerializer(agencies, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
    else:
      try:
        agency = Agency.objects.get(created_by=request.user)
        serializer = AgencySerializer(agency)
        return Response(serializer.data, status=status.HTTP_200_OK)
      except Agency.DoesNotExist:
        return Response({"detail": "Agency not found."}, status=status.HTTP_404_NOT_FOUND)



class EditAgencyView(APIView):
  permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

  def put(self, request, agency_id):
    try:
      agency = Agency.objects.get(id=agency_id)
    except Agency.DoesNotExist:
      return Response({'error': 'Agency not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = AgencySerializer(agency, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

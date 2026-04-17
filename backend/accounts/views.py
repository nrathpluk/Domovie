from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, UserSerializer


# ===== Django Template Views (session-based, for admin panel) =====

def login_view(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'movies:index'))
        return render(request, 'accounts/login.html', {'error': True})
    return render(request, 'accounts/login.html', {'error': False})


def logout_view(request):
    logout(request)
    return redirect('movies:index')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            return render(request, 'accounts/register.html', {'error': 'รหัสผ่านไม่ตรงกัน'})
        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {'error': 'ชื่อผู้ใช้นี้มีอยู่แล้ว'})
        user = User.objects.create_user(username=username, password=password1)
        login(request, user)
        messages.success(request, f'ยินดีต้อนรับ {user.username}!')
        return redirect('movies:index')
    return render(request, 'accounts/register.html', {'error': None})


# ===== REST API Views (JWT-based, for frontend) =====

@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'username': user.username,
        'is_staff': user.is_staff,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_logout(request):
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
    except Exception:
        pass
    return Response({'detail': 'Logged out'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_me(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def api_register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'User created'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

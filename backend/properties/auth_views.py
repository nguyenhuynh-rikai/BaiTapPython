from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from .auth_serializers import ChangePasswordSerializer, LoginSerializer, RegisterSerializer, UserProfileSerializer


def user_response(user, token):
    role = "tenant"
    if user.is_superuser or user.is_staff:
        role = "admin"
    elif user.groups.filter(name="landlord").exists():
        role = "landlord"
    elif user.groups.filter(name="tenant").exists():
        role = "tenant"

    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "role": role,
        },
        "token": token.key,
    }


@extend_schema(tags=["Authentication"])
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)

        return Response(user_response(user, token), status=status.HTTP_201_CREATED)


@extend_schema(tags=["Authentication"])
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        return Response(user_response(user, token))


@extend_schema(tags=["Authentication"])
class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Xoa token cu de user phai login lai sau khi doi mat khau.
        Token.objects.filter(user=request.user).delete()

        return Response({"detail": "Password changed successfully. Please login again."})


@extend_schema(tags=["Authentication"])
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=None)
    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response({"detail": "Logged out successfully."})


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    @extend_schema(tags=["Authentication"])
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    @extend_schema(tags=["Authentication"])
    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


from django.contrib.auth.models import User, Group
from rest_framework.permissions import IsAdminUser

@extend_schema(tags=["Admin User Management"])
class AdminUserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all().order_by('id')
        data = []
        for u in users:
            role = "tenant"
            if u.is_superuser or u.is_staff:
                role = "admin"
            elif u.groups.filter(name="landlord").exists():
                role = "landlord"
            elif u.groups.filter(name="tenant").exists():
                role = "tenant"
            
            data.append({
                "id": u.id,
                "username": u.username,
                "role": role,
                "date_joined": u.date_joined.strftime("%Y-%m-%d %H:%M:%S") if u.date_joined else ""
            })
        return Response(data)


@extend_schema(tags=["Admin User Management"])
class AdminUserDetailView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        role = request.data.get("role")
        if role not in ["tenant", "landlord", "admin"]:
            return Response({"detail": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

        # Xóa các group cũ
        user.groups.clear()
        
        # Thêm vào group mới
        group, _ = Group.objects.get_or_create(name=role)
        user.groups.add(group)

        # Cập nhật quyền staff/superuser
        if role == "admin":
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_superuser = False
        user.save()

        return Response({"detail": "User role updated successfully"})


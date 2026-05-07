from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer

@api_view(['GET'])
def post_list(request):

    posts = Post.objects.all()

    serializer = PostSerializer(posts, many=True)

    return Response(serializer.data)

@api_view(['POST'])
def create_post(request):

    serializer = PostSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):

    return Response({
        "user": request.user.username
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    return Response({"message": "Đã tạo bài viết"})

from rest_framework.permissions import IsAdminUser

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_post(request, pk):
    return Response({"message": "Đã xóa"})
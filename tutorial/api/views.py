from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
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
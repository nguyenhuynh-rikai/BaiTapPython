from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Category
from .serializers import PostSerializer, CategorySerializer
from .permissions import IsAuthorOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .responses import custom_response

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(status='published')
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_fields = ['category__slug', 'status']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)

        return custom_response(
            data=serializer.data,
            message="Lấy danh sách bài viết thành công",
            status_code=status.HTTP_200_OK
        )

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()

        serializer = self.get_serializer(post)

        return custom_response(
            data=serializer.data,
            message="Lấy chi tiết bài viết thành công",
            status_code=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(author=request.user)

        return custom_response(
            data=serializer.data,
            message="Tạo bài viết thành công",
            status_code=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        post = self.get_object()

        serializer = self.get_serializer(
            post,
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return custom_response(
            data=serializer.data,
            message="Cập nhật bài viết thành công",
            status_code=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()

        post.delete()

        return custom_response(
            data=None,
            message="Xóa bài viết thành công",
            status_code=status.HTTP_204_NO_CONTENT
        )
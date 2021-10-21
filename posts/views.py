from rest_framework            import permissions
from rest_framework.viewsets   import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination

from .serializers import PostSerializer
from .models import Post


class IsAuthenticatedOrOwnerOrAnonymReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and request.user.is_authenticated and 
            obj.author == request.user
        )


class PostViewSet(ModelViewSet):
    queryset = Post.objects.select_related('author')
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedOrOwnerOrAnonymReadOnly]
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
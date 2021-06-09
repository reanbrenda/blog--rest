from rest_framework.generics import (
	ListAPIView,
	RetrieveAPIView,
	UpdateAPIView,
	DestroyAPIView,
	CreateAPIView,
	RetrieveUpdateAPIView
	)
from django.db.models import Q


from rest_framework.filters import (
        SearchFilter,
        OrderingFilter,
    )
from .pagination import PostLimitOffsetPagination,PostPageNumberPagination
from posts.models import Post
from .serializers import (
	PostListSerializer,
	PostDetailSerializer,
	PostCreateUpdateSerializer,
	)
from rest_framework.permissions import(
	AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
	)
from .permissions import IsOwnerOrReadOnly
class PostCreateAPIView(CreateAPIView) :
	queryset=Post.objects.all()
	serializer_class=PostListSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

class PostListAPIView(ListAPIView):
    serializer_class = PostListSerializer
    filter_backends= [SearchFilter, OrderingFilter]
    permission_classes = [AllowAny]
    search_fields = ['title', 'content', 'user__first_name']
    pagination_class = PostPageNumberPagination #PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        #queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
        queryset_list = Post.objects.all() #filter(user=self.request.user)
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                    Q(title__icontains=query)|
                    Q(content__icontains=query)|
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query)
                    ).distinct()
        return queryset_list
class PostUpdateAPIView(RetrieveUpdateAPIView) :
	queryset=Post.objects.all()
	serializer_class=PostDetailSerializer
	lookup_field='slug'
	permission_classes = [IsAuthenticated]
class PostDeleteAPIView(DestroyAPIView) :
	queryset=Post.objects.all()
	serializer_class=PostDetailSerializer
	lookup_field='slug'


class PostDetailAPIView(RetrieveAPIView) : 
	queryset=Post.objects.all()
	serializer_class=PostDetailSerializer
	lookup_field='slug'
	permission_classes = [AllowAny]




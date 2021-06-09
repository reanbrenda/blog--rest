from rest_framework.serializers import ModelSerializer,SerializerMethodField
from posts.models import Post
from accounts.api.serializers import UserDetailSerializer
class PostDetailSerializer(ModelSerializer):
	user = UserDetailSerializer(read_only=True)
	class Meta:
		model = Post
		fields = [
            'id',
            'title',
            'slug',
            'content',
            'publish',
        ]
class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'publish',
        ]

class PostListSerializer(ModelSerializer):
	user = UserDetailSerializer(read_only=True)
	class Meta:
		model = Post
		fields = [
            'user',
            'id',
            'title',
            'slug',
            'content',
            'publish',
        ]



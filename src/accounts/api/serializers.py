from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework.serializers import (
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
    )


User = get_user_model()

class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]
class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                            }
    def create(self,validated_data):
        username=validated_data['username']
        password=validated_data['password']
        email=validated_data['email']
        user_obj=User(
            username=username,
            email=email

            )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data
    def validate(self, data):
        email = data['email']
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError("This user has already registered.")
        return data

class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(required=False,allow_blank=True)
    email = EmailField(label='Email Address')
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'token',
            
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                            }
    def validate(self, data):
        user_obj=None
        email = data.get('email',None)
        username=data.get('username',None)
        password=data['password']
        if not email and  not username:
            raise ValidationError("username or password required to login")
        user = User.objects.filter(
            Q(email=email) |
            Q(username=username)

            ).distinct()
        if user.exists and user.count()==1:
            user_obj=user.first()
        else:
          raise ValidationError("This username/email is not valid.")
        if user_obj:
            if not user_obj.check_password(password):
               raise ValidationError("Wrong password.") 
        data["token"]="tokenized"
        return data

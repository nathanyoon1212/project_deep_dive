from django.db                  import transaction
from rest_framework.serializers import ModelSerializer
from .models import User

class UserInfoSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ("kakao_id", "name", "nickname", "email", "mobile")
        exrta_kwargs = {
            "id"    : {"read_only"  : True},
            "email" : {"validators" : []}
        }

class UserSerializer(ModelSerializer):
    def update(self, instance, validated_data):
        instance.nickname = validated_data.get("nickname", instance.nickname)
        instance.moblie = validated_data.get("moblie", instance.mobile)

    class Meta:
        model = User
        fields = ("kakao_id", "name", "nickname", "email", "mobile")
        extra_kwargs = {
            "email" : {"read_only": True}
        }

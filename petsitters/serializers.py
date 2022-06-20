from django.db                  import transaction
from rest_framework             import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from .models import (Petsitter, PetsitterImage, PetsitterType,
                    Type, Comment)

class PetsitterSerializer(ModelSerializer):

    def update(self,instance, validated_data):
        instance.title       = validated_data.get("title", instance.title)
        instance.price       = validated_data.get("price", instance.price)
        instance.information = validated_data.get("information", instance.information)
        instance.address     = validated_data.get("address", instance.address)
        instance.save()

        class Meta:
            model = Petsitter
            fields = ["id", "name", "title", "price", "grade", "count", "information", "address"]
            extra_kwargs = {
                "id" : {"read_only" : True}
            }
            
class PetsitterImageSerializer(ModelSerializer):

    def update(self, instance, validated_data):
        instance.image_url = validated_data.get("image_url", instance.image_url)
        instance.save()

        class Meta:
            model = PetsitterImage
            fields = ["id", "image_url"]
            extra_kwarges = {
                "id" : {"read_only" : True}
            }

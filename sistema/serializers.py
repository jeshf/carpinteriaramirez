from rest_framework import serializers
from sistema.models import *
from django.contrib.auth import get_user_model
class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ResponseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Response
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user.username
        response = super(ResponseSerializer, self).create(validated_data)
        response.repliedBy = user
        response.save()
        return response

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
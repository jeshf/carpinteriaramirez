from rest_framework import serializers
from sistema.models import *
from rest_auth.registration.serializers import RegisterSerializer
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

class CustomRegisterSerializer(RegisterSerializer):
    password1 = serializers.CharField(write_only=True)
    is_active = serializers.BooleanField(required=True)  # este campo es necesario
    is_admin = serializers.BooleanField(required=True)  # este campo es necesario
    name = serializers.CharField(required=True)
    firstLastName = serializers.CharField(required=True)
    secondLastName = serializers.CharField(required=True)
    date_joined = serializers.DateTimeField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'password1': self.validated_data.get('password1', ''),
            'is_active': self.validated_data.get('is_active', ''),
            'is_admin': self.validated_data.get('is_admin', ''),
            'name': self.validated_data.get('name', ''),
            'firstLastName': self.validated_data.get('firstLastName', ''),
            'secondLastName': self.validated_data.get('secondLastName', ''),
            'date_joined': self.validated_data.get('date_joined', ''),
            'username': self.validated_data.get('name', ''),
            'email': self.validated_data.get('email', ''),
        }
class CustomUserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('password1','is_active','is_admin','name','firstLastName',
                            'secondLastName','date_joined','username','email')
        read_only_fields = ('username',)


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
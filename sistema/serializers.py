from rest_framework import serializers
from sistema.models import *
#from rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
    #def create(self, validated_data):
        #user = self.context['request'].user.username
        #comment = super(CommentSerializer, self).create(validated_data)
        #comment.createdBy = user
        #comment.save()
        #return comment

class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
    def create(self, validated_data):
        if not validated_data.get('imagePath'):
            raise serializers.ValidationError('Selecciona una imagen')
        instance = super(ImageSerializer, self).create(validated_data)
        instance.save()
        return instance
class ResponseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Response
        fields = '__all__'

    #def create(self, validated_data):
        #user = self.context['request'].user.username
        #response = super(ResponseSerializer, self).create(validated_data)
        #response.repliedBy = user
        #response.save()
        #return response

#logger = logging.getLogger(__name__)
class UserSerializer(serializers.ModelSerializer):
    #password2 = serializers.ReadOnlyField()

    class Meta:
        model = get_user_model()
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'user_permissions': {'write_only': True, 'required': False},
        }

    def create(self, validated_data):
        if not validated_data.get('password'):
            raise serializers.ValidationError('La contraseña no puede estar vacía')
        instance = super(UserSerializer, self).create(validated_data)
        instance.set_password(validated_data.get('password'))
        instance.is_active=True
        instance.save()
        #logger.info(_('User {} created ok'.format(instance.username)))
        return instance

    def update(self, instance, validated_data):
        if validated_data.get('password'):
            instance.set_password(validated_data.pop('password'))
        #logger.info(_('User {} update ok'.format(instance.username)))
        return super(UserSerializer, self).update(instance=instance, validated_data=validated_data)

class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
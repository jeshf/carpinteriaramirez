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
            raise serializers.ValidationError('The password not empty')
        instance = super(UserSerializer, self).create(validated_data)
        instance.set_password(validated_data.get('password'))
        instance.save()
        #logger.info(_('User {} created ok'.format(instance.username)))
        return instance

    def update(self, instance, validated_data):
        if validated_data.get('password'):
            instance.set_password(validated_data.pop('password'))
        #logger.info(_('User {} update ok'.format(instance.username)))
        return super(UserSerializer, self).update(instance=instance, validated_data=validated_data)

    #@classmethod
    #def get_permissions(cls, obj):
        #groups = obj.groups.all()
        #response_permissions = []
        # add permissions from the groups
        #for group in groups:
            #permissions = group.permissions.all()
            #for permission in permissions:
                #if utils.permission_exist(permission.id, response_permissions):
                    #continue
                #response_permissions.append(PermissionSerializer(permission).data)
        # add permissions individuals
        #for permission in obj.user_permissions.all():
            #if not utils.permission_exist(permission.id, response_permissions):
                #continue
            #response_permissions.append(PermissionSerializer(permission).data)
        #return response_permissions or None
#class CustomRegisterSerializer(RegisterSerializer):
    #password1 = serializers.CharField(write_only=True)
    #is_active = serializers.BooleanField(required=True)
    #is_staff = serializers.BooleanField(required=True)
    #is_superuser = serializers.BooleanField(required=True)
    #name = serializers.CharField(required=True)
    #firstLastName = serializers.CharField(required=True)
    #secondLastName = serializers.CharField(required=True)
    #last_login = serializers.DateTimeField(required=True)
    #date_joined = serializers.DateTimeField(required=True)
    #username = serializers.CharField(required=True)
    #email = serializers.EmailField(required=True)
    #def get_cleaned_data(self):
        #super(CustomRegisterSerializer, self).get_cleaned_data()
        #return {
            #'password1': self.validated_data.get('password1', ''),
            #'is_active': self.validated_data.get('is_active', ''),
            #'is_staff': self.validated_data.get('is_staff', ''),
            #'is_superuser': self.validated_data.get('is_superuser', ''),
            #'name': self.validated_data.get('name', ''),
            #'firstLastName': self.validated_data.get('firstLastName', ''),
            #'secondLastName': self.validated_data.get('secondLastName', ''),
            #'last_login': self.validated_data.get('date_joined', ''),
            #'date_joined': self.validated_data.get('date_joined', ''),
            #'username': self.validated_data.get('name', ''),
            #'email': self.validated_data.get('email', ''),
        #}
#class CustomUserDetailsSerializer(serializers.ModelSerializer):

    #class Meta:
        #model = CustomUser
        #fields = ('password1','is_active','is_staff','is_s','name','firstLastName',
        #                   'secondLastName','date_joined','username','email')
        #read_only_fields = ('username',)


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
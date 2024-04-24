from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField(read_only=True)
    is_admin = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = User
        fields = ['id','username','name','email','is_admin']

    def get_name(self,obj):
        name =  obj.first_name
        
        if name =="":
            name = obj.email
        return name
    
    def get_is_admin(self,obj):
        is_admin =  obj.is_staff
        return is_admin
    
class UserSerializerWithToken(UserSerializer):

    token = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = User
        fields = ['id','username','name','email','is_admin','token']

    def get_token(self,obj):
            token = RefreshToken.for_user(obj)
            return str(token.access_token)



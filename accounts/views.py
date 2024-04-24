from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.decorators import api_view,permission_classes

from rest_framework.permissions import IsAuthenticated,IsAdminUser

from .serializers import UserSerializer,UserSerializerWithToken
from django.contrib.auth.models import User

from django.contrib.auth.hashers import make_password


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

   def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k,v in serializer.items():
            data[k]=v
        return data
 
class MyTokenobtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
def RegisterUser(request):

    data = request.data

    try:
        user = User.objects.create(
            first_name=data['name'],
            username = data['email'],
            email=data['email'],
            password = make_password(data['password'])
        )

        serializer = UserSerializerWithToken(user,many=False)
        return Response({
                'data': serializer.data,
                'message': 'user created successfully'
            },status=status.HTTP_201_CREATED)
    
    except Exception as e:

        return Response({
            'data': {},
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

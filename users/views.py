from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view,permission_classes

from rest_framework.permissions import IsAuthenticated,IsAdminUser

from accounts.serializers import UserSerializer,UserSerializerWithToken
from django.contrib.auth.models import User

from django.contrib.auth.hashers import make_password

from django.core.paginator import Paginator


# **Userside Funtionalities** 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):

    try:
        user = request.user   
        serializer = UserSerializer(user, many=False)
        if serializer.is_valid:
            return Response({
                'data': serializer.data,
                'message': 'user fetched successfully'
            })
        else:
            return Response({
                'data': serializer.errors,
                'message': 'validation error'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        
        return Response({
            'data': {},
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def updateUser(request):

    try:
        user = request.user
        print(user)
        serializer = UserSerializerWithToken(user,many=False,partial=True)

        data = request.data
        user.first_name = data['name']
        user.username = data['email']
        user.email = data['email']

        if data['password'] != '':
            user.password = make_password(data['password'])
        
        user.save()

        return Response({

                    'data': serializer.data,
                    'message': 'user updated successfully'
                },status=status.HTTP_200_OK)

    except Exception as e:

        return Response({
            'data': {},
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    
# **Adminside functionalities**

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):

    try:
        user = User.objects.all() 
        if request.GET.get('search'):
                search = request.GET.get('search')
                user = user.filter(first_name__icontains=search)

        page_naumber = request.GET.get('page',1)
        paginator=  Paginator(user,200)
        serializer = UserSerializer(paginator.page(page_naumber), many=True)  
    
        if serializer.is_valid:
            return Response({
                'data': serializer.data,
                'message': 'user fetched successfully'
            },status=status.HTTP_200_OK)
        else:
            return Response({
                'data': serializer.errors,
                'message': 'validation error'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        
        return Response({
            'data': {},
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def DeleteUser(request,pk):
    
    try:
        user = User.objects.get(id=pk)
        user.delete()
        return Response({
                'data': {},
                'message': 'user deleted successfully'
            },status=status.HTTP_200_OK)
    
    except Exception as e :

        return Response({
            'data': {},
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def UserUpdateById(request,pk):
    try:
        user = User.objects.get(id=pk)

        data = request.data
        user.first_name = data['name']
        user.username = data['email']
        user.email = data['email']
        user.is_staff = data['is_admin']
        
        user.save()
        serializer = UserSerializer(user,many=False,partial=True)

        return Response({

                    'data': serializer.data,
                    'message': 'user updated successfully'
                },status=status.HTTP_200_OK)

    except Exception as e:

        return Response({
            'data': {},
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


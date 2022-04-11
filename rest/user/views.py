from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from .serializers import RegisterSerializer

@api_view(['POST'])
def login_api(request):
    serializer=AuthTokenSerializer(data=request.data)
    if serializer.is_valid():
        user=serializer.validated_data['user']

        created,token=AuthToken.objects.create(user)

        return Response({
            'userinfo':{
                'id':user.id,
                'username':user.username,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'email':user.email
            },
            'token':token
        })
    else:
        return Response(serializer.errors)

@api_view(["POST"])
def register_api(request):
    serializer=RegisterSerializer(data=request.data)
    if serializer.is_valid():
        print(serializer)
        user=serializer.save()
        created,token=AuthToken.objects.create(user)
        return Response({
        'userinfo':{
            'id':user.id,
            'username':user.username,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email':user.email
        },
        'token':token
    })
    
    else:
        print('errors')
        return Response(serializer.errors)


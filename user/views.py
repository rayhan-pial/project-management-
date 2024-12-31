from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer, LoginSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from django.contrib.auth import authenticate
from rest_framework.decorators import action
from .customPermissions import IsAuthenticatedOrPostOnly



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes =[IsAuthenticatedOrPostOnly]



class LoginUserView(APIView):

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "refresh": {"type": "string"},
                    "access": {"type": "string"},
                },
            }
        },
    )
    def post(self,request):
        try :
            data = request.data
            serializer = LoginSerializer(data = data)
            if serializer.is_valid():
                email = serializer.data['email']
                user = authenticate(email = email, password = data['password'])

                if user is None:

                    return Response({'msg':'Invalid Pass'})

                refresh = RefreshToken.for_user(user)

                return Response(
                {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                },status=status.HTTP_200_OK)

            return Response({'msg':'Invalid Something'})

        except Exception as e:
            return Response({'msg':'Not valid'})



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import New_User
from .serializers import UserSerializer

class UserRegistration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'created'}, status=status.HTTP_200_OK)
        return Response({'message': 'already exist'}, status=status.HTTP_200_OK)

class UserLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            user = New_User.objects.get(email=email)
            if user.check_password(password):
                serializer = UserSerializer(user)  
                return Response({'message': 'all correct', 'user_data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'password incorrect'}, status=status.HTTP_200_OK)
        except New_User.DoesNotExist:
            return Response({'message': 'user does not exist'}, status=status.HTTP_200_OK)


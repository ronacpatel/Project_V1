


from rest_framework import serializers
from .models import New_User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = New_User
        fields = ['id', 'first_name', 'last_name', 'address', 'phone_number', 'email', 'password', 'reset_question', 'reset_answer']
        extra_kwargs = {'password': {'write_only': True}}

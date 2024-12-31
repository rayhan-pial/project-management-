from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email','password', 'first_name', 'last_name','joined_date']
        extra_kwargs = {'password': {'write_only': True},
                        'joined_date':{'read_only':True}}

    def create(self, validated_data):

        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')


        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=first_name,
            last_name=last_name
            )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

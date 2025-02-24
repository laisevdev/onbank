from rest_framework import serializers
from autenticacao.models import User 

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,  min_length=6)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "cpf", "date_of_birth", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            cpf=validated_data["cpf"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            date_of_birth=validated_data["date_of_birth"],
            password=validated_data["password"],
        )
        return user

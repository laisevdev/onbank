from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from autenticacao.models import User
from .serializers import UserRegisterSerializer
from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse


class RegisterUserView(generics.CreateAPIView):
    authentication_classes = []  
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "Usuário cadastrado com sucesso!", "email": user.email},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def register_user(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        date_of_birth = request.POST.get('date_of_birth')
        password = request.POST.get('password')

        response = requests.post('http://127.0.0.1:8000/api/cadastro/', json={
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'cpf': cpf,
            'date_of_birth': date_of_birth,
            'password': password
        })
        
        print("API Response:", response.status_code, response.text)

        if response.status_code == status.HTTP_201_CREATED:
            return JsonResponse({"success": True})  # Resposta JSON correta
        else:
            return JsonResponse({"success": False, "errors": response.json()}, status=400)

    return render(request, 'autenticacao/register.html')

def login_user(request):
        return render(request, 'autenticacao/login.html')
 
def dashboard(request):
        return render(request, 'autenticacao/dashboard.html')   
'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def protected_view(request):
    return Response({"message": "Você acessou uma rota protegida!"})
'''
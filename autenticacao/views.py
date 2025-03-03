from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from autenticacao.models import User
from .serializers import UserRegisterSerializer
from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.utils.timezone import now



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

User = get_user_model()  # Pega o modelo de usuário personalizado

def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        response = requests.post('http://127.0.0.1:8000/api/login/', json={
            'email': email,
            'password': password
        })

        if response.status_code == 200:
            data = response.json()  # A API deve retornar o token JWT Sliding
            sliding_token = data.get('token')

            if sliding_token:
                # Armazena o token na sessão
                request.session['sliding_token'] = sliding_token  

                # Busca o usuário no banco de dados
                user = User.objects.filter(email=email).first()

                if user:
                    # Salva ID, nome e último login na sessão
                    request.session['user_id'] = user.id  
                    request.session['user_name'] = user.first_name  
                    request.session['last_login'] = user.last_login.strftime('%d/%m/%Y %H:%M') if user.last_login else "Nunca"

                    # Atualiza o `last_login` do usuário
                    user.last_login = now()
                    user.save(update_fields=['last_login'])

                return redirect('dashboard')

        return render(request, 'autenticacao/login.html', {'error': 'Email ou senha inválidos!'})

    return render(request, 'autenticacao/login.html')

@login_required(login_url='login')
def dashboard(request):
    if not request.user:
        return redirect('login')  # Redireciona para login se não estiver autenticado
    
    context = {
        'user_name': request.session.get('user_name', 'Cliente'),
    }
    
    return render(request, 'autenticacao/dashboard.html', context)

def logout_user(request):
    if 'sliding_token' in request.session:
        del request.session['sliding_token']

    return redirect('login_user')  
'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def protected_view(request):
    return Response({"message": "Você acessou uma rota protegida!"})
'''
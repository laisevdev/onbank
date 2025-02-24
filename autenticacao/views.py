from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status, request
from autenticacao.models import User
from .serializers import UserRegisterSerializer


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
    
'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def protected_view(request):
    return Response({"message": "Você acessou uma rota protegida!"})
'''
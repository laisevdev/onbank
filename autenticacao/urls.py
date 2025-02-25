from django.urls import path
from rest_framework_simplejwt.views import TokenObtainSlidingView, TokenRefreshSlidingView
from autenticacao.views import RegisterUserView, register_user


urlpatterns = [
    path('api/login/', TokenObtainSlidingView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshSlidingView.as_view(), name='token_refresh'),  
    path('api/cadastro/', RegisterUserView.as_view(), name="register"),
    path('cadastrar/', register_user, name='register_user'),  # Nova rota para o templat
    #path('api/protected/', protected_view, name='protected_view'),
]

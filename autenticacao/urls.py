from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from autenticacao.views import protected_view, RegisterUserView


urlpatterns = [
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
     path('api/cadastro/', RegisterUserView.as_view(), name="register"),
    #path('api/protected/', protected_view, name='protected_view'),
]

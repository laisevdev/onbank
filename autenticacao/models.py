from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import MinLengthValidator
from .validators.cpf_validator import validate_cpf  


class MyUserManager(BaseUserManager):
    def create_user(self, cpf, email, first_name, last_name, date_of_birth, password=None):
        if not email:
            raise ValueError("O email é obrigatório.")
        if not first_name or not last_name:
            raise ValueError("Nome e sobrenome são obrigatórios.")
        
        user = self.model(
            cpf=cpf,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, email, first_name, last_name, date_of_birth, password=None):
    
        user = self.create_user(
            cpf=cpf,
            email=email,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    
class User(AbstractBaseUser, PermissionsMixin):
    DONO_CONTA = 'usuario'
    GERENTE_BANCO = 'gerente_banco'

    ROLE_CHOICES = [
        (DONO_CONTA, 'Usuario'),
        (GERENTE_BANCO, 'Gerente do Banco'),
    ]

    tipo_usuario = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=DONO_CONTA,
    )

    def __str__(self):
        return f"{self.username} ({self.get_tipo_usuario_display()})"

    email =  models.EmailField(null=False, blank=False, max_length=62, unique=True)
    cpf = models.CharField(
        max_length=11,
        unique=True,
        verbose_name="CPF",
        validators=[MinLengthValidator(11), validate_cpf]
    )
    date_of_birth = models.DateField(verbose_name="Data de Nascimento")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Usuario')
    first_name = models.CharField(null=False, blank=False, max_length=30)
    last_name = models.CharField(null=False, blank=False,max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  
    user_permissions = models.ManyToManyField('auth.Permission', blank=True, related_name='user_permissions_usuario_customizado')
    groups = models.ManyToManyField('auth.Group', blank=True, related_name='groups_usuario_customizado')

    objects = MyUserManager()  

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'cpf', 'date_of_birth']

    def __str__(self):
        return self.email
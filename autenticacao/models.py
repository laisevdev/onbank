from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import MinLengthValidator
from .validators.cpf_validator import validate_cpf  


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("O usuário deve ter um endereço de email válido.")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
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
    is_staff = models.BooleanField(default=False)  # Necessário para acesso ao admin
    user_permissions = models.ManyToManyField('auth.Permission', blank=True, related_name='user_permissions_usuario_customizado')
    groups = models.ManyToManyField('auth.Group', blank=True, related_name='groups_usuario_customizado')

    objects = MyUserManager()  # Associamos o novo gerenciador aqui

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'cpf', 'date_of_birth']

    def __str__(self):
        return self.email
'''
 
class User(AbstractUser):
    DONO_CONTA = 'dono_conta'
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
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Usuario')
     
    REQUIRED_FIELDS = ['email']
    user_permissions = models.ManyToManyField('auth.Permission', blank=True, related_name='user_permissions_usuario_customizado')
    groups = models.ManyToManyField('auth.Group', blank=True, related_name='groups_usuario_customizado')

class UserRecover(models.Model):
    class ValidToken(models.TextChoices):
        not_used = "not used"
        used = "used"
        
    email =  models.EmailField(null=False, blank=False, max_length=62, unique=True)
    cpf = models.CharField(null=False, blank=False, max_length=14)
    token = models.CharField(null=False, blank=False, max_length=128)
    initial_time = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    expired_time= models.DateTimeField(null=False, blank=False)
    usage =  models.CharField(null=False, blank=False, choices=ValidToken.choices, default=ValidToken.not_used)

'''
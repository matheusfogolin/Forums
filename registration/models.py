from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from tinymce.models import HTMLField
from django_resized import ResizedImageField
from main import models as mainModels

class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, gender, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            gender=gender,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, gender, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
            gender=gender,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    GENDER_CHOICES = (
         ('M', 'Masculino'),
         ('F', 'Feminino')
     )
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    gender = models.CharField('Sexo', max_length = 1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField('Data de Nascimento')
    creation_date = models.DateTimeField(auto_now_add = True)
    update_date = models.DateTimeField('Data de alteração', null=True)
    last_login = models.DateTimeField('Último Login', null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField('Nome', max_length = 30)
    last_name = models.CharField('Sobrenome', max_length = 30)
    bio = HTMLField()
    profile_pic = ResizedImageField('Foto de perfil', size=[50, 80], quality = 100, upload_to = "users", null = True, blank = True)
    
    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["gender", "date_of_birth"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def full_name(self):
        return self.first_name + " " + self.last_name
    
    @property
    def num_posts(self):
        return mainModels.Post.objects.filter(user=self).count()
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
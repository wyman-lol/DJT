from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser, BaseUserManager

class UserManager(BaseUserManager):

    def _create_user(self, username, telephone, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not telephone:
            raise ValueError('The given telephone must be set')
        user = self.model(username=username, telephone=telephone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, telephone=None, password=None, **extra_fields):
        extra_fields['is_superuser'] = False
        extra_fields['is_staff'] = False
        return self._create_user(username, telephone, password, **extra_fields)

    def create_superuser(self, username, telephone, password, **extra_fields):
        extra_fields['is_superuser'] = True
        extra_fields['is_staff'] = True
        return self._create_user(username, telephone, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    telephone = models.CharField(max_length=11, unique=True)
    username = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    join_date = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(blank=True)

    objects = UserManager()
    # 创建superuser时候改为telephone优先
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['username', 'email']

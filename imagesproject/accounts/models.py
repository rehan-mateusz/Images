import json
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError


class Plan(models.Model):
    name = models.CharField(max_length=50)
    thumbnails_sizes = models.JSONField(
        help_text='format: {"sizes": "[[width1, height1], [width2, height2], ...]"}')
    can_share = models.BooleanField(default=False)
    has_original = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        if len(self.thumbnails_sizes.keys()) != 1:
            raise ValidationError('JSON must have exactly one key - "sizes"')
        elif 'sizes' not in self.thumbnails_sizes.keys():
            raise ValidationError('JSON must have "sizes" key')
        try:
            sizes = json.loads(self.thumbnails_sizes['sizes'])
        except:
            raise ValidationError(
                'Sizes must be put in format [[width1, height1],'
                + ' [width2, height2], ...] widths and heights must be integers')
        for size in sizes:
            if not isinstance(size, list) or len(size) != 2:
                raise ValidationError(
                    'Sizes must be put in format [[width1, height1], '
                    + '[width2, height2], ...]')
            if not (isinstance(size[0], int) and isinstance(size[1], int)):
                raise ValidationError('All sizes must be integers')
            if not (size[0] >= 0 and size[1] >= 0):
                raise ValidationError('All sizes must be positive')


class MyAccountManager(BaseUserManager):
    def create(self, email, username, password=None):
        if not email:
            raise ValueError("Email adress required")
        if not username:
            raise ValueError("Username required")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Account(AbstractUser):
    email = models.EmailField(verbose_name='email',
                              max_length=64, unique=True)
    username = models.CharField(verbose_name='username',
                                max_length=32, unique=True)
    plan = models.ForeignKey(
        Plan,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

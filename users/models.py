from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
# Create your models here.

class Users(AbstractUser):
    image = models.ImageField(upload_to='users_img', blank=True, null=True, default='default_img/default.png')

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )


    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username

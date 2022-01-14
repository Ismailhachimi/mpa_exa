from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db.models import Q

from accounts.managers import UserManager
from events.models import Event

from datetime import datetime


# TODO : add more data to the user


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    objects = UserManager()

    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def isAvailable(self, start: datetime, end: datetime):
        user_q = Q(**{
            'expert' if self.groups.filter(name='freelancer').exists() else 'client': self
        })

        return not Event.objects.filter(
            user_q &
            (Q(main_start__gte=start, main_start__lt=end) |
                Q(main_end__lte=end, main_end__gt=start) |
                Q(main_start__lte=start, main_end__gte=end))
        ).exists()

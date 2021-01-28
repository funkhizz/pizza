# -*- coding: utf-8 -*-

from django.db import models

from custom_user.models import AbstractEmailUser


class User(AbstractEmailUser):
    USERNAME_FIELD = "email"

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    REQUIRED_FIELDS = ["first_name", "last_name"]

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_short_name(self):
        return "%s" % self.first_name

    def __str__(self):
        return self.email


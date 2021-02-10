# -*- coding: utf-8 -*-

from .email import email_welcome


def send_welcome_email(user_name, user_email, request):
    """
    Purpose: Send a nice welcome email :).
    """

    email_welcome(user_name, user_email, request)

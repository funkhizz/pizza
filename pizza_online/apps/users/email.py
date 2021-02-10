# -*- coding: utf-8 -*-

import socket

from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMultiAlternatives
from django.urls import reverse

from premailer import transform


def prepare_html_email(template, context, base_url):
    initial_html = render_to_string(template, context)
    return transform(initial_html, base_url=base_url)


def email_welcome(user_name, user_email, request):

    text_template = "email/welcome.txt"
    html_template = "email/welcome.html"

    site_url = settings.ROOT_URLCONF
    try:
        short_url = socket.gethostname().replace("www.", "")
    except:
        short_url = 'localhost'

    subject = str(("Welcome to %s" % short_url))

    context = {
        "subject": subject,
        "user_name": user_name,
        "user_email": user_email,
        "login_url": "{0}{1}".format(site_url, reverse(settings.LOGIN_URL)),
        "site_name": settings.CLIENT_NAME,
        "account_email": settings.SUPPORT_EMAIL,
        "site_url": site_url,
        "short_url": short_url,
    }

    text_content = render_to_string(text_template, context)
    html_content = prepare_html_email(html_template, context, site_url)

    msg = EmailMultiAlternatives(
        subject=subject, body=text_content, to=[user_email],
    )
    msg.attach_alternative(html_content, "text/html")

    try:
        msg.send()

    except Exception as e:
        if settings.DEBUG:
            to = settings.WEB_DEV_STAFF
        else:
            to = settings.WEB_DEV_STAFF + settings.CLIENT_STAFF

        send_mail(
            "FAIL: Welcome email",
            str(e),
            settings.DEFAULT_FROM_EMAIL,
            to,
            fail_silently=False,
        )

    return True

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
import smtplib
from functools import wraps

from celery import shared_task
from dalite.celery import app as celery_app

from django.core.mail import send_mail

logger = logging.getLogger("peerinst-models")


def try_async(func):
    """
    Wrap celery functions such that they default to synchronous operation
    if no workers are available
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        available_workers = celery_app.control.ping(timeout=0.5)
        if len(available_workers):
            return func.delay(*args, **kwargs)
        else:
            func(*args, **kwargs)

    return wrapper


@try_async
@shared_task
def send_email_async(*args, **kwargs):
    try:
        send_mail(*args, **kwargs)
    except smtplib.SMTPException:
        err = "There was an error sending the email."
        logger.error(err)

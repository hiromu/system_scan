# -*- coding: utf-8 -*-

import json

from django.conf import settings
from django.http import HttpResponse
from django.core.mail import EmailMessage

def error_as_json_response(form):
    errors = {'status': 'error'}
    for field in form:
        if field.errors:
            errors[field.auto_id] = []
            for error in field.errors:
                errors[field.auto_id].append(error)
    return HttpResponse(json.dumps(errors), mimetype = 'application/json')

def send_notification_mail(recipients, subject, body):
    email = EmailMessage(subject, body, settings.NOTIFICATION_SENDER, bcc = [recipient.email for recipient in recipients])
    email.send(fail_silently = True)

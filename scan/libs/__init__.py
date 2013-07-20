# -*- coding: utf-8 -*-

import json

from django.http import HttpResponse

def error_as_json_response(form):
    errors = {'status': 'error'}
    for field in form:
        if field.errors:
            errors[field.auto_id] = []
            for error in field.errors:
                errors[field.auto_id].append(error)
    return HttpResponse(json.dumps(errors), mimetype = 'application/json')

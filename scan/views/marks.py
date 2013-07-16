# -*- coding: utf-8 -*-

from django.shortcuts import redirect

def index(request, contest_id, genre_id):
    return redirect('scan.views.index')

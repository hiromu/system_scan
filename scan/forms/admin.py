# -*- coding: utf-8 -*-

from scan.models import *

import json

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import CharField, CheckboxSelectMultiple, Form, ModelForm, TextInput
from django.utils.translation import ugettext_lazy as _

class GenreAddForm(ModelForm):
    name = CharField(label = _(u"ジャンル名"))

    class Meta:
        model = Genre
        fields = ('name',)

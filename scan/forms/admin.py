# -*- coding: utf-8 -*-

from scan.models import Genre

from django.contrib.auth.models import User
from django.forms import BooleanField, CharField, ModelForm
from django.utils.translation import ugettext_lazy as _

class GenreAddForm(ModelForm):
    name = CharField(label = _(u"ジャンル名"))

    class Meta:
        model = Genre
        fields = ('name',)

class UserEditForm(ModelForm):
    is_staff = BooleanField(label = _(u'管理者'), required = False)

    class Meta:
        model = User
        fields = ('is_staff',)

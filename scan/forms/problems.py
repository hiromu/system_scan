# -*- coding: utf-8 -*-

from scan.models import *

import json

from django.forms import CharField, CheckboxSelectMultiple, ModelForm, Form, ChoiceField, ModelChoiceField, RadioSelect, TextInput, Textarea, IntegerField
from django.utils.translation import ugettext_lazy as _

problem_types = (
    _(u'ラジオボタン'),
    _(u'チェックボックス'),
    _(u'テキスト'),
    _(u'テキストエリア'),
)

class ProblemEditForm(ModelForm):
    type = ChoiceField(label = _(u'タイプ'), choices = [(i, problem_types[i]) for i in range(len(problem_types))], widget = RadioSelect)
    title = CharField(label = _(u'タイトル'), widget = TextInput)
    statement = CharField(label = _(u'問題文'), widget = Textarea)
    option = CharField(label = _(u'オプション'), widget = Textarea, required = False)
    result = CharField(label = _(u'正解'), widget = Textarea)
    point = IntegerField(label = _(u'配点'))

    class Meta:
        model = Problem
        fields = ('title', 'statement', 'point', 'type', 'option', 'result')

class ProblemDeleteForm(ModelForm):
    class Meta:
        model = Problem
        fields = ()

# -*- coding: utf-8 -*-

from scan.models import *

from django.forms import CharField, CheckboxSelectMultiple, ModelForm, Form, ChoiceField, RadioSelect, TextInput, Textarea, IntegerField
from django.utils.translation import ugettext_lazy as _

problem_types = (
    _(u"ラジオボタン"),
    _(u"チェックボックス"),
    _(u"テキスト"),
    _(u"テキストエリア"),
)

class ProblemEditForm(ModelForm):
    class Meta:
        model = Problem

    type = ChoiceField(label = _(u"タイプ"), choices = [(i, problem_types[i]) for i in range(len(problem_types))], widget = RadioSelect)
    title = CharField(label = _(u"タイトル"), widget = TextInput)
    statement = CharField(label = _(u"問題文"), widget = Textarea)
    option = CharField(label = _(u"オプション"), widget = Textarea)
    result = CharField(label = _(u"正解"), widget = Textarea)
    point = IntegerField(label = _(u"配点"))
    def __init__(self, contest, problem, *args, **kwargs):
        super(ProblemEditForm, self).__init__(*args, **kwargs)
        #genres = contest.genres.all()
        #self.fields['genre'] = ChoiceField(label = _(u"ジャンル"), choices = [(i, genres[i]) for i in range(len(genres))], widget = RadioSelect)

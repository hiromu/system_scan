# -*- coding: utf-8 -*-

import json

from scan.models import Answer

from django.forms import CharField, CheckboxSelectMultiple, ChoiceField, ModelForm, MultipleChoiceField, RadioSelect, Textarea, TextInput
from django.utils.translation import ugettext_lazy as _

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ('answer', 'point')

    def __init__(self, problem, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.problem = problem
        del self.fields['point']

        if problem.type == 0:
            option = json.loads(problem.option)
            self.fields['answer'] = ChoiceField(choices = [(i, option[i]) for i in range(len(option))], widget = RadioSelect)
        elif problem.type == 1:
            option = json.loads(problem.option)
            self.fields['answer'] = MultipleChoiceField(choices = [(i, option[i]) for i in range(len(option))], widget = CheckboxSelectMultiple)
        elif problem.type == 2:
            self.fields['answer'] = CharField(widget = TextInput)
        elif problem.type == 3:
            self.fields['answer'] = CharField(widget = Textarea)

        self.fields['answer'].label = problem.title
        self.fields['answer'].help_text = problem.statement

    def clean(self, *args, **kwargs):
        cleaned_data = super(AnswerForm, self).clean(*args, **kwargs)

        if self.problem.type == 0:
            answer = cleaned_data.get('answer')
            if answer == self.problem.result:
                cleaned_data['point'] = self.problem.point
            else:
                cleaned_data['point'] = 0
        elif self.problem.type == 1:
            answer = cleaned_data.get('answer')
            try:
                answer = [int(i) for i in answer]
            except TypeError:
                self._errors['answer'] = self.error_class([_(u"不正な値です。")])
                del cleaned_data['answer']
            else:
                if answer == json.loads(self.problem.result):
                    cleaned_data['point'] = self.problem.point
                else:
                    cleaned_data['point'] = 0

        return cleaned_data

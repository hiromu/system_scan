# -*- coding: utf-8 -*-

import json

from scan.models import Answer

from django.forms import CharField, CheckboxSelectMultiple, ModelForm, ChoiceField, ModelChoiceField, RadioSelect, TextInput, Textarea, IntegerField

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ('answer', 'point')

    def __init__(self, problem, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.problem = problem

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
        self.fields['answer'].widget.attrs['readonly'] = True
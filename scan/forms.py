# -*- coding: utf-8 -*-

from system_scan.scan.models import *

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import CheckboxSelectMultiple, ModelForm

class ContestForm(ModelForm):
	class Meta:
		model = Contest
		fields = ('name', 'start', 'end')

	def clean(self):
		cleaned_data = super(ContestForm, self).clean()
		start = cleaned_data.get('start')
		end = cleaned_data.get('end')

		if start < datetime.datetime.now():
			self._errors['start'] = self.error_class(['開始日時を現在時刻より前に設定することはできません。'])
			del cleaned_data['start']
		if end < start:
			self._errors['end'] = self.error_class(['終了日時を開始日時より前に設定することはできません。'])
			del cleaned_data['end']

		return cleaned_data

class ContestGenreForm(ModelForm):
	class Meta:
		model = Contest
		fields = ('genres',)

	def __init__(self, *args, **kwargs):
		super(ContestGenreForm, self).__init__(*args, **kwargs)
		self.fields['genres'].help_text = ''
		#self.fields['genres'].widget = CheckboxSelectMultiple()

class PrivilegeForm(ModelForm):
	class Meta:
		model = Privilege
		fields = ('user',)

	def __init__(self, contest, *args, **kwargs):
		super(PrivilegeForm, self).__init__(*args, **kwargs)
		self.fields['user'].queryset = User.objects.exclude(id__in = Privilege.objects.filter(contest = contest).values_list('id', flat = True))

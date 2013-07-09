# -*- coding: utf-8 -*-

from system_scan.scan.models import *

from django.core.exceptions import ValidationError
from django.forms import ModelForm

class ContestForm(ModelForm):
	class Meta:
		model = Contest

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

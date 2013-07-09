# -*- coding: utf-8 -*-

import datetime

from django.contrib import admin
from django.db.models import CharField, DateTimeField, ForeignKey, ManyToManyField, Model, PositiveIntegerField, TextField

class Genre(Model):
	name = CharField(max_length = 50)

	def __unicode__(self):
		return self.name

class Contest(Model):
	name = CharField('名前', max_length = 50)
	start = DateTimeField('開始日時')
	end = DateTimeField('終了日時')
	genres = ManyToManyField(Genre, verbose_name = '問題ジャンル')
	users = ManyToManyField('auth.User', verbose_name = 'ユーザー名')

	def __unicode__(self):
		return self.name

class Problem(Model):
	contest = ForeignKey(Contest)
	genre = ForeignKey(Genre)
	type = PositiveIntegerField()
	statement = TextField()
	option = TextField()
	result = TextField()
	point = PositiveIntegerField()

	def __unicode__(self):
		return self.statement

class Answer(Model):
	user = ForeignKey('auth.User')
	problem = ForeignKey(Problem)
	answer = TextField()
	point = PositiveIntegerField()

	def __unicode__(self):
		return self.answer

class Score(Model):
	user = ForeignKey('auth.User')
	contest = ForeignKey(Contest)
	genre = ForeignKey(Genre)
	score = PositiveIntegerField()

	def __unicode__(self):
		return self.score

admin.site.register(Contest)
admin.site.register(Genre)
admin.site.register(Problem)
admin.site.register(Answer)
admin.site.register(Score)

# -*- coding: utf-8 -*-

import datetime

from django.contrib import admin
from django.db import models

class Genre(models.Model):
	name = models.CharField(max_length = 50)

	def __unicode__(self):
		return self.name

class Contest(models.Model):
	name = models.CharField('名前', max_length = 50)
	start = models.DateTimeField('開始日時')
	end = models.DateTimeField('終了日時')
	genres = models.ManyToManyField(Genre, verbose_name = '問題ジャンル')
	users = models.ManyToManyField('auth.User', verbose_name = 'ユーザー名')

	def __unicode__(self):
		return self.name

class Problem(models.Model):
	contest = models.ForeignKey(Contest)
	genre = models.ForeignKey(Genre)
	type = models.PositiveIntegerField()
	statement = models.TextField()
	option = models.TextField()
	result = models.TextField()
	point = models.PositiveIntegerField()

	def __unicode__(self):
		return self.statement

class Answer(models.Model):
	user = models.ForeignKey('auth.User')
	problem = models.ForeignKey(Problem)
	answer = models.TextField()
	point = models.PositiveIntegerField()

	def __unicode__(self):
		return self.answer

class Score(models.Model):
	user = models.ForeignKey('auth.User')
	contest = models.ForeignKey(Contest)
	genre = models.ForeignKey(Genre)
	score = models.PositiveIntegerField()

	def __unicode__(self):
		return self.score

admin.site.register(Contest)
admin.site.register(Genre)
admin.site.register(Problem)
admin.site.register(Answer)
admin.site.register(Score)

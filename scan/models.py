# -*- coding: utf-8 -*-

import os

from django.contrib import admin
from django.db.models import CharField, DateTimeField, ForeignKey, ManyToManyField, Model, PositiveIntegerField, TextField, ImageField
from django.utils.translation import ugettext_lazy as _

class Genre(Model):
    name = CharField(max_length = 50)

    def __unicode__(self):
        return self.name

class Contest(Model):
    name = CharField(_(u'名前'), max_length = 50)
    start = DateTimeField(_(u'開始日時'))
    end = DateTimeField(_(u'終了日時'))
    genres = ManyToManyField(Genre, verbose_name = _(u'問題ジャンル'))
    users = ManyToManyField('auth.User', verbose_name = _(u'ユーザー名'))

    def __unicode__(self):
        return self.name

class Problem(Model):
    contest = ForeignKey(Contest)
    genre = ForeignKey(Genre)
    type = PositiveIntegerField()
    title = TextField()
    statement = TextField()
    option = TextField(blank = True)
    result = TextField()
    point = PositiveIntegerField()

    def __unicode__(self):
        return self.statement

def get_upload_path(instance, filename):
    return os.path.join('figures', str(instance.problem.id), filename)

class Figure(Model):
    problem = ForeignKey(Problem)
    graphics = ImageField(upload_to = get_upload_path)
    caption = TextField()
    sequence_number = PositiveIntegerField()

    def __unicode__(self):
        return self.caption

class Answer(Model):
    user = ForeignKey('auth.User')
    problem = ForeignKey(Problem)
    answer = TextField()
    point = PositiveIntegerField(null = True)

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

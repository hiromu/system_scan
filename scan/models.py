# -*- coding: utf-8 -*-

import os

from django.contrib import admin
from django.db.models import CharField, DateTimeField, ForeignKey, ManyToManyField, Model, PositiveIntegerField, TextField, ImageField
from django.utils import timezone
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

    def get_state(self):
        now = timezone.now()
        if now < self.start:
            return _(u'あと%(period)sで開始') % {'period': (self.start - now) // 1000000 * 1000000}
        if now >= self.start and now < self.end:
            return _(u'あと%(period)sで終了') % {'period': (self.end - now) // 1000000 * 1000000}
        if now >= self.end:
            return _(u'終了しました')

class Problem(Model):
    contest = ForeignKey(Contest)
    genre = ForeignKey(Genre)
    type = PositiveIntegerField()
    title = TextField()
    statement = TextField()
    option = TextField(blank = True)
    result = TextField()
    point = PositiveIntegerField(_(u'点数'))
    author = ForeignKey('auth.User')
    sequence_number = PositiveIntegerField()

    def __unicode__(self):
        return self.statement

class Comment(Model):
    user = ForeignKey('auth.User')
    problem = ForeignKey(Problem)
    datetime = DateTimeField()
    body = TextField()

class Figure(Model):
    def get_upload_path(instance, filename):
        return os.path.join('figures', str(instance.problem.id), filename)

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

admin.site.register(Contest)
admin.site.register(Genre)
admin.site.register(Problem)
admin.site.register(Figure)
admin.site.register(Answer)

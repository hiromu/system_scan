from django.db import models
from django.contrib import admin

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length = 50)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    admin = models.BooleanField()

    def __unicode__(self):
        return self.user_name

class Contest(models.Model):
    name = models.CharField(max_length = 50)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __unicode__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.name

class Privilege(models.Model):
    user = models.ForeignKey(User)
    contest = models.ForeignKey(Contest)

    def __unicode__(self):
        return self.user

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
    user = models.ForeignKey(User)
    problem = models.ForeignKey(Problem)
    answer = models.TextField()
    point = models.PositiveIntegerField()

    def __unicode__(self):
        return self.answer

class Score(models.Model):
    user = models.ForeignKey(User)
    contest = models.ForeignKey(Contest)
    genre = models.ForeignKey(Genre)
    score = models.PositiveIntegerField()

    def __unicode__(self):
        return self.score

admin.site.register(User)
admin.site.register(Contest)
admin.site.register(Genre)
admin.site.register(Privilege)
admin.site.register(Problem)
admin.site.register(Answer)
admin.site.register(Score)

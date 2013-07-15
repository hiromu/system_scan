# -*- coding: utf-8 -*-

from scan.models import *
from scan.forms.problem import *

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

@login_required
def index(request, contest_id, genre_id):
    contest = get_object_or_404(Contest, pk = contest_id)
    genre = get_object_or_404(Genre, pk = genre_id)
    if not request.user in contest.users.all():
        return redirect('scan.views.index')

    problems = Problem.objects.filter(contest = contest, genre = genre).order_by('id')
    context = {'contest': contest, 'genre': genre, 'problems': problems}
    return render_to_response('problems/index.html', context, RequestContext(request))

@login_required
def add(request, contest_id, genre_id):
    return redirect('scan.views.index')

@login_required
def edit(request, contest_id, genre_id, problem_id):
    contest = get_object_or_404(Contest, pk = contest_id)
    genre = get_object_or_404(Genre, pk = genre_id)
    if not request.user in contest.users.all():
        return redirect('scan.views.index')

    problem = get_object_or_404(Problem, pk = problem_id)
    form = ProblemEditForm(contest, problem)
    context = {'contest_id': contest_id, 'form': form}
    return render_to_response('contests/edit_problem.html', context, RequestContext(request))

@login_required
def delete(request, contest_id, genre_id, problem_id):
    return redirect('scan.views.index')

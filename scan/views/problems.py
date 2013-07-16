# -*- coding: utf-8 -*-

from scan.models import *
from scan.forms.problems import *

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
    contest = get_object_or_404(Contest, pk = contest_id)
    genre = get_object_or_404(Genre, pk = genre_id)
    if not request.user in contest.users.all():
        return redirect('scan.views.index')

    if request.method == 'POST':
        form = ProblemEditForm(request.POST)
        if form.is_valid():
            problem = form.save(commit = False)
            problem.contest = contest
            problem.genre = genre
            problem.save()
            return redirect('scan.views.problems.index', contest_id, genre_id)
    else:
        form = ProblemEditForm()

    context = {'contest': contest, 'genre': genre, 'form': form}
    return render_to_response('problems/edit.html', context, RequestContext(request))

@login_required
def edit(request, contest_id, genre_id, problem_id):
    contest = get_object_or_404(Contest, pk = contest_id)
    genre = get_object_or_404(Genre, pk = genre_id)
    if not request.user in contest.users.all():
        return redirect('scan.views.index')

    problem = get_object_or_404(Problem, pk = problem_id)
    if request.method == 'POST':
        form = ProblemEditForm(request.POST, instance = problem)
        if form.is_valid():
            form.save()
            return redirect('scan.views.problems.index', contest_id, genre_id)
    else:
        form = ProblemEditForm(instance = problem)

    context = {'contest': contest, 'genre': genre, 'form': form, 'is_edit': True}
    return render_to_response('problems/edit.html', context, RequestContext(request))

@login_required
def delete(request, contest_id, genre_id, problem_id):
    contest = get_object_or_404(Contest, pk = contest_id)
    genre = get_object_or_404(Genre, pk = genre_id)
    if not request.user in contest.users.all():
        return redirect('scan.views.index')

    problem = get_object_or_404(Problem, pk = problem_id)
    if request.method == 'POST':
        form = ProblemDeleteForm(request.POST)
        if form.is_valid():
            problem.delete()
            return redirect('scan.views.problems.index', contest_id, genre_id)
    else:
        form = ProblemDeleteForm()

    context = {'contest': contest, 'genre': genre, 'form': form, 'problem': problem}
    return render_to_response('problems/delete.html', context, RequestContext(request))

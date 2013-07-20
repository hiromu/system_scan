# -*- coding: utf-8 -*-

import datetime, json

from scan.forms.problems import ProblemEditForm, ProblemDeleteForm, FigureAddForm
from scan.models import Contest, Genre, Problem, Figure
from scan.libs import error_as_json_response

from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

def check(request, contest_id, genre_id):
    contest = get_object_or_404(Contest, pk = contest_id)
    genre = get_object_or_404(Genre, pk = genre_id)
    if not request.user in contest.users.all():
        return redirect('scan.views.index')
    if datetime.datetime.now() > contest.end:
        return redirect('scan.views.marks.index', contest_id, genre_id)
    return contest, genre

@login_required
def index(request, contest_id, genre_id):
    result = check(request, contest_id, genre_id)
    if not isinstance(result, tuple):
        return result
    contest, genre = result

    problems = Problem.objects.filter(contest = contest, genre = genre).order_by('id')
    context = {'subtitles': [contest.name, _(u'問題設定')], 'contest': contest, 'genre': genre, 'problems': problems}
    return render_to_response('problems/index.html', context, RequestContext(request))

@login_required
def add(request, contest_id, genre_id):
    result = check(request, contest_id, genre_id)
    if not isinstance(result, tuple):
        return result
    contest, genre = result

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

    context = {'subtitles': [contest.name, _(u'問題追加')], 'contest': contest, 'genre': genre, 'form': form}
    return render_to_response('problems/edit.html', context, RequestContext(request))

@login_required
def edit(request, contest_id, genre_id, problem_id):
    result = check(request, contest_id, genre_id)
    if not isinstance(result, tuple):
        return result
    contest, genre = result

    problem = get_object_or_404(Problem, pk = problem_id)
    if request.method == 'POST':
        form = ProblemEditForm(request.POST, instance = problem)
        if form.is_valid():
            form.save()
            return redirect('scan.views.problems.index', contest_id, genre_id)
    else:
        form = ProblemEditForm(instance = problem)
    figure_form = FigureAddForm()

    figures = Figure.objects.filter(problem = problem).order_by('sequence_number')
    context = {'subtitles': [contest.name, _(u'問題編集')], 'contest': contest, 'genre': genre, 'form': form, 'is_edit': True, 'problem': problem, 'figure_form': figure_form, 'figures':figures}
    return render_to_response('problems/edit.html', context, RequestContext(request))

@login_required
def delete(request, contest_id, genre_id, problem_id):
    result = check(request, contest_id, genre_id)
    if not isinstance(result, tuple):
        return result
    contest, genre = result

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

@login_required
def add_figure(request, contest_id, genre_id, problem_id):
    result = check(request, contest_id, genre_id)
    if not isinstance(result, tuple):
        return result
    contest, genre = result
    problem = get_object_or_404(Problem, pk = problem_id)
    if request.method == 'POST':
        form = FigureAddForm(request.POST, request.FILES)
        if form.is_valid():
            figure = form.save(commit = False)
            figure.problem = problem
            figure.sequence_number = 1
            figure.save()
            return HttpResponse(json.dumps({'status': 'success'}) , mimetype = 'application/json')
        else:
            return error_as_json_response(form)
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required
def delete_figure(request, contest_id, genre_id, problem_id, figure_id):
    result = check(request, contest_id, genre_id)
    if not isinstance(result, tuple):
        return result
    contest, genre = result
    problem = get_object_or_404(Problem, pk = problem_id)
    figure = get_object_or_404(Figure, pk = figure_id)
    figure.graphics.delete()
    figure.delete()
    return HttpResponse(json.dumps({'status': 'success'}), mimetype = 'application/json')

@login_required
def get_figures(request, contest_id, genre_id, problem_id):
    result = check(request, contest_id, genre_id)
    if not isinstance(result, tuple):
        return result
    contest, genre = result
    problem = get_object_or_404(Problem, pk = problem_id)
    figures = Figure.objects.filter(problem = problem).order_by('sequence_number')
    figure_list = []
    for figure in figures:
        figure_list.append({'url': figure.graphics.url, 'caption': figure.caption, 'delete': reverse('scan.views.problems.delete_figure', args=[contest_id, genre_id, problem_id, figure.id])})
    return HttpResponse(json.dumps(figure_list), mimetype = 'application/json')

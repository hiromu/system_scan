# -*- coding: utf-8 -*-

import datetime

from scan.forms.contests import AnswerForm
from scan.models import Contest, Genre, Problem

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render_to_response, RequestContext

def check(request, contest_id, genre_id):
    contest = get_object_or_404(Contest, pk = contest_id)
    genre = get_object_or_404(Genre, pk = genre_id)
    if request.user in contest.users.all():
        return redirect('scan.views.contests.index', contest_id)
    if datetime.datetime.now() < contest.start:
        return redirect('scan.views.contests.index', contest_id)
    return contest, genre

@login_required
def index(request, contest_id):
    contest = get_object_or_404(Contest, pk = contest_id)

    context = {'contest': contest, 'genres': contest.genres.all(), 'now': datetime.datetime.now(), 'users': contest.users.all()}
    return render_to_response('contests/index.html', context, RequestContext(request))

@login_required
def problem(request, contest_id, genre_id):
    result = check(request, contest_id, genre_id)
    if not isinstance(result, tuple):
        return result

    return redirect('scan.views.contests.answer', contest_id, genre_id, 0)

@login_required
def answer(request, contest_id, genre_id, problem_id):
    result = check(request, contest_id, genre_id)
    if not isinstance(result, tuple):
        return result
    contest, genre = result

    problem_id = int(problem_id)
    problems = Problem.objects.filter(contest = contest, genre = genre).order_by('id')
    if problem_id > len(problems):
        return redirect('scan.views.contests.index', contest_id)
    elif problem_id == len(problems):
        return redirect('scan.views.contests.finish', contest_id, genre_id)

    try:
        answer = Answer.objects.get(problem = problems[problem_id], user = request.user)
    except ObjectDoesNotExist:
        answer = None

    if request.method == 'POST':
        form = AnswerForm(problems[problem_id], request.POST, instance = answer)
        if form.is_valid():
            answer = form.save(commit = False)
            answer.contest = contest
            answer.genre = genre
            answer.user = request.user
            answer.problem = problems[problem_id]
            answer.save()
            return redirect('scan.views.contests.answer', contest_id, genre_id, problem_id + 1)
    else:
        form = AnswerForm(problems[problem_id], instance = answer)

    context = {'contest': contest, 'form': form, 'genre': genre, 'problem_id': problem_id + 1}
    return render_to_response('contests/answer.html', context, RequestContext(request))

@login_required
def finish(request, contest_id, genre_id):
    result = check(request, contest_id, genre_id)
    if not isinstance(result, tuple):
        return result
    contest, genre = result

    context = {'contest': contest, 'genre': genre}
    return render_to_response('contests/finish.html', context, RequestContext(request))

# -*- coding: utf-8 -*-

from scan.forms.contests import *
from scan.models import Contest, Genre, Problem

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render_to_response, RequestContext

@login_required
def index(request, contest_id):
    contest = get_object_or_404(Contest, pk = contest_id)

    context = {'subtitles': [contest.name], 'contest_id': contest_id, 'genres': contest.genres.all(), 'users': contest.users.all()}
    return render_to_response('contests/index.html', context, RequestContext(request))

@login_required
def problem(request, contest_id, genre_id):
    contest = get_object_or_404(Contest, pk = contest_id)
    genre = get_object_or_404(Genre, pk = genre_id)
    if request.user in contest.users.all():
        return redirect('scan.views.contests.index', contest_id)

    return redirect('scan.views.contests.answer', contest_id, genre_id, 0)

@login_required
def answer(request, contest_id, genre_id, problem_id):
    contest = get_object_or_404(Contest, pk = contest_id)
    genre = get_object_or_404(Genre, pk = genre_id)
    if request.user in contest.users.all():
        return redirect('scan.views.contests.index', contest_id)

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

    context = {'contest_id': contest_id, 'form': form, 'problem_id': problem_id + 1}
    return render_to_response('contests/answer.html', context, RequestContext(request))

@login_required
def finish(request, contest_id, genre_id):
    contest = get_object_or_404(Contest, pk = contest_id)
    genre = get_object_or_404(Genre, pk = genre_id)
    if request.user in contest.users.all():
        return redirect('scan.views.contests.index', contest_id)

    context = {'contest_id': contest_id, 'genre': genre}
    return render_to_response('contests/finish.html', context, RequestContext(request))

@login_required
def problem_manage(request, contest_id):
    contest = get_object_or_404(Contest, pk = contest_id)
    if not request.user.is_staff:
        return redirect('scan.views.index')
    problems = Problem.objects.filter(contest = contest)
    context = {'contest_id': contest_id, 'problems': problems}
    return render_to_response('contests/problem_manage.html', context, RequestContext(request))

@login_required
def edit_problem(request, contest_id, problem_id):
    return redirect('scan.views.index')

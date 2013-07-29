# -*- coding: utf-8 -*-

import datetime

from scan.forms.marks import AnswerForm
from scan.models import Answer, Contest, Figure, Genre, Problem

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

def check(request, contest_id, genre_id):
    contest = get_object_or_404(Contest, pk = contest_id)
    genre = get_object_or_404(Genre, pk = genre_id)
    if not request.user in contest.users.all():
        return redirect('scan.views.contests.index', contest_id)
    if not datetime.datetime.now() > contest.end:
        return redirect('scan.views.contests.index', contest_id)
    return contest, genre

def get_problem(contest, genre, problem_id):
    problems = Problem.objects.filter(contest = contest, genre = genre).order_by('id')

    problem_id = int(problem_id)
    if problem_id >= len(problems):
        raise Http404
    return problems[problem_id]

@login_required
def index(request, contest_id, genre_id):
    result = check(request, contest_id, genre_id)
    if not isinstance(result, tuple):
        return result
    contest, genre = result

    problems = Problem.objects.filter(contest = contest, genre = genre).order_by('id')
    answers = Answer.objects.filter(problem__in = problems)

    array = {}
    for answer in answers:
        if not answer.problem.id in array:
            array[answer.problem.id] = True
        if answer.point == None:
            array[answer.problem.id] = False
    marked = [k for k, v in array.items() if v]

    array = []
    for i in range(len(problems)):
        array.append({'index': i, 'problem': problems[i]})

    context = {'subtitles': [contest.name, genre.name], 'contest': contest, 'genre': genre, 'marked': marked, 'problems': array}
    return render_to_response('marks/index.html', context, RequestContext(request))

@login_required
def problem(request, contest_id, genre_id, problem_id):
    result = check(request, contest_id, genre_id)
    if not isinstance(result, tuple):
        return result
    contest, genre = result

    problem = get_problem(contest, genre, problem_id)
    answers = Answer.objects.filter(problem = problem).order_by('id')

    context = {'subtitles': [contest.name, genre.name],'answers': answers, 'contest': contest, 'genre': genre, 'problem': problem, 'problem_id': int(problem_id), 'problem_index': int(problem_id) + 1}
    return render_to_response('marks/problem.html', context, RequestContext(request))

@login_required
def mark(request, contest_id, genre_id, problem_id, answer_id):
    result = check(request, contest_id, genre_id)
    if not isinstance(result, tuple):
        return result
    contest, genre = result

    problem = get_problem(contest, genre, problem_id)
    answer = get_object_or_404(Answer, pk = answer_id, problem = problem)

    if request.method == 'POST':
        form = AnswerForm(problem, request.POST, instance = answer)
        if form.is_valid():
            answer = form.save()

            answers = Answer.objects.filter(problem = problem).order_by('id')
            for i in range(1, len(answers)):
                if answers[i - 1].id == int(answer_id):
                    return redirect('scan.views.marks.mark', contest_id, genre_id, problem_id, answers[i].id)
            return redirect('scan.views.marks.finish', contest_id, genre_id, problem_id)
    else:
        form = AnswerForm(problem, instance = answer)

    figures = Figure.objects.filter(problem = problem).order_by('sequence_number')
    context = {'subtitles': [contest.name, genre.name], 'answer': answer, 'contest': contest, 'genre': genre, 'figures': figures, 'form': form, 'problem': problem, 'problem_id': int(problem_id), 'problem_index': int(problem_id) + 1}
    return render_to_response('marks/mark.html', context, RequestContext(request))

@login_required
def finish(request, contest_id, genre_id, problem_id):
    result = check(request, contest_id, genre_id)
    if not isinstance(result, tuple):
        return result
    contest, genre = result

    problem = get_problem(contest, genre, problem_id)
    context = {'subtitles': [contest.name, genre.name], 'contest': contest, 'genre': genre, 'problem': problem, 'problem_id': int(problem_id), 'problem_index': int(problem_id) + 1}
    return render_to_response('marks/finish.html', context, RequestContext(request))

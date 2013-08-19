# -*- coding: utf-8 -*-

import datetime, math, json

from scan.forms.contests import AnswerForm
from scan.models import Contest, Genre, Problem, Answer, Figure

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Sum, Q
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
    genres = contest.genres.all()
    total = 0

    data = {}
    for genre in genres:
        data[genre.id] = {'genre': genre}

    problems = Problem.objects.filter(contest = contest).values('genre').annotate(count = Count('id'), max_score = Sum('point'))
    for problem in problems:
        data[problem['genre']]['num_problems'] = problem['count']
        data[problem['genre']]['max_score'] = problem['max_score']

    answers = Answer.objects.filter(problem__contest = contest, user = request.user).values('problem__genre').annotate(count = Count('id'))
    for answer in answers:
        data[answer['problem__genre']]['answer'] = answer['count']

    if datetime.datetime.now() > contest.end:
        problems = Problem.objects.filter(contest = contest).values('genre').annotate(total = Sum('point'))
        for problem in problems:
            data[problem['genre']]['total'] = problem['total']

        answers = Answer.objects.filter(user = request.user, problem__contest = contest).values('problem__genre').annotate(total = Sum('point'))
        for answer in answers:
            data[answer['problem__genre']]['point'] = answer['total']
            if answer['total']:
                total += answer['total']

    genres = []
    for i in sorted(data.keys()):
        for key in ['answer', 'point', 'num_problems', 'total', 'max_score']:
            if not key in data[i]:
                data[i][key] = 0
        genres.append(data[i])

    context = {'subtitles': [contest.name], 'contest': contest, 'genres': genres, 'now': datetime.datetime.now(), 'users': contest.users.all(), 'total': total}
    return render_to_response('contests/index.html', context, RequestContext(request))

@login_required
def problem(request, contest_id, genre_id):
    result = check(request, contest_id, genre_id)
    if not isinstance(result, tuple):
        return result
    contest, genre = result

    if not datetime.datetime.now() > contest.end:
        return redirect('scan.views.contests.answer', contest_id, genre_id, 0)

    problems = Problem.objects.filter(contest = contest, genre = genre).order_by('sequence_number', 'id')
    answers = Answer.objects.filter(user = request.user, problem__contest = contest, problem__genre = genre)

    total = 0
    points = {}
    for problem in problems:
        points[problem.id] = -1
    for answer in answers:
        points[answer.problem.id] = answer.point
        if answer.point:
            total += answer.point

    data = []
    for i in range(len(problems)):
        data.append({'index': i, 'point': points[problems[i].id], 'problem': problems[i]})

    context = {'subtitles': [contest.name, genre.name], 'contest': contest, 'genre': genre, 'problems': data, 'total': total}
    return render_to_response('contests/problem.html', context, RequestContext(request))

@login_required
def answer(request, contest_id, genre_id, problem_id):
    result = check(request, contest_id, genre_id)
    if not isinstance(result, tuple):
        return result
    contest, genre = result

    problem_id = int(problem_id)
    problems = Problem.objects.filter(contest = contest, genre = genre).order_by('sequence_number', 'id')
    if problem_id > len(problems):
        return redirect('scan.views.contests.index', contest_id)
    elif problem_id == len(problems):
        return redirect('scan.views.contests.finish', contest_id, genre_id)

    try:
        answer = Answer.objects.get(problem = problems[problem_id], user = request.user)
    except ObjectDoesNotExist:
        answer = None

    if datetime.datetime.now() > contest.end:
        form = AnswerForm(problems[problem_id], instance = answer, disable = True)
        figures = Figure.objects.filter(problem = problems[problem_id]).order_by('sequence_number')
        context = {'subtitles': [contest.name, genre.name], 'contest': contest, 'form': form, 'genre': genre, 'figures': figures, 'problem': problems[problem_id],'problems_id': range(len(problems)), 'answer': answer, 'problem_id': problem_id}
        return render_to_response('contests/view.html', context, RequestContext(request))
    else:
        if request.method == 'POST':
            form = AnswerForm(problems[problem_id], request.POST, instance = answer)
            if form.is_valid():
                new_answer = form.save(commit = False)
                if new_answer.answer:
                    new_answer.user = request.user
                    new_answer.problem = problems[problem_id]
                    new_answer.save()
                elif answer:
                    answer.delete()
                return redirect('scan.views.contests.answer', contest_id, genre_id, problem_id + 1)
        else:
            form = AnswerForm(problems[problem_id], instance = answer)

        figures = Figure.objects.filter(problem = problems[problem_id]).order_by('sequence_number')
        context = {'subtitles': [contest.name, genre.name], 'contest': contest, 'form': form, 'genre': genre, 'problem_id': problem_id + 1, 'figures': figures}

        if problem_id > 0:
            context['previous'] = problem_id - 1
        return render_to_response('contests/answer.html', context, RequestContext(request))

@login_required
def finish(request, contest_id, genre_id):
    result = check(request, contest_id, genre_id)
    if not isinstance(result, tuple):
        return result
    contest, genre = result

    context = {'subtitles': [contest.name, genre.name], 'contest': contest, 'genre': genre}
    return render_to_response('contests/finish.html', context, RequestContext(request))

@login_required
def ranking(request, contest_id):
    contest = get_object_or_404(Contest, pk = contest_id)
    if not datetime.datetime.now() > contest.end:
        return redirect('scan.views.contests.index', contest_id)

    users = Answer.objects.filter(problem__contest = contest).values('user').annotate(total = Sum('point')).order_by('-total')
    answers = Answer.objects.filter(problem__contest = contest).values('user', 'problem__genre').annotate(total = Sum('point'))
    unmarked = Answer.objects.filter(problem__contest = contest, point = None).count()

    genre_id = []
    genres = []
    for genre in contest.genres.filter(problem__contest = contest).annotate(max_score = Sum('problem__point')):
        genre_id.append(genre.id)
        genres.append({'name': genre.name, 'max_score': genre.max_score})

    score = {}
    for answer in answers:
        if answer['user'] not in score:
            score[answer['user']] = {}
        if answer['total'] != None:
            score[answer['user']][answer['problem__genre']] = answer['total']

    ranking = []
    for i in range(len(users)):
        result = []
        for genre in genre_id:
            if genre in score[users[i]['user']]:
                result.append((genre, score[users[i]['user']][genre]))
            else:
                result.append((genre, 0))
        ranking.append({'index': i + 1, 'user': User.objects.get(pk = users[i]['user']), 'total': users[i]['total'], 'score': result})

        if len(ranking) > 1 and ranking[-2]['total'] == ranking[-1]['total']:
            ranking[-1]['index'] = ranking[-2]['index']

    context = {'contest': contest, 'genre_id': genre_id, 'genres': genres, 'ranking': ranking, 'unmarked': unmarked}
    return render_to_response('contests/ranking.html', context, RequestContext(request))

@login_required
def detail(request, contest_id):
    contest = get_object_or_404(Contest, pk = contest_id)
    if not datetime.datetime.now() > contest.end:
        return redirect('scan.views.contests.index', contest_id)
    if Answer.objects.filter(problem__contest = contest).count() == 0 or Answer.objects.filter(problem__contest = contest, point = None).count() > 0:
        return redirect('scan.views.contests.ranking', contest_id)

    users = User.objects.filter(answer__problem__contest = contest).annotate(total = Sum('answer__point')).order_by('id').order_by('-total')
    ranking = [[i + 1 , users[i]] for i in xrange(len(users))]
    for i in xrange(len(ranking)-1):
        if ranking[i][1].total == ranking[i+1][1].total:
            ranking[i+1][0] = ranking[i][0]
    problems = Problem.objects.filter(contest = contest).annotate(point_sum = Sum('answer__point'))
    for problem in problems:
        if problem.point_sum:
            problem.percentage = float(problem.point_sum) / (problem.point * len(users)) * 100
        else:
            problem.percentage = 0

    genres = contest.genres.filter(problem__contest = contest).annotate(max_score = Sum('problem__point'))
    genre_points = dict([(genre['problem__genre'], genre['point_sum']) for genre in Answer.objects.filter(problem__contest = contest).values('problem__genre').annotate(point_sum = Sum('point'))])
    for genre in genres:
        genre.problems = []
        for i in xrange(len(problems)):
            if problems[i].genre == genre:
                genre.problems.append((len(genre.problems), problems[i]))
        genre.point_sum = genre_points[genre.id]
        genre.percentage = float(genre.point_sum) / (genre.max_score * len(users)) * 100

    summary = {}
    if users:
        summary['average'] = float(sum([user.total for user in users])) / len(users)
        summary['standard_deviation'] = math.sqrt(sum([(float(user.total) - summary['average'])**2 for user in users]) / len(users))
        summary['max_score'] = Problem.objects.filter(contest = contest).aggregate(max_score = Sum('point'))['max_score']
        summary['borders'] = [summary['average'] + summary['standard_deviation'] * (i - 3)  for i in xrange(1, 7)]

    ranking_svg = {'offset': 40, 'height': 1000}
    ranking_svg['lines'] = [(50, ranking_svg['height'] + ranking_svg['offset'] - float(i + 1) * 10 * ranking_svg['height'] / summary['max_score'], 110) for i in xrange(summary['max_score'] / 10 - 1)]
    ranking_svg['bold_lines'] = [(40, ranking_svg['height'] + ranking_svg['offset'] - float(i) * 100 * ranking_svg['height'] / summary['max_score'], 110, i * 100) for i in xrange(summary['max_score'] / 100 + 1)]
    level_colors = ['#3fa9f5', '#7ac943', '#ff931e', '#ff1d25', '#ff7bac', '#bdccd4', '#fcee21']
    ranking_svg['level_borders'] = [[0, ranking_svg['offset'] + (summary['max_score'] - summary['borders'][i]) * ranking_svg['height'] / summary['max_score'], 110, (summary['borders'][i] - (0 if i == 0 else summary['borders'][i-1])) * ranking_svg['height'] / summary['max_score'], level_colors[i], i] for i in xrange(len(summary['borders']))]
    if summary['borders'][5] < summary['max_score']:
        ranking_svg['level_borders'].append([ranking_svg['level_borders'][0][0], ranking_svg['offset'], ranking_svg['level_borders'][0][2], ranking_svg['level_borders'][5][1] - ranking_svg['offset'], level_colors[6], 6])
    for border in ranking_svg['level_borders']:
        if border[1] + border[3] < ranking_svg['offset']:
            border[3] = 0;
        elif border[1] < ranking_svg['offset']:
            border[1] = ranking_svg['offset']

    is_writer = request.user in contest.users.all()

    json_param = {
        'scale_height': ranking_svg['height'],
        'scale_offset': ranking_svg['offset'],
        'max_score': summary['max_score']
    }

    for user in ranking:
        user.append({'standard_score': (float(user[1].total) - summary['average']) * 10 / summary['standard_deviation'] + 50.0})

    context = {'contest': contest, 'ranking': ranking, 'ranking_svg': ranking_svg, 'summary': summary, 'genres': genres, 'is_writer': is_writer, 'json_param': json.dumps(json_param)}
    return render_to_response('contests/detail.html', context, RequestContext(request))

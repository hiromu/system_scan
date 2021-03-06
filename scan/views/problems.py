# -*- coding: utf-8 -*-

import datetime, json, yaml

from scan.forms.contests import AnswerForm
from scan.forms.problems import ProblemEditForm, UploadProblemForm, ProblemDeleteForm, FigureAddForm, CommentForm
from scan.models import Contest, Genre, Problem, Figure, Comment
from scan.libs import error_as_json_response, send_notification_mail

from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
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

    problems = Problem.objects.filter(contest = contest, genre = genre).order_by('sequence_number', 'id')
    context = {'subtitles': [contest.name, _(u'問題設定')], 'contest': contest, 'genre': genre, 'problems': problems}
    return render(request, 'problems/index.html', context)

@login_required
def rearrange(request, contest_id, genre_id):
    result = check(request, contest_id, genre_id)
    if not isinstance(result, tuple):
        return result
    contest, genre = result
    problems = Problem.objects.filter(contest = contest, genre = genre).order_by('sequence_number', 'id')
    if request.method == 'POST' and request.POST['sequence']:
        sequence = json.loads(request.POST['sequence'])
        for problem in problems:
            problem.sequence_number = sequence[str(problem.id)]
            problem.save()
        return redirect('scan.views.problems.index', contest_id, genre_id)

    context = {'subtitles': [contest.name, _(u'問題並べ替え')], 'contest': contest, 'genre': genre, 'problems': problems}
    return render(request, 'problems/rearrange.html', context)

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
            problem.author = request.user
            problem.sequence_number = Problem.objects.filter(contest = contest, genre = genre).count() + 1
            problem.save()
            if 'preview' in request.POST and request.POST['preview'] == 'true':
                return redirect('scan.views.problems.preview', contest_id, genre_id, problem.id)
            else:
                return redirect('scan.views.problems.index', contest_id, genre_id)
    else:
        form = ProblemEditForm()

    context = {'subtitles': [contest.name, _(u'問題追加')], 'contest': contest, 'genre': genre, 'form': form}
    return render(request, 'problems/edit.html', context)

@login_required
def upload(request, contest_id, genre_id):
    result = check(request, contest_id, genre_id)
    if not isinstance(result, tuple):
        return result
    contest, genre = result

    if request.method == 'POST':
        form = UploadProblemForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            valid = True
            for data in yaml.safe_load_all(file.read().decode('utf8')):
                if data['type'] == 'radio':
                    type = 0
                    option = json.dumps(data['list'])
                elif data['type'] == 'checkbox':
                    type = 1
                    option = json.dumps(data['list'])
                elif data['type'] == 'text':
                    type = 2
                elif data['type'] == 'textarea':
                    type = 3
                else:
                    valid = False
                    form._errors['file'] = form.error_class([_(u"不正なタイプです。")])
                    continue
                problem = Problem(
                                  contest = contest,
                                  genre = genre,
                                  type = type,
                                  title = data['title'],
                                  statement = data['question'],
                                  result = data['answer'],
                                  point = data['point'],
                                  author = request.user,
                                  sequence_number = Problem.objects.filter(contest = contest, genre = genre).count() + 1
                                  )
                if type == 0 or type == 1:
                    problem.option = option
                problem.save()
            if valid:
                return redirect('scan.views.problems.index', contest_id, genre_id)
    else:
        form = UploadProblemForm()
    context = {'form': form, 'contest': contest, 'genre': genre}
    return render(request, 'problems/upload.html', context)

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
            if request.POST['figure-sequence']:
                figures = Figure.objects.filter(problem = problem).order_by('sequence_number')
                sequence = json.loads(request.POST['figure-sequence'])
                for figure in figures:
                    figure.sequence_number = sequence[str(figure.id)]
                    figure.save()
            form.save()
            if 'preview' in request.POST and request.POST['preview'] == 'true':
                return redirect('scan.views.problems.preview', contest_id, genre_id, problem_id)
            else:
                return redirect('scan.views.problems.index', contest_id, genre_id)
    else:
        form = ProblemEditForm(instance = problem)
    figure_form = FigureAddForm()
    comment_form = CommentForm()

    comments = Comment.objects.filter(problem = problem).order_by('datetime')
    figures = Figure.objects.filter(problem = problem).order_by('sequence_number')
    context = {'subtitles': [contest.name, _(u'問題編集')], 'contest': contest, 'genre': genre, 'form': form, 'is_edit': True, 'problem': problem, 'figure_form': figure_form, 'figures':figures, 'comment_form': comment_form, 'comments': comments}
    return render(request, 'problems/edit.html', context)

@login_required
def delete(request, contest_id, genre_id, problem_id):
    result = check(request, contest_id, genre_id)
    if not isinstance(result, tuple):
        return result
    contest, genre = result

    problem = get_object_or_404(Problem, pk = problem_id)
    if problem.author != request.user:
        return redirect('scan.views.problems.index', contest_id, genre_id)
    if request.method == 'POST':
        form = ProblemDeleteForm(request.POST)
        if form.is_valid():
            problem.delete()
            return redirect('scan.views.problems.index', contest_id, genre_id)
    else:
        form = ProblemDeleteForm()

    context = {'subtitles': [contest.name, _(u'問題削除')], 'contest': contest, 'genre': genre, 'form': form, 'problem': problem}
    return render(request, 'problems/delete.html', context)

@login_required
def update_point(request, contest_id, genre_id, problem_id):
    result = check(request, contest_id, genre_id)
    if not isinstance(result, tuple):
        return result
    contest, genre = result

    problem = get_object_or_404(Problem, pk = problem_id)
    if request.method == 'POST':
        if request.POST['point']:
            point = int(request.POST['point'])
            problem.point = point
            problem.save()
            return HttpResponse(json.dumps({'status': 'success'}) , mimetype = 'application/json')
        else:
            return HttpResponseBadRequest()
    else:
         return HttpResponseNotAllowed(['POST'])

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
            figure.sequence_number = Problem.objects.filter(contest = contest, genre = genre).count() + 1
            figure.save()
            return HttpResponse(json.dumps({'status': 'success'}) , mimetype = 'application/json')
        else:
            return error_as_json_response(form)

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
        figure_list.append({'id': figure.id, 'url': figure.graphics.url, 'caption': figure.caption, 'delete': reverse('scan.views.problems.delete_figure', args=[contest_id, genre_id, problem_id, figure.id])})

    return HttpResponse(json.dumps(figure_list), mimetype = 'application/json')

@login_required
def post_comment(request, contest_id, genre_id, problem_id):
    result = check(request, contest_id, genre_id)
    if not isinstance(result, tuple):
        return result
    contest, genre = result

    problem = get_object_or_404(Problem, pk = problem_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.problem = problem
            comment.user = request.user
            comment.datetime = datetime.datetime.now()
            comment.save()
            send_notification_mail(contest.users.all(), _(u'[%(contest)s - %(genre)s] (新規コメント) %(title)s') % {'contest': contest.name, 'genre': genre.name, 'title': problem.title}, _(u'%(name)s によって問題にコメントが追加されました。\n%(url)s\n---------------------\n%(body)s') % {'name': u'%(last)s %(first)s (%(name)s)' % {'last': request.user.last_name, 'first': request.user.first_name, 'name': request.user.username}, 'url': ('https' if request.is_secure() else 'http') + '://' + request.get_host() + reverse('scan.views.problems.edit', args = [contest_id, genre_id, problem_id]), 'body': comment.body})
            return redirect('scan.views.problems.edit', contest_id, genre_id, problem_id)
        else:
            return redirect('scan.views.problems.edit', contest_id, genre_id, problem_id)

    return HttpResponseNotAllowed(['POST'])

@login_required
def preview(request, contest_id, genre_id, problem_id):
    result = check(request, contest_id, genre_id)
    if not isinstance(result, tuple):
        return result
    contest, genre = result

    problem = get_object_or_404(Problem, pk = problem_id)
    form = AnswerForm(problem)
    figures = Figure.objects.filter(problem = problem).order_by('sequence_number')
    context = {'subtitles': [contest.name, genre.name], 'contest': contest, 'form': form, 'genre': genre, 'problem': problem, 'problem_id': 0, 'figures': figures, 'is_preview': True}
    return render(request, 'contests/answer.html', context)

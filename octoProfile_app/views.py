from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from urllib.request import urlopen
from django.http import HttpResponseForbidden, Http404

from django.core import serializers
from json import dumps
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied


import json
import locale
import datetime
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

User = get_user_model()


def index(req):
    return render(req, 'index.html')


def searchUser(req):
    username = req.POST['username']
    return redirect(f'/{username}')


def user(req, username):
    username = str.lower(username)

    # Get User Info

    with urlopen(f'https://api.github.com/users/{username}') as response:
        source = response.read()
    data = json.loads(source)

    # Get Limit Call API

    with urlopen(f'https://api.github.com/rate_limit') as response:
        source = response.read()
    limit_data = json.loads(source)

    # Get User Repo Info
    with urlopen(f'https://api.github.com/users/{username}/repos') as response:
        source = response.read()
    sorted_by_stars = json.loads(source)
    sorted_by_forks = json.loads(source)
    sorted_by_size = json.loads(source)

    # Sorted by stars

    def sort_user_repo_by_stars(sorted_by_stars):
        return sorted_by_stars['stargazers_count']

    sorted_by_stars.sort(key=sort_user_repo_by_stars, reverse=True)

    def labels_chart(sorted_by_stars):
        labels = []
        for i in sorted_by_stars:
            labels.append(i['name'])
        labelJSON = dumps(labels)
        return labelJSON

    def value_chart(sorted_by_stars):
        values = []
        for i in sorted_by_stars:
            values.append(i['stargazers_count'])
        return values

    # Sorted by forks

    def sort_user_repo_by_forks(sorted_by_forks):
        return sorted_by_forks['forks']

    sorted_by_forks.sort(key=sort_user_repo_by_forks, reverse=True)

    def labels_fork(sorted_by_forks):
        labels_most_forked = []
        for i in sorted_by_forks:
            labels_most_forked.append(i['language'])
        labels_fork_json = json.dumps(labels_most_forked)
        return labels_fork_json

    def values_fork(sorted_by_forks):
        values_most_forked = []
        for i in sorted_by_forks:
            values_most_forked.append(i['forks'])
        return values_most_forked

    # Sorted by size
    def sort_user_repo_by_size(sorted_by_size):
        return sorted_by_size['size']

    sorted_by_size.sort(key=sort_user_repo_by_size, reverse=True)

    def labels_size(sorted_by_size):
        labels_most_size = []
        for i in sorted_by_size:
            name_label = (i['name'][:7] +
                          '...') if len(i['name']) > 10 else i['name']
            labels_most_size.append(name_label)
        labels_size_json = json.dumps(labels_most_size)
        return labels_size_json

    def values_size(sorted_by_size):
        values_most_size = []
        for i in sorted_by_size:
            values_most_size.append(i['size'])
        return values_most_size

    created_at = data['created_at']
    created_at = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
    created_at = created_at.strftime("%B %d, %Y")

    context = {
        'username': username,
        'data': data,
        'created_at': created_at,
        'limit_data': limit_data,
        'sorted_by_stars': sorted_by_stars[:8],
        'sorted_by_forks': sorted_by_forks[:8],
        'sorted_by_size': sorted_by_size[:8],
        'value_chart': value_chart(sorted_by_stars)[:5],
        'labels_chart': labels_chart(sorted_by_stars[:5]),
        'labels_most_forked': labels_fork(sorted_by_forks),
        'values_most_forked': values_fork(sorted_by_forks),
        'labels_most_size': labels_size(sorted_by_size[:5]),
        'values_most_size': values_size(sorted_by_size)[:5],
    }

    return render(req, 'user.html', context)


def bad_request(req, exception):
    return render(req, '400.html', status=400)


def permission_denied(req, exception):
    return render(req, '403.html', status=403)


def page_not_found(req, exception):
    return render(req, '404.html', status=404)


def server_error(request):
    return render(request, '500.html', status=500)

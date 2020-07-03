from django.shortcuts import render, redirect
from django.http import JsonResponse
from urllib.request import urlopen

from django.core import serializers
from json import dumps
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response

import json
import datetime
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

User = get_user_model()


def index(req):
    labels = ['data', 'hello', 'wassup']
    values = []
    dataJSON = dumps(labels)

    return render(req, 'index.html', {'data': dataJSON})


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

    def value_chart(sorted_by_stars):
        values = []
        for i in sorted_by_stars:
            values.append(i['stargazers_count'])
        return values
    print(value_chart(sorted_by_stars)[:5])

    # Sorted by forks

    def sort_user_repo_by_forks(sorted_by_forks):
        return sorted_by_forks['forks']

    sorted_by_forks.sort(key=sort_user_repo_by_forks, reverse=True)

    # Sorted by size
    def sort_user_repo_by_size(sorted_by_size):
        return sorted_by_size['size']

    sorted_by_size.sort(key=sort_user_repo_by_size, reverse=True)

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
        'value_chart': value_chart(sorted_by_forks)[:5],
    }
    return render(req, 'user.html', context)


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = ["Blue", "Yellow", "Green", "Purple", "Orange"]
        default_items = []
        data = {
            "labels": labels,
            "default": default_items,
        }
        return Response(data)

import re

import json
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse

import search
import imdb_url
# Create your views here.


def make_link(movie_id):
    link = "%s%s" %(imdb_url.query_url, movie_id) 
    return link


def index(request):
    ans = request.GET.get('q', None)
    if ans is None or ans ==  "":
        return HttpResponse("Information request cannot be fulfilled")
    movie_ids, movie_names = search.get_movie_names(ans)
    if movie_ids == []:
        return HttpResponse("No Movies could be Found")
    json_answer = {}
    movie_tuple = zip(movie_ids, movie_names)
    for tup in movie_tuple:
        link = make_link(tup[0])
        json_answer[tup[1]] = link
    return JsonResponse(json_answer) 


def display_info(request):
    ans = request.GET.get('q', None)
    if ans is None or ans ==  "":
        return HttpResponse("Information request cannot be fulfilled")
    ans = re.search(r'tt[0-9]+', ans).group()
    movie_info = search.get_info_on_movie(ans)
    return JsonResponse(movie_info)

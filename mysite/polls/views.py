from django.shortcuts import render
import search
import json
from django.http import JsonResponse
from django.http import HttpResponse
import re
# Create your views here.


def make_link_for_html(movie_id):
    link = '<a href = "http://localhost:8000/polls/info/?q=' \
            + movie_id + '"> Link </a>'
    return link


def make_link(movie_id):
    link = 'http://localhost:8000/polls/info/?q=' \
            + movie_id  
    return link


def index(request):
    ans = request.GET.get('q', 'Nothing')
    movie_ids, movie_names, id_name_map = search.get_movie_names(ans)
    print movie_ids
    answer = ""
    json_answer = {}
    for movie_index in range(0, len(movie_ids)):
        link = make_link_for_html(movie_ids[movie_index])
        link2 = make_link(movie_ids[movie_index])
        ans = link + " " + movie_names[movie_index] + "<br>"
        answer += link + " " + movie_names[movie_index] + "<br>"
        json_answer[movie_names[movie_index]] = link2
    print "\n"
    return JsonResponse(json_answer) 
    return HttpResponse(answer)


def display_info(request):
    ans = request.GET.get('q', 'Nothing')
    ans = re.search(r'tt[0-9]+', ans).group()
    movie_info = search.get_info_on_movie(ans)
    return JsonResponse(movie_info)


from django.http import JsonResponse

import search
import imdb_url


def make_link(movie_id):
    link = "%s%s" % (imdb_url.query_url, movie_id)
    return link


def get_search_param(req):
    req = str(req)
    req = req.replace('>', "").replace("'", "").replace('>', "")
    req = req.split('/')
    return req[len(req) - 1]


def index(request):
    req = get_search_param(request)
    if req == "":
        return JsonResponse({'Error Code': "400"})
    movie_ids, movie_summaries = search.get_movie_names(req)
    if movie_ids == []:
        return JsonResponse({'Error Code':  "404"})
    movie_tuple = zip(movie_ids, movie_summaries)
    movie_objects = []
    for tup in movie_tuple:
        link = make_link(tup[0])
        tup[1]['Link'] = link
        movie_objects.append(tup[1])
    return JsonResponse(movie_objects, safe=False)


def display_info(request):
    req = get_search_param(request)
    if req == "":
        return JsonResponse({'Error Code': "400"})
    movie_info = search.get_info_on_movie(req)
    if movie_info == {}:
        return JsonResponse({'Error Code': "404"})
    return JsonResponse(movie_info)

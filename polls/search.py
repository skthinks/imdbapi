import re

import requests
from more_itertools import unique_everseen

import imdb_url

def get_possible_movie_ids(movie_name):
    url = "%s%s&s=all" % (imdb_url.id_url, movie_name)
    r = requests.get(url)
    movie_id = re.findall(r'tt[0-9]+', r.text, re.M)
    if not movie_id:
        return []
    movie_id_list = list(unique_everseen(movie_id))
    return movie_id_list


def get_name_of_movie(movie_id):
    url = "%s%s/?ref_=fn_al_tt_1" % (imdb_url.name_url, movie_id)
    r = requests.get(url)
    movie_name = re.search(r'<title>.*IMDb', r.text)
    return movie_name.group()


def get_mini_of_movie(movie_id):
    url = "%s%s/?ref_=fn_al_tt_1" %(imdb_url.name_url, movie_id)
    r = requests.get(url)
    movie_summary = {}
    movie_summary['Title'] = get_title(r.text)
    movie_summary['Genres'] = get_genres(r.text)
    movie_summary['Rating'] = get_rating(r.text)
    return movie_summary


def get_movie_names(movie_name):
    movie_id_list = get_possible_movie_ids(movie_name)
    if movie_id_list == []:
        return [],[]
    summary = []
    movie_name_list = []
    for movie_id in movie_id_list:
        movie_name = get_name_of_movie(movie_id)
        movie_name = movie_name.replace("<title>", "").replace("- IMDb", "")
        movie_name_list.append(movie_name) 
        movie_summary = get_mini_of_movie(movie_id)
        summary.append(movie_summary)
    return movie_id_list, summary


def get_title(r_text):
    try:
        movie_name = re.search(r'<title>.*IMDb', r_text)
        movie_name = movie_name.group()
        movie_name = movie_name.replace("<title>", "").replace("- IMDb", "")
    except AttributeError:
        movie_name = "N/A"
    return movie_name


def get_rating(r_text):
    try:
        rating = re.search('ratingValue......', r_text).group()
        rating = re.search(r'[0-9]+.[0-9]+', rating).group()
    except AttributeError:
        rating = "N/A"
    return rating


def get_year(r_text):
    try:
        year = re.search('titleYear.*', r_text).group()
        year = re.search('[0-9]+', year).group()
    except AttributeError:
        year = "N/A"
    return year


def get_directors(r_text):
    directors = []
    directors.append("N/A")
    try:
        directors = re.search('Directed by .*', r_text).group()
        directors = directors.split('With ')
    except:
        directors[0] = "N/A"
    return directors[0]


def get_actors(r_text):
    directors = []
    directors.append("N/A")
    try:
        directors = re.search('Directed by .*', r_text).group()  
        directors = directors.split('With ')
        actors = re.match(r'(?:[^.:;]+[.:;]){1}', directors[1]).group() 
    except:
        actors = "N/A"
    return actors


def get_duration(r_text):
    try:
        duration = re.search('[0-9]h [0-9]+min', r_text).group()
    except:
        duration = "N/A"
    return duration


def get_genres(r_text):
    try:
        genre = re.findall('genre/[A-Z].*inf"', r_text)
        genres = []
        for gen in genre:
            gen = re.search('/.*\?', gen).group()
            gen = gen.replace('/', "").replace('?', "")
            genres.append(gen)
    except:
        genres = []
    return genres


def get_info_on_movie(movie_id):
    url = "http://imdb.com/title/"+movie_id+"/?ref_=fn_al_tt_1"
    r = requests.get(url)
    movie = {}
    movie['Title'] = get_title(r.text)
    movie['Movie Rating'] = get_rating(r.text)
    movie['Release Year'] = get_year(r.text)
    movie['Director'] = get_directors(r.text)
    movie['Duration'] = get_duration(r.text)
    movie['Genres'] = get_genres(r.text)
    movie['Actors'] = get_actors(r.text)
    return movie


def main():
    movie_search = raw_input()
    get_movie_names(movie_search)


# main():

import re

import requests
from BeautifulSoup import BeautifulSoup
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
    url = "%s%s/?ref_=fn_al_tt_1" % (imdb_url.name_url, movie_id)
    r = requests.get(url)
    movie_summary = {}
    movie_summary['Title'] = get_title(r.text)
    movie_summary['Genres'] = get_genres(r.text)
    movie_summary['Rating'] = get_rating(r.text)
    return movie_summary


def get_movie_names(movie_name):
    movie_id_list = get_possible_movie_ids(movie_name)
    if movie_id_list == []:
        return [], []
    summary = []
    for movie_id in movie_id_list:
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
        directors = re.search('Directed by .*', r_text).group( 
        directors = directors.split('With ')
        actors = re.match(r'(?:[^.:;]+[.:;]){1}', directors[1]).group()
    except:
        actors = "N/A"
    return actors


def get_duration(r_text):
    try:
        duration = re.search('[0-9]h [0-9]+min', r_text).group()
    except AttributeError:
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


def get_writers(soup):
    try:
        writers = list(soup.findAll("span", itemprop="creator"))
        writer = []
        for dire in writers:
            if "schema.org/Person" in str(dire):
                direct = BeautifulSoup(str(dire))
                directors = (direct.find("span", itemprop="name")).contents
                writer.append(directors[0])
    except:
        writer = []
    return writer


def get_rated(soup):
    try:
        rated = soup.find("span", itemprop="contentRating").contents
        return rated[0]
    except:
        return "N/A"


def get_awards(soup):
    try:
        awards_list = list(soup.findAll("span", itemprop="awards"))
        sentences = []
        for award in awards_list:
            b = str(award)
            b = b.replace("<b>", "").replace("</b>", "")
            c = BeautifulSoup(b)
            d = c.find("span", itemprop="awards").contents
            e = d[0].replace('\n', ".")
            f = e.replace("\t", "").replace(".", "")
            f = f.split()
            sentence = ' '.join(f)
            sentences.append(sentence)
        final_award = ' '.join(sentences)
    except:
            final_award = "N/A"
    return final_award


def get_info_on_movie(movie_id):
    url = "%s%s/?ref_=fn_al_tt_1" % (imdb_url.name_url, movie_id)
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    movie = {}
    movie['Title'] = get_title(r.text)
    if movie['Title'] == "N/A":
        return {}
    movie['Movie Rating'] = get_rating(r.text)
    movie['Release Year'] = get_year(r.text)
    movie['Director'] = get_directors(r.text)
    movie['Duration'] = get_duration(r.text)
    movie['Genres'] = get_genres(r.text)
    movie['Actors'] = get_actors(r.text)
    movie['Writers'] = get_writers(soup)
    movie['Awards'] = get_awards(soup)
    movie['Rated'] = get_rated(soup)
    return movie

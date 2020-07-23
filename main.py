from flask import Flask
from flask_caching import Cache
import requests


GHIBLI_BASE = 'https://ghibliapi.herokuapp.com/'

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})  # demo purposes only


@app.route('/movies')
@cache.cached(timeout=60)
def list_movies():
    '''List movies and the people in them.'''

    # fetch movies and convert them to dict by resource id
    movies_by_resource_id = {
        GHIBLI_BASE + 'films/' + movie['id']: movie
        for movie in ghibli_request('films')
    }

    # fetch people and add them to movies
    movies_by_resource_id = attach_names(movies_by_resource_id, ghibli_request('people'))

    # very crude formatting
    return '<br>'.join([
        f'{movie["title"]}: {", ".join(movie.get("persons", []))}'
        for movie in movies_by_resource_id.values()
    ])


def attach_names(movies_by_resource_id, persons):
    '''Attach names of people to each movie they have referenced.'''
    for person in persons:
        for movie_resource_id in person['films']:
            if 'persons' not in movies_by_resource_id[movie_resource_id]:
                movies_by_resource_id[movie_resource_id]['persons'] = []
            movies_by_resource_id[movie_resource_id]['persons'].append(person['name'])

    return movies_by_resource_id


def ghibli_request(endpoint):
    '''Send GET request to Ghibli API'''
    return requests.get(GHIBLI_BASE + endpoint).json()

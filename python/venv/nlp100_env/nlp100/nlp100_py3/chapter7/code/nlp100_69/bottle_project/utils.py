from pymongo import MongoClient
from bson.regex import Regex
from bottle import request
from IPython import embed

client = MongoClient('localhost', 27017)
collection = client.nlp100.artists

def search_artists():
    params = { item[0]: item[1] for item in request.forms.items() if item[1]}
    if int(params.pop('name_search_condition')) and 'name' in params:
        params['name'] = Regex(params['name'])
    if int(params.pop('alias_search_condition')) and 'aliases.name' in params:
        params['aliases.name'] = Regex(params['aliases.name'])
    results = collection.find(
            params,
            { '_id': 0, 'name': 1, 'aliases.name': 1, 'rating.value': 1 }
        ).sort(
            [('rating.value', -1)]
        ).limit(50) if params else []
    return results

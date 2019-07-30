from bottle import route, abort, template
from utils import *
from IPython import embed

@route('/artist', method=['GET', 'POST'])
def artist():
    try:
        if request.method == 'GET':
            return template('index', results=None)
        elif request.method == 'POST':
            results = search_artists()
            return template('index', results=results)
        else:
            raise
    except:
        abort(500)

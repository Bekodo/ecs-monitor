#!/usr/bin/python3

import settings
from flask import Flask, g, render_template
from functions import get_db, query_db

app = Flask(__name__)

@app.route('/')
def index():
    title = 'Test'
    context = {}
    for line in query_db('select * from ecs_cluster_blocs_pro'):
        context[line[0]]={'cpu':line[1],'task':line[2]}
    return render_template('char.html', title=title, context=context)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
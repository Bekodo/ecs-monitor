#!/usr/bin/python3

import settings
from flask import Flask, g, render_template
from functions import get_db, query_db

app = Flask(__name__)

@app.route('/')
def index():
    title = 'Check Stats'
    context = {}
    for line in query_db("select * from ecs_cluster_blocs_pro WHERE TIME BETWEEN '2021-01-02 10:45' AND '2021-01-02 15:00'"):
        cpu = (line[1] if line[1] else 0)
        task = (line[2] if line[2] else 0)
        mem = (line[3] if line[3] else 0)
        context[line[0]]={'cpu':cpu,'task':task,'mem':mem}
    return render_template('char.html', title=title, context=context)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
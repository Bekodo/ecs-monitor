#!/usr/bin/python3

import settings
from flask import Flask, g, render_template, redirect, url_for
from functions import get_db, query_db

app = Flask(__name__)

@app.route('/<period>')
def graphs(period):
    periods = {'3h': '-3 hours', '6h': '-6 hours', '12h': '-12 hours', '1d': '-1 days', '3d': '-3 days', '1w': '-7 days', '1m': '-1 month',}
    period = periods.get(period, '-1 days')
    context = {}
    sql = "select TIME,CPU,TASKCOUNT,MEM from ecs_cluster_blocs_pro WHERE TIME > datetime('now', '" + period + "')"
    for line in query_db(sql):
        cpu = (line[1] if line[1] else 0)
        task = (line[2] if line[2] else 0)
        mem = (line[3] if line[3] else 0)
        context[line[0]]={'cpu':cpu,'task':task,'mem':mem}
    return render_template('char.html', title='Graph Stats', context=context)

@app.route('/')
def index():
    return redirect(url_for('graphs',period='1d'))

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
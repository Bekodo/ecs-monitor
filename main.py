#!/opt/local/bin/python3.7

import settings
from functions import periods, metrics, createrrdimagecpu, createrrdimagemem, createrrdimagetask
from flask import Flask, render_template, redirect, url_for, send_file
import rrdtool

app = Flask(__name__,static_url_path='/ecs/blocs-pro/static')

@app.route('/ecs/blocs-pro/img/<metric>/<period>')
def chartimage(metric,period):
    period = (period if period in periods else '1d')
    metric = (metric if metric in metrics else 'cpu')
    if (metric == 'cpu'):
        filename = createrrdimagecpu(settings.RRDFILE, period)
    elif (metric == 'mem'):
        filename = createrrdimagemem(settings.RRDFILE, period)
    elif (metric == 'task'):
        filename = createrrdimagetask(settings.RRDFILE, period)
    else:
        filename = createrrdimagecpu(settings.RRDFILE, period)
    return send_file(filename, mimetype='image/gif')
    
@app.route('/ecs/blocs-pro/<metric>')
def chartpage(metric):
    return render_template('metric.html', title='Graph Stats', metric=metric, metrics=metrics)

@app.route('/ecs/blocs-pro/')
def index():
    return render_template('index.html', title='Graph Stats', metrics=metrics)


#!/opt/local/bin/python3.7

import settings
from functions import periods, metrics, createrrdimagecpu, createrrdimagemem, createrrdimagetask
from flask import Flask, render_template, redirect, url_for, send_file
import datetime
from pytz import timezone
import rrdtool

app = Flask(__name__,static_url_path='/ecs/blocs-pro/static')

@app.route('/ecs/blocs-pro/img/<metric>/<period>')
def chartimage(metric,period):
    fmt = "%d-%m-%Y %H\:%M"
    stimezone = 'Europe/Dublin'
    now_utc = datetime.datetime.now()
    amsterdam_tz = timezone('Europe/Amsterdam')
    now_tz = amsterdam_tz.localize(now_utc)
    dublin_tz = timezone(stimezone)
    now_timezone = now_tz.astimezone(dublin_tz)
    strdate = now_timezone.strftime(fmt)
    period = (period if period in periods else '1d')
    metric = (metric if metric in metrics else 'cpu')
    if (metric == 'cpu'):
        filename = createrrdimagecpu(settings.RRDFILE, period, strdate)
    elif (metric == 'mem'):
        filename = createrrdimagemem(settings.RRDFILE, period, strdate)
    elif (metric == 'task'):
        filename = createrrdimagetask(settings.RRDFILE, period, strdate)
    else:
        filename = createrrdimagecpu(settings.RRDFILE, period, strdate)
    return send_file(filename, mimetype='image/png', cache_timeout=-1)
    
@app.route('/ecs/blocs-pro/<metric>')
def chartpage(metric):
    return render_template('metric.html', title='Graph Stats', metric=metric, metrics=metrics)

@app.route('/ecs/blocs-pro/')
def index():
    return render_template('index.html', title='Graph Stats', metrics=metrics)


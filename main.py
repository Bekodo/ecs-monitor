import settings
from functions import periods, metrics, createrrdimagecpu, createrrdimagemem, createrrdimagetask, strdate
from flask import Flask, render_template, redirect, url_for, send_file, request
import rrdtool

app = Flask(__name__,static_url_path='/ecs/monitor/static')

@app.route('/ecs/monitor/img/<service>/<metric>/<period>')
def chartimage(service, metric, period):
    period = (period if period in periods else '1d')
    metric = (metric if metric in metrics else 'cpu')
    metric = (metric if metric in metrics else 'blocs-pro')
    rrdfile = settings.RRDPATH + service + '_ecs_mem_cpu_task.rrd'

    if (metric == 'cpu'):
        filename = createrrdimagecpu(rrdfile, period, strdate)
    elif (metric == 'mem'):
        filename = createrrdimagemem(rrdfile, period, strdate)
    elif (metric == 'task'):
        filename = createrrdimagetask(rrdfile, period, strdate)
    else:
        filename = createrrdimagecpu(rrdfile, period, strdate)
    return send_file(filename, mimetype='image/png', cache_timeout=-1)
    
@app.route('/ecs/monitor/<service>/<metric>')
def chartpage(service, metric):
    # auth = request.authentication
    # username = auth.username
    username = "hector"
    return render_template('metric.html', metric=metric, service='blocs-pro', username=username)

@app.route('/ecs/monitor/')
def index():
    # auth = request.authentication
    # username = auth.username
    username = "hector"
    return render_template('index.html', service='blocs-pro', username=username)


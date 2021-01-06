import rrdtool
import tempfile
import datetime
from pytz import timezone
from os import path, getcwd

periods = {'1d': 'end-1d', '1w': 'end-1w', '1m': 'end-1m',}
metrics = ['cpu','mem','task']

fmt = "%d-%m-%Y %H\:%M"
stimezone = 'Europe/Dublin'
now_utc = datetime.datetime.now()
amsterdam_tz = timezone('Europe/Amsterdam')
now_tz = amsterdam_tz.localize(now_utc)
dublin_tz = timezone(stimezone)
now_timezone = now_tz.astimezone(dublin_tz)
strdate = now_timezone.strftime(fmt)

filepath = path.abspath(getcwd())
filepath += '/rrdtool/img/'

def createrrdimagecpu(rrdfile, period='1d'):    
    fileimage = filepath + 'cpu-' + period + '.png'
    try:
        rrdtool.graph(str(fileimage), "-s", "%s" % periods.get(period), "-e", "now",
            "--width=380", "--height=140", "--rigid",
            '--alt-autoscale-max', '--lower-limit=0',
            "--title=CPU Metrics",
            "--color=CANVAS#222225",
            "--color=FONT#FFFFFF",
            "--color=BACK#222225",
            "DEF:cpu=%s:cpu:AVERAGE" % rrdfile,
            "LINE1:cpu#00CF00FF:Cpu",
            "AREA:cpu#00CF0033",
            r"GPRINT:cpu:LAST:Current\: %6.2lf %s",
            r"GPRINT:cpu:AVERAGE:Average\: %6.2lf %s",
            r"GPRINT:cpu:MAX:Maximum\: %6.2lf %s\n",
            r"COMMENT:Last updated\: %s\r" % strdate)
    except Exception as e:
        print(e)
    return fileimage

def createrrdimagemem(rrdfile, period='1d'):
    fileimage = filepath + 'mem-' + period + '.png'
    try:
        rrdtool.graph(str(fileimage), "-s", "%s" % periods.get(period), "-e", "now",
            "--width=380", "--height=140", "--rigid",
            '--alt-autoscale-max', '--lower-limit=0',
            "--title=Memory Metrics",
            "--color=CANVAS#222225",
            "--color=FONT#FFFFFF",
            "--color=BACK#222225",
            "DEF:mem=%s:mem:AVERAGE" % rrdfile,
            "LINE1:mem#005199FF:Mem",
            "AREA:mem#00519933",
            r"GPRINT:mem:LAST:Current\:%6.2lf %s",
            r"GPRINT:mem:AVERAGE:Average\:%6.2lf %s",
            r"GPRINT:mem:MAX:Maximum\:%6.2lf %s\n",
            r"COMMENT:Last updated\: %s\r" % strdate)
    except Exception as e:
        print(e)
    return fileimage

def createrrdimagetask(rrdfile, period='1d'):
    fileimage = filepath + 'task-' + period + '.png'
    try:
        rrdtool.graph(str(fileimage), "-s", "%s" % periods.get(period), "-e", "now",
            "--width=380", "--height=140", "--rigid",
            '--alt-autoscale-max', '--lower-limit=0',
            "--title=Tasks Metrics",
            "--color=CANVAS#222225",
            "--color=FONT#FFFFFF",
            "--color=BACK#222225",
            "DEF:task=%s:task:AVERAGE" % rrdfile,
            "LINE1:task#008199FF:Task",
            "AREA:task#00819933",
            r"GPRINT:task:LAST:Current\:%6.2lf %s",
            r"GPRINT:task:AVERAGE:Average\:%6.2lf %s",
            r"GPRINT:task:MAX:Maximum\:%6.2lf %s\n",
            r"COMMENT:Last updated\: %s\r" % strdate)
    except Exception as e:
        print(e)
    return fileimage

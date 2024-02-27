import settings
import rrdtool
from os import path, getcwd
from datetime import datetime
import pytz

periods = settings.PRERIODS
metrics = settings.METRICS
services = settings.SERVICES

filepath = path.abspath(getcwd())
filepath += settings.IMGPATH


def getstrdate(rrdfile):
    fmt = "%d-%m-%Y %H\:%M"
    tsdate = datetime.fromtimestamp(rrdtool.last(rrdfile))
    amsterdam_tz = pytz.timezone('Europe/Amsterdam')
    now_tz = amsterdam_tz.localize(tsdate)
    return now_tz.strftime(fmt)
    

def static_createrrdimagecpu(service, period):
    fileimage = filepath + service + '-cpu-' + period + '.png'
    return fileimage


def static_createrrdimagemem(service, period):
    fileimage = filepath + service + '-mem-' + period + '.png'
    return fileimage


def static_createrrdimagetask(service, period):
    fileimage = filepath + service + '-task-' + period + '.png'
    return fileimage


def createrrdimagecpu(rrdfile, service, period):  
    fileimage = filepath + service + '-cpu-' + period + '.png'
    period = periods.get(period, '1d')
    strdate=getstrdate(rrdfile)
    try:
        rrdtool.graph(str(fileimage), "-s", "%s" % period[0], "-e", "now",
            "--imgformat=PNG",
            "--width=380", "--height=140", "--rigid",
            '--lower-limit=0',
            "--upper-limit=100",
            "--title=CPU Metrics %s - %s " % (period[1], service),
            "--color=CANVAS#222225",
            "--color=FONT#FFFFFF",
            "--color=BACK#222225",
            "--font=TITLE:10:",
            "--font=UNIT:8:",
            "--watermark=Bekodo",
            "--border=0",
            "HRULE:60#ec4646",
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


def createrrdimagemem(rrdfile, service, period):
    fileimage = filepath + service + '-mem-' + period + '.png'
    period = periods.get(period, '1d')
    strdate=getstrdate(rrdfile)
    try:
        rrdtool.graph(str(fileimage), "-s", "%s" % period[0], "-e", "now",
            "--imgformat=PNG",
            "--width=380", "--height=140", "--rigid",
            '--lower-limit=0',
            "--upper-limit=100",
            "--title=Memory Metrics %s - %s " % (period[1], service),
            "--color=CANVAS#222225",
            "--color=FONT#FFFFFF",
            "--color=BACK#222225",
            "--font=TITLE:10:",
            "--font=UNIT:8:",
            "--watermark=Bekodo",
            "--border=0",
            "HRULE:60#ec4646",
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


def createrrdimagetask(rrdfile, service, period):
    fileimage = filepath + service + '-task-' + period + '.png'
    period = periods.get(period, '1d')
    strdate=getstrdate(rrdfile)
    try:
        rrdtool.graph(str(fileimage), "-s", "%s" % period[0], "-e", "now",
            "--imgformat=PNG",
            "--width=380", "--height=140", "--rigid",
            '--alt-autoscale-max',
            '--lower-limit=0',
            "--title=Tasks Metrics %s - %s " % (period[1], service),
            "--color=CANVAS#222225",
            "--color=FONT#FFFFFF",
            "--color=BACK#222225",
            "--font=TITLE:10:",
            "--font=UNIT:8:",
            "--watermark=Bekodo",
            "--border=0",
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
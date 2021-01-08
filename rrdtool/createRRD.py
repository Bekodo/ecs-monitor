#!/opt/local/bin/python3.7

import rrdtool

#Reference https://apfelboymchen.net/gnu/rrd/create/
#http://rrdwizard.appspot.com/

rrdtool.create("ecs_mem_cpu_task.rrd",
"--step", "300",
"--start", "now",
"DS:cpu:GAUGE:600:0:U",
"DS:mem:GAUGE:600:0:U",
"DS:task:GAUGE:600:0:U",
"RRA:AVERAGE:0.5:1:288",
"RRA:MIN:0.5:1:288",
"RRA:MAX:0.5:1:288",
"RRA:LAST:0.5:1:288",
"RRA:AVERAGE:0.5:3:672",
"RRA:MIN:0.5:3:672",
"RRA:MAX:0.5:3:672",
"RRA:LAST:0.5:3:672",
"RRA:AVERAGE:0.5:12:744",
"RRA:MIN:0.5:12:744",
"RRA:MAX:0.5:12:744",
"RRA:LAST:0.5:12:744",
"RRA:AVERAGE:0.5:72:1460",
"RRA:MIN:0.5:72:1460",
"RRA:MAX:0.5:72:1460",
"RRA:LAST:0.5:72:1460")
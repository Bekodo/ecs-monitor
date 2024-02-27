DATE=`date '+%d/%m/%Y %H\:%M'`
echo $DATE

rrdtool graph 'graph.png' \
--width '450' \
--height '150' \
--start end-1d \
--title "CPU and Memory " \
--color "CANVAS#222225" \
--color "FONT#FFFFFF" \
--color "BACK#222225" \
DEF:"cpu=ecs_mem_cpu_task.rrd:cpu:AVERAGE" \
DEF:"mem=ecs_mem_cpu_task.rrd:mem:AVERAGE" \
LINE1:"cpu#00CF00FF:Cpu" \
AREA:"cpu#00CF0033" \
GPRINT:"cpu:LAST:Current\:%8.2lf %s" \
GPRINT:"cpu:AVERAGE:Average\:%8.2lf %s" \
GPRINT:"cpu:MAX:Maximum\:%8.2lf %s\n" \
LINE1:"mem#005199FF:Mem" \
AREA:"mem#00519933" \
GPRINT:"mem:LAST:Current\:%8.2lf %s" \
GPRINT:"mem:AVERAGE:Average\:%8.2lf %s" \
GPRINT:"mem:MAX:Maximum\:%8.2lf %s\n" \
COMMENT:"Last updated\: $DATE\r"
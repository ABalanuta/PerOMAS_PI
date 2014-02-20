# gnuplot script file for plotting bandwidth over time
#!/usr/bin/gnuplot
reset
set terminal pngcairo  transparent enhanced font "arial,10" fontscale 1.0 size 1500,400
set isosamples 3, 3 

#set ytics 0.5
#set mytics 0.1

set xdata time
set timefmt "%Y-%m-%dT%H:%M:%S"
set format x "%H:%M"
set yrange [*: *]
set xrange [* : time(0) ]    # 86400 sec = 1 day
#set xrange [ time(0) - 3600 : time(0) ]    # 86400 sec = 1 day
set label 1 strftime("%T",time(0)) at screen 0.5,0.5   # show the current time

set xlabel "Hour"
set ylabel "Temperature"

set title "Title"
set key below
set grid

plot "/home/artur-adm/lcd/values.txt" using 1:2 title "Temperature" with lines

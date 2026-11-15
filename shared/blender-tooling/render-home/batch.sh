#!/bin/bash
cd /home/user/r; OUT=/home/user/r/out/review; mkdir -p $OUT
L="lonely-mountain mirkwood dragon-mountain lake-town christmas-village christmas-village-mini ocarina-box gustave-dore bag-end gollums-cave"
for l in $L; do /home/user/venv/bin/python scene.py -- specs/$l.json front34 48 1440x960 $OUT > logs/$l-p1.log 2>&1; echo "p1 $l $(date +%T)" >> logs/progress.txt; done
for l in $L; do /home/user/venv/bin/python scene.py -- specs/$l.json back34,close,wide 48 1440x960 $OUT > logs/$l-p2.log 2>&1; echo "p2 $l $(date +%T)" >> logs/progress.txt; done
echo ALLDONE >> logs/progress.txt

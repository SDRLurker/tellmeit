#!/bin/bash 
while [ 1 ] 
do
    pid=`ps -ef | grep "tellmeit.py" | grep -v 'grep' | awk '{print $2'}`
    if [ -z $pid ]; then
        ./tellmeit.py
    fi
    sleep 60
done

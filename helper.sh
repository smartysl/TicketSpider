#!/bin/bash
fromcity=`awk '{print $1}' config`
tocity=`awk '{print $2}' config`
date=`awk '{print $3}' config`
python3 ticket.py ${fromcity} ${tocity} ${date}

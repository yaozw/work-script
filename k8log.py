#!/usr/bin/python3

# a tool is to make k8s log easier to read

import json
import sys
import fileinput
import re

def getLevel(level):
  if level==10:
    return ' TRA '
  elif level==20:
    return ' DBG '
  elif level==30:
    return ' INFO '
  elif level==40:
    return '\033[1;33m WARN \033[0m'
  elif level==50:
    return '\033[1;31m ERROR \033[0m'
  elif level==60:
    return '\033[1;31m FATAL \033[0m'

def esc(str):
  return str.replace('\\',"").replace('""','"')

def parseLines(lines):
  for line in lines:
    # {"version":"1.2.0","timestamp":"2023-12-28T02:24:33.776341534Z","severity":"debug","service_id":"ses-c85-ft5-umb2-eric-ses-etmapigateway","message":"Internal health check hit...","metadata":{"level":20,"category":"etmapigateway.service-launch","transactionId":"","tenantId":"","traceId":"","server-type":"mts","hostname":"ses-c85-ft5-umb2-eric-ses-etmapigateway-220.2.100-656d6ccdl2xmr","pid":24}}

    try:
      logObj = json.loads(line)
      level = ''
      if 'message' in logObj:
        print(logObj['timestamp'],  logObj['message'])
      elif 'msg' in logObj:
       level = getLevel(logObj['level'])
       print(logObj['time'] + ' ' + level + ' ' + logObj['msg'])
      elif 'level' in logObj['metadata']:
       level = getLevel(logObj['metadata']['level'])
       print(logObj['timestamp'] + ' ' + level + ' ' + logObj['message'])
    except:
      #print(line, 'can not parse:')
      continue   


if __name__ == '__main__':
  if len(sys.argv) == 1:
    try:
      fileinput.filename()
    except:
      print('a tool is to make k8s log easier to read')
      print('usage: k8log [logfilepath]')
      print('       kubectl logs -f $podname |k8log')
      sys.exit(1) 

  if len(sys.argv) == 1:
    #pipe
    with fileinput.input() as lines:
      print(lines)
      parseLines(lines)
  else:
    #file
    fPath = sys.argv[1] 
    with open(fPath) as f:
      parseLines(f.readlines())




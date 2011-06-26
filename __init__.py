from fabulous import *
import json


try:
  f = open("%s/hosts.json" % file_path, 'r')
  env.hosts = [str(x) for x in json.loads(f.read())['hosts']]
  f.close()
  print 'loaded'
except IOError:
  env.hosts = []
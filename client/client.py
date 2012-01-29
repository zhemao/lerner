#!/usr/bin/env python

import redis
import json
import sys
import os
import pynotify as notify

if __name__ == '__main__':
    notify.init("notistream")

    if len(sys.argv) < 2:
        f = open(os.path.expanduser('~/.notistream.json'))
    else:
        f = open(sys.argv[1])

    config = json.load(f)

    r = redis.StrictRedis(host=config['host'], port=config['port'])
    ps = r.pubsub()
    ps.subscribe(config['channels'])

    for msg in ps.listen():
        if msg['type'] == 'message':
            n = notify.Notification(msg['data'])
            n.show()


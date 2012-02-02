#!/usr/bin/env python

from flask import Flask, request
from gevent import monkey; monkey.patch_socket()
from gevent.wsgi import WSGIServer
import redis
import json

r = redis.StrictRedis()

app = Flask(__name__)
app.config.from_object('settings')

r = redis.StrictRedis(host=app.config.get('PUBSUB_HOST', '127.0.0.1'),
                      port=app.config.get('PUBSUB_PORT', 6379))

auth = app.config.get('AUTH', '')
if auth:
    r.execute_command('auth', auth)

@app.route('/', methods=['POST'])
def generic():
    message = request.form['message']
    channel = request.form['channel']

    notified = r.publish(channel, message)
    
    return str(notified)

@app.route('/github', methods=['POST'])
def github():
    payload = json.loads(request.form['payload'])
    owner = payload['repository']['owner']['name']
    repo_name = owner + '/' + payload['repository']['name']
    headcommit = payload['commits'][0]
    commit_message = headcommit['message']
    author = headcommit['author']['name']

    message = '%s commited to %s: %s' % (author, repo_name, commit_message)

    notified = r.publish(repo_name, message)

    return str(notified)

if __name__ == '__main__':
    port = app.config.get('WEB_PORT', 8080)
    
    WSGIServer(('0.0.0.0', port), app).serve_forever()

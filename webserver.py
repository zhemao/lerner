#!/usr/bin/env python

from flask import Flask, request
from gevent import monkey; monkey.patch_socket()
from gevent.wsgi import WSGIServer
import redis
import json

r = redis.StrictRedis()

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/github', methods=['POST'])
def github():
    payload = json.loads(request.form['payload'])
    owner = payload['repository']['owner']['name']
    repo_name = owner + '/' + payload['repository']['name']
    repo_url = payload['repository']['url']
    headcommit = payload['commits'][0]
    commit_message = headcommit['message']
    author = headcommit['author']['name']

    message = '%s commited to %s: %s' % (author, repo_name, commit_message)

    print(message)
    
    r.publish(repo_url, message)

    return 'OK'

if __name__ == '__main__':
    WSGIServer(('0.0.0.0', 8080), app).serve_forever()

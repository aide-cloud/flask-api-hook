#!/bin/python3
import json
import os

import flask
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


# gitHub hook just the push event
@app.route('/github', methods=['POST'])
def github_hook():
    # get all body data
    data = request.get_json()
    # data to json utf-8
    data = json.dumps(data, ensure_ascii=False)
    print (data)
    if 'ref' in data and data['ref'] == 'refs/heads/master':
        # git pull
        git_pull()

    return 'Github hook received'


# check if the app is running
@app.route('/check')
def status():
    # get user ip
    ip = request.remote_addr
    # get user agent
    user_agent = request.headers.get('User-Agent')
    # get user host
    host = request.headers.get('Host')
    # get user port
    port = request.headers.get('X-Forwarded-Port')

    return flask.jsonify({'ip': ip, 'user_agent': user_agent, 'host': host, 'port': port})


# git pull shell
def git_pull():
    # execute shell
    print ('git pull')
    os.system('git pull')
    return 'git pull'


if __name__ == '__main__':
    app.run("0.0.0.0", port=18080, debug=True)

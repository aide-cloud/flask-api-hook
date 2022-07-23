#!/bin/python3
import json
import os

from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    # view index.html
    return render_template('index.html')


# gitHub hook just the push event
@app.route('/github', methods=['POST'])
def github_hook():
    # get all body data
    data = request.get_json()
    # data to json utf-8
    data_json = json.dumps(data, ensure_ascii=False)
    print (data_json)
    if 'res' in data and data['ref'] == 'refs/heads/master':
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

    return jsonify({'ip': ip, 'user_agent': user_agent, 'host': host, 'port': port})


# response
def response(status=200, message="OK", data=None):
    if data is None:
        data = []
    return jsonify({
        'status': status,
        'message': message,
        'data': data
    })


# add_users
@app.route('/add_users', methods=['GET', 'POST', 'DELETE', 'PUT'])
def add_users():
    # get all body data
    try:
        # method
        if request.method != 'POST':
            return response(status=405, message="request method must be POST")
        data = request.get_json()
        if 'name' in data and 'age' in data:
            aeg = int(data['age'])
            if data['name'] != '' and (2 < len(data['name']) or 16 > len(data['name'])) and aeg >= 18:
                # add user
                return response(200, 'OK', data)
        return response(400, 'Bad Request')
    except Exception:
        return response(400, 'Bad Request', 'Age must be an integer')


# delete_users
@app.route('/delete_users', methods=['GET', 'POST', 'DELETE', 'PUT'])
def delete_users():
    try:
        # method
        if request.method != 'DELETE':
            return response(400, "request method must be DELETE")
        # get param id
        id = request.args.get('id')
        idInt = int(id)
        if idInt is None or idInt <= 0:
            return response(status=400, message="Bad Request")
        return response(200, "delete user success, id: " + str(idInt))
    except Exception as e:
        return response(status=400, message="Bad Request" + str(e))


# update_user
@app.route('/update_user', methods=['GET', 'POST', 'DELETE', 'PUT'])
def update_user():
    try:
        # method put
        if request.method != 'PUT':
            return response(status=400, message="request method must be PUT")
        # get all body data
        data = request.get_json()
        if "id" in data:
            id = int(data['id'])
            if id is not None and id >= 0:
                return response(200, "update user success, id: " + str(id))

        return response(status=400, message="Bad Request")
    except Exception as e:
        return response(status=400, message="Bad Request" + str(e))


# get_users
@app.route('/get_users', methods=['GET', 'POST', 'DELETE', 'PUT'])
def get_users():
    # get param id
    try:
        # method get
        if request.method != 'GET':
            return response(status=400, message="request method must be GET")
        id = request.args.get('id')
        idInt = int(id)
        if idInt is None or idInt <= 0:
            return response(status=400, message="Bad Request1")
        data = []
        for i in range(idInt):
            data.append({'id': i, 'name': 'user_' + str(i), 'age': i})
        return response(200, "get user success, id: " + str(idInt), data)
    except Exception as e:
        return response(status=400, message="Bad Request" + str(e))


# git pull shell
def git_pull():
    # execute shell
    print ('git pull')
    os.system('git pull')
    return 'git pull'


if __name__ == '__main__':
    app.run("0.0.0.0", port=18080, debug=True)

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
    # get the commit hash
    print(data)
    return 'Github hook received'


if __name__ == '__main__':
    app.run()

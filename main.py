import json
from flask import request
from flask import Flask, render_template, jsonify


application = Flask(__name__)


@application.route("/")
def index():
    return render_template("index.html")


@application.route("/checkLogin", methods=["POST"])
def check_login():
    output = request.get_json()
    user_and_pass = json.loads(output)

    from api.LoginExtract import login
    _, is_login = login(user_and_pass["user"], user_and_pass["pass"])

    return jsonify('', render_template("checkLogin.html", x=str(is_login)))


if __name__ == '__main__':
    application.run(debug=True)

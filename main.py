from flask import request, redirect, url_for
from flask import Flask, render_template


application = Flask(__name__)


@application.route("/")
def index():
    return render_template("index.html")


@application.route("/loginFailed", methods=["POST", "GET"])
def check_login():
    output = request.form.to_dict()
    print(output)

    from api.LoginExtract import login
    _, is_login = login(output["username"], output["password"])

    if is_login:
        return redirect(url_for('login_successfully'))
    else:
        return render_template("loginFailed.html")


@application.route("/timeTable", methods=["POST", "GET"])
def login_successfully():
    return render_template("loginSuccessfully.html")


if __name__ == '__main__':
    application.run(debug=True)

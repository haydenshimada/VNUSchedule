import os
import flask
from api.gg_api import event_body

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

from flask import request, redirect, url_for
from flask import Flask, render_template
import flask

application = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
application.secret_key = b'_5#y2L"F4Q871-rl38fuz\n\xec]/'

data = []


@application.route("/")
def index():
    return redirect(url_for('login'))


@application.route("/dang-nhap")
def login():
    return render_template("index.html")

@application.route("/error")
def error():
    return render_template("error.html")


@application.route("/loi-dang-nhap", methods=["POST", "GET"])
def check_login():
    output = request.form.to_dict()

    from api.LoginExtract import login
    global data
    is_login, data = login(output["username"], output["password"])

    if is_login:
        return redirect(url_for('login_successfully'))
    else:
        if data == 'Username or Password is incorrect!':
            return render_template("loginFailed.html")
        else:
            return redirect(url_for('error'))


# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "api/credentials.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/calendar']
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'


@application.route('/create_calendar_in_background', methods=['GET', 'POST'])
def create_calendar_in_background():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    service = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

    event = service.events().insert(calendarId='primary', body=event_body).execute()

    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.redirect(flask.url_for('index'))


@application.route('/authorize', methods=['GET', 'POST'])
def authorize():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    flask.session['state'] = state

    return flask.redirect(authorization_url)


@application.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = flask.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.redirect(flask.url_for('create_calendar_in_background'))


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


@application.route("/thoi-khoa-bieu", methods=["POST", "GET"])
def login_successfully():
    header = '''
    <!DOCTYPE html>
<html lang="vi">
<head>
    <meta name = "viewport" content="width=device-width, initial-scale=1.0">
    <meta charset="utf-8">
    <title>VNUSchedule</title>
    <link rel="icon" href="{{ url_for('static', filename='image/icon.png') }}">
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style/mainPage.css') }}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
</head>
<body>
    <section id="header">
        <div class="imageHeader">
            <img src="{{ url_for('static', filename='image/logo.png') }}" alt="">
        </div>
        <div class="h1Header">
            <h1>Cổng thông tin đào tạo Đại học</h1>
        </div>
        <div id="logout">
            <form action="/dang-nhap">
                <button type="submit" id="logout_button">Đăng xuất</button>
            </form>
        </div>
    </section>
    <button id="convert2Img" onclick="downloadTimeTable()">Lưu hình ảnh</button>
    
    <form action="/authorize" method="post">
        <button type="submit" id="convert2Cal">Lưu vào<br>Google Calendar </button>
    </form>
    <section>
        <div id="timeTable">'''

    content = '''
            <table>
                <tr id="tableHeader">
                    <th id="sequenceNumber">Tiết</th>
                    <th id="timePeriod">Thời gian học</th>
                    <th>Thứ 2</th>
                    <th>Thứ 3</th>
                    <th>Thứ 4</th>
                    <th>Thứ 5</th>
                    <th>Thứ 6</th>
                    <th>Thứ 7</th>
                </tr>'''

    # time_table_matrix = [["", "", "", "", "", ""],
    #                      ["", "", "", "", "", "Pháp luật và đạo đức nghề nghiệp trong CNTT"],
    #                      ["", "", "Bóng chuyền 1", "", "", "Pháp luật và đạo đức nghề nghiệp trong CNTT"],
    #                      ["", "", "Bóng chuyền 1", "", "", ""],
    #                      ["", "", "", "", "", ""],
    #                      ["", "", "", "", "", ""],
    #                      ["Nguyên lý hệ điều hành", "", "Công nghệ phần mềm", "", "", "Kinh tế chính trị Mác-Lênin"],
    #                      ["Nguyên lý hệ điều hành", "", "Công nghệ phần mềm", "", "", "Kinh tế chính trị Mác-Lênin"],
    #                      ["Nguyên lý hệ điều hành", "", "Công nghệ phần mềm", "", "", ""],
    #                      ["Nguyên lý hệ điều hành", "", "Trí tuệ nhân tạo", "", "Mạng máy tính", ""],
    #                      ["", "", "Trí tuệ nhân tạo", "", "Mạng máy tính", ""],
    #                      ["", "", "Trí tuệ nhân tạo", "", "Mạng máy tính", ""]]

    if not data:
        return redirect(url_for("index"))

    from api import ExcelExport
    from api.LoginExtract import table_extract
    time_table_matrix = ExcelExport.html_table(table_extract(data))

    is_fill = [([False] * len(time_table_matrix[0])) for _ in range(len(time_table_matrix))]

    default_color = ['FF6363', 'FFAB76', 'FFFDA2', 'BAFFB4', '76E3FF', 'A275E3', 'F3D1F4', 'FFFDE1']
    color_index = 0
    subject_list = []
    for i in range(len(time_table_matrix)):
        content += '''
                <tr>
                    <td class="sequenceNumber">{no}</td>
                    <td class="timePeriod">{hour}h - {hour}h50</td>'''.format(no=i + 1, hour=i + 7)
        for j in range(len(time_table_matrix[i])):
            subject = time_table_matrix[i][j]
            if not is_fill[i][j]:
                if subject != "" and subject not in subject_list:
                    subject_list.append(subject)
                    check_below = i + 1
                    while (check_below < len(time_table_matrix)) and (time_table_matrix[check_below][j] == subject):
                        is_fill[check_below][j] = True
                        check_below += 1
                    content += '''
                    <td rowspan="{size}" style="background-color: #{color}">{subject}</td>'''.format(size=check_below - i, color=default_color[color_index], subject=subject)
                    is_fill[i][j] = True
                    color_index = (color_index + 1) % len(default_color)
                else:
                    content += '''
                    <td></td>'''
                    is_fill[i][j] = True
        content += '''
                </tr>'''
    content += '''
            </table> 
            <div id='emptySpace'></div>
        </div> 
    </section>'''
    header += content
    header += '''
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/dom-to-image/2.6.0/dom-to-image.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/g/filesaver.js"></script>
    <script src="{{ url_for('static', filename='javascript/mainPage.js') }}"></script>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
    <!--    <script type=text/javascript>-->
<!--    #     $(function() {-->
<!--    #       $('#convert2Cal').on('click', function(e) {-->
<!--    #         e.preventDefault()-->
<!--    #         $.getJSON('/create_calendar_in_background',-->
<!--    #             function(data) {-->
<!--    #           //do nothing-->
<!--    #         });-->
<!--    #         return false;-->
<!--    #       });-->
<!--    #     });-->
<!--    # </script>-->
    </body>
</html>
    '''

    file = open("templates/loginSuccessfully.html", "w", encoding="utf-8")
    file.write(header)
    file.close()

    return render_template("loginSuccessfully.html")


if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification.
    # ACTION ITEM for developers:
    #     When running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

    # application.run(debug=True)
    application.run('localhost', 8080, debug=True)

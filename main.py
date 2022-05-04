import csv

from flask import request, redirect, url_for
from flask import Flask, render_template
from api.gg_api import create_calendar
import numpy as np

application = Flask(__name__)


data = []


@application.route("/")
def index():
    return render_template("index.html")


@application.route('/create_calendar_in_background')
def create_calendar_in_background():
    create_calendar()
    return "nothing"


@application.route("/loginFailed", methods=["POST", "GET"])
def check_login():
    output = request.form.to_dict()

    from api.LoginExtract import login
    global data
    data, is_login = login(output["username"], output["password"])

    # data = np.matrix(data)
    # with open('sample.csv', 'w') as f:
    #     mywriter = csv.writer(f, delimiter=',')
    #     mywriter.writerows(data)

    if is_login:
        return redirect(url_for('login_successfully'))
    else:
        return render_template("loginFailed.html")


@application.route("/timeTable", methods=["POST", "GET"])
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
    </section>
    <button id="convert2Img" onclick="downloadTimeTable()">Save as PNG</button>
    <button id="convert2Cal">Save to Google Calendar</button>
    <section>
        <div id="timeTable">
    '''

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
            </tr>
    '''

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

    from api import ExcelExport
    from api.LoginExtract import table_extract
    time_table_matrix = ExcelExport.html_table(table_extract(data))

    is_fill = [([False] * len(time_table_matrix[0])) for _ in range(len(time_table_matrix))]

    subject_list = []
    for i in range(len(time_table_matrix)):
        content += '''
            <tr>
                <td class="sequenceNumber">{no}</td>
                <td class="timePeriod">{hour}h - {hour}h50</td>
        '''.format(no=i+1, hour=i+7)
        for j in range(len(time_table_matrix[i])):
            subject = time_table_matrix[i][j]
            if not is_fill[i][j]:
                if subject != "" and subject not in subject_list:
                    subject_list.append(subject)
                    check_below = i + 1
                    while (check_below < len(time_table_matrix)) and (time_table_matrix[check_below][j] == subject):
                        is_fill[check_below][j] = True
                        check_below += 1
                    content += '<td rowspan="{size}">{subject}</td>'.format(size=check_below - i, subject=subject)
                    is_fill[i][j] = True
                else:
                    content += '<td></td>'
                    is_fill[i][j] = True
        content += "</tr>"
    content += "</table> </div> </section>"
    header += content
    header += '''
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/dom-to-image/2.6.0/dom-to-image.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/g/filesaver.js"></script>
    <script src="{{ url_for('static', filename='javascript/mainPage.js') }}"></script>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
    <script type=text/javascript>
        $(function() {
          $('#convert2Cal').on('click', function(e) {
            e.preventDefault()
            $.getJSON('/create_calendar_in_background',
                function(data) {
              //do nothing
            });
            return false;
          });
        });
    </script>
    </body>
</html>
    '''

    file = open("templates/loginSuccessfully.html", "w", encoding="utf-8")
    file.write(header)
    file.close()

    return render_template("loginSuccessfully.html")


if __name__ == '__main__':
    application.run(debug=True)

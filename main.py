from flask import request, redirect, url_for
from flask import Flask, render_template

application = Flask(__name__)


@application.route("/")
def index():
    return render_template("index.html")


@application.route("/loginFailed", methods=["POST", "GET"])
def check_login():
    output = request.form.to_dict()

    from api.LoginExtract import login
    _, is_login = login(output["username"], output["password"])

    if is_login:
        return redirect(url_for('login_successfully'))
    else:
        return render_template("loginFailed.html")


@application.route("/timeTable", methods=["POST", "GET"])
def login_successfully():
    header = '''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta name = "viewport" content="width=device-width, initial-scale=1.0">
    <meta charset="utf-8">
    <title>VNUSchedule</title>
    <link rel="icon" href="{{ url_for('static', filename='image/icon.png') }}">
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style/index.css') }}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <style>
        #timeTable {
            margin-top: 20px;
            align-items: center;
        }
            
        table {
            margin-left: auto; 
            margin-right: auto;
        }
        
        table, tr, td {
            border: 1px solid black;
        }

        td {
            width: 16.6%;
            height: 50px;
            text-align: center;
        }
    </style>
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
    <button id="convert2Img">Save as PNG</button>
    <section>
        <div id="timeTable">
    '''

    content = "<table>"

    time_table_matrix = [["", "", "", "", "", ""],
                         ["", "", "", "", "", "Pháp luật"],
                         ["", "", "Bóng chuyền 1", "", "", "Pháp luật"],
                         ["", "", "Bóng chuyền 1", "", "", ""],
                         ["", "", "", "", "", ""],
                         ["", "", "", "", "", ""],
                         ["Nguyên lý hệ điều hành", "", "Công nghệ phần mềm", "", "", "Kinh tế"],
                         ["Nguyên lý hệ điều hành", "", "Công nghệ phần mềm", "", "", "Kinh tế"],
                         ["Nguyên lý hệ điều hành", "", "Công nghệ phần mềm", "", "", ""],
                         ["Nguyên lý hệ điều hành", "", "Trí tuệ nhân tạo", "", "Mạng máy tính", ""],
                         ["", "", "Trí tuệ nhân tạo", "", "Mạng máy tính", ""],
                         ["", "", "Trí tuệ nhân tạo", "", "Mạng máy tính", ""]]
    is_fill = [([False] * len(time_table_matrix[0])) for _ in range(len(time_table_matrix))]

    subject_list = []
    for i in range(len(time_table_matrix)):
        content += "<tr>"
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
    
    <script src="{{ url_for('static', filename='javascript/html2canvas.min.js') }}"></script>
    <script>
        document.getElementById("convert2Img").onclick = function () {
            const screenshotTarget = document.getElementById("timeTable");
            html2canvas(screenshotTarget).then((canvas) => {
                const base64Image = canvas.toDataURL("image/png");
                var anchor = document.createElement("a");
                anchor.setAttribute("href", base64Image);
                anchor.setAttribute("download", "Time Table.png");
                anchor.click();
                anchor.remove();
            });
        };
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

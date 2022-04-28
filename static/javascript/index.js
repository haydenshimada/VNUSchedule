var username = document.forms['form']['username'];
var password = document.forms['form']['password'];

var user_error = document.getElementById('user_error');
var pass_error = document.getElementById('pass_error');

var login_failed = document.getElementById('login_failed');

username.addEventListener('textInput', user_verify);
password.addEventListener('textInput', pass_verify);

function validated() {
    const user = username.value;
    const pass = password.value;

    if(user.length < 8) {
        username.style.border = "1px solid red";
        user_error.style.display = 'block';
        username.focus();
        return false;
    }

    if(pass.length < 6) {
        password.style.border = "1px solid red";
        pass_error.style.display = 'block';
        password.focus();
        return false;
    }

    // const dict_values = {user, pass};
    // const s = JSON.stringify(dict_values);
    // console.log(s);
    // $.ajax({
    //     url:"/checkLogin",
    //     type:"post",
    //     contextType: "application/json",
    //     data: JSON.stringify(s),
    //     success: function (data) {
    //         $(checkLogin).replaceWith(data);
    //     }
    // });

    if (document.getElementById("checkLogin").value === "False") {
        login_failed.style.display = "block";
        username.value = "";
        password.value = "";
        username.focus();
        return false;
    }
}

function user_verify() {
    if (username.value.length >= 7) {
        username.style.border = "1px solid black";
        user_error.style.display = 'none';
        return true;
    }
}

function pass_verify() {
    if (password.value.length >= 5) {
        password.style.border = "1px solid black";
        pass_error.style.display = 'none';
        return true;
    }
}
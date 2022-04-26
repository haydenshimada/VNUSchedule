function login() {
    document.getElementById("login_failed").style.display = 'block';
}

var username = document.forms['form']['username'];
var password = document.forms['form']['password'];

var user_error = document.getElementById('user_error');
var pass_error = document.getElementById('pass_error');

var login_failed = document.getElementById('login_failed');

username.addEventListener('textInput', user_verify);
password.addEventListener('textInput', pass_verify);

function validated() {
    if(username.value.length < 8) {
        username.style.border = "1px solid red";
        user_error.style.display = 'block';
        username.focus();
        return false;
    }

    if(password.value.length < 6) {
        password.style.border = "1px solid red";
        pass_error.style.display = 'block';
        password.focus();
        return false;
    }
    if (username.value == '20020295' && password.value == '123456' /*wrong username or password*/) {
        login_failed.style.display = 'block';
        username.value = "";
        password.value = "";
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
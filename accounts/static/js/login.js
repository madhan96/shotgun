function validateCredentials() {
    document.querySelector(".error_msg").style.display = 'none';

    let userName = document.forms["userLoginForm"]["username"].value;
    let password = document.forms["userLoginForm"]["password"].value;
    if (document.querySelector(".error_msg_dj"))
        document.querySelector(".error_msg_dj").style.display = "none";
    let isValidName = validateUserName(userName);
    let isValidPass = validatePassword(password);

    if (isValidName && isValidPass) {
        document.querySelector(".login-button").style.display = "none";
        document.querySelector(".logging_button").style.display = "block";

        document.forms["userLoginForm"].setAttribute("action", "login");
        document.forms["userLoginForm"].setAttribute("method", "post");
        document.forms["userLoginForm"].submit();

    }
}

function validateUserName(userName) {
    if (!userName) {
        document.forms["userLoginForm"]["username"].style.border = "1px solid #f2042c";
        document.querySelector(".error_msg_un").style.display = "block";
        return false;
    }
    return true;
}

function validatePassword(password) {
    if (!password) {
        document.forms["userLoginForm"]["password"].style.border = "1px solid #f2042c";
        document.querySelector(".error_msg_pw").style.display = "block";
        return false;
    }
    return true;
}

function resetField(element) {
    if (element.name == "username" && element.value.length > 0) {
        document.forms["userLoginForm"]["username"].style.border = "1px solid #bfbcbc";
        document.querySelector(".error_msg_un").style.display = "none";
    }
    if (element.name == "password" && element.value.length > 0) {
        document.forms["userLoginForm"]["password"].style.border = "1px solid #bfbcbc";
        document.querySelector(".error_msg_pw").style.display = "none";
    }
}


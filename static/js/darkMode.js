
function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toGMTString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function darkMode() {
    var isDarkMode = getCookie("mode");

    if (isDarkMode === "") {
        console.log("creating cookie");
        setCookie("mode", "dark", 365);
        var element = document.body;
        element.classList.toggle("dark-mode");
    }



    if (isDarkMode == "light") {
        console.log(isDarkMode);
        setCookie("mode", "dark", 365);
        var element = document.body;
        element.classList.toggle("dark-mode");

    } else if (isDarkMode == "dark") {
        console.log(isDarkMode);
        setCookie("mode", "light", 365);
        var element = document.body;
        element.classList.toggle("dark-mode");

    }


}


function bodyLoadDarkMode() {

    var isDarkMode = getCookie("mode");

    if (isDarkMode == "dark") {
        var element = document.body;
        element.classList.toggle("dark-mode");

    }


}

bodyLoadDarkMode();

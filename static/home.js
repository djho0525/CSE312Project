/*var useDarkTheme = localStorage.getItem("darkTheme") === "true";
setDarkMode(useDarkTheme);

function setDarkMode(isDark) {
    // Based on https://stackoverflow.com/a/37416531
    var LightMode = document.getElementById("lightMode");
    LightMode.disabled = isDark;
    localStorage.setItem("darkTheme", isDark)
}*/
var useDarkTheme = localStorage.getItem("LightDark") === "dark";
setDarkMode(useDarkTheme);

function loadBody(){
    let prevState = document.getElementById("lightModeCheckbox")
    if (localStorage.getItem("LightDark")=="dark") {
        prevState.checked = true
    }
}
function setDarkMode(darkMode){
    console.log(darkMode)
    if(darkMode == true) {
        //document.cookie = "LightDark=dark";
        localStorage.setItem("LightDark", "dark")
    }
    else{
        localStorage.setItem("LightDark", "light")
    }
    if(localStorage.getItem("LightDark") == "dark"){
        let lightModeOFF = document.getElementById("lightMode")
        lightModeOFF.disabled = true
        let darkModeOFF = document.getElementById("darkMode")
        darkModeOFF.disabled = false
        localStorage.setItem("LightDark", "dark")
    }
    else if(localStorage.getItem("LightDark") == "light"){
        let darkModeOFF = document.getElementById("darkMode")
        darkModeOFF.disabled = true
        let lightModeOFF = document.getElementById("lightMode")
        lightModeOFF.disabled = false
        localStorage.setItem("LightDark", "light")
    }
}
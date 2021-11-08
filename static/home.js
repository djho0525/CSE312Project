function enableButton(){
    let button = document.getElementById("submit-mode")
    button.disabled=false
}

const socket = new WebSocket('ws://' + window.location.host + '/websocket');

function signOut(){
    fetch('http://' + window.location.host  +  '/logout')
}

/*var useDarkTheme = localStorage.getItem("LightDark") === "dark";
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
}*/
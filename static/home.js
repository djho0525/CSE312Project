function enableButton(){
    let button = document.getElementById("submit-mode")
    button.disabled=false
}

const socket = new WebSocket('ws://' + window.location.host + '/websocket');

function signOut(){
    fetch('http://' + window.location.host  +  '/logout')
}

// Call the updateVote function whenever data is received from the server over the WebSocket
socket.onmessage = updateVote;

// Read the name/comment the user is sending to chat and send it to the server over the WebSocket as a JSON string
// Called whenever the user clicks the Send button or pressed enter
function sendMessage(imageToLikeID) {
    console.log(imageToLikeID)
    const likesCaptionElement = document.getElementById(imageToLikeID)
    const numLikesWithText = likesCaptionElement.innerHTML
    const numLikes = numLikesWithText.slice("Likes ♥: ".length)
    console.log("NUMBER OF LIKES FROM ELEMENTID: " + numLikes)
    socket.send(JSON.stringify({'imageid': imageToLikeID, 'likes': numLikes}));
}

// Called when the server sends a new message over the WebSocket and renders that message so the user can read it
function updateVote(message) {
    const imageIDAndLikesObj = JSON.parse(message.data);
    console.log("Message received from server:")
    console.log(imageIDAndLikesObj)
    const imageToLikeID = document.getElementById(imageIDAndLikesObj.imageid)
    imageToLikeID.innerHTML = "Likes ♥: " + imageIDAndLikesObj.likes
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
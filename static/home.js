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
// Called whenever the user clicks the Like button
function sendMessage(imageToLikeID) {
    //console.log(imageToLikeID)
    const likesCaptionElement = document.getElementById(imageToLikeID)
    const numLikesWithText = likesCaptionElement.innerHTML
    const numLikes = numLikesWithText.slice("Likes ♥: ".length)
    //console.log("NUMBER OF LIKES FROM ELEMENTID: " + numLikes)
    socket.send(JSON.stringify({'imageid': imageToLikeID, 'likes': numLikes}));
}

// Called when the server sends a new message over the WebSocket and renders that message so the user can read it
function updateVote(message) {
    const imageIDAndLikesObj = JSON.parse(message.data);
    //console.log("Message received from server:")
    //console.log(imageIDAndLikesObj)
    const imageToLikeID = document.getElementById(imageIDAndLikesObj.imageid)
    imageToLikeID.innerHTML = "Likes ♥: " + imageIDAndLikesObj.likes
}

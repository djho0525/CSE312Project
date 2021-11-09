const socket = new WebSocket("ws://" + window.location.host + "/websocket");
console.log(socket);
socket.onmessage = addMessage;

document.addEventListener("keypress", function (event) {
    if (event.code === "Enter") {
        sendMessage();
    }
});

function sendMessage() {
    var message = $("#input_message").val();
    $("#input_message").val("");
    socket.send(JSON.stringify({'listener': "direct_message", 'message': message}));
}

function addMessage(message) {
    console.log("or here?")
    messages = $("#display_message").html() + message.data + "<br/>";
    $("#display_message").html(messages);
}

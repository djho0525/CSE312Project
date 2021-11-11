const socket = new WebSocket("ws://" + window.location.host + "/websocket");
socket.onmessage = webSocketListener;

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

function webSocketListener(data) {
    var content = JSON.parse(data.data)
    var listener = content['listener']

    if (listener == 'direct_message') {
        if (content['type'] == 'chatroom') {
            var messages = $("#display_message").html() + "<b>" + content['sender'] + ": </b>" + content['message'] + "<br/>";
            $("#display_message").html(messages);
        }
        else if (content['type'] == 'notif') {
            $('.toast-header strong').text(content['sender'] + ' says...');
            $('.toast-body').html(content['message'] + '<br><br><a href="/messages?user=' + content['sender'] + '" class="btn btn-warning">Reply</a>')
            $('.toast').toast('show');
        }
    }
}

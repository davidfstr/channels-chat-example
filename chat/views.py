from django.http import HttpResponse
import json


def index(request):
    return HttpResponse("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>Chat Rooms</title>
</head>
<body>
    What chat room would you like to enter?<br/>
    <input id="room-name-input" type="text" size="100"/><br/>
    <input id="room-name-submit" type="button" value="Enter"/>
</body>
<script>
    document.querySelector('#room-name-input').focus();
    document.querySelector('#room-name-input').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#room-name-submit').click();
        }
    };
    
    document.querySelector('#room-name-submit').onclick = function(e) {
        var roomName = document.querySelector('#room-name-input').value;
        window.location.pathname = '/chat/' + roomName;
    };
</script>
</html>
""")


def room(request, room_name: str):
    return HttpResponse("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>Chat Room</title>
</head>
<body>
    <textarea id="chat-log" cols="100" rows="20"></textarea><br/>
    <input id="chat-message-input" type="text" size="100"/><br/>
    <input id="chat-message-submit" type="button" value="Send"/>
</body>
<script>
    var roomName = %(room_name_json)s;
    
    var chatSocket = null;
    
    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#chat-message-submit').click();
        }
    };
    
    document.querySelector('#chat-message-submit').onclick = function(e) {
        var messageInputDom = document.querySelector('#chat-message-input');
        var message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        
        messageInputDom.value = '';
    };
    
    function openChatSocket() {
        chatSocket = new WebSocket(
            'ws://' + window.location.host + 
            '/ws/chat/' + roomName + '/');
        
        chatSocket.onmessage = function(e) {
            var data = JSON.parse(e.data);
            var message = data['message'];
            document.querySelector('#chat-log').value += (message + '\\n');
        };
        
        // Reopen WebSocket if it closes unexpectedly
        chatSocket.onclose = function(e) {
            openChatSocket();
        };
    }
    
    openChatSocket();
</script>
</html>
""" % dict(
    room_name_json=json.dumps(room_name)
))

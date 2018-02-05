from asgiref.sync import AsyncToSync
from channels.generic.websocket import WebsocketConsumer
import hashlib
import json


class ChatConsumer(WebsocketConsumer):
    @property
    def _room_name(self):
        return self.scope['url_route']['kwargs']['room_name']
    
    @property
    def _chat_channel_name(self):
        # NOTE: Channel names cannot have special characters
        return 'chat_' + hashlib.sha1(self._room_name.encode('utf8')).hexdigest()
    
    def connect(self):
        AsyncToSync(self.channel_layer.group_add)(
            self._chat_channel_name,
            self.channel_name)
        self.accept()
    
    def disconnect(self, close_code):
        AsyncToSync(self.channel_layer.group_discard)(
            self._chat_channel_name,
            self.channel_name)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        AsyncToSync(self.channel_layer.group_send)(
            self._chat_channel_name,
            {
                'type': 'chat_message',
                'message': message
            })
    
    # Handles the "chat_message" event when it's sent to our group
    def chat_message(self, event):
        message = event['message']
        
        self.send(text_data=json.dumps({
            'message': message
        }))

from channels.generic.websocket import WebsocketConsumer
import json


class Consumer(WebsocketConsumer):
    """Consumer to allow clients send and receive messages"""

    def connect(self):
        """Allows connection"""
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        """Receive connection"""
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))


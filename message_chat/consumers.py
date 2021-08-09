from channels.generic.websocket import WebsocketConsumer
import json


class Consumer(WebsocketConsumer):
    """Consumer to allow clients send and receive messages"""

    def connect(self):
        """Allows connection"""
        self.accept()

    def receive(self, text_data):
        """Receive connection"""
        # Send message to websockets
        self.send(text_data=json.dumps({'message': json.loads(text_data)['message']}))

    def disconnect(self, close_code):
        pass



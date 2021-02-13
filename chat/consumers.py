import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import time


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        """Установка соединения"""
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        """Разрыв соединения"""
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        """Приём данных"""
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now_time = time.time()
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'time': time.ctime(now_time),
                'message': message
            }
        )

    def chat_message(self, event):
        """Отправка данных"""
        time = event['time']
        message = event['message']
        self.send(text_data=json.dumps({
            'time': time,
            'message': message
        }))

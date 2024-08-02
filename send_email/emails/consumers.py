import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import EmailMessage
from datetime import datetime

class EmailConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'start':
            self.import_emails()

    def import_emails(self):
        for i in range(0, 101, 10):
            self.send(text_data=json.dumps({
                'type': 'progress',
                'status': 'Загрузка сообщений...',
                'progress': i
            }))
            self.sleep(1) 
        self.send(text_data=json.dumps({
            'type': 'progress',
            'status': 'Получение сообщений...',
            'progress': 100
        }))

        messages = EmailMessage.objects.all()[:10]
        for message in messages:
            self.send(text_data=json.dumps({
                'type': 'message',
                'message': {
                    'subject': message.subject,
                    'sent_date': message.sent_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'received_date': message.received_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'body': message.body,
                    'attachments': message.attachments
                }
            }))

    def sleep(self, seconds):
        import time
        time.sleep(seconds)

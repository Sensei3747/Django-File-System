from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import ChatTable, UserProfile
from datetime import datetime
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender_id = self.scope['session'].get('user_id')
        self.receiver_id = int(self.scope['url_route']['kwargs']['receiver_id'])

        self.room_name = f"chat_{min(self.sender_id, self.receiver_id)}_{max(self.sender_id, self.receiver_id)}"
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        await self.mark_messages_as_read()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Fetch sender and receiver safely
        sender = await self.get_user(self.sender_id)
        receiver = await self.get_user(self.receiver_id)

        # Save message safely
        chat = await self.save_message(sender, receiver, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.fname,
                'timestamp': chat.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'is_read': False
            }
        )
    @sync_to_async
    def mark_messages_as_read(self):
        ChatTable.objects.filter(
            sender_id=self.receiver_id,
            receiver_id=self.sender_id,
            is_read=False
        ).update(is_read=True)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def get_user(self, user_id):
        return UserProfile.objects.get(id=user_id)

    @sync_to_async
    def save_message(self, sender, receiver, message):
        return ChatTable.objects.create(sender=sender, receiver=receiver, message=message)

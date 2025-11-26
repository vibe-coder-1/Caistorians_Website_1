from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
import bleach
from .models import GroupChatRoom, GroupMessage

# Allowed HTML tags and attributes (optional)
ALLOWED_TAGS = ['b', 'i', 'u', 'strong', 'em', 'a']
ALLOWED_ATTRS = {'a': ['href', 'title']}

class CohortChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.cohort_year = self.scope['url_route']['kwargs'].get('cohort_year')
        self.group_name = f"cohort_chat_{self.cohort_year}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data or '{}')
        message_text = (data.get('text') or '').strip()
        user = self.scope.get('user')

        if not message_text or not user or not user.is_authenticated:
            return

        # Sanitize input to prevent HTML/JS injection
        safe_text = bleach.clean(message_text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS)

        # Save message to DB
        message = await self.save_message(user.id, self.cohort_year, safe_text)

        # Broadcast to group including color
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'broadcast_message',
                'text': message.text,
                'sender': user.username,
                'time': message.sent_at.strftime('%H:%M'),
                'color': message.color,
            }
        )

    async def broadcast_message(self, event):
        await self.send(text_data=json.dumps({
            'text': event['text'],
            'sender': event['sender'],
            'time': event['time'],
            'color': event['color'],
        }))

    @database_sync_to_async
    def save_message(self, user_id, cohort_year, text):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.get(id=user_id)
        room, _ = GroupChatRoom.objects.get_or_create(cohort_year=cohort_year)
        return GroupMessage.objects.create(sender=user, room=room, text=text)

import json
from channels.generic.websocket import AsyncWebsocketConsumer


class PromptConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = None
        self.user = None

    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
        else:
            self.group_name = f"user_{self.user.id}"
            # Join user group
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            await self.send(text_data=json.dumps({"message": "WebSocket connection established"}))

    async def disconnect(self, close_code):
        # Leave group
        # Only discard if group_name exists
        if hasattr(self, 'group_name') and self.group_name:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Receive message from group
    async def send_prompt(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))

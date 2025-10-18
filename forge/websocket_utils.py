from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_to_websocket(user, message: dict):
    """
    Sends a message to the user via WebSocket.
    Requires Django Channels and a configured consumer.
    """
    channel_layer = get_channel_layer()
    group_name = f"user_{user.id}"

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "send.prompt",
            "message": message
        }
    )

import jwt
from django.conf import settings
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

User = get_user_model()


class JwtAuthMiddleware:
    """
    JWT middleware for WebSocket connections using query param ?token=...
    Compatible with Channels 4.x
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Default to anonymous user
        scope['user'] = AnonymousUser()

        # Parse token from query string
        query_string = scope.get('query_string', b'').decode()
        params = parse_qs(query_string)
        token_list = params.get('token', None)

        if token_list:
            token = token_list[0]
            try:
                payload = jwt.decode(
                    token, settings.SECRET_KEY, algorithms=["HS256"])
                user = await database_sync_to_async(User.objects.get)(id=payload['user_id'])
                scope['user'] = user
            except Exception:
                pass

        # Call the next ASGI app
        return await self.app(scope, receive, send)

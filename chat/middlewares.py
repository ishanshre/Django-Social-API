from channels.middleware import BaseMiddleware

from django.contrib.auth import get_user_model

from rest_framework_simplejwt.authentication import JWTAuthentication 

from django.db import close_old_connections

from asgiref.sync import sync_to_async


User = get_user_model()

class JwtAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)
        self.auth = JWTAuthentication()
    

    async def __call__(self, scope, receive, send):
        close_old_connections()
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            token = headers[b'authorization'].decode("utf=8")
            if token.startswith("Bearer "):
                token = token[7:]
                try:
                    validated_token = await sync_to_async(self.auth.get_validated_token)(token)
                    user = await sync_to_async(self.auth.get_user)(validated_token)
                    scope['user'] = user
                except Exception as e:
                    print("jwt token websocket middleware exception: ", e)
        return await super().__call__(scope, receive, send)
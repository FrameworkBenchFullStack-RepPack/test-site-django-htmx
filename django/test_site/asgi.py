"""
ASGI config for test_site project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/asgi/
"""

import os
import asyncio

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_site.settings")

django_asgi_app = get_asgi_application()

from .live import live_broadcast_async


class LifespanGuard:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "lifespan":
            while True:
                message = await receive()
                if message["type"] == "lifespan.startup":
                    asyncio.get_running_loop().create_task(live_broadcast_async())
                    await send({"type": "lifespan.startup.complete"})
                    return
                elif message["type"] == "lifespan.shutdown":
                    await send({"type": "lifespan.shutdown.complete"})
                    return

        return await self.app(scope, receive, send)


application = LifespanGuard(django_asgi_app)
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

from . import consumers


application = ProtocolTypeRouter({
    #"http": (regular Django views)
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url("^ws/chat/(?P<room_name>[^/]+)/$", consumers.ChatConsumer),
        ])
    ),
})
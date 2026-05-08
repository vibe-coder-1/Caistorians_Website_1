try:
    from django.urls import re_path
    from .consumers import ChatConsumer
except ImportError as e:
    print(f"\nError: Django or Channels not available.\n{e}")

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<year>\d+)/$", ChatConsumer.as_asgi()),
]

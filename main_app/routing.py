# used for defining a websocket url pattern

from django.urls import path
from . import consumers #consumers are like how we use views
                        # they handle all of our websocket connections
websocket_urlpatterns = [
    path('ws/projects/<int:project_pk>/', consumers.ProjectConsumer.as_asgi()),
]
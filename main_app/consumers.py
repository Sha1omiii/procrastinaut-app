import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ProjectConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.project_pk = self.scope['url_route']['kwargs']['project_pk']
        self.project_group_name = f'project_{self.project_pk}'

        #handles joining a chat
        await self.channel_layer.group_add(
            self.project_group_name,
            self.channel_name
        )

        await self.accept()
    #handles leaving a chat 
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.project_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # handles sending a message to the group (project)
        await self.channel_layer.group_send(
            self.project_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        # handles sending message to the websocket
        await self.send(text_data=json.dumps({ 
            'message': message
        }))
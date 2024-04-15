import json
import time
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer
# from chat.helpers import get_last_50_messages, get_user_contact, get_current_chat, get_media_content, message_read_by_user_add
from chat.models import *
# from chat.ws_helpers import *
from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder
from user.models import User
from datetime import date



class ChatConsumer(WebsocketConsumer):

    def message_list(self, data):
        return "name"

    def message_list_data(self, data):
        user = self.scope['user']
        user_contact = get_user_contact(data['from'])
        current_chat = get_current_chat(data['chatId'])
        chat=Chat.objects.filter(pk=current_chat.id)
        for contact in chat.first().participants.all():
            if contact==user_contact:
                get_chat_list_data1_for_websocket(user)
            else:
                friend_user=User.objects.filter(pk=contact.user_id)
                get_chat_list_data1_for_websocket(friend_user.first())

    # @database_sync_to_async
    def set_status(self, status):
        user = self.scope['user']
        user.set_online_status(status)

    def chat_list(self, data):
        user = self.scope['user']
        chat_list_data = get_chat_list_for_websocket(user)
        if chat_list_data:
            content=chat_list_data.first().chat_data
            content['command']='chat_list'
            self.send(text_data=json.dumps(content, sort_keys=True, indent=1, cls=DjangoJSONEncoder))


    def chat_info(self, data):
        channel_id = data.get("chatId")
        user = self.scope['user']
        chat = Chat.objects.get(pk=int(channel_id))
        if chat.is_group == True:
            basic_info = {
                                "id":chat.id,
                                "channel_name":chat.group_name,
                                "is_group":chat.is_group,
                                "no_of_participants":chat.participants.count(),
                                "channel_avatar":chat.group_avatar.url if chat.group_avatar else None
                            }
            channel_info = {"command": "chat_info", "user_basic_info": basic_info, "is_group":chat.is_group}
        else:
            channel_info = chat.get_channel_info(user)
        self.send(text_data=json.dumps(channel_info))

    # @database_sync_to_async
    def set_online_channel(self, online_channel_id):
        user = self.scope['user']
        user.set_online_channel(online_channel_id)

    def delete_message(self, data):
        message_ids = data['message_ids']
        try:
            messages = Message.objects.filter(id__in=message_ids)
            messages.delete()
        except Exception as e:
            raise
        messages = get_last_50_messages(data['chatId'])
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def report_message(self, data):
        message_id = data['message_id']
        message_sender_id = data['message_sender_id']
        user_id = data['user_id']
        chat_id = data['chatId']
        try:
            report_user = ReportUser.objects.get_or_create(reported_by_id=user_id, reported_user_id=message_sender_id,
                                                           reported_message_channel=chat_id)
            if not report_user[1]:
                report_user[0].count = report_user[0].count + 1
                report_user[0].save()
            report_user[0].notify_admin()
            messages = Message.objects.filter(id=message_id)
            messages.delete()
        except Exception as e:
            raise
        messages = get_last_50_messages(data['chatId'])
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def fetch_messages(self, data):
        messages = get_last_50_messages(data['chatId'])
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def read_message(self, data):
        reading_user = get_user_contact(data['user_id'])
        chat_id = (data['chatId'])
        message_read_by_user_add(reading_user, chat_id)
        content = {
            'command': 'read_message',
            'messages': data}
        self.send_message(content)


    def new_message(self, data):
        user_contact = get_user_contact(data['from'])
        type_of_content = data['type_of_content']
        media = data['media_id']
        current_chat = get_current_chat(data['chatId'])
        chat_id = current_chat.id
        chat = Chat.objects.get(pk=chat_id)
        chat_partcipants = chat.participants.all()
        if user_contact in chat_partcipants:
            offline_locator = data['offline_locator']
            message = Message(contact=user_contact, content=data['message'], type_of_content=type_of_content, offline_locator=offline_locator)
            if media:
                message.media_id = int(media)
            today=date.today()
            if current_chat.messages.last():
                if today>current_chat.messages.last().timestamp.date():
                    self.message_list_data(data)
            message.save()
            s = current_chat.messages.add(message)
            self.message_list_data(data)
            current_chat.save()
            notify_participants(message.id,chat_id)
            content = {
                'command': 'new_message',
                'message': self.message_to_json(message)
            }
            return self.send_chat_message(content)
        else:
            content = {
                'command': 'response',
                'message': self.not_permission_for_message(data['from'])
            }
            return self.send_chat_message(content)

    def user_action(self, data):
        return self.send_user_action(data)

    def send_user_action(self, data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': data
            }
        )

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        message_read = False
        room_no = self.scope['url_route']['kwargs'].get('room_name', "")
        user = self.scope['user']
        user_contact = get_user_contact(user.id)
        contact = None
        chat = Chat.objects.get(pk = int(room_no))
        contact_msg_read = ContactMessageRead.objects.filter(message = message, chat = chat, msg_read_mode=True)
        readed_by = []
        for contact_read in contact_msg_read:
            contact = contact_read.contact
            readed_by.append({"reader":contact.user.id, "reader_mode": contact.user.msg_read_mode})
        return {
            'id': message.id,
            'author': {
                'username': message.contact.user.full_name,
                'author_id': message.contact.user.id,
                'avatar': message.contact.user.avatar.url if message.contact.user.avatar else None,
                'id': message.contact.user.id
            },
            'user_id': message.contact.user.id,
            'content': message.content,
            'type_of_content': message.type_of_content,
            'offline_locator':message.offline_locator,
            'media': self.get_media(message),
            'timestamp': str(message.timestamp),
            'seen_by': readed_by
            
        }

    def not_permission_for_message(self, user_id):
        return {
            'user_id': user_id,
            'content': "You are not permitted to send msg"
        }

    def get_media(self, message):
        if message.media:
            # if message.type_of_content=='video':
            return {
                    'id': message.media.id,
                    'url': message.media.content.url if message.media.content else None,
                    'content_name':message.media.content.name.split("/")[-1],
                    'thumbnail':message.media.thumbnail.url if message.media.type_of_content=='video' else None,
                    'extension': message.media.extention,
                    'duration':message.media.duration,
                }

        return {}

    commands = {
            'fetch_messages': fetch_messages,
            'new_message': new_message,
            'message_list': message_list,
            'set_status': set_status,
            'chat_info': chat_info,
            'chat_list': chat_list,
            'user_action': user_action,
            'delete_message': delete_message,
            'report_message': report_message,
            'read_message': read_message,
        }

    def connect(self):
        if self.scope['user'] != "":
            self.scope['user'] = User.objects.get(pk=self.scope['user'])

        if self.scope['path'] == "/api/v1/ws/online":
            self.set_status("online")

        if self.scope['path'] == "/api/v1/ws/offline":
            self.set_status("offline")

        self.room_name = self.scope['url_route']['kwargs'].get('room_name', "")
        self.room_group_name = 'chat_%s' % self.room_name

        if self.room_name != "":
            self.set_status("online")
            self.set_online_channel(int(self.room_name))
            chat = Chat.objects.filter(id=int(self.room_name)).first()
            self.send_chat_message({"message":{"user_id":self.scope['user'].id, "status":"online"}, "command":"read_prevoius_message"})
            if chat:
                
                # if(self.scope['user'].msg_read_mode):#condition added
                ContactMessageRead.populate_old_messages(chat)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        return self.accept()

    def disconnect(self, close_code):
        if self.scope['path'] == "/api/v1/ws/online":
            self.set_status("offline")

        channel_name = self.scope['url_route']['kwargs'].get('room_name', "")
        if channel_name != "":
            self.set_online_channel(0)

        if self.room_group_name:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        user=User.objects.filter(pk=message['message']['user_id'])
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))

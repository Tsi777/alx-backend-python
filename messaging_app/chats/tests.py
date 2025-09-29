from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Conversation, ConversationParticipant

class ConversationTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='user1@example.com', password='pass1234', first_name='User', last_name='One', role='guest'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com', password='pass1234', first_name='User', last_name='Two', role='guest'
        )
        self.client.force_authenticate(user=self.user1)

    def test_create_conversation(self):
        url = reverse('conversation-list')  # Use 'conversation-list'
        data = {'participants': [str(self.user1.user_id), str(self.user2.user_id)]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['participants']), 2)

class MessageTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='user1@example.com', password='pass1234', first_name='User', last_name='One', role='guest'
        )
        self.conversation = Conversation.objects.create()
        ConversationParticipant.objects.create(conversation=self.conversation, user=self.user1)
        self.client.force_authenticate(user=self.user1)

    def test_send_message(self):
        url = reverse('conversation-message-list', kwargs={'conversation_pk': str(self.conversation.conversation_id)})  # Use 'conversation-message-list'
        data = {
            'conversation': str(self.conversation.conversation_id),
            'message_body': 'Hello, this is a test message'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message_body'], 'Hello, this is a test message')

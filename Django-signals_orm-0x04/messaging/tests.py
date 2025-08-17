from django.test import TestCase
from django.contrib.auth import get_user_model
from messaging.models import Message, Notification, MessageHistory

User = get_user_model()

class UserDeletionSignalTest(TestCase):
    def setUp(self):
        # Create users
        self.sender = User.objects.create(email='sender@example.com', password='pass1234', first_name='Sender', last_name='User')
        self.receiver = User.objects.create(email='receiver@example.com', password='pass1234', first_name='Receiver', last_name='User')

        # Create a message
        self.message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello"
        )

        # Create a notification for the receiver
        Notification.objects.create(user=self.receiver, message=self.message)

        # Create a message history entry manually (simulate edit)
        MessageHistory.objects.create(message=self.message, old_content="Old content")

    def test_user_deletion_cascades_related_data(self):
        user_id = self.receiver.user_id  # use user_id, not id
        self.receiver.delete()

        self.assertFalse(Message.objects.filter(receiver_id=user_id).exists())
        self.assertFalse(Message.objects.filter(sender_id=user_id).exists())
        self.assertFalse(Notification.objects.filter(user_id=user_id).exists())
        self.assertFalse(MessageHistory.objects.filter(message=self.message).exists())

from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        return (
            self.filter(receiver=user, edited=False)  # or read=False depending on your field
            .only('id', 'content', 'timestamp', 'sender_id')  # optimize fields
            .select_related('sender')  # fetch sender in same query
        )

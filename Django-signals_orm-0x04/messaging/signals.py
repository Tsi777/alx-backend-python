from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.db.models.signals import post_delete
from django.contrib.auth import get_user_model

@receiver(post_save, sender=Message)
def notify_receiver_on_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:  # Means we're updating an existing message
        try:
            old_instance = Message.objects.get(pk=instance.pk)
            if instance.content != old_instance.content:
                # Log old content
                MessageHistory.objects.create(
                    message=old_instance,
                    old_content=old_instance.content
                )
                instance.edited = True  # Mark the message as edited
        except Message.DoesNotExist:
            pass

User = get_user_model()

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    # Delete all messages sent or received by this user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications for this user
    Notification.objects.filter(user=instance).delete()

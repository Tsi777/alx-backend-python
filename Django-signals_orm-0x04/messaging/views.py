from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page 
from .models import Message

User = get_user_model()

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return HttpResponse("User and related data deleted successfully.")


@login_required
def unread_messages_list(request):
    user = request.user

    unread_via_manager = Message.unread.unread_for_user(user)

    unread_direct = Message.objects.filter(receiver=user, read=False)\
        .only('id', 'content', 'timestamp', 'sender_id')\
        .select_related('sender')

    combined_unread = unread_via_manager.union(unread_direct)

    messages_data = [
        {
            "id": msg.id,
            "content": msg.content,
            "sender": msg.sender.email,
            "timestamp": msg.timestamp.isoformat(),
        }
        for msg in combined_unread
    ]

    return JsonResponse({"unread_messages": messages_data})


@cache_page(60)  
@login_required
def threaded_messages_view(request):
    top_level_messages = Message.objects.filter(
        sender=request.user,
        parent_message__isnull=True
    ).select_related('sender', 'receiver').prefetch_related('replies__sender')

    def serialize_message(msg):
        return {
            "id": msg.id,
            "content": msg.content,
            "sender": msg.sender.email,
            "receiver": msg.receiver.email,
            "timestamp": msg.timestamp.isoformat(),
            "replies": [serialize_message(reply) for reply in msg.replies.all()]
        }

    data = [serialize_message(msg) for msg in top_level_messages]

    return JsonResponse({"messages": data})

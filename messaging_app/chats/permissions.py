from rest_framework import permissions

# Re-export IsAuthenticated so it can be imported from this file too
IsAuthenticated = permissions.IsAuthenticated

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Only participants of the conversation can view, modify, or send messages.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Allow read-only methods if user is a participant
        if request.method in permissions.SAFE_METHODS:
            if hasattr(obj, 'participants'):
                return user in obj.participants.all()
            if hasattr(obj, 'conversation'):
                return user in obj.conversation.participants.all()
            return False

        # For PUT, PATCH, DELETE — enforce stricter check
        if request.method in ["PUT", "PATCH", "DELETE"]:
            if hasattr(obj, 'conversation'):
                return user in obj.conversation.participants.all()
            if hasattr(obj, 'participants'):
                return user in obj.participants.all()

        return False

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

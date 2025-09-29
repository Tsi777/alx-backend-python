from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from .permissions import IsAuthenticated, IsParticipantOfConversation
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer, ConversationCreateSerializer,
    MessageSerializer, MessageCreateSerializer
)
from .filters import MessageFilter
from .pagination import MessagePagination


class ForbiddenAccess(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "You are not a participant of this conversation."
    default_code = "permission_denied"


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__first_name', 'participants__last_name']
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ConversationCreateSerializer
        return ConversationSerializer


class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MessageFilter
    search_fields = ['message_body', 'sender__first_name', 'sender__last_name']
    ordering_fields = ['sent_at']
    pagination_class = MessagePagination

    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation_id')
        user = self.request.user

        if conversation_id:
            try:
                conversation = Conversation.objects.get(id=conversation_id)
            except Conversation.DoesNotExist:
                return Message.objects.none()

            if user not in conversation.participants.all():
                raise ForbiddenAccess()

            return Message.objects.filter(conversation=conversation)

        # fallback: all messages from conversations user participates in
        return Message.objects.filter(conversation__participants=user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MessageCreateSerializer
        return MessageSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

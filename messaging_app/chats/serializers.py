from rest_framework import serializers
from .models import User, Conversation, Message, ConversationParticipant

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at'
        ]
        read_only_fields = ['user_id', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    # Example of SerializerMethodField for a formatted date string
    sent_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at', 'sent_at_formatted', 'conversation']
        read_only_fields = ['message_id', 'sent_at']

    def get_sent_at_formatted(self, obj):
        return obj.sent_at.strftime("%Y-%m-%d %H:%M:%S")

class MessageCreateSerializer(serializers.ModelSerializer):
    message_body = serializers.CharField(max_length=1000)  # Explicit CharField
    class Meta:
        model = Message
        fields = ['message_body', 'conversation']

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']
        read_only_fields = ['conversation_id', 'created_at']

class ConversationCreateSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all()
    )

    class Meta:
        model = Conversation
        fields = ['participants']

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        conversation = Conversation.objects.create()
        for user in participants:
            ConversationParticipant.objects.create(conversation=conversation, user=user)
        return conversation

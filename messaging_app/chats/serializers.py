from rest_framework import serializers
from .models import User, Conversation, Message

# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get('phone_number', ''),
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

# Serializer for the Message model
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # Include sender details

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at', 'created_at']
        read_only_fields = ['sent_at', 'created_at']

# Serializer for the Conversation model
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages']

    def get_messages(self, obj):
        messages = Message.objects.filter(conversation=obj)
        return MessageSerializer(messages, many=True).data

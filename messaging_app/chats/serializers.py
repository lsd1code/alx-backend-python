from rest_framework import serializers
from .models import User, Message, Conversation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'user_id',
            'first_name',
            'last_name',
            'email',
        )


class MessageSerializer(serializers.ModelSerializer):
    def validate_message(self, data):
        if len(str(data['message_body'])) < 1:
            raise serializers.ValidationError("Message body cannot be empty")

    
    class Meta:
        model = Message
        fields = ('message_id', 'message_body', 'sent_at', 'sender_id')
        
        
class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True)
    total_messages = serializers.SerializerMethodField()
    created_by = serializers.StringRelatedField()    

    def get_total_messages(self, obj: Conversation):
        return len(obj.messages.all())
    
    
    class Meta:
        model = Conversation
        fields = ('conversation_id', 'created_by', 'total_messages', 'created_at', 'participants_id', 'messages')

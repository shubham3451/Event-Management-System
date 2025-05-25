from rest_framework import serializers
from .models import *




class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        start_time = serializers.DateTimeField(input_formats=['%Y-%m-%d %H:%M'])
        end_time = serializers.DateTimeField(input_formats=['%Y-%m-%d %H:%M'])
        fields = ['id', 'creator', 'title', 'description', 'start_time', 'end_time',
                  'location', 'is_recurring', 'recurrence_pattern', 'created_at', 'version_number']
        read_only_fields = ['id', 'creator', 'created_at', 'version_number']

    def create(self, validated_data):
        # Get the user from the context
        user = self.context['request'].user
        
        # Set the creator field
        validated_data['creator'] = user

        # Create the Event
        event = Event.objects.create(**validated_data)

        # Automatically create EventCollaborator with role='owner'
        EventCollaborator.objects.create(
            event=event,
            shared_by=user,
            collaborators=user,
            role='owner'
        )

        return event


class EventCollaborationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCollaborator
        fields = ['collaborators', 'role']

class EventVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventVersion
        fields = '__all__'


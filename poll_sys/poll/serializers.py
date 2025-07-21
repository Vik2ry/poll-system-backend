from django.contrib.auth.models import User, AnonymousUser
from rest_framework import serializers, status
from .models import Poll, Option, Vote
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_staff', 'is_superuser', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True}, # password is write only
            'is_staff': {'read_only': True},  # is_staff is read only
            'date_joined': {'read_only': True} # date_joined is read only
        }

    def create(self, validated_data):
        """Create a new user"""
        if validated_data.get('is_superuser'):
            user = User.objects.create_superuser(**validated_data)
        else:
            user = User.objects.create_user(**validated_data)
        return user
    
class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'label']
        extra_kwargs = {'poll': {'read_only': True}}

class PollSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True, required=False)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'title', 'description', 'is_active', 'created_by', 'created_at', 'expires_at', 'options']
        
    # method to customize the representation of the poll. It's called when the poll is serialized
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if request and not request.user.is_superuser:
            data.pop('is_active', None)
            data.pop('created_at', None)

        return data
      
        
    def create(self, validated_data):
        poll = Poll.objects.create(created_by=self.context['request'].user, **validated_data)
        return poll


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        exclude = ['user', 'poll']
        
    
    def validate(self, data):
        """Verify that the user has not already voted for the poll and that the option belongs to the poll"""
        user = self.context['request'].user
        poll = self.context['poll']
        option = data['option']

        # Verify that the option belongs to the poll
        if option.poll != poll:
            raise serializers.ValidationError("❌ This option does not belong to the poll. ❌")

        # Verify that the user has not already voted for the poll
        if Vote.objects.filter(user=user, poll=poll).exists():
            raise serializers.ValidationError("❌ You have already voted for this poll. ❌")
        
        return data
        
    def create(self, validated_data):
        user = self.context['request'].user
        poll = self.context['poll']
        option = validated_data['option']
        
        if isinstance(user, AnonymousUser):
            return Response({"error": "Vous devez être connecté pour voter."}, status=status.HTTP_403_FORBIDDEN)
                    
        vote = Vote.objects.create(user=user, poll=poll, option=option)
        return vote
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Prompt, PromptMetadata, PromptEmbedding


class PromptEmbeddingSerializer(serializers.ModelSerializer):
    vector = serializers.ListField(
        child=serializers.FloatField(),
        help_text="Numerical embedding vector representing the prompt."
    )

    class Meta:
        model = PromptEmbedding
        fields = ['model_name', 'vector']


class PromptMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptMetadata
        fields = ['model_used', 'sent_via_websocket', 'extra_info']


class PromptSerializer(serializers.ModelSerializer):
    metadata = PromptMetadataSerializer(required=False)
    embedding = PromptEmbeddingSerializer(required=False)

    class Meta:
        model = Prompt
        fields = ['id', 'user', 'text', 'response',
                  'created_at', 'metadata', 'embedding']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        metadata_data = validated_data.pop('metadata', None)
        embedding_data = validated_data.pop('embedding', None)
        user = self.context['request'].user

        prompt = Prompt.objects.create(user=user, **validated_data)

        if metadata_data:
            PromptMetadata.objects.create(prompt=prompt, **metadata_data)
        if embedding_data:
            PromptEmbedding.objects.create(prompt=prompt, **embedding_data)

        return prompt


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

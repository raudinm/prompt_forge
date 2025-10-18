from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class Prompt(models.Model):
    """
    Represents a user-submitted prompt along with the generated response.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='prompts')
    text = models.TextField()  # The original user prompt
    response = models.TextField()  # The model-generated response
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prompt {self.id} by {self.user.username}"


class PromptEmbedding(models.Model):
    """
    Represents the embedding (vector representation) associated with a prompt.
    """
    prompt = models.OneToOneField(
        Prompt, on_delete=models.CASCADE, related_name='embedding'
    )
    model_name = models.CharField(
        max_length=100, default='text-embedding-3-small')
    # Numerical embedding (list of floats)
    vector = ArrayField(models.FloatField())
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Embedding for Prompt {self.prompt.id}"


class PromptMetadata(models.Model):
    """
    Stores additional technical or contextual information related to a prompt.
    """
    prompt = models.OneToOneField(
        Prompt, on_delete=models.CASCADE, related_name='metadata'
    )
    model_used = models.CharField(max_length=50, default='gpt-3.5-turbo')
    sent_via_websocket = models.BooleanField(default=False)
    extra_info = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Metadata for Prompt {self.prompt.id}"

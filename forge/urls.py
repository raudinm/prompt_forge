from django.urls import path
from .views import PromptCreateView, SimilarPromptsView


urlpatterns = [
    path('prompts/', PromptCreateView.as_view(), name='create-prompt'),
    path('prompts/similar/', SimilarPromptsView.as_view(), name='similar-prompts'),
]

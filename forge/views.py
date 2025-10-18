from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from forge.utils import generate_embedding, generate_response
from forge.websocket_utils import send_to_websocket
from .models import Prompt, PromptEmbedding, PromptMetadata
from .serializers import PromptSerializer
from .throttles import CustomBurstRateThrottle, CustomSustainedRateThrottle


class PromptCreateView(APIView):
    """
    Handles prompt creation requests.
    - Authenticated users only.
    - Applies custom burst and sustained throttling.
    - Optionally sends response through WebSocket if 'send_via_websocket=True'.
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [CustomBurstRateThrottle, CustomSustainedRateThrottle]

    def post(self, request):
        text = request.data.get('prompt')
        send_ws = request.data.get('send_via_websocket', False)

        if not text:
            return Response({'error': 'prompt is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate model response (e.g. from OpenAI or internal LLM)
        response_text = generate_response(text)

        # Create Prompt instance
        prompt = Prompt.objects.create(
            user=request.user,
            text=text,
            response=response_text
        )

        # Generate embedding (vector)
        embedding_vector = generate_embedding(text)

        # Create embedding record
        PromptEmbedding.objects.create(
            prompt=prompt,
            vector=embedding_vector,
            model_name="all-MiniLM-L6-v2"
        )

        # Create metadata
        PromptMetadata.objects.create(
            prompt=prompt,
            sent_via_websocket=send_ws,
            model_used="GPT-2"
        )

        # Optionally send via WebSocket
        if send_ws:
            send_to_websocket(request.user, {
                'prompt': text,
                'response': response_text,
                'embedding_length': len(embedding_vector)
            })

        serializer = PromptSerializer(prompt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SimilarPromptsView(APIView):
    """
    Returns a list of prompts that are similar to the given query.
    Currently performs a basic textual match.
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [CustomBurstRateThrottle, CustomSustainedRateThrottle]

    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'query parameter "q" is required'}, status=status.HTTP_400_BAD_REQUEST)

        # TODO: implement FAISS
        similar_prompts = Prompt.objects.filter(text__icontains=query)[:10]
        serializer = PromptSerializer(similar_prompts, many=True)
        return Response(serializer.data)

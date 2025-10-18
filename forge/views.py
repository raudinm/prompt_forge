import os
import faiss
import numpy as np
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from prompt_forge import settings
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


# Path to the FAISS index file stored on disk
INDEX_PATH = os.path.join(settings.BASE_DIR, 'faiss_prompt_index.faiss')


class SimilarPromptsView(APIView):
    """
    Returns prompts similar to the query using FAISS vector similarity.
    Index is persisted on disk to avoid rebuilding every request.
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [CustomBurstRateThrottle, CustomSustainedRateThrottle]

    def get_faiss_index(self):
        """
        Loads FAISS index from disk if it exists, otherwise rebuilds it.
        Returns the index and a list of prompt IDs corresponding to each vector.
        """
        embeddings_qs = PromptEmbedding.objects.select_related('prompt').all()
        if not embeddings_qs.exists():
            return None, []

        ids = []
        vectors = []

        for emb in embeddings_qs:
            vectors.append(np.array(emb.vector, dtype='float32'))
            ids.append(emb.prompt.id)

        vectors = np.stack(vectors)
        dim = vectors.shape[1]

        # Load existing index from disk if available
        if os.path.exists(INDEX_PATH):
            index = faiss.read_index(INDEX_PATH)
            # If the index size does not match the current number of embeddings, rebuild it
            if index.ntotal != len(vectors):
                index = faiss.IndexFlatL2(dim)
                index.add(vectors)
                faiss.write_index(index, INDEX_PATH)
        else:
            # Create and persist the index for the first time
            index = faiss.IndexFlatL2(dim)
            index.add(vectors)
            faiss.write_index(index, INDEX_PATH)

        return index, ids

    def get(self, request):
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response({'error': 'query parameter "q" is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate the embedding for the input query
        query_vector = np.array(generate_embedding(query), dtype='float32')

        # Load or rebuild FAISS index
        index, ids = self.get_faiss_index()
        if not index:
            return Response([], status=status.HTTP_200_OK)

        # Perform similarity search (top 5 most similar prompts)
        k = min(5, len(ids))
        distances, indices = index.search(
            np.expand_dims(query_vector, axis=0), k)
        similar_ids = [ids[i] for i in indices[0]]

        # Retrieve and serialize the matching prompts
        similar_prompts = Prompt.objects.filter(id__in=similar_ids)
        serializer = PromptSerializer(similar_prompts, many=True)
        return Response(serializer.data)

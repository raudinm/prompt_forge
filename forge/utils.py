from transformers import pipeline
from sentence_transformers import SentenceTransformer

# Initialize the local model (can be GPT2, MPT, BLOOM, etc.)
generator = pipeline("text-generation", model="gpt2")
model = SentenceTransformer('all-MiniLM-L6-v2')


def generate_response(prompt: str) -> str:
    """
    Generates a text completion based on the given prompt using a local model.
    """
    result = generator(prompt, max_length=150, do_sample=True)
    return result[0]['generated_text']


def generate_embedding(text: str) -> list[float]:
    """
    Generates an embedding vector for the given text.
    Returns a list of floats compatible with ArrayField.
    """
    embedding = model.encode(text)
    return embedding.tolist()  # Compatible with ArrayField

"""Shared configuration values for the routing and content-engine phases."""

import os


MODEL_NAME = "BAAI/bge-small-en-v1.5"
CHROMA_COLLECTION_NAME = "bot_personas"
DEFAULT_THRESHOLD = 0.55
CHROMA_HOST = "http://chromadb:8000"
CHROMA_PERSIST_DIR = "./chroma_data"
DEFAULT_MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-small-latest")
MISTRAL_API_KEY_ENV = "MISTRAL_API_KEY"
CONTENT_POST_CHAR_LIMIT = 280
DEFAULT_TOPIC_TEMPERATURE = 0.2
DEFAULT_POST_TEMPERATURE = 0.7

import os
import logging
from sentence_transformers import SentenceTransformer, CrossEncoder
import chromadb

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure proxy from environment variables if provided
# Supported env vars: HTTP_PROXY, HTTPS_PROXY, ALL_PROXY
# If no proxy env vars are provided, default to the local proxy at 172.25.72.41:7890
# You can override by setting HTTP_PROXY/HTTPS_PROXY/ALL_PROXY in your environment.
http_proxy = os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy')
https_proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
all_proxy = os.environ.get('ALL_PROXY') or os.environ.get('all_proxy')

# default proxy (will be used only if no env var is set)
_default_proxy = 'http://127.0.0.1:7890'

if all_proxy:
    os.environ['HTTP_PROXY'] = all_proxy
    os.environ['HTTPS_PROXY'] = all_proxy
    os.environ['http_proxy'] = all_proxy
    os.environ['https_proxy'] = all_proxy
    logger.info('Set HTTP_PROXY/HTTPS_PROXY from ALL_PROXY')
else:
    if http_proxy:
        os.environ['HTTP_PROXY'] = http_proxy
        os.environ['http_proxy'] = http_proxy
        logger.info('Set HTTP_PROXY')
    else:
        # Set default proxy when none provided
        os.environ['HTTP_PROXY'] = _default_proxy
        os.environ['http_proxy'] = _default_proxy
        logger.info(f'No HTTP_PROXY provided, using default: {_default_proxy}')

    if https_proxy:
        os.environ['HTTPS_PROXY'] = https_proxy
        os.environ['https_proxy'] = https_proxy
        logger.info('Set HTTPS_PROXY')
    else:
        # Set default https proxy when none provided
        os.environ['HTTPS_PROXY'] = _default_proxy
        os.environ['https_proxy'] = _default_proxy
        logger.info(f'No HTTPS_PROXY provided, using default: {_default_proxy}')

# Initialize chroma client
chromadb_client = chromadb.PersistentClient(path="./chroma_db")
chromadb_collection = chromadb_client.get_or_create_collection(name="default")

# Load cross encoder and embedding model with error handling
try:
    cross_encoder = CrossEncoder('cross-encoder/mmarco-mMiniLMv2-L12-H384-v1')
    logger.info('Loaded CrossEncoder model successfully')
except Exception as e:
    logger.exception('Failed to load CrossEncoder model: %s', e)
    cross_encoder = None

try:
    embedding_model = SentenceTransformer("shibing624/text2vec-base-chinese")
    logger.info('Loaded SentenceTransformer model successfully')
except Exception as e:
    logger.exception('Failed to load SentenceTransformer model: %s', e)
    embedding_model = None


def embed_chunk(chunk: str) -> list[float]:
    if embedding_model is None:
        raise RuntimeError('Embedding model is not loaded')
    embedding = embedding_model.encode(chunk, normalize_embeddings=True)
    return embedding.tolist()
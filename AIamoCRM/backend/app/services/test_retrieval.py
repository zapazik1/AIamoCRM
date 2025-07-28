import os
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables (especially OPENAI_API_KEY)
load_dotenv()

# --- Configuration ---
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "amocrm_kb")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
# --- ---

# Глобальные клиенты, инициализируются один раз на уровне модуля
_chroma_client = None
_openai_client = None
_openai_api_key = None
_openai_ef = None

logging.info("=== Инициализация модуля services.test_retrieval ===")
logging.info(f"Настройки: CHROMA_DB_PATH={CHROMA_DB_PATH}, COLLECTION_NAME={COLLECTION_NAME}, EMBEDDING_MODEL={EMBEDDING_MODEL}")

def get_chroma_client():
    """Initializes and returns a persistent ChromaDB client."""
    global _chroma_client
    
    if _chroma_client is not None:
        logging.debug("Используется существующий клиент ChromaDB")
        return _chroma_client
        
    try:
        logging.info(f"Создание нового постоянного клиента ChromaDB по пути: {CHROMA_DB_PATH}")
        client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        logging.info(f"ChromaDB клиент успешно инициализирован из директории: {CHROMA_DB_PATH}")
        _chroma_client = client
        return client
    except Exception as e:
        logging.error(f"Ошибка инициализации клиента ChromaDB: {e}")
        raise

def get_openai_client():
    """Initializes and returns the OpenAI client."""
    global _openai_client, _openai_api_key
    
    if _openai_client is not None and _openai_api_key is not None:
        logging.debug("Используется существующий клиент OpenAI")
        return _openai_client, _openai_api_key
        
    try:
        logging.info("Создание нового клиента OpenAI")
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Переменная окружения OPENAI_API_KEY не установлена.")
        client = OpenAI(api_key=api_key)
        logging.info("Клиент OpenAI успешно инициализирован.")
        _openai_client = client
        _openai_api_key = api_key
        return client, api_key
    except Exception as e:
        logging.error(f"Ошибка инициализации клиента OpenAI: {e}")
        raise

def get_openai_embedding_function():
    """Initializes and returns the OpenAI embedding function."""
    global _openai_ef, _openai_api_key
    
    if _openai_ef is not None:
        logging.debug("Используется существующая функция эмбеддинга OpenAI")
        return _openai_ef
        
    # Убедимся, что у нас есть API ключ
    if _openai_api_key is None:
        logging.info("Получение API ключа OpenAI для функции эмбеддинга")
        _, _openai_api_key = get_openai_client()
        
    try:
        logging.info(f"Создание новой функции эмбеддинга OpenAI с моделью: {EMBEDDING_MODEL}")
        ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=_openai_api_key,
            model_name=EMBEDDING_MODEL
        )
        _openai_ef = ef
        logging.info(f"Функция эмбеддинга OpenAI успешно инициализирована с моделью: {EMBEDDING_MODEL}")
        return ef
    except Exception as e:
        logging.error(f"Ошибка инициализации функции эмбеддинга OpenAI: {e}")
        raise

def retrieve_amocrm_context(query: str, top_k: int = 5) -> list[dict]:
    """
    Retrieves relevant context chunks from the amoCRM ChromaDB collection.

    Args:
        query: The user's query string.
        top_k: The number of top relevant chunks to retrieve.

    Returns:
        A list of dictionaries, where each dictionary contains the 'text'
        and 'metadata' of a retrieved chunk. Returns empty list on error.
    """
    try:
        # Используем синглтоны вместо создания новых клиентов
        chroma_client = get_chroma_client()
        openai_ef = get_openai_embedding_function()

        # Получаем коллекцию напрямую, так как она уже создана в vector_store.py
        try:
            collection = chroma_client.get_collection(
                name=COLLECTION_NAME,
                embedding_function=openai_ef
            )
            logging.info(f"Accessed ChromaDB collection: '{COLLECTION_NAME}' using OpenAI EF.")
            # --- Добавляем проверку количества ---
            try:
                count = collection.count()
                logging.info(f"Collection '{COLLECTION_NAME}' contains {count} items.")
                if count == 0:
                    logging.warning(f"Collection '{COLLECTION_NAME}' is empty. Indexing might be needed.")
            except Exception as count_e:
                logging.error(f"Could not get count for collection '{COLLECTION_NAME}': {count_e}")
            # --- Конец проверки ---
        except Exception as e:
            logging.error(f"Could not get collection '{COLLECTION_NAME}': {e}")
            # Попытка листинга остается полезной
            try:
                collections = chroma_client.list_collections()
                logging.info(f"Available collections: {[c.name for c in collections]}")
            except Exception as list_e:
                logging.error(f"Could not list collections: {list_e}")
            return []

        # Query the collection using query_texts, letting Chroma handle embedding
        try:
            results = collection.query(
                query_texts=[query],
                n_results=top_k,
                include=['documents', 'metadatas', 'distances']
            )
            logging.info(f"ChromaDB query executed for text query. Found {len(results.get('ids', [[]])[0])} results.")

            # Format the results
            retrieved_docs = []
            ids = results.get('ids', [[]])[0]
            documents = results.get('documents', [[]])[0]
            metadatas = results.get('metadatas', [[]])[0]
            distances = results.get('distances', [[]])[0]

            for i in range(len(ids)):
                 retrieved_docs.append({
                     "id": ids[i],
                     "text": documents[i],
                     "metadata": metadatas[i] if metadatas else {},
                     "distance": distances[i]
                 })

            # Sort by distance (ascending, smaller is better)
            retrieved_docs.sort(key=lambda x: x['distance'])

            return retrieved_docs

        except Exception as e:
            logging.error(f"Error querying ChromaDB collection: {e}")
            return []

    except Exception as e:
        logging.error(f"An unexpected error occurred in retrieve_amocrm_context: {e}")
        return []

# Инициализируем клиенты при загрузке модуля
try:
    logging.info("=== Инициализация постоянных клиентов при загрузке модуля ===")
    chroma_client = get_chroma_client()
    openai_client, api_key = get_openai_client()
    openai_ef = get_openai_embedding_function()
    logging.info("✅ Все клиенты успешно инициализированы на уровне модуля!")
    logging.info(f"✅ ChromaDB клиент: {CHROMA_DB_PATH}")
    logging.info(f"✅ OpenAI клиент: инициализирован (API ключ скрыт)")
    logging.info(f"✅ Функция эмбеддинга: модель {EMBEDDING_MODEL}")
except Exception as e:
    logging.error(f"❌ Ошибка при инициализации клиентов на уровне модуля: {e}")

# --- Interactive Testing ---
# if __name__ == "__main__":
#     print("--- amoCRM KB Retrieval Test ---")
#     print(f"Using ChromaDB from: {CHROMA_DB_PATH}")
#     print(f"Collection: {COLLECTION_NAME}")
#     print(f"Embedding Model: {EMBEDDING_MODEL}")
#     print("Enter your query about amoCRM (or type 'quit' to exit):")

#     while True:
#         user_query = input("Query: ")
#         if user_query.lower() == 'quit':
#             break
#         if not user_query:
#             continue

#         print(f"Retrieving top 5 results for: '{user_query}'...")
#         retrieved_chunks = retrieve_amocrm_context(user_query, top_k=5)

#         if retrieved_chunks:
#             print("--- Retrieved Chunks ---")
#             for i, chunk in enumerate(retrieved_chunks):
#                 print(f"--- Chunk {i+1} (Distance: {chunk['distance']:.4f}) ---")
#                 print(f"Source URL: {chunk['metadata'].get('source_url', 'N/A')}")
#                 print(f"Document Title: {chunk['metadata'].get('doc_title', 'N/A')}")
#                 # print(f"Metadata: {chunk['metadata']}") # Uncomment for full metadata
#                 print("--- Text ---")
#                 print(chunk['text'])
#                 print("------")
#         else:
#             print("Could not retrieve any chunks. Check logs for errors.")

#     print("Exiting test.") 
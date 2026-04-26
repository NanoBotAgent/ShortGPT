import enum
import os

from dotenv import load_dotenv

from shortGPT.database.db_document import TinyMongoDocument

load_dotenv('./.env')


class ApiProvider(enum.Enum):
    OPENAI = "OPENAI_API_KEY"
    OPENAI_BASE_URL = "OPENAI_BASE_URL"
    GEMINI = "GEMINI_API_KEY"
    ELEVEN_LABS = "ELEVENLABS_API_KEY"
    PEXELS = "PEXELS_API_KEY"


class ApiKeyManager:
    api_key_doc_manager = TinyMongoDocument("api_db", "api_keys", "key_doc", create=True)

    @classmethod
    def get_api_key(cls, key: str | ApiProvider):
        if isinstance(key, ApiProvider):
            key = key.value
        api_key = cls.api_key_doc_manager._get(key)
        if api_key:
            return api_key
        env_key = key.replace(" ", "_").upper()
        api_key = os.environ.get(env_key)
        if api_key:
            return api_key
        return ""

    @classmethod
    def set_api_key(cls, key: str | ApiProvider, value: str):
        if isinstance(key, ApiProvider):
            key = key.value
        return cls.api_key_doc_manager._save({key: value})

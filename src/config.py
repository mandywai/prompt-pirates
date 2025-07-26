import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file in src folder
load_dotenv('src/.env')

class Config:
    """Configuration class that loads settings from environment variables."""
    
    # Google API Configuration
    GEMINI_API_KEY: Optional[str] = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL: str = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')
    
    # PDF Configuration
    PDF_FOLDER: str = os.getenv('PDF_FOLDER', 'src/books')
    DEFAULT_CHUNK_SIZE: int = int(os.getenv('DEFAULT_CHUNK_SIZE', '500'))
    
    # Memory Configuration
    FAISS_INDEX_PATH: str = os.getenv('FAISS_INDEX_PATH', 'src/faiss_index.faiss')
    CHUNK_METADATA_PATH: str = os.getenv('CHUNK_METADATA_PATH', 'src/chunk_metadata.pkl')
    EMBEDDING_MODEL: str = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.GEMINI_API_KEY:
            print("⚠️  Warning: GEMINI_API_KEY not set in environment variables")
            print("   Please set it in your .env file or environment")
            return False
        return True
    
    @classmethod
    def print_config(cls):
        """Print current configuration (without sensitive data)."""
        print("🔧 Current Configuration:")
        print(f"   GEMINI_MODEL: {cls.GEMINI_MODEL}")
        print(f"   PDF_FOLDER: {cls.PDF_FOLDER}")
        print(f"   DEFAULT_CHUNK_SIZE: {cls.DEFAULT_CHUNK_SIZE}")
        print(f"   EMBEDDING_MODEL: {cls.EMBEDDING_MODEL}")
        print(f"   LOG_LEVEL: {cls.LOG_LEVEL}")
        print(f"   GEMINI_API_KEY: {'✅ Set' if cls.GEMINI_API_KEY else '❌ Not set'}")

# Convenience function to get config
def get_config() -> Config:
    """Get the configuration instance."""
    return Config 
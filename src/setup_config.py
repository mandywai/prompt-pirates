#!/usr/bin/env python3
"""
Simple script to set up Google API key for the RAG agent.
"""

import os

def create_env_file():
    """Create a .env file with the Google API key."""
    
    print("🔑 Setting up Google API Key for RAG Agent")
    print("=" * 50)
    
    # Check if .env already exists
    if os.path.exists('.env'):
        print("✅ .env file already exists")
        with open('.env', 'r') as f:
            content = f.read()
            if 'GOOGLE_API_KEY' in content:
                print("✅ GOOGLE_API_KEY is already configured")
                return
            else:
                print("⚠️  GOOGLE_API_KEY not found in .env")
    
    # Get API key from user
    print("\n📝 Please enter your Google API key:")
    print("   You can get one from: https://makersuite.google.com/app/apikey")
    print("   (The key will be saved in .env file)")
    
    api_key = input("\n🔑 Google API Key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Please run this script again.")
        return
    
    # Create .env file
    env_content = f"""# Google API Configuration
GEMINI_API_KEY={api_key}

# Model Configuration
GEMINI_MODEL=gemini-2.0-flash

# PDF Configuration
PDF_FOLDER=src/books
DEFAULT_CHUNK_SIZE=500

# Memory Configuration
FAISS_INDEX_PATH=src/faiss_index.faiss
CHUNK_METADATA_PATH=src/chunk_metadata.pkl
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Logging Configuration
LOG_LEVEL=INFO
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("\n✅ .env file created successfully!")
        print("🔒 API key saved securely")
        
        # Test the configuration
        print("\n🧪 Testing configuration...")
        os.environ['GOOGLE_API_KEY'] = api_key
        
        try:
            from config import get_config
            config = get_config()
            if config.GEMINI_API_KEY:
                print("✅ Configuration test successful!")
                print("🚀 You can now run: adk web")
            else:
                print("❌ Configuration test failed")
        except Exception as e:
            print(f"❌ Configuration test failed: {e}")
            
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

def main():
    create_env_file()

if __name__ == "__main__":
    main() 
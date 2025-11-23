"""
Test script to verify the setup and functionality
"""
import sys
import os

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    required_packages = [
        ('langchain', 'LangChain'),
        ('streamlit', 'Streamlit'),
        ('ollama', 'Ollama'),
        ('textblob', 'TextBlob'),
        ('pandas', 'Pandas'),
        ('plotly', 'Plotly'),
        ('bcrypt', 'bcrypt'),
        ('dotenv', 'python-dotenv')
    ]

    all_ok = True
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {name} installed")
        except ImportError:
            print(f"  ✗ {name} NOT installed")
            all_ok = False

    return all_ok

def test_ollama_connection():
    """Test Ollama connection"""
    print("\nTesting Ollama connection...")
    try:
        from ollama import Client
        client = Client(host='http://localhost:11434')
        # Try to list models
        models = client.list()
        print("  ✓ Ollama is running")

        # Check if gemma2:2b is installed
        model_names = [model['name'] for model in models.get('models', [])]
        if any('gemma' in name.lower() for name in model_names):
            print("  ✓ Gemma model is installed")
            return True
        else:
            print("  ✗ Gemma model NOT found")
            print("    Run: ollama pull gemma2:2b")
            return False
    except Exception as e:
        print(f"  ✗ Ollama connection failed: {str(e)}")
        print("    Make sure Ollama is running: ollama serve")
        return False

def test_database():
    """Test database functionality"""
    print("\nTesting database...")
    try:
        from database import Database

        # Create test database
        test_db = Database("data/test_emosup.db")

        # Test user creation
        user_id = test_db.create_user(
            "test_user_" + str(os.getpid()),
            f"test_{os.getpid()}@example.com",
            "testpass123",
            "Test User"
        )

        if user_id:
            print("  ✓ Database operations working")

            # Cleanup
            test_db.close()
            if os.path.exists("data/test_emosup.db"):
                os.remove("data/test_emosup.db")

            return True
        else:
            print("  ✗ Database user creation failed")
            return False

    except Exception as e:
        print(f"  ✗ Database test failed: {str(e)}")
        return False

def test_emotion_analyzer():
    """Test emotion analyzer"""
    print("\nTesting emotion analyzer...")
    try:
        from emotion_analyzer import EmotionAnalyzer

        analyzer = EmotionAnalyzer()

        # Test sentiment analysis
        result = analyzer.analyze_text("I am feeling very happy today!")

        if result and 'primary_emotion' in result:
            print(f"  ✓ Emotion detection working")
            print(f"    Detected emotion: {result['primary_emotion']}")
            print(f"    Sentiment: {result['mood_label']}")
            return True
        else:
            print("  ✗ Emotion detection failed")
            return False

    except Exception as e:
        print(f"  ✗ Emotion analyzer test failed: {str(e)}")
        return False

def test_textblob_data():
    """Test if TextBlob corpora is downloaded"""
    print("\nTesting TextBlob data...")
    try:
        from textblob import TextBlob
        blob = TextBlob("This is a test sentence.")
        _ = blob.sentiment
        print("  ✓ TextBlob corpora available")
        return True
    except Exception as e:
        print(f"  ✗ TextBlob corpora missing: {str(e)}")
        print("    Run: python -m textblob.download_corpora")
        return False

def test_config():
    """Test configuration file"""
    print("\nTesting configuration...")
    try:
        import config

        if hasattr(config, 'OLLAMA_BASE_URL'):
            print(f"  ✓ Configuration loaded")
            print(f"    Ollama URL: {config.OLLAMA_BASE_URL}")
            print(f"    Model: {config.MODEL_NAME}")
            return True
        else:
            print("  ✗ Configuration incomplete")
            return False

    except Exception as e:
        print(f"  ✗ Configuration test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("Emotional Support Companion - Setup Test")
    print("="*60)
    print()

    results = {
        "Imports": test_imports(),
        "TextBlob Data": test_textblob_data(),
        "Configuration": test_config(),
        "Emotion Analyzer": test_emotion_analyzer(),
        "Database": test_database(),
        "Ollama": test_ollama_connection()
    }

    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)

    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:20s}: {status}")

    print()

    all_passed = all(results.values())

    if all_passed:
        print("✓ All tests passed! Your setup is complete.")
        print("\nYou can now run the application:")
        print("  streamlit run app.py")
    else:
        print("✗ Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  - Install missing packages: pip install -r requirements.txt")
        print("  - Download TextBlob data: python -m textblob.download_corpora")
        print("  - Start Ollama: ollama serve")
        print("  - Install Gemma model: ollama pull gemma2:2b")

    print()
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

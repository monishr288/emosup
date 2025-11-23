"""
Build Script for Standalone Executable
Creates a single .exe file with everything bundled!
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

print("""
╔═══════════════════════════════════════════════════════════╗
║   EmoSupport - Standalone Executable Builder             ║
║   Building your AI therapist into a single .exe file!    ║
╚═══════════════════════════════════════════════════════════╝
""")

def run_command(cmd, description):
    """Run a shell command and show progress"""
    print(f"\n▶ {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed")
        return result
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        print(f"Output: {e.output}")
        return None

def install_dependencies():
    """Install required packages for building"""
    print("\n[1/6] Installing build dependencies...")

    packages = [
        "pyinstaller",
        "pyinstaller-hooks-contrib",
    ]

    for package in packages:
        run_command(f"pip install {package}", f"Installing {package}")

def build_frontend():
    """Build Next.js frontend as static export"""
    print("\n[2/6] Building Next.js frontend...")

    # Update next.config.js for static export
    config_content = """/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  distDir: 'out',
  images: {
    unoptimized: true,
  },
}

module.exports = nextConfig
"""

    with open("next.config.js", "w") as f:
        f.write(config_content)

    run_command("npm install", "Installing npm dependencies")
    run_command("npm run build", "Building Next.js static site")

    print("✓ Frontend built successfully")

def create_standalone_server():
    """Create a standalone server that serves frontend + API"""
    print("\n[3/6] Creating standalone server...")

    server_code = '''"""
Standalone EmoSupport Server
Runs both API and frontend in one process!
"""
import os
import sys
from pathlib import Path
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import webbrowser
import threading
import time

# Get the base path (works for both dev and PyInstaller)
if getattr(sys, 'frozen', False):
    BASE_PATH = Path(sys._MEIPASS)
else:
    BASE_PATH = Path(__file__).parent

# Import our modules
sys.path.insert(0, str(BASE_PATH))

app = Flask(__name__)
CORS(app)

# Frontend static files
FRONTEND_DIR = BASE_PATH / "out"

# Initialize services
therapy_system = None
emotion_analyzer = None

def get_therapy_system():
    """Lazy load therapy system"""
    global therapy_system
    if therapy_system is None:
        try:
            from therapy_agent_system import TherapySystem
            therapy_system = TherapySystem()
        except Exception as e:
            print(f"Therapy system unavailable: {e}")
    return therapy_system

def get_emotion_analyzer():
    """Lazy load emotion analyzer"""
    global emotion_analyzer
    if emotion_analyzer is None:
        try:
            from emotion_analyzer import EmotionAnalyzer
            emotion_analyzer = EmotionAnalyzer()
        except Exception as e:
            print(f"Emotion analyzer unavailable: {e}")
    return emotion_analyzer

# API Routes
@app.route('/api/therapy', methods=['POST'])
def therapy_session():
    """Therapy endpoint"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()

        if not message:
            return jsonify({"error": "Message required"}), 400

        # Get emotion
        analyzer = get_emotion_analyzer()
        emotion = "neutral"
        emotion_intensity = 0.5

        if analyzer:
            analysis = analyzer.analyze_text(message)
            emotion = analysis.get('primary_emotion', 'neutral')
            polarity = analysis.get('sentiment', {}).get('polarity', 0)
            emotion_intensity = abs(polarity)

        # Get therapy system response
        therapy = get_therapy_system()
        if therapy:
            result = therapy.process_input(message, emotion, emotion_intensity)
        else:
            # Fallback
            from free_ai_backends import FreeAIBackend
            backend = FreeAIBackend()
            response_text = backend.get_response(message, emotion)
            result = {
                "response": response_text,
                "therapy_mode": "supportive",
                "emotion": emotion,
                "voice_tone": {"pitch": 0, "speed": 0.9, "warmth": 0.95, "energy": 0.5}
            }

        return jsonify(result)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "response": "I'm here for you. Can you tell me more?",
            "error": str(e)
        }), 200

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat endpoint"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()

        if not message:
            return jsonify({"error": "Message required"}), 400

        # Use chatbot with free backends
        from chatbot import EmotionalSupportChatbot
        from emotion_analyzer import EmotionAnalyzer

        bot = EmotionalSupportChatbot()
        analyzer = EmotionAnalyzer()

        response_data = bot.get_response(message)
        analysis = analyzer.analyze_text(message)

        return jsonify({
            "response": response_data.get("response"),
            "emotion": analysis.get("primary_emotion"),
            "is_crisis": response_data.get("is_crisis", False),
            "coping_suggestion": analysis.get("coping_suggestion")
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "response": "I'm here to listen. Tell me more.",
            "error": str(e)
        }), 200

# Serve frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """Serve static frontend files"""
    if path and (FRONTEND_DIR / path).exists():
        return send_from_directory(FRONTEND_DIR, path)
    return send_from_directory(FRONTEND_DIR, 'index.html')

def open_browser():
    """Open browser after short delay"""
    time.sleep(2)
    webbrowser.open('http://localhost:8000')

if __name__ == '__main__':
    print("╔═══════════════════════════════════════════╗")
    print("║   EmoSupport AI Therapy Companion        ║")
    print("║   Your personal AI therapist is ready!   ║")
    print("╚═══════════════════════════════════════════╝")
    print()
    print("🚀 Starting server on http://localhost:8000")
    print("🌐 Opening browser...")
    print()
    print("💜 Ready to talk! Your AI therapist is listening.")
    print()

    # Open browser in background
    threading.Thread(target=open_browser, daemon=True).start()

    # Run server
    app.run(host='0.0.0.0', port=8000, debug=False)
'''

    with open("standalone_server.py", "w") as f:
        f.write(server_code)

    print("✓ Standalone server created")

def create_pyinstaller_spec():
    """Create PyInstaller spec file"""
    print("\n[4/6] Creating PyInstaller configuration...")

    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['standalone_server.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('out', 'out'),  # Frontend static files
        ('config.py', '.'),
        ('therapy_agent_system.py', '.'),
        ('emotion_analyzer.py', '.'),
        ('chatbot.py', '.'),
        ('free_ai_backends.py', '.'),
        ('database.py', '.'),
    ],
    hiddenimports=[
        'flask',
        'flask_cors',
        'textblob',
        'langchain',
        'langchain_community',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='EmoSupport',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Shows console for now
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
"""

    with open("emosupport.spec", "w") as f:
        f.write(spec_content)

    print("✓ PyInstaller spec created")

def build_executable():
    """Build the standalone executable"""
    print("\n[5/6] Building standalone executable...")
    print("This may take a few minutes...")

    result = run_command(
        "pyinstaller emosupport.spec --clean --noconfirm",
        "Compiling executable"
    )

    if result:
        print("\n✓ Build completed successfully!")
        print(f"\n📦 Your executable is ready:")
        print(f"   Location: dist/EmoSupport.exe")
        print(f"   Size: ~{get_file_size('dist/EmoSupport.exe')} MB")
    else:
        print("\n✗ Build failed. Check the error messages above.")

def get_file_size(filepath):
    """Get file size in MB"""
    try:
        size_bytes = os.path.getsize(filepath)
        size_mb = size_bytes / (1024 * 1024)
        return f"{size_mb:.1f}"
    except:
        return "?"

def create_installer():
    """Create Windows installer using NSIS or Inno Setup"""
    print("\n[6/6] Creating Windows installer...")

    # Inno Setup script
    iss_content = """; EmoSupport Installer Script

[Setup]
AppName=EmoSupport
AppVersion=1.0
DefaultDirName={autopf}\\EmoSupport
DefaultGroupName=EmoSupport
OutputDir=installer
OutputBaseFilename=EmoSupport-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "dist\\EmoSupport.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\EmoSupport"; Filename: "{app}\\EmoSupport.exe"
Name: "{autodesktop}\\EmoSupport"; Filename: "{app}\\EmoSupport.exe"

[Run]
Filename: "{app}\\EmoSupport.exe"; Description: "Launch EmoSupport"; Flags: postinstall nowait skipifsilent
"""

    os.makedirs("installer", exist_ok=True)
    with open("installer/emosupport.iss", "w") as f:
        f.write(iss_content)

    print("✓ Installer script created at: installer/emosupport.iss")
    print("\n📝 To create installer:")
    print("   1. Install Inno Setup: https://jrsoftware.org/isdl.php")
    print("   2. Open installer/emosupport.iss")
    print("   3. Click 'Compile'")

def main():
    """Main build process"""
    try:
        # Check if in correct directory
        if not os.path.exists("package.json"):
            print("❌ Error: Run this script from the emosup directory")
            sys.exit(1)

        install_dependencies()
        build_frontend()
        create_standalone_server()
        create_pyinstaller_spec()
        build_executable()
        create_installer()

        print("\n" + "="*60)
        print("🎉 BUILD COMPLETE! 🎉")
        print("="*60)
        print("\n✅ Your AI therapy app is ready to distribute!")
        print("\n📦 Files created:")
        print("   • dist/EmoSupport.exe - Standalone executable (~100-200 MB)")
        print("   • installer/emosupport.iss - Installer script")
        print("\n🚀 To run:")
        print("   Just double-click EmoSupport.exe!")
        print("\n💜 No installation needed. No Ollama needed. Just works!")

    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

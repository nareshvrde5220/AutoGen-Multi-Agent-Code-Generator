#!/usr/bin/env python
"""Quick setup and verification script for AutoGen Multi-Agent Framework."""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Print formatted header."""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_python_version():
    """Check if Python version is 3.10+."""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ ERROR: Python 3.10+ required")
        return False
    print("✅ Python version OK")
    return True

def install_dependencies():
    """Install required packages."""
    print_header("Installing Dependencies")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: Failed to install dependencies: {e}")
        return False

def check_api_key():
    """Check if OpenAI API key is set."""
    print_header("Checking API Configuration")
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key:
        masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
        print(f"✅ OPENAI_API_KEY found: {masked_key}")
        return True
    else:
        print("❌ OPENAI_API_KEY not found in environment")
        print("\nTo set your API key:")
        print("\nWindows PowerShell:")
        print('  $env:OPENAI_API_KEY="your_api_key_here"')
        print("\nLinux/Mac:")
        print('  export OPENAI_API_KEY="your_api_key_here"')
        print("\nOr create a .env file:")
        print('  OPENAI_API_KEY=your_api_key_here')
        return False

def verify_autogen():
    """Verify AutoGen installation."""
    print_header("Verifying AutoGen Installation")
    try:
        import autogen
        print(f"✅ AutoGen version: {autogen.__version__}")
        return True
    except ImportError:
        print("❌ ERROR: AutoGen not installed")
        return False

def verify_structure():
    """Verify project structure."""
    print_header("Verifying Project Structure")
    
    required_paths = [
        "src/agents",
        "src/orchestrator",
        "src/utils",
        "config/config.yaml",
        "ui/streamlit_app.py",
        "requirements.txt",
    ]
    
    all_exist = True
    for path_str in required_paths:
        path = Path(path_str)
        if path.exists():
            print(f"✅ {path_str}")
        else:
            print(f"❌ {path_str} - NOT FOUND")
            all_exist = False
    
    return all_exist

def test_import():
    """Test importing main modules."""
    print_header("Testing Module Imports")
    
    try:
        from src.orchestrator import create_autogen_pipeline
        print("✅ AutoGen pipeline import successful")
        
        from src.agents import (
            RequirementAgent, CodingAgent, ReviewAgent,
            DocumentationAgent, TestAgent, DeploymentAgent, UIAgent
        )
        print("✅ All agent imports successful")
        
        from src.utils import config, setup_logger
        print("✅ Utility imports successful")
        
        return True
    except ImportError as e:
        print(f"❌ ERROR: Import failed: {e}")
        return False

def show_usage_examples():
    """Show usage examples."""
    print_header("Usage Examples")
    
    print("\n1. Command Line Interface:")
    print('   python -m src.main run "Create a REST API for managing todos"')
    
    print("\n2. Streamlit UI:")
    print("   streamlit run ui/streamlit_app.py")
    
    print("\n3. Python API:")
    print("""
from src.orchestrator import create_autogen_pipeline

pipeline = create_autogen_pipeline(model="gpt-4o")
results = pipeline.execute_pipeline(
    user_requirement="Create a CLI tool",
    save_outputs=True
)
    """)

def main():
    """Main setup function."""
    print("\n🚀 AutoGen Multi-Agent Framework Setup\n")
    
    success = True
    
    # Run checks
    success &= check_python_version()
    success &= install_dependencies()
    success &= verify_autogen()
    success &= verify_structure()
    success &= test_import()
    api_key_set = check_api_key()
    
    # Summary
    print_header("Setup Summary")
    
    if success and api_key_set:
        print("✅ ✅ ✅ All checks passed! System ready to use.")
        show_usage_examples()
        print("\n📖 For detailed documentation, see AUTOGEN_README.md")
        return 0
    elif success:
        print("⚠️  Setup complete but API key not configured.")
        print("   Set OPENAI_API_KEY environment variable to use the system.")
        show_usage_examples()
        return 1
    else:
        print("❌ Setup incomplete. Please resolve errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

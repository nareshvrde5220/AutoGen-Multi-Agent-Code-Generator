#!/usr/bin/env python3
"""
Verification script for Multi-Agent Framework installation.
Run this to verify all components are properly installed and configured.
"""

import sys
from pathlib import Path
import importlib.util

# ANSI color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_header(text):
    """Print a header with formatting."""
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    print(f"{BLUE}{text.center(60)}{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}\n")


def print_success(text):
    """Print success message."""
    print(f"{GREEN}✓ {text}{RESET}")


def print_error(text):
    """Print error message."""
    print(f"{RED}✗ {text}{RESET}")


def print_warning(text):
    """Print warning message."""
    print(f"{YELLOW}⚠ {text}{RESET}")


def print_info(text):
    """Print info message."""
    print(f"  {text}")


def check_python_version():
    """Check if Python version is 3.10+."""
    print_header("Checking Python Version")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 10:
        print_success(f"Python version: {version_str}")
        return True
    else:
        print_error(f"Python version: {version_str} (requires 3.10+)")
        return False


def check_directory_structure():
    """Check if all required directories exist."""
    print_header("Checking Directory Structure")
    
    required_dirs = [
        "src/agents",
        "src/orchestrator",
        "src/utils",
        "tests",
        "output/generated_code",
        "output/documentation",
        "output/tests",
        "ui",
        "config"
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print_success(f"Directory exists: {dir_path}")
        else:
            print_error(f"Directory missing: {dir_path}")
            all_exist = False
    
    return all_exist


def check_required_files():
    """Check if all required files exist."""
    print_header("Checking Required Files")
    
    required_files = [
        "src/agents/__init__.py",
        "src/agents/requirement_agent.py",
        "src/agents/coding_agent.py",
        "src/agents/review_agent.py",
        "src/agents/documentation_agent.py",
        "src/agents/test_agent.py",
        "src/agents/deployment_agent.py",
        "src/agents/ui_agent.py",
        "src/orchestrator/pipeline.py",
        "src/utils/config.py",
        "src/utils/logger.py",
        "ui/streamlit_app.py",
        "config/config.yaml",
        "config/.env.example",
        "requirements.txt",
        "README.md",
        "QUICKSTART.md"
    ]
    
    all_exist = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print_success(f"File exists: {file_path}")
        else:
            print_error(f"File missing: {file_path}")
            all_exist = False
    
    return all_exist


def check_dependencies():
    """Check if required Python packages are installed."""
    print_header("Checking Python Dependencies")
    
    required_packages = [
        ("openai", "OpenAI API client"),
        ("streamlit", "Streamlit web framework"),
        ("pydantic", "Data validation"),
        ("dotenv", "Environment variables"),
        ("yaml", "YAML configuration"),
        ("tenacity", "Retry logic")
    ]
    
    all_installed = True
    for package_name, description in required_packages:
        # Handle package name variations
        import_name = package_name
        if package_name == "dotenv":
            import_name = "dotenv"
        elif package_name == "yaml":
            import_name = "yaml"
        
        try:
            spec = importlib.util.find_spec(import_name)
            if spec is not None:
                print_success(f"{package_name} - {description}")
            else:
                print_error(f"{package_name} - {description} (not installed)")
                all_installed = False
        except (ImportError, ModuleNotFoundError):
            print_error(f"{package_name} - {description} (not installed)")
            all_installed = False
    
    if not all_installed:
        print_warning("\nTo install missing dependencies, run:")
        print_info("pip install -r requirements.txt")
    
    return all_installed


def check_configuration():
    """Check if configuration is set up."""
    print_header("Checking Configuration")
    
    env_file = Path("config/.env")
    
    if env_file.exists():
        print_success("Environment file exists: config/.env")
        
        # Check if API key is set
        try:
            with open(env_file, 'r') as f:
                content = f.read()
                if 'OPENAI_API_KEY=' in content:
                    if 'your_openai_api_key_here' in content:
                        print_warning("API key not configured (using example value)")
                        print_info("Edit config/.env to add your actual API key")
                        return False
                    else:
                        print_success("API key appears to be configured")
                        return True
                else:
                    print_error("OPENAI_API_KEY not found in .env file")
                    return False
        except Exception as e:
            print_error(f"Error reading .env file: {e}")
            return False
    else:
        print_warning("Environment file not found: config/.env")
        print_info("Copy config/.env.example to config/.env and add your API key")
        return False


def check_imports():
    """Try importing main modules."""
    print_header("Checking Module Imports")
    
    sys.path.insert(0, str(Path.cwd()))
    
    modules_to_check = [
        ("src.agents", "Agents package"),
        ("src.orchestrator", "Orchestrator package"),
        ("src.utils", "Utils package")
    ]
    
    all_imported = True
    for module_name, description in modules_to_check:
        try:
            importlib.import_module(module_name)
            print_success(f"{description} imported successfully")
        except ImportError as e:
            print_error(f"{description} import failed: {e}")
            all_imported = False
    
    return all_imported


def print_summary(results):
    """Print summary of verification results."""
    print_header("Verification Summary")
    
    total = len(results)
    passed = sum(results.values())
    
    for check_name, passed_check in results.items():
        if passed_check:
            print_success(check_name)
        else:
            print_error(check_name)
    
    print(f"\n{passed}/{total} checks passed")
    
    if passed == total:
        print_success("\n✨ All checks passed! Your installation is ready to use.")
        print_info("\nNext steps:")
        print_info("1. Configure your API key in config/.env")
        print_info("2. Run: streamlit run ui/streamlit_app.py")
        print_info("3. Or read QUICKSTART.md for more options")
    else:
        print_warning("\n⚠️  Some checks failed. Please address the issues above.")


def main():
    """Run all verification checks."""
    print(f"{BLUE}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     Multi-Agent Framework - Installation Verification     ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{RESET}")
    
    results = {
        "Python Version": check_python_version(),
        "Directory Structure": check_directory_structure(),
        "Required Files": check_required_files(),
        "Python Dependencies": check_dependencies(),
        "Configuration": check_configuration(),
        "Module Imports": check_imports()
    }
    
    print_summary(results)
    
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())

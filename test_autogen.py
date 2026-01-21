"""Test script to verify AutoGen integration."""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def test_agent_imports():
    """Test that all agents can be imported."""
    print("Testing agent imports...")
    try:
        from src.agents import (
            RequirementAgent,
            CodingAgent,
            ReviewAgent,
            DocumentationAgent,
            TestAgent,
            DeploymentAgent,
            UIAgent
        )
        print("✅ All agents imported successfully")
        return True
    except Exception as e:
        print(f"❌ Agent import failed: {e}")
        return False

def test_autogen_availability():
    """Test that AutoGen is available."""
    print("\nTesting AutoGen availability...")
    try:
        from autogen import ConversableAgent, GroupChat, GroupChatManager
        print("✅ AutoGen imported successfully")
        return True
    except Exception as e:
        print(f"❌ AutoGen import failed: {e}")
        print("   Run: pip install pyautogen==0.2.35")
        return False

def test_agent_initialization():
    """Test initializing an agent."""
    print("\nTesting agent initialization...")
    
    # Use a dummy API key for structure test
    test_api_key = os.getenv("OPENAI_API_KEY", "test_key_for_structure_check")
    
    try:
        from src.agents import RequirementAgent
        agent = RequirementAgent(api_key=test_api_key, model="gpt-4o")
        
        # Check that agent has the required methods
        assert hasattr(agent, 'get_agent'), "Missing get_agent method"
        assert hasattr(agent, 'analyze_requirements'), "Missing analyze_requirements method"
        
        # Check that underlying AutoGen agent exists
        autogen_agent = agent.get_agent()
        from autogen import ConversableAgent
        assert isinstance(autogen_agent, ConversableAgent), "Not a ConversableAgent"
        
        print("✅ Agent initialization successful")
        print(f"   Agent name: {agent.name}")
        print(f"   Agent model: {agent.model}")
        return True
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pipeline_import():
    """Test importing the AutoGen pipeline."""
    print("\nTesting pipeline import...")
    try:
        from src.orchestrator import create_autogen_pipeline, AutoGenPipeline
        print("✅ AutoGen pipeline imported successfully")
        return True
    except Exception as e:
        print(f"❌ Pipeline import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config():
    """Test configuration loading."""
    print("\nTesting configuration...")
    try:
        from src.utils import config
        
        # Check that config can be accessed
        model = config.get('api', 'model_id', default='gpt-4o')
        max_rounds = config.get('pipeline', 'max_rounds', default=10)
        
        print(f"✅ Configuration loaded successfully")
        print(f"   Model: {model}")
        print(f"   Max rounds: {max_rounds}")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_full_agent_set():
    """Test that all 7 agents can be initialized."""
    print("\nTesting full agent set...")
    
    test_api_key = os.getenv("OPENAI_API_KEY", "test_key")
    
    try:
        from src.agents import (
            RequirementAgent, CodingAgent, ReviewAgent,
            DocumentationAgent, TestAgent, DeploymentAgent, UIAgent
        )
        
        agents = [
            RequirementAgent(test_api_key, "gpt-4o"),
            CodingAgent(test_api_key, "gpt-4o"),
            ReviewAgent(test_api_key, "gpt-4o"),
            DocumentationAgent(test_api_key, "gpt-4o"),
            TestAgent(test_api_key, "gpt-4o"),
            DeploymentAgent(test_api_key, "gpt-4o"),
            UIAgent(test_api_key, "gpt-4o"),
        ]
        
        agent_names = [agent.name for agent in agents]
        print(f"✅ All 7 agents initialized:")
        for name in agent_names:
            print(f"   - {name}")
        
        return True
    except Exception as e:
        print(f"❌ Full agent set test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("="*60)
    print("  AutoGen Integration Test Suite")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("Agent Imports", test_agent_imports()))
    results.append(("AutoGen Availability", test_autogen_availability()))
    results.append(("Agent Initialization", test_agent_initialization()))
    results.append(("Pipeline Import", test_pipeline_import()))
    results.append(("Configuration", test_config()))
    results.append(("Full Agent Set", test_full_agent_set()))
    
    # Summary
    print("\n" + "="*60)
    print("  Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! AutoGen integration is working correctly.")
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("\n⚠️  Note: OPENAI_API_KEY not set. Set it to run actual agent operations.")
        else:
            print("\n✅ OPENAI_API_KEY is configured. Ready for production use!")
        
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed. Please check errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

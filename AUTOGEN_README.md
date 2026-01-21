# AutoGen Integration - Multi-Agent Framework

## Overview

The Multi-Agent Coding Framework has been fully rebuilt using **Microsoft AutoGen** framework with **GPT-4o** model for proper multi-agent orchestration and collaboration.

## What's New

### AutoGen Framework Integration
- **All 7 agents** now use AutoGen's `ConversableAgent` class
- **GroupChat orchestration** with `GroupChatManager` for coordinated agent collaboration
- **Proper agent-to-agent communication** instead of sequential pipeline
- **Automatic speaker selection** based on conversation context

### Model Configuration
- **Primary Model**: `gpt-4o` (configured in `config/config.yaml`)
- **Fallback models**: `gpt-4o`, `gpt-4-turbo` available in UI
- All agents use consistent model configuration

### Architecture Changes

#### Agents (All using AutoGen ConversableAgent)
1. **RequirementAnalyst** - Analyzes and structures requirements
2. **SeniorDeveloper** - Generates production-ready Python code  
3. **CodeReviewer** - Reviews code with APPROVED/NEEDS_REVISION feedback
4. **TechnicalWriter** - Creates comprehensive documentation
5. **QAEngineer** - Generates pytest test cases
6. **DevOpsEngineer** - Creates deployment configurations
7. **UIDesigner** - Generates Streamlit UI code

#### Orchestration
- **AutoGenPipeline** (`src/orchestrator/autogen_pipeline.py`)
  - Uses AutoGen GroupChat for agent coordination
  - Orchestrator agent manages workflow sequence
  - Supports iterative code review with automatic revisions
  - Parallel execution of documentation, tests, and deployment

### Configuration

#### config/config.yaml
```yaml
api:
  provider: "openai"
  model_id: "gpt-4o"
  api_key_env: "OPENAI_API_KEY"

pipeline:
  max_iterations: 3
  max_rounds: 10
```

#### Environment Variables
```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional
MODEL_NAME=gpt-4o
```

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

Key packages:
- `pyautogen==0.2.35` - Microsoft AutoGen framework
- `openai>=1.58.1` - OpenAI API client
- `streamlit==1.39.0` - Web UI

### 2. Set Up API Key
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your_openai_api_key_here"

# Linux/Mac
export OPENAI_API_KEY="your_openai_api_key_here"
```

## Usage

### Command Line Interface

```bash
# Run with default model (gpt-4o)
python -m src.main run "Create a REST API for managing todos"

# Specify custom model
python -m src.main run "Create a data pipeline" --model gpt-4o

# Read requirements from file
python -m src.main run @requirements.txt

# With custom API key
python -m src.main run "Create a web scraper" --api-key YOUR_KEY
```

### Streamlit UI

```bash
streamlit run ui/streamlit_app.py
```

Navigate to http://localhost:8501

#### UI Features:
- **API Key Configuration** - Enter OpenAI API key securely
- **Model Selection** - Choose from gpt-4o, gpt-4-turbo, or other OpenAI models
- **Live Progress Tracking** - See each agent's work in real-time
- **Organized Output Tabs** - View code, docs, tests, deployment separately
- **Download Artifacts** - Download generated files
- **Error Handling** - Detailed error messages with traceback

### Python API

```python
from src.orchestrator import create_autogen_pipeline

# Initialize pipeline
pipeline = create_autogen_pipeline(
    api_key="your_openai_key",
    model="gpt-4o"
)

# Execute
results = pipeline.execute_pipeline(
    user_requirement="Create a CLI tool for file encryption",
    save_outputs=True
)

# Access outputs
print(results['outputs']['requirements'])
print(results['outputs']['code'])
print(results['outputs']['documentation'])
```

## AutoGen GroupChat Workflow

```
User Requirement
      ↓
Orchestrator (manages workflow)
      ↓
RequirementAnalyst → Structured Requirements
      ↓
SeniorDeveloper → Python Code
      ↓
CodeReviewer → Review (APPROVED or NEEDS_REVISION)
      ↓ (if NEEDS_REVISION)
SeniorDeveloper → Revised Code (iterative)
      ↓ (when APPROVED)
Parallel Execution:
  ├─→ TechnicalWriter → Documentation
  ├─→ QAEngineer → Test Cases
  ├─→ DevOpsEngineer → Deployment Config
  └─→ UIDesigner → Streamlit UI
      ↓
TERMINATE (all artifacts complete)
```

## Agent System Messages

Each agent has a specialized system message defining its role:

- **RequirementAnalyst**: Business analyst converting natural language to structured specs
- **SeniorDeveloper**: Expert Python developer (10+ years) generating production code
- **CodeReviewer**: Principal engineer reviewing for correctness, security, performance
- **TechnicalWriter**: Technical documentation specialist
- **QAEngineer**: QA engineer creating comprehensive pytest tests
- **DevOpsEngineer**: DevOps engineer for containerization and deployment
- **UIDesigner**: UI/UX engineer specializing in Streamlit

## Output Structure

```
output/
└── run_YYYYMMDD_HHMMSS_runid/
    ├── generated_code/
    │   ├── generated_code.py
    │   └── streamlit_ui.py
    ├── documentation/
    │   ├── requirements.md
    │   ├── code_review.md
    │   ├── documentation.md
    │   └── deployment_config.md
    └── tests/
        └── test_generated.py
```

## Key Features

### 1. Iterative Code Review
- CodeReviewer provides structured feedback
- SeniorDeveloper revises based on feedback
- Up to 3 iterations (configurable)
- Automatic approval detection

### 2. Parallel Artifact Generation
- Documentation, tests, deployment, and UI generated concurrently
- Faster overall execution
- Independent agent operations

### 3. Conversation History
- Full GroupChat message history captured
- Agent-to-agent communication logged
- Metadata including message count, timing

### 4. Error Handling
- Graceful error recovery
- Detailed error logging
- Failed step isolation

## Troubleshooting

### API Key Issues
```bash
# Verify environment variable
echo $env:OPENAI_API_KEY  # Windows
echo $OPENAI_API_KEY      # Linux/Mac
```

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Model Not Found
- Ensure you have access to gpt-4o model
- Fallback to gpt-4o if needed
- Check OpenAI account quotas

### AutoGen Errors
```bash
# Verify AutoGen version
pip show pyautogen

# Should be 0.2.35 or higher
```

## Performance Considerations

- **Model**: gpt-4o recommended for best results
- **Max Rounds**: Default 10 (increase for complex projects)
- **Max Iterations**: Default 3 for code review loop
- **Temperature**: 
  - 0.2 for code generation (deterministic)
  - 0.3-0.4 for requirements, docs, tests
  - 0.1 for orchestrator (focused)

## Development

### Adding New Agents

```python
from autogen import ConversableAgent

class MyAgent:
    def __init__(self, api_key: str, model: str = "gpt-4o", temperature: float = 0.3):
        llm_config = {
            "model": model,
            "api_key": api_key,
            "temperature": temperature,
            "max_tokens": 2000,
        }
        
        self.agent = ConversableAgent(
            name="MyAgentName",
            system_message="Your agent's role and instructions",
            llm_config=llm_config,
            human_input_mode="NEVER",
        )
    
    def get_agent(self) -> ConversableAgent:
        return self.agent
```

### Modifying GroupChat

Edit `src/orchestrator/autogen_pipeline.py`:
- Adjust `max_rounds` for conversation length
- Modify `speaker_selection_method` ("auto", "round_robin", "random")
- Update orchestrator's system message for workflow changes

## Contributing

When contributing to the AutoGen integration:
1. Maintain ConversableAgent wrapper pattern
2. Update orchestrator system message for new agents
3. Test with gpt-4o model
4. Document agent system messages
5. Update this README

## License

Same as main project license.

## Support

For issues related to:
- **AutoGen Framework**: https://github.com/microsoft/autogen
- **OpenAI API**: https://platform.openai.com/docs
- **This Project**: See main README.md

---

**Version**: 2026.1.0  
**Framework**: Microsoft AutoGen 0.2.35  
**Model**: OpenAI GPT-4o  
**Last Updated**: January 2026

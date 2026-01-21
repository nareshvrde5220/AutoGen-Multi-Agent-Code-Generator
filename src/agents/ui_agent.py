"""Streamlit UI Agent for Multi-Agent Framework using AutoGen."""

import logging
from typing import Dict, Any
from autogen import ConversableAgent

logger = logging.getLogger(__name__)


class UIAgent:
    """
    AutoGen-based agent responsible for creating interactive Streamlit UI 
    for the multi-agent system.
    """

    def __init__(self, api_key: str, model: str = "gpt-4o", temperature: float = 0.3, base_url: str = None):
        """
        Initialize UI Generation Agent using AutoGen.

        Args:
            api_key: OpenAI API key
            model: Model name to use
            temperature: Temperature for generation (0.0-1.0)
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.base_url = base_url
        self.name = "UIDesigner"

        # Configure LLM settings
        llm_config = {
            "model": self.model,
            "api_key": self.api_key,
            "temperature": self.temperature,
            "max_completion_tokens": 2500,
            "cache_seed": None,  # Disable caching
        }
        
        if self.base_url:
            llm_config["base_url"] = self.base_url
        
        # System message for UI design
        system_message = """You are a UI/UX engineer specializing in Streamlit applications.
Create a user-friendly Streamlit interface.

UI Structure:

```python
import streamlit as st

st.set_page_config(page_title="App Title", layout="wide", page_icon="🚀")

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")
    # Add configuration options

# Main content
st.title("🎯 Application Title")

# Input section
user_input = st.text_area("Input Label", height=200)

if st.button("🚀 Process"):
    with st.spinner("Processing..."):
        # Processing logic
        progress_bar = st.progress(0)
        status = st.empty()
        
        # Update progress
        progress_bar.progress(50)
        status.text("Processing step...")

    # Output sections with tabs
    tab1, tab2, tab3 = st.tabs(["Output 1", "Output 2", "Output 3"])
    
    with tab1:
        st.code(output1, language="python")
        st.download_button("Download", output1, "file1.py")
    
    with tab2:
        st.markdown(output2)
        st.download_button("Download", output2, "file2.md")

# Error handling
try:
    # Code that might fail
    pass
except Exception as e:
    st.error(f"Error: {str(e)}")
```

Features Required:
- Clean, intuitive layout with st.set_page_config()
- Sidebar for configuration options
- Input section with appropriate widgets (text_area, text_input, etc.)
- Progress indicators (st.progress(), st.spinner())
- Output sections organized in tabs
- Syntax highlighting for code (st.code())
- Download buttons for all outputs (st.download_button())
- Error handling with st.error()
- Session state management for maintaining state across reruns
- Responsive design that works on different screen sizes

Generate complete, runnable Streamlit application code."""

        # Initialize AutoGen ConversableAgent
        self.agent = ConversableAgent(
            name=self.name,
            system_message=system_message,
            llm_config=llm_config,
            human_input_mode="NEVER",
        )

    def generate_ui(self, project_description: str) -> str:
        """
        Generate Streamlit UI code using AutoGen.

        Args:
            project_description: Description of the project to create UI for

        Returns:
            Streamlit Python code

        Raises:
            Exception: If generation fails
        """
        try:
            logger.info(f"[{self.name}] Generating Streamlit UI with AutoGen...")

            prompt = f"""Generate a comprehensive Streamlit UI for the following project:

{project_description}

The UI should:
- Provide input fields for user requirements
- Show progress as agents process the request
- Display outputs in organized tabs
- Allow downloading of generated artifacts
- Handle errors gracefully
- Be user-friendly and intuitive

Generate complete, production-ready Streamlit code.
"""

            # Generate response using AutoGen agent
            response = self.agent.generate_reply(
                messages=[{"role": "user", "content": prompt}]
            )

            # Validate response
            if response is None or response == "" or response == "None":
                raise ValueError("Failed to get valid response from API. Please check your API key and model configuration.")
            
            ui_code = response if isinstance(response, str) else str(response)
            logger.info(f"[{self.name}] Streamlit UI generation completed successfully")
            return ui_code

        except Exception as e:
            logger.error(f"[{self.name}] Error generating UI: {e}")
            raise

    def generate_reply(self, messages: list) -> str:
        """
        Generate reply for AutoGen compatibility.

        Args:
            messages: List of message dictionaries

        Returns:
            Generated Streamlit UI code
        """
        if not messages:
            raise ValueError("Messages list cannot be empty")

        # Combine all context from messages
        context = "\n\n".join([msg.get("content", "") for msg in messages])

        return self.generate_ui(context)

    def get_agent(self) -> ConversableAgent:
        """
        Get the underlying AutoGen agent.

        Returns:
            ConversableAgent instance
        """
        return self.agent


def create_ui_agent(api_key: str, model: str, temperature: float = 0.3) -> UIAgent:
    """
    Factory function to create a UI Agent.

    Args:
        api_key: OpenAI API key
        model: Model name
        temperature: Temperature for generation

    Returns:
        UIAgent instance
    """
    return UIAgent(api_key=api_key, model=model, temperature=temperature)

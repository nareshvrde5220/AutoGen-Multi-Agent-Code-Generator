"""Streamlit UI for Multi-Agentic Coding Framework with AutoGen (2026 Edition)."""

import streamlit as st
import sys
import os
import traceback
from pathlib import Path
from datetime import datetime

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.orchestrator.autogen_pipeline import create_pipeline
from src.utils import setup_logger

# Page configuration with modern 2026 theme
st.set_page_config(
    page_title="AutoGen Multi-Agent Code Generator | 2026",
    layout="wide",
    page_icon="🚀",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "# AutoGen Multi-Agent Code Generator 2026\nPowered by AutoGen with GPT-4o"
    }
)

# Custom CSS for compact layout with monitor compatibility
st.markdown("""
<style>
    /* Scale down to 90% for optimal single-window fit */
    .main .block-container {
        max-width: 100% !important;
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
        zoom: 0.9;
    }
    
    /* Responsive adjustments for different screen sizes */
    @media (max-width: 1366px) {
        .main .block-container {
            zoom: 0.85;
        }
    }
    
    @media (min-width: 1920px) {
        .main .block-container {
            zoom: 0.92;
        }
    }
    
    @media (min-width: 2560px) {
        .main .block-container {
            zoom: 1.0;
        }
    }
    
    /* Readable metrics with proper scaling */
    [data-testid="stMetricValue"] {
        font-size: 1.4rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.95rem !important;
    }
    
    /* Optimal spacing */
    .element-container {
        margin-bottom: 0.4rem !important;
    }
    
    /* Readable expander */
    .streamlit-expanderHeader {
        font-size: 1rem !important;
        padding: 0.6rem !important;
    }
    
    /* Readable text areas */
    textarea {
        font-size: 1rem !important;
        line-height: 1.5 !important;
    }
    
    /* Readable buttons */
    button {
        font-size: 1.05rem !important;
        padding: 0.5rem 1rem !important;
    }
    
    /* Sidebar scaling */
    section[data-testid="stSidebar"] {
        zoom: 0.9;
    }
    
    /* Advanced Settings slider - fill full width */
    .stExpander [data-testid="stSlider"] {
        width: 100% !important;
    }
    
    .stExpander [data-testid="stSlider"] > div {
        width: 100% !important;
    }
    
    .stExpander .stSlider > div > div {
        padding-right: 0 !important;
    }
    
    /* Agent status indicators */
    .agent-pending {
        padding: 0.4rem 0.8rem;
        margin: 0.3rem 0;
        border-radius: 6px;
        background: #f3f4f6;
        color: #6b7280;
    }
    
    .agent-running {
        padding: 0.4rem 0.8rem;
        margin: 0.3rem 0;
        border-radius: 6px;
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        color: white;
        font-weight: 600;
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    .agent-completed {
        padding: 0.4rem 0.8rem;
        margin: 0.3rem 0;
        border-radius: 6px;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        font-weight: 600;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'pipeline_results' not in st.session_state:
    st.session_state.pipeline_results = None
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'agent_status' not in st.session_state:
    st.session_state.agent_status = {
        'requirement': 'pending',
        'coding': 'pending',
        'review': 'pending',
        'documentation': 'pending',
        'testing': 'pending',
        'deployment': 'pending',
        'ui': 'pending'
    }

# Modern 2026 Theme CSS
st.markdown("""
<style>
    /* 2026 Modern Theme */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .sub-header {
        font-size: 1rem;
        color: #6b7280;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 300;
    }
    
    .section-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1f2937;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        border-left: 4px solid #667eea;
        padding-left: 1rem;
    }
    
    /* Status badges */
    .status-success {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 4px 6px rgba(16, 185, 129, 0.3);
    }
    
    .status-error {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 4px 6px rgba(239, 68, 68, 0.3);
    }
    
    .status-warning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 4px 6px rgba(245, 158, 11, 0.3);
    }
    
    /* Card styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f9fafb;
        padding: 10px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 8px;
        padding: 0 24px;
        font-weight: 600;
        background-color: white;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: #667eea;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(16, 185, 129, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(16, 185, 129, 0.4);
    }
    
    /* Download button */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border-radius: 8px;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(16, 185, 129, 0.2);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f9fafb 0%, #ffffff 100%);
    }
    
    /* Input fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1rem;
        color: #6b7280;
        font-size: 0.85rem;
        margin-top: 2rem;
        border-top: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with modern design
with st.sidebar:
    st.markdown("### 🚀 AI Configuration")
    st.markdown("---")

    # API Key input
    api_key = st.text_input(
        "🔑 OpenAI API Key",
        type="password",
        value=st.session_state.api_key,
        help="Enter your OpenAI API key for GPT-4o",
        placeholder="sk-..."
    )

    if api_key:
        st.session_state.api_key = api_key
        os.environ['OPENAI_API_KEY'] = api_key
        st.success("✅ API Key configured")
    
    # Model selection
    model = st.selectbox(
        "🤖 AI Model",
        ["gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo", "gpt-4o-mini"],
        index=0,
        help="Select the AI model to use"
    )
    st.info(f"**Selected Model:** {model}")
    
    # Custom API endpoint
    base_url = st.text_input(
        "🌐 Custom API Base URL (Optional)",
        value="",
        help="For custom API endpoints (leave empty for official OpenAI API)",
        placeholder="http://localhost:11434/v1 (optional)"
    )
    if base_url and base_url.strip():
        st.info(f"🔗 Using custom endpoint")
    else:
        base_url = None

    # Advanced settings with better UI
    with st.expander("⚙️ Advanced Settings", expanded=False):
        max_iterations = st.slider(
            "Max Code Review Iterations",
            min_value=1,
            max_value=5,
            value=2,
            help="Maximum number of AutoGen feedback iterations between coding and review agents"
        )

        save_outputs = st.checkbox(
            "💾 Save Outputs to Files",
            value=True,
            help="Save generated artifacts to output directory with timestamps"
        )

    st.markdown("---")

    # Information with modern badges
    st.markdown("### 📚 About Multi-Agent Framework")
    st.info("""
    **Multi-Agentic System powered by AutoGen with GPT-4o**
    
    This framework orchestrates 7 specialized AI agents that collaborate to transform 
    natural language requirements into production-ready code with full documentation, 
    tests, and deployment configuration.
    """)
    
    st.markdown("#### 🔄 Agent Pipeline")
    
    # Dynamic agent status display
    agents = [
        ('requirement', '📋', 'Requirement Analyst', 'Structure requirements'),
        ('coding', '💻', 'Senior Developer', 'Generate code'),
        ('review', '🔍', 'Code Reviewer', 'Review & iterate (AutoGen loop)'),
        ('documentation', '📖', 'Tech Writer', 'Create documentation'),
        ('testing', '🧪', 'QA Engineer', 'Generate tests'),
        ('deployment', '🚀', 'DevOps', 'Deployment config'),
        ('ui', '🎨', 'UI Designer', 'Streamlit interface')
    ]
    
    for idx, (key, icon, name, desc) in enumerate(agents, 1):
        status = st.session_state.agent_status[key]
        status_class = f"agent-{status}"
        st.markdown(f'<div class="{status_class}">{idx}. {icon} <strong>{name}</strong> - {desc}</div>', unsafe_allow_html=True)
    
    # Footer
    current_year = datetime.now().year
    st.caption(f"© {current_year} AutoGen Multi-Agent Code Generator • Powered by AutoGen with GPT-4o")

# Main content with hero section
st.markdown('<div class="main-header">🚀 AutoGen Multi-Agent Code Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Transform Ideas into Production-Ready Code with AI Agent Collaboration</div>', unsafe_allow_html=True)

# Feature highlights
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🤖 AI Agents", "7", help="Specialized agents working together")
with col2:
    st.metric("🔄 Framework", "Multi-Agent", help="Collaborative agent system")
with col3:
    st.metric("⚡ Model", "GPT-4o", help="OpenAI's GPT-4o via AutoGen")
with col4:
    st.metric("📅 Version", "2026", help="Latest 2026 edition")

# Input section with modern design
st.markdown('<div class="section-header">📝 Enter Your Requirements</div>', unsafe_allow_html=True)

requirement_input = st.text_area(
    "Describe what you want to build:",
    height=120,
    placeholder="Example: Create a REST API endpoint that handles user authentication with JWT tokens, includes rate limiting, and proper error handling...",
    help="Provide a clear, detailed description of what you want to build. Be specific about functionality, constraints, and expected behavior.",
    key="requirement_input"
)

# Sample requirements with better UI
with st.expander("💡 Quick Start Examples", expanded=False):
    st.markdown("**Click any example to load it:**")
    
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📊 Simple Function", use_container_width=True):
            requirement_input = "Create a Python function that calculates the factorial of a number with input validation and error handling"
            st.rerun()

        if st.button("🌐 REST API"):
            requirement_input = """Create a REST API using FastAPI that:
- Manages a todo list with CRUD operations
- Stores data in SQLite database
- Includes authentication using JWT tokens
- Has input validation using Pydantic models"""
            st.rerun()

    with col2:
        if st.button("📁 Data Processor", use_container_width=True):
            requirement_input = "Build a CSV data processor that reads a file, removes duplicates, validates data types, and exports to JSON with error logging"
            st.rerun()

        if st.button("🧮 Calculator Class", use_container_width=True):
            requirement_input = "Create a Calculator class with basic arithmetic operations, history tracking, and a clear method. Include comprehensive unit tests"
            st.rerun()

# Process button with modern styling
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Add custom CSS for processing state
    if st.session_state.processing:
        st.markdown("""
        <style>
        .stButton > button {
            background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
            color: white !important;
            border: none !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
    process_button = st.button(
        "🚀 Generate Code with AI Agents" if not st.session_state.processing else "⏳ Processing...",
        type="primary",
        disabled=not requirement_input or not st.session_state.api_key or st.session_state.processing,
        use_container_width=True,
        help="Start the multi-agent pipeline"
    )

if not st.session_state.api_key:
    st.error("🔒 **API Key Required** - Please enter your OpenAI API key in the sidebar to start generating code.")
elif not requirement_input:
    st.info("💡 **Ready to Start** - Enter your requirements above or click a sample example to begin.")

# Processing logic with enhanced UI
if process_button and requirement_input and st.session_state.api_key:
    st.session_state.processing = True
    
    # Reset agent statuses
    for key in st.session_state.agent_status:
        st.session_state.agent_status[key] = 'pending'

    try:
        # Create modern progress indicators
        progress_container = st.container()
        
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Agent status cards
            agent_status = st.empty()

        # Initialize pipeline
        status_text.markdown("### 🔧 Initializing AutoGen Multi-Agent Pipeline...")
        with agent_status:
            st.info("⚙️ Setting up 7 specialized AI agents with AutoGen orchestration...")
        progress_bar.progress(5)

        try:
            # Set base_url environment variable if provided
            if base_url and base_url.strip():
                os.environ['OPENAI_BASE_URL'] = base_url.strip()
                st.session_state.base_url = base_url.strip()
            
            pipeline = create_pipeline(api_key=st.session_state.api_key, model=model)
        except Exception as init_error:
            tb = traceback.format_exc()
            st.error(f"❌ **Pipeline Initialization Error:**\n\n{str(init_error)}\n\n**Traceback:**\n```\n{tb}```")
            raise

        # Execute with status updates
        progress_bar.progress(10)
        
        # Agent 1: Requirements
        st.session_state.agent_status['requirement'] = 'running'
        status_text.markdown("### 📋 Agent 1/7: Requirement Analyst")
        with agent_status:
            st.info("🔍 Analyzing requirements...")
        
        requirements = pipeline.requirement_agent.analyze_requirements(requirement_input)
        with agent_status:
            with st.expander("📋 Requirements Analysis Result", expanded=True):
                st.markdown(requirements[:1000] + ("..." if len(requirements) > 1000 else ""))
        st.session_state.agent_status['requirement'] = 'completed'
        progress_bar.progress(20)
        
        # Agent 2 & 3: Coding + Review Loop
        st.session_state.agent_status['coding'] = 'running'
        st.session_state.agent_status['review'] = 'running'
        status_text.markdown("### 💻 Agent 2-3/7: Senior Developer & Code Reviewer")
        with agent_status:
            st.info("🔄 Generating code with review iterations...")
        
        code_approved = False
        iteration = 0
        code = None
        review = None
        
        while not code_approved and iteration < max_iterations:
            iteration += 1
            if iteration == 1:
                code = pipeline.coding_agent.generate_code(requirements)
            else:
                code = pipeline.coding_agent.generate_code(requirements, feedback=review)
            
            review = pipeline.review_agent.review_code(code, requirements=requirements)
            
            if pipeline.review_agent.is_approved(review):
                code_approved = True
            elif iteration >= max_iterations:
                break
        
        st.session_state.agent_status['coding'] = 'completed'
        st.session_state.agent_status['review'] = 'completed'
        progress_bar.progress(45)
        
        # Agent 4: Documentation
        st.session_state.agent_status['documentation'] = 'running'
        status_text.markdown("### 📖 Agent 4/7: Tech Writer")
        with agent_status:
            st.info("📝 Creating documentation...")
        
        documentation = pipeline.documentation_agent.generate_documentation(code, requirements=requirements)
        with agent_status:
            with st.expander("📖 Documentation Result", expanded=True):
                st.markdown(documentation[:1000] + ("..." if len(documentation) > 1000 else ""))
        st.session_state.agent_status['documentation'] = 'completed'
        progress_bar.progress(60)
        
        # Agent 5: Testing
        st.session_state.agent_status['testing'] = 'running'
        status_text.markdown("### 🧪 Agent 5/7: QA Engineer")
        with agent_status:
            st.info("🧪 Generating test cases...")
        
        tests = pipeline.test_agent.generate_tests(code, requirements=requirements)
        with agent_status:
            with st.expander("🧪 Test Cases Result", expanded=True):
                test_preview = tests[:800] + ("..." if len(tests) > 800 else "")
                st.code(test_preview, language="python")
        st.session_state.agent_status['testing'] = 'completed'
        progress_bar.progress(75)
        
        # Agent 6: Deployment
        st.session_state.agent_status['deployment'] = 'running'
        status_text.markdown("### 🚀 Agent 6/7: DevOps")
        with agent_status:
            st.info("🚀 Creating deployment config...")
        
        deployment = pipeline.deployment_agent.generate_deployment_config(code, requirements=requirements)
        with agent_status:
            with st.expander("🚀 Deployment Config Result", expanded=True):
                st.markdown(deployment[:1000] + ("..." if len(deployment) > 1000 else ""))
        st.session_state.agent_status['deployment'] = 'completed'
        progress_bar.progress(88)
        
        # Agent 7: UI
        st.session_state.agent_status['ui'] = 'running'
        status_text.markdown("### 🎨 Agent 7/7: UI Designer")
        with agent_status:
            st.info("🎨 Generating Streamlit interface...")
        
        ui_context = f"Requirements: {requirements[:500]}...\nCode: {code[:500]}..."
        ui = pipeline.ui_agent.generate_ui(ui_context)
        st.session_state.agent_status['ui'] = 'completed'
        
        # Build results
        results = {
            'user_requirement': requirement_input,
            'outputs': {
                'requirements': requirements,
                'code': code,
                'review': review,
                'documentation': documentation,
                'tests': tests,
                'deployment': deployment,
                'ui': ui
            },
            'metadata': {
                'iterations': iteration,
                'status': 'success'
            }
        }
        
        # Save outputs if enabled
        if save_outputs:
            import uuid
            from datetime import datetime
            from pathlib import Path
            run_id = str(uuid.uuid4())[:8]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            from src.utils import config
            run_dir_base = config.output_dir / f"run_{timestamp}_{run_id}"
            
            (run_dir_base / "documentation").mkdir(parents=True, exist_ok=True)
            (run_dir_base / "generated_code").mkdir(parents=True, exist_ok=True)
            (run_dir_base / "tests").mkdir(parents=True, exist_ok=True)
            
            (run_dir_base / "documentation" / "requirements.md").write_text(requirements, encoding='utf-8')
            (run_dir_base / "generated_code" / "generated_code.py").write_text(code, encoding='utf-8')
            (run_dir_base / "documentation" / "code_review.md").write_text(review, encoding='utf-8')
            (run_dir_base / "documentation" / "documentation.md").write_text(documentation, encoding='utf-8')
            (run_dir_base / "tests" / "test_generated_code.py").write_text(tests, encoding='utf-8')
            (run_dir_base / "documentation" / "deployment_config.md").write_text(deployment, encoding='utf-8')
            (run_dir_base / "streamlit_ui.py").write_text(ui, encoding='utf-8')
            
            results['run_id'] = run_id
        
        st.session_state.pipeline_results = results

        progress_bar.progress(100)
        status_text.markdown("### ✅ Pipeline Completed Successfully!")
        with agent_status:
            st.success("🎉 All 7 AutoGen agents have completed their tasks!")
        
        # Reset processing state
        st.session_state.processing = False

    except Exception as e:
        st.error(f"❌ **Pipeline Error:** {str(e)}")
        with st.expander("🔍 View Error Details"):
            st.exception(e)
        st.session_state.processing = False

# Display results with modern UI
if st.session_state.pipeline_results:
    results = st.session_state.pipeline_results

    st.markdown("---")
    st.markdown('<div class="section-header">📊 AutoGen Pipeline Results</div>', unsafe_allow_html=True)
    st.markdown("**Generated Artifacts from Multi-Agent Collaboration**")

    # Metadata with modern cards
    st.markdown("#### 📈 Execution Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        status = results['metadata']['status'].upper()
        if status == 'SUCCESS':
            st.markdown('<div class="status-success">✅ SUCCESS</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-error">❌ FAILED</div>', unsafe_allow_html=True)
    with col2:
        st.metric("🔄 Review Iterations", results['metadata']['iterations'])
    with col3:
        max_iter_reached = results['metadata'].get('max_iterations_reached', False)
        st.metric("⚡ Iteration Limit", "Reached" if max_iter_reached else "Within Limit")
    with col4:
        run_id = results.get('run_id', 'N/A')
        st.metric("🆔 Run ID", run_id)

    # Output tabs with modern design
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 Requirements Analysis",
        "💻 Python Code",
        "🔍 Code Review",
        "📖 Documentation",
        "🧪 Test Suite",
        "🚀 Deployment"
    ])

    with tab1:
        st.markdown("### 📋 Structured Requirements")
        st.info("**Generated by Requirement Analyst Agent**")
        st.markdown(results['outputs']['requirements'])
        st.download_button(
            "📥 Download Requirements (Markdown)",
            results['outputs']['requirements'],
            "requirements.md",
            "text/markdown",
            use_container_width=True,
            key="download_requirements"
        )

    with tab2:
        st.markdown("### 💻 Generated Python Code")
        st.info("**Generated by Senior Developer Agent (AutoGen)**")
        code = results['outputs']['code']
        # Extract code from markdown if wrapped
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].split("```")[0].strip()

        st.code(code, language="python", line_numbers=True)
        st.download_button(
            "📥 Download Code",
            code,
            "generated_code.py",
            "text/x-python",
            use_container_width=True,
            key="download_code"
        )

    with tab3:
        st.markdown("### Code Review Feedback")
        review = results['outputs']['review']

        if "APPROVED" in review:
            st.success("✅ Code Approved")
        elif "NEEDS_REVISION" in review:
            st.warning("⚠️ Code Needs Revision")

        st.markdown(review)
        st.download_button(
            "📥 Download Review",
            review,
            "code_review.md",
            "text/markdown",
            use_container_width=True,
            key="download_review"
        )

    with tab4:
        st.markdown("### 📖 Technical Documentation")
        st.info("**Generated by Tech Writer Agent**")
        st.markdown(results['outputs']['documentation'])
        st.download_button(
            "📥 Download Documentation (Markdown)",
            results['outputs']['documentation'],
            "documentation.md",
            "text/markdown",
            use_container_width=True,
            key="download_documentation"
        )

    with tab5:
        st.markdown("### 🧪 Test Suite (pytest)")
        st.info("**Generated by QA Engineer Agent**")
        tests = results['outputs']['tests']
        # Extract code from markdown if wrapped
        if "```python" in tests:
            tests = tests.split("```python")[1].split("```")[0].strip()
        elif "```" in tests:
            tests = tests.split("```")[1].split("```")[0].strip()

        st.code(tests, language="python", line_numbers=True)
        st.download_button(
            "📥 Download Tests (Python)",
            tests,
            "test_generated_code.py",
            "text/x-python",
            use_container_width=True,
            type="primary",
            key="download_tests"
        )

    with tab6:
        st.markdown("### 🚀 Deployment Configuration")
        st.info("**Generated by DevOps Agent**")
        st.markdown(results['outputs']['deployment'])
        st.download_button(
            "📥 Download Deployment Config",
            results['outputs']['deployment'],
            "deployment_config.md",
            "text/markdown",
            key="download_deployment",
            use_container_width=True
        )

    # Download all button with modern design
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📦 Download All Artifacts (ZIP)", use_container_width=True, type="secondary"):
            if save_outputs:
                st.success("✅ All artifacts saved to `output/` directory with timestamp!")
                st.info(f"📂 Check: `output/{datetime.now().strftime('%Y%m%d_%H%M%S')}/`")
            else:
                st.warning("⚠️ Enable 'Save Outputs to Files' in sidebar to save artifacts")

# Compact footer
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown(f"""
<center style="padding: 10px 0; font-size: 0.85em;">
<strong>🚀 Multi-Agentic Framework © {datetime.now().year}</strong><br>
Powered by AutoGen with GPT-4o • Version 2026.1.0
</center>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

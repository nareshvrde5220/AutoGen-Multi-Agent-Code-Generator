# 🚀 Quick Start Guide - Multi-Agentic Coding Framework

This guide will get you up and running with the Multi-Agent Framework in 5 minutes!

## ⚡ Prerequisites

- Python 3.10 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## 📝 Step 1: Configure API Key

1. Navigate to the project directory:
   ```bash
   cd Multi_Agent_Coding_Exercise
   ```

2. Copy the environment example file:
   ```bash
   # Windows
   copy config\.env.example config\.env
   
   # Unix/Mac
   cp config/.env.example config/.env
   ```

3. Open `config/.env` in your text editor and add your API key:
   ```bash
   OPENAI_API_KEY=your_actual_api_key_here
   ```

## 🎯 Step 2: Choose Your Launch Method

### Option A: Windows (Easiest)

Double-click `deploy.bat` and select option 3 to launch the UI.

Or run from command line:
```cmd
deploy.bat
```

### Option B: Manual Start (All Platforms)

1. Activate the virtual environment:
   ```bash
   # Windows
   .\genaivnv\Scripts\activate
   
   # Unix/Mac
   source genaivnv/bin/activate
   ```

2. Install dependencies (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

3. Launch the Streamlit UI:
   ```bash
   streamlit run ui/streamlit_app.py
   ```

## 🎨 Step 3: Use the Web Interface

1. Open your browser to `http://localhost:8501`

2. Enter your API key in the sidebar (if not set in .env)

3. Type your requirement in the text area, for example:
   ```
   Create a Python function that calculates the factorial of a number
   ```

4. Click "🚀 Start Agent Pipeline"

5. Wait for the agents to process (typically 2-3 minutes)

6. View results in the tabs:
   - 📋 Requirements
   - 💻 Code
   - 🔍 Review
   - 📖 Documentation
   - 🧪 Tests
   - 🚀 Deployment

7. Download any artifact using the download buttons

## 📚 Example Requirements to Try

### Simple Examples

**1. Factorial Function:**
```
Create a Python function that calculates the factorial of a number
```

**2. Calculator:**
```
Create a command-line calculator that supports basic arithmetic operations
```

### Intermediate Examples

**3. CSV Processor:**
```
Build a CSV data processor that reads a file, removes duplicates, and exports to JSON
```

**4. Password Validator:**
```
Create a password validator that checks for:
- Minimum 8 characters
- At least one uppercase letter
- At least one number
- At least one special character
```

### Advanced Examples

**5. REST API:**
```
Create a REST API using FastAPI that:
- Manages a todo list with CRUD operations
- Stores data in SQLite database
- Includes authentication using JWT tokens
- Has input validation using Pydantic models
```

**6. Web Scraper:**
```
Build a web scraper that:
- Extracts article titles and URLs from a news website
- Handles pagination
- Saves results to CSV
- Includes error handling and retry logic
```

## 🔧 Advanced Usage

### Using the Python API

```python
from src.orchestrator import create_pipeline

# Initialize pipeline
pipeline = create_pipeline()

# Execute
results = pipeline.execute_pipeline(
    "Create a Python function that calculates the factorial of a number",
    save_outputs=True
)

# Access results
print(results['outputs']['code'])
```

### Using the CLI

```bash
# Run a requirement
python src/main.py run "Create a factorial function"

# Launch UI
python src/main.py ui

# Run tests
python src/main.py test
```

## 📂 Where Are My Files?

All generated files are saved to the `output/` directory:

```
output/
├── generated_code/     # Your generated code
├── documentation/      # Generated documentation
└── tests/             # Generated test files
```

Each file has a timestamp in its name for easy tracking.

## ❓ Common Issues

### Issue 1: API Key Error
**Error:** `OPENAI_API_KEY not found`

**Solution:** Make sure you've:
1. Created `config/.env` from `.env.example`
2. Added your actual API key
3. Saved the file

### Issue 2: Module Not Found
**Error:** `ModuleNotFoundError: No module named 'src'`

**Solution:** Make sure you're in the project root directory and the virtual environment is activated.

### Issue 3: Port Already in Use
**Error:** `Port 8501 is already in use`

**Solution:** Either:
- Close the other Streamlit app
- Or use a different port: `streamlit run ui/streamlit_app.py --server.port=8502`

## 🎓 Next Steps

1. **Explore the Documentation:** Read [README.md](README.md) for comprehensive documentation

2. **Try Examples:** Run `python examples.py` for programmatic usage examples

3. **Run Tests:** Execute `pytest tests/` to run the test suite

4. **Customize Agents:** Edit `config/config.yaml` to adjust agent parameters

5. **Deploy with Docker:** Use `docker-compose up` for containerized deployment

## 💡 Tips for Best Results

1. **Be Specific:** Provide clear, detailed requirements
2. **Use Examples:** Include example inputs/outputs if applicable
3. **Specify Technologies:** Mention frameworks, libraries, or patterns you want
4. **Review Iterations:** The system will iterate up to 3 times on code review
5. **Save Outputs:** Enable "Save Outputs to Files" to keep all artifacts

## 📞 Need Help?

- Check the [Troubleshooting](README.md#troubleshooting) section
- Review the logs in `logs/` directory
- Open an issue on GitHub
- Contact support

## 🎉 You're Ready!

That's it! You're now ready to transform your ideas into production-ready code with AI agents.

**Happy Coding! 🚀**

---

*For more detailed information, see the [complete README](README.md)*

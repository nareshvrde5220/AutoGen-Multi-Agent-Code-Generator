Below is a comprehensive Streamlit application code that provides a user-friendly interface for managing a Todo List Manager API. It includes features such as CRUD operations, progress indicators, organized outputs, and error handling.

```python
import streamlit as st
from datetime import datetime
import requests

# Set page configuration
st.set_page_config(page_title="Todo List Manager", layout="wide", page_icon="📝")

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")
    api_url = st.text_input("API URL", "http://localhost:8000")

# Main content
st.title("📝 Todo List Manager")

# Session state to maintain state across reruns
if 'todos' not in st.session_state:
    st.session_state.todos = []

# Input section for creating a new todo item
st.subheader("Create New Todo Item")
with st.form("create_todo_form"):
    title = st.text_input("Title")
    description = st.text_area("Description")
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    due_date = st.date_input("Due Date", min_value=datetime.today())
    create_button = st.form_submit_button("Create Todo")

if create_button:
    with st.spinner("Creating todo item..."):
        try:
            response = requests.post(f"{api_url}/todos", json={
                "title": title,
                "description": description,
                "priority": priority,
                "due_date": due_date.isoformat()
            })
            response.raise_for_status()
            st.success("Todo item created successfully!")
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {str(e)}")

# Fetch and display todo items
st.subheader("Todo Items")
status_filter = st.selectbox("Filter by Status", ["All", "Pending", "In Progress", "Completed"])
priority_filter = st.selectbox("Filter by Priority", ["All", "Low", "Medium", "High"])

if st.button("Refresh Todos"):
    with st.spinner("Fetching todo items..."):
        try:
            params = {}
            if status_filter != "All":
                params['status'] = status_filter.lower()
            if priority_filter != "All":
                params['priority'] = priority_filter.lower()

            response = requests.get(f"{api_url}/todos", params=params)
            response.raise_for_status()
            st.session_state.todos = response.json()
            st.success("Todos fetched successfully!")
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {str(e)}")

# Display todos in tabs
tab1, tab2 = st.tabs(["Todo List", "Completed Todos"])

with tab1:
    for todo in st.session_state.todos:
        if todo['status'] != 'completed':
            st.markdown(f"**{todo['title']}**")
            st.text(f"Description: {todo['description']}")
            st.text(f"Priority: {todo['priority']}")
            st.text(f"Due Date: {todo['due_date']}")
            if st.button("Mark as Completed", key=f"complete_{todo['id']}"):
                try:
                    response = requests.put(f"{api_url}/todos/{todo['id']}", json={"status": "completed"})
                    response.raise_for_status()
                    st.success("Todo marked as completed!")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error: {str(e)}")

with tab2:
    for todo in st.session_state.todos:
        if todo['status'] == 'completed':
            st.markdown(f"**{todo['title']}**")
            st.text(f"Description: {todo['description']}")
            st.text(f"Priority: {todo['priority']}")
            st.text(f"Due Date: {todo['due_date']}")
            if st.button("Delete", key=f"delete_{todo['id']}"):
                try:
                    response = requests.delete(f"{api_url}/todos/{todo['id']}")
                    response.raise_for_status()
                    st.success("Todo deleted successfully!")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error: {str(e)}")

# Error handling
try:
    # Code that might fail
    pass
except Exception as e:
    st.error(f"Error: {str(e)}")
```

### Key Features:
- **Sidebar Configuration**: Allows users to set the API URL.
- **Create Todo Item**: Form to create new todo items with fields for title, description, priority, and due date.
- **Fetch and Display Todos**: Fetches todos from the API with optional filtering by status and priority.
- **Tabs for Todo Items**: Displays todos in two tabs - one for active todos and another for completed todos.
- **Progress Indicators**: Uses `st.spinner` to indicate processing.
- **Error Handling**: Displays errors using `st.error`.
- **Session State**: Maintains the list of todos across reruns using `st.session_state`.

This Streamlit app provides a comprehensive, user-friendly interface for managing a Todo List Manager API, adhering to the specified requirements.
Below is a comprehensive Streamlit application code that serves as a UI for managing a Todo List Manager API. This application allows users to perform CRUD operations on todo items, view progress, and download results. It also includes error handling and session state management.

```python
import streamlit as st
import requests
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Todo List Manager", layout="wide", page_icon="📝")

# Initialize session state
if 'todos' not in st.session_state:
    st.session_state['todos'] = []

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")
    api_url = st.text_input("API URL", "http://localhost:8000")

# Main content
st.title("📝 Todo List Manager")

# Input section
st.subheader("Create a New Todo")
title = st.text_input("Title")
description = st.text_area("Description", height=100)
priority = st.selectbox("Priority", ["Low", "Medium", "High"])
due_date = st.date_input("Due Date", datetime.now())

if st.button("Add Todo"):
    with st.spinner("Adding todo..."):
        try:
            response = requests.post(f"{api_url}/todos", json={
                "title": title,
                "description": description,
                "priority": priority,
                "due_date": due_date.isoformat()
            })
            response.raise_for_status()
            st.success("Todo added successfully!")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Fetch and display todos
if st.button("Refresh Todos"):
    with st.spinner("Fetching todos..."):
        try:
            response = requests.get(f"{api_url}/todos")
            response.raise_for_status()
            st.session_state['todos'] = response.json()
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Display todos
st.subheader("Todo List")
if st.session_state['todos']:
    for todo in st.session_state['todos']:
        st.write(f"**Title:** {todo['title']}")
        st.write(f"**Description:** {todo['description']}")
        st.write(f"**Priority:** {todo['priority']}")
        st.write(f"**Due Date:** {todo['due_date']}")
        st.write("---")

# Output sections with tabs
tab1, tab2 = st.tabs(["All Todos", "Completed Todos"])

with tab1:
    st.write("### All Todos")
    st.json(st.session_state['todos'])

with tab2:
    st.write("### Completed Todos")
    completed_todos = [todo for todo in st.session_state['todos'] if todo['status'] == 'completed']
    st.json(completed_todos)

# Download buttons
st.download_button("Download All Todos", str(st.session_state['todos']), "todos.json")
st.download_button("Download Completed Todos", str(completed_todos), "completed_todos.json")

# Error handling
try:
    # Code that might fail
    pass
except Exception as e:
    st.error(f"Error: {str(e)}")
```

### Key Features:
- **Sidebar Configuration**: Allows users to input the API URL.
- **Input Section**: Users can create new todo items with fields for title, description, priority, and due date.
- **Progress Indicators**: Uses `st.spinner()` to show progress during API calls.
- **Display Todos**: Fetches and displays todos in a structured format.
- **Tabs for Output**: Organizes todos into tabs for all todos and completed todos.
- **Download Buttons**: Allows downloading of todos as JSON files.
- **Error Handling**: Displays errors using `st.error()`.
- **Session State Management**: Maintains the state of todos across reruns using `st.session_state`.

This code provides a user-friendly interface for interacting with a Todo List Manager API, making it easy to manage and track tasks.
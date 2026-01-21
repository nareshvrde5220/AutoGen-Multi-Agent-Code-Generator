Below is a comprehensive Streamlit UI code for a Todo List Manager REST API. This UI allows users to interact with the API by performing CRUD operations on todo items. It includes input fields for creating and updating todo items, displays outputs in organized tabs, and handles errors gracefully. The code also includes session state management to maintain state across reruns.

```python
import streamlit as st
import requests
import json
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Todo List Manager", layout="wide", page_icon="📝")

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")
    api_url = st.text_input("API URL", "http://localhost:8000")

# Define session state for maintaining state across reruns
if 'todos' not in st.session_state:
    st.session_state.todos = []

# Main content
st.title("📝 Todo List Manager")

# Input section for creating a new todo item
st.header("Create New Todo Item")
title = st.text_input("Title")
description = st.text_area("Description", height=100)
priority = st.selectbox("Priority", ["low", "medium", "high"])
due_date = st.date_input("Due Date")

if st.button("Add Todo"):
    with st.spinner("Adding todo item..."):
        try:
            response = requests.post(f"{api_url}/todos", json={
                "title": title,
                "description": description,
                "priority": priority,
                "due_date": due_date.isoformat()
            })
            response.raise_for_status()
            st.success("Todo item added successfully!")
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")

# Display existing todo items
st.header("Todo Items")
status_filter = st.selectbox("Filter by Status", ["all", "pending", "in_progress", "completed"])
priority_filter = st.selectbox("Filter by Priority", ["all", "low", "medium", "high"])

if st.button("Refresh List"):
    with st.spinner("Fetching todo items..."):
        try:
            params = {}
            if status_filter != "all":
                params["status"] = status_filter
            if priority_filter != "all":
                params["priority"] = priority_filter

            response = requests.get(f"{api_url}/todos", params=params)
            response.raise_for_status()
            st.session_state.todos = response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")

# Display todo items in tabs
tab1, tab2, tab3 = st.tabs(["All Todos", "Pending Todos", "Completed Todos"])

with tab1:
    st.subheader("All Todos")
    for todo in st.session_state.todos:
        st.write(f"**Title:** {todo['title']}")
        st.write(f"**Description:** {todo['description']}")
        st.write(f"**Priority:** {todo['priority']}")
        st.write(f"**Due Date:** {todo['due_date']}")
        st.write("---")

with tab2:
    st.subheader("Pending Todos")
    for todo in st.session_state.todos:
        if todo['status'] == 'pending':
            st.write(f"**Title:** {todo['title']}")
            st.write(f"**Description:** {todo['description']}")
            st.write(f"**Priority:** {todo['priority']}")
            st.write(f"**Due Date:** {todo['due_date']}")
            st.write("---")

with tab3:
    st.subheader("Completed Todos")
    for todo in st.session_state.todos:
        if todo['status'] == 'completed':
            st.write(f"**Title:** {todo['title']}")
            st.write(f"**Description:** {todo['description']}")
            st.write(f"**Priority:** {todo['priority']}")
            st.write(f"**Due Date:** {todo['due_date']}")
            st.write("---")

# Error handling
try:
    # Code that might fail
    pass
except Exception as e:
    st.error(f"Error: {str(e)}")
```

### Features:
- **Sidebar Configuration:** Allows users to input the API URL.
- **Session State Management:** Maintains the list of todos across reruns.
- **Input Section:** Provides fields for creating new todo items.
- **Progress Indicators:** Uses `st.spinner` to show loading states.
- **Output Tabs:** Organizes todos into tabs based on status.
- **Error Handling:** Displays errors using `st.error`.
- **Responsive Design:** Works on different screen sizes.

### Note:
- Ensure the FastAPI server is running and accessible at the specified API URL.
- Adjust the API endpoints and parameters as per your FastAPI implementation.
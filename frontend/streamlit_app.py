"""
Minimal Streamlit Frontend for Chatbot Platform

This is a functional, unstyled interface for testing the API.
For production, consider building a proper React frontend.
"""

import streamlit as st
import requests
from typing import Optional

# Configuration
API_BASE_URL = "http://localhost:8000"

# Initialize session state
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "current_project" not in st.session_state:
    st.session_state.current_project = None
if "chat_session_id" not in st.session_state:
    st.session_state.chat_session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []


def make_request(method: str, endpoint: str, data: dict = None, auth: bool = True):
    """Make API request with error handling."""
    url = f"{API_BASE_URL}{endpoint}"
    headers = {}
    
    if auth and st.session_state.access_token:
        headers["Authorization"] = f"Bearer {st.session_state.access_token}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        st.error(f"API Error: {e.response.text}")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None


def login_page():
    """Login and registration page."""
    st.title("🤖 Chatbot Platform")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                url = f"{API_BASE_URL}/auth/login"

                payload = {
                    "username": email,      # OAuth expects this field name
                    "password": password
                }

                try:
                    response = requests.post(
                        url,
                        data=payload,        # <-- FORM DATA (not JSON)
                        headers={"Content-Type": "application/x-www-form-urlencoded"}
                    )

                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.access_token = data["access_token"]
                        st.success("Logged in successfully!")
                        st.rerun()
                    else:
                        st.error(f"Login failed: {response.text}")

                except Exception as e:
                    st.error(f"Login error: {str(e)}")


    
    with tab2:
        with st.form("register_form"):
            email = st.text_input("Email", key="reg_email")
            password = st.text_input("Password", type="password", key="reg_password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Register")
            
            if submit:
                if password != confirm_password:
                    st.error("Passwords do not match!")
                elif len(password) < 8:
                    st.error("Password must be at least 8 characters!")
                else:
                    data = {"email": email, "password": password}
                    response = make_request("POST", "/auth/register", data, auth=False)
                    
                    if response:
                        st.success("Registered successfully! Please login.")


def project_selector():
    """Project selection and creation."""
    st.sidebar.title("Projects")
    
    # List projects
    projects_data = make_request("GET", "/projects")
    
    if projects_data:
        projects = projects_data.get("projects", [])
        
        if projects:
            project_names = {p["name"]: p for p in projects}
            selected_name = st.sidebar.selectbox(
                "Select Project",
                options=list(project_names.keys())
            )
            
            if selected_name:
                st.session_state.current_project = project_names[selected_name]
        else:
            st.sidebar.info("No projects yet. Create one below!")
    
    # Create new project
    with st.sidebar.expander("Create New Project"):
        with st.form("create_project"):
            name = st.text_input("Project Name")
            description = st.text_area("Description")
            submit = st.form_submit_button("Create")
            
            if submit and name:
                data = {"name": name, "description": description}
                response = make_request("POST", "/projects", data)
                
                if response:
                    st.success(f"Created project: {name}")
                    st.rerun()
    
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()


def prompt_manager():
    """Manage prompts for current project."""
    project = st.session_state.current_project
    
    with st.expander("System Prompts"):
        # List existing prompts
        prompts_data = make_request("GET", f"/projects/{project['id']}/prompts")
        
        if prompts_data:
            prompts = prompts_data.get("prompts", [])
            
            if prompts:
                st.write("**Current Prompts:**")
                for i, prompt in enumerate(prompts, 1):
                    st.text_area(
                        f"Prompt {i}",
                        value=prompt["content"],
                        disabled=True,
                        key=f"prompt_{i}"
                    )
            else:
                st.info("No prompts yet. Add one below!")
        
        # Add new prompt
        with st.form("add_prompt"):
            content = st.text_area("New System Prompt")
            submit = st.form_submit_button("Add Prompt")
            
            if submit and content:
                data = {"content": content}
                response = make_request("POST", f"/projects/{project['id']}/prompts", data)
                
                if response:
                    st.success("Prompt added!")
                    st.rerun()


def chat_interface():
    """Main chat interface."""
    project = st.session_state.current_project
    
    st.title(f"💬 {project['name']}")
    
    if project.get("description"):
        st.caption(project["description"])
    
    # Prompt manager
    prompt_manager()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if user_input := st.chat_input("Type your message..."):
        # Add user message to display
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Send to API
        data = {
            "project_id": project["id"],
            "message": user_input,
        }
        
        if st.session_state.chat_session_id:
            data["session_id"] = st.session_state.chat_session_id
        
        with st.spinner("Thinking..."):
            response = make_request("POST", "/chat", data)
        
        if response:
            # Save session ID
            if not st.session_state.chat_session_id:
                st.session_state.chat_session_id = response["session_id"]
            
            # Add assistant message to display
            assistant_message = response["assistant_message"]["content"]
            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            st.rerun()
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat_session_id = None
        st.rerun()


def main():
    """Main application."""
    st.set_page_config(
        page_title="Chatbot Platform",
        page_icon="🤖",
        layout="wide"
    )
    
    # Check authentication
    if not st.session_state.access_token:
        login_page()
    else:
        # Show project selector
        project_selector()
        
        # Show chat interface if project selected
        if st.session_state.current_project:
            chat_interface()
        else:
            st.info("👈 Select or create a project to start chatting!")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
API Testing Script for Chatbot Platform

This script demonstrates the complete API flow:
1. User registration
2. User login
3. Project creation
4. Prompt creation
5. Chat interaction
"""

import requests
import json
from typing import Optional

API_BASE_URL = "http://localhost:8000"


class ChatbotClient:
    """Client for interacting with the Chatbot Platform API."""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.token: Optional[str] = None
    
    def register(self, email: str, password: str) -> dict:
        """Register a new user."""
        response = requests.post(
            f"{self.base_url}/auth/register",
            json={"email": email, "password": password}
        )
        response.raise_for_status()
        return response.json()
    
    def login(self, email: str, password: str) -> dict:
        """Login and save access token."""
        response = requests.post(
            f"{self.base_url}/auth/login",
            data={"username": email, "password": password}
        )
        response.raise_for_status()
        data = response.json()
        self.token = data["access_token"]
        return data
    
    def _headers(self) -> dict:
        """Get headers with authentication."""
        if not self.token:
            raise ValueError("Not authenticated. Call login() first.")
        return {"Authorization": f"Bearer {self.token}"}
    
    def create_project(self, name: str, description: str = "") -> dict:
        """Create a new project."""
        response = requests.post(
            f"{self.base_url}/projects",
            headers=self._headers(),
            json={"name": name, "description": description}
        )
        response.raise_for_status()
        return response.json()
    
    def list_projects(self) -> dict:
        """List all projects."""
        response = requests.get(
            f"{self.base_url}/projects",
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_project(self, project_id: str) -> dict:
        """Get a specific project."""
        response = requests.get(
            f"{self.base_url}/projects/{project_id}",
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()
    
    def create_prompt(self, project_id: str, content: str) -> dict:
        """Create a prompt for a project."""
        response = requests.post(
            f"{self.base_url}/projects/{project_id}/prompts",
            headers=self._headers(),
            json={"content": content}
        )
        response.raise_for_status()
        return response.json()
    
    def list_prompts(self, project_id: str) -> dict:
        """List prompts for a project."""
        response = requests.get(
            f"{self.base_url}/projects/{project_id}/prompts",
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()
    
    def chat(self, project_id: str, message: str, session_id: Optional[str] = None) -> dict:
        """Send a chat message."""
        data = {"project_id": project_id, "message": message}
        if session_id:
            data["session_id"] = session_id
        
        response = requests.post(
            f"{self.base_url}/chat",
            headers=self._headers(),
            json=data
        )
        response.raise_for_status()
        return response.json()


def main():
    """Run the complete API flow test."""
    print("=" * 60)
    print("Chatbot Platform API Test")
    print("=" * 60)
    
    client = ChatbotClient()
    
    # 1. Register
    print("\n1. Registering user...")
    try:
        user = client.register("test1@example.com", "testpassword123")
        print(f"✓ Registered user: {user['email']}")
    except requests.exceptions.HTTPError as e:
        if "already registered" in str(e):
            print("✓ User already exists, proceeding to login...")
        else:
            raise
    
    # 2. Login
    print("\n2. Logging in...")
    auth = client.login("test1@example.com", "testpassword123")
    print(f"✓ Logged in successfully")
    print(f"  Token: {auth['access_token'][:20]}...")
    
    # 3. Create Project
    print("\n3. Creating project...")
    project = client.create_project(
        name="Test Chatbot",
        description="A test chatbot for API demonstration"
    )
    print(f"✓ Created project: {project['name']}")
    print(f"  ID: {project['id']}")
    
    # 4. List Projects
    print("\n4. Listing projects...")
    projects = client.list_projects()
    print(f"✓ Found {projects['total']} project(s)")
    for p in projects['projects']:
        print(f"  - {p['name']}")
    
    # 5. Create Prompts
    print("\n5. Creating system prompts...")
    prompt1 = client.create_prompt(
        project['id'],
        "You are a helpful assistant that provides clear and concise answers."
    )
    print(f"✓ Created prompt 1")
    
    prompt2 = client.create_prompt(
        project['id'],
        "Always be polite and professional in your responses."
    )
    print(f"✓ Created prompt 2")
    
    # 6. List Prompts
    print("\n6. Listing prompts...")
    prompts = client.list_prompts(project['id'])
    print(f"✓ Found {prompts['total']} prompt(s)")
    for i, p in enumerate(prompts['prompts'], 1):
        print(f"  {i}. {p['content'][:50]}...")
    
    # 7. Start Chat
    print("\n7. Starting chat conversation...")
    
    # First message
    response1 = client.chat(
        project['id'],
        "Hello! What is artificial intelligence?"
    )
    session_id = response1['session_id']
    print(f"✓ User: {response1['message']['content']}")
    print(f"✓ Assistant: {response1['assistant_message']['content'][:100]}...")
    
    # Continue conversation
    print("\n8. Continuing conversation...")
    response2 = client.chat(
        project['id'],
        "Can you explain machine learning?",
        session_id=session_id
    )
    print(f"✓ User: {response2['message']['content']}")
    print(f"✓ Assistant: {response2['assistant_message']['content'][:100]}...")
    
    print("\n" + "=" * 60)
    print("✓ API Test Complete!")
    print("=" * 60)
    print(f"\nSession ID: {session_id}")
    print(f"Project ID: {project['id']}")
    print("\nYou can now use these IDs to continue testing via:")
    print("- Streamlit UI: streamlit run frontend/streamlit_app.py")
    print("- API Docs: http://localhost:8000/docs")
    print("- cURL commands from the README")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API at", API_BASE_URL)
        print("Make sure the server is running:")
        print("  - Docker: docker-compose up")
        print("  - Local: make dev")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

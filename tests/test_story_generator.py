import pytest
from app import generate_story
import os
import streamlit as st

def test_environment_variables():
    """Test that environment variables are properly loaded"""
    assert os.getenv('ANTHROPIC_API_KEY') is not None, "ANTHROPIC_API_KEY not found in environment"

def test_generate_story_inputs():
    """Test story generation with sample inputs"""
    test_inputs = {
        "main_character": "Luna",
        "location": "Enchanted Forest",
        "theme": "Being kind to others",
        "challenges": "Making new friends",
        "activities": "Reading books and painting"
    }
    
    story = generate_story(**test_inputs)
    
    # Basic validation of story content
    assert story is not None, "Story should not be None"
    assert len(story) > 0, "Story should not be empty"
    assert isinstance(story, str), "Story should be a string"
    
    # Check if story contains key elements
    assert test_inputs["main_character"] in story, "Story should contain main character name"
    assert test_inputs["location"] in story, "Story should contain location"

def test_session_state_initialization():
    """Test Streamlit session state initialization"""
    # Reset session state
    for key in st.session_state.keys():
        del st.session_state[key]
    
    # Import main to trigger session state initialization
    from app import main
    
    assert 'step' in st.session_state, "Session state should contain 'step'"
    assert st.session_state.step == 1, "Initial step should be 1"

@pytest.mark.parametrize("step,expected_keys", [
    (1, ["step"]),
    (2, ["step", "main_character"]),
    (3, ["step", "main_character", "location"]),
    (4, ["step", "main_character", "location", "theme"]),
    (5, ["step", "main_character", "location", "theme", "challenges"]),
])
def test_progressive_state_management(step, expected_keys):
    """Test that state is properly managed as user progresses"""
    # Reset session state
    for key in st.session_state.keys():
        del st.session_state[key]
    
    # Initialize state
    st.session_state.step = step
    
    # Add required previous states
    if step > 1:
        st.session_state.main_character = "Test Character"
    if step > 2:
        st.session_state.location = "Test Location"
    if step > 3:
        st.session_state.theme = "Test Theme"
    if step > 4:
        st.session_state.challenges = "Test Challenges"
    
    for key in expected_keys:
        assert key in st.session_state, f"Session state should contain '{key}' at step {step}"

def test_story_content_guidelines():
    """Test that generated story follows content guidelines"""
    test_inputs = {
        "main_character": "Alex",
        "location": "Magic School",
        "theme": "Never give up",
        "challenges": "Learning new spells",
        "activities": "Playing with friends"
    }
    
    story = generate_story(**test_inputs)
    
    # Check story structure
    paragraphs = story.split('\n\n')
    assert len(paragraphs) >= 10, "Story should have at least 10 paragraphs"
    
    # Check content guidelines
    assert "." in story, "Story should contain complete sentences"
    assert "!" in story, "Story should contain exciting moments"
    assert test_inputs["theme"].lower() in story.lower(), "Story should incorporate the theme"

@pytest.fixture
def mock_anthropic_client(mocker):
    """Mock Anthropic API client for testing"""
    class MockResponse:
        content = "This is a test story about Luna in the Enchanted Forest..."
    
    mock_client = mocker.patch('anthropic.Client')
    mock_client.return_value.messages.create.return_value = MockResponse()
    return mock_client

def test_api_integration(mock_anthropic_client):
    """Test integration with Anthropic API"""
    test_inputs = {
        "main_character": "Luna",
        "location": "Enchanted Forest",
        "theme": "Being kind",
        "challenges": "Making friends",
        "activities": "Reading"
    }
    
    story = generate_story(**test_inputs)
    assert story is not None
    
    # Verify API was called with correct parameters
    mock_anthropic_client.return_value.messages.create.assert_called_once()
    call_args = mock_anthropic_client.return_value.messages.create.call_args
    assert call_args is not None
    
    # Verify model and max tokens
    assert call_args.kwargs['model'] == "claude-3-sonnet-20240229"
    assert call_args.kwargs['max_tokens'] == 2000

def test_error_handling(mocker):
    """Test error handling in story generation"""
    # Mock Anthropic client to raise an exception
    mocker.patch('anthropic.Client', side_effect=Exception("API Error"))
    
    with pytest.raises(Exception):
        generate_story("Luna", "Forest", "Kindness", "Challenges", "Reading")
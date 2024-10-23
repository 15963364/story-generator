import streamlit as st
import anthropic
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def load_css():
    with open('styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def generate_story(main_character, location, theme, challenges, activities):
    """Generate a story using Anthropic's Claude API"""
    client = anthropic.Client(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    prompt = f"""Please write a cheerful, engaging 10-paragraph children's story (aimed at 5-year-olds) with the following elements:

Main Character: {main_character}
Setting/Location: {location}
Theme/Moral Lesson: {theme}
Challenges: {challenges}
Favorite Activities: {activities}

The story should:
- Use simple language appropriate for young children
- Be upbeat and positive throughout
- Clearly demonstrate the moral lesson
- Include moments of wonder and excitement
- End on a happy, satisfying note
- Keep paragraphs short and easy to follow
"""

    try:
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content
    except Exception as e:
        st.error(f"Error generating story: {str(e)}")
        return None

def show_progress_bar(step):
    total_steps = 5
    progress = (step - 1) / total_steps
    st.progress(progress, text=f"Step {step} of {total_steps}")

def main():
    # Load CSS
    load_css()
    
    # Configure page
    st.set_page_config(
        page_title="Story Generator",
        page_icon="📖",
        layout="centered"
    )

    st.markdown("<h1 style='text-align: center;'>📖 Magic Story Generator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Create wonderful stories for children!</p>", unsafe_allow_html=True)

    # Initialize session state
    if 'step' not in st.session_state:
        st.session_state.step = 1

    show_progress_bar(st.session_state.step)

    # Step 1: Main Character
    if st.session_state.step == 1:
        st.markdown("### Who is our hero?")
        with st.container():
            main_character = st.text_input(
                "",
                placeholder="Enter the main character's name",
                help="This could be a child, animal, or magical creature!"
            )
            if st.button("Next", key="char_next") and main_character:
                st.session_state.main_character = main_character
                st.session_state.step = 2
                st.experimental_rerun()

    # Step 2: Location
    elif st.session_state.step == 2:
        st.markdown("### Where does our story take place?")
        with st.container():
            location = st.text_input(
                "",
                placeholder="Enter the magical place",
                help="Could be a magical forest, a busy city, or even outer space!"
            )
            if st.button("Next", key="loc_next") and location:
                st.session_state.location = location
                st.session_state.step = 3
                st.experimental_rerun()

    # Step 3: Theme
    elif st.session_state.step == 3:
        st.markdown("### What lesson should we learn?")
        with st.container():
            theme = st.text_input(
                "",
                placeholder="Enter the story's message",
                help="Examples: Being kind, trying your best, making friends"
            )
            if st.button("Next", key="theme_next") and theme:
                st.session_state.theme = theme
                st.session_state.step = 4
                st.experimental_rerun()

    # Step 4: Challenges
    elif st.session_state.step == 4:
        st.markdown("### What challenges will our hero face?")
        with st.container():
            challenges = st.text_input(
                "",
                placeholder="Enter the challenges",
                help="What problems or obstacles will they need to overcome?"
            )
            if st.button("Next", key="chall_next") and challenges:
                st.session_state.challenges = challenges
                st.session_state.step = 5
                st.experimental_rerun()

    # Step 5: Activities
    elif st.session_state.step == 5:
        st.markdown("### What does our hero love to do?")
        with st.container():
            activities = st.text_input(
                "",
                placeholder="Enter favorite activities",
                help="What makes our hero happy? What are they good at?"
            )
            if st.button("Create Story!", key="create_story") and activities:
                st.session_state.activities = activities
                st.session_state.step = 6
                st.experimental_rerun()

    # Generate Story
    elif st.session_state.step == 6:
        try:
            with st.spinner("🌟 Creating your magical story..."):
                story = generate_story(
                    st.session_state.main_character,
                    st.session_state.location,
                    st.session_state.theme,
                    st.session_state.challenges,
                    st.session_state.activities
                )
                if story:
                    st.session_state.story = story
                    st.session_state.step = 7
                    st.experimental_rerun()
                else:
                    st.error("Failed to generate story. Please try again.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # Show Story
    elif st.session_state.step == 7:
        st.balloons()
        st.markdown(
            f"""
            <div class='story-container'>
                {st.session_state.story}
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("✨ Create Another Story"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.experimental_rerun()

if __name__ == "__main__":
    main()
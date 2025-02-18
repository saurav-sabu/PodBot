import streamlit as st
import time
import pyttsx3
from src.helper import *


# Function for text-to-speech
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Custom Styling
st.markdown(
    """
    <style>
    .main { background-color: #f4f4f4; }
    .stTextInput, .stButton, .stTextArea { font-size: 18px !important; }
    h1, h2, h3, h4 { text-align: center; color: #ff5733; }
    .sidebar .sidebar-content { background-color: #2c3e50; color: white; }
    </style>
    """,
    unsafe_allow_html=True
)

# Page Navigation
st.sidebar.title("🎙️ Podcast App")
st.sidebar.markdown("---")
page = st.sidebar.radio("📌 Navigate to", ["🏠 Home", "ℹ️ About", "📧 Contact"])

if page == "🏠 Home":
    st.title("🎤 Podcast Generator")
    st.markdown("### 🎯 Enter a topic to generate an engaging podcast")
    topic = st.text_input("🔍 Topic:", "Machine Learning")
    if st.button("🚀 Generate Podcast"):
        llm = initialize_llm()
        interviewer, guest = Agents(topic,llm)
        interview_task, guest_task = Tasks(interviewer,guest)
        st.subheader("📝 Podcast Transcript:")
        with st.expander("📜 View Transcript"):
            text = podcast_generation(interviewer,guest,interview_task,guest_task)
            st.markdown(text)
                # text_to_speech(text)

elif page == "ℹ️ About":
    st.title("📖 About the App")
    st.markdown(
        """
        🎙️ **Podcast Generator** is an AI-powered application that creates engaging podcast-like content based on your chosen topic.
        
        🔹 **Features:**
        - 📢 Generate structured podcast transcripts
        - 🎧 Text-to-Speech functionality
        - 📜 Beautiful UI with interactive elements
        
        🚀 **Enjoy creating podcasts effortlessly!**
        """
    )

elif page == "📧 Contact":
    st.title("📞 Contact Us")
    st.markdown("✉️ Reach out to us at: [contact@podcastapp.com](mailto:contact@podcastapp.com)")
    st.markdown("📌 Follow us on [Twitter](https://twitter.com/podcastapp) for updates!")

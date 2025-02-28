import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is not set in environment variables.")
    st.stop()  # Stop the app if the API key is not set

# Initialize the Gemini API
try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Failed to configure Gemini API: {e}")
    st.stop()  # Stop the app if configuration fails

# Function to generate response using the Gemini API
def generate_response(user_input):
    # Define generation configuration
    generation_config = {
        "temperature": 0.4,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
    }

    # Initialize the model with generation_config
    model = genai.GenerativeModel(
        "gemini-2.0-flash",
        generation_config=generation_config,
    )
    
    # Create a system prompt for Rizzler's personality
    rizzler_prompt = """You are 'rizzler', a chatbot meant to help people learn gen Z lingo. You have a cool persona and your message should be a mix of funny and helpful. Give the user an example of how a word can be used. Keep it precise and short. Separate your answer to different paragraphs. Use emojis. If asked for questions unrelated to gen z, apologize and do not answer."""
    
    # Create a chat session
    chat = model.start_chat(history=[])
    
    # Send the system prompt first to establish Rizzler's persona
    chat.send_message(rizzler_prompt)
    
    # Send the user's input
    response = chat.send_message(user_input)
    
    return response.text

st.set_page_config(page_title="Rizzler Chat", layout="centered")
st.title("📝 Rizzler Chat")
st.markdown("*Your personal guide to Gen Z lingo — funny, fresh, and helpful!* ✨")

# Initialize chat history in session state
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Yo! I'm Rizzler, here to teach you some Gen Z lingo. Hit me up with a word you're curious about! 🧢✨"}
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_input = st.chat_input("Type a message...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            with st.spinner("Rizzler is typing..."):
                # Get response from Gemini
                rizzler_response = generate_response(user_input)
                
                # Display with simulated typing effect
                full_response = ""
                for char in rizzler_response:
                    full_response += char
                    message_placeholder.markdown(full_response + "▌")
                    import time
                    time.sleep(0.005)  # Adjust typing speed here
                    
                # Final display without cursor
                message_placeholder.markdown(full_response)
                
                # Save to chat history
                st.session_state.messages.append({"role": "assistant", "content": rizzler_response})
            
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            message_placeholder.write("Network error, my dude. 🧢")
            st.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": "Network error, my dude. 🧢"})

# Add a sidebar with information about the app
with st.sidebar:
    st.title("About Rizzler")
    st.markdown("""
    Rizzler is your Gen Z slang translator. Just ask about any Gen Z term, and Rizzler will:
    
    - Explain what it means 🧠
    - Give examples of how to use it 💬
    - Keep it real with some Gen Z flavor 🔥
    
    Try asking about terms like:
    - no cap
    - bussin
    - slay
    - rizz
    - based
    - sus
    """)
    
    st.divider()
    st.caption("Powered by Gemini API and Streamlit")

# Add an expander with some examples at the bottom
with st.expander("Need some inspiration? Here are some Gen Z terms to ask about"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        - yeet
        - mid
        - fr
        - bet
        - sheesh
        """)
    with col2:
        st.markdown("""
        - vibe check
        - main character
        - rent free
        - lives in my head
        - understood the assignment
        """)
    with col3:
        st.markdown("""
        - it's giving
        - lowkey/highkey
        - caught in 4K
        - ate that
        - touch grass
        """)
from openai import OpenAI
import os
import streamlit as st

@st.cache_resource
def initialize_openai():
    api_key = os.environ.get("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
    if not api_key:
        st.error("OpenAI API key not found. Please set it in your environment variables or Streamlit secrets.")
        return None
    
    # Log the first few characters of the API key for debugging
    st.write(f"API Key (first 5 chars): {api_key[:5]}...")
    
    try:
        client = OpenAI(api_key=api_key)
        # Test the API key with a simple request
        client.models.list()
        return client
    except Exception as e:
        st.error(f"Error initializing OpenAI client: {str(e)}")
        return None

def generate_battlemap(prompt):
    client = initialize_openai()
    if not client:
        return None

    try:
        # First, use GPT-4 to parse and summarize the prompt
        summary_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes battle map descriptions for a text-to-image AI. Provide a concise summary in 50 words or less."},
                {"role": "user", "content": f"Summarize this battle map description in 50 words or less: {prompt}"}
            ]
        )
        summarized_prompt = summary_response.choices[0].message.content

        # Now use the summarized prompt to generate the image
        image_response = client.images.generate(
            model="dall-e-3",
            prompt=f"Create a top-down view battlemap for a tabletop RPG based on this description: {summarized_prompt}",
            size="1024x1024",
            quality="standard",
            n=1
        )
        return image_response.data[0].url
    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        return None

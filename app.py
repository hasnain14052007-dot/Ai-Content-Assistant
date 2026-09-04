import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(page_title="AI Content Assistant", page_icon="📝", layout="centered")

st.title("📝 AI Content Assistant")
st.write("Generate tailored social media posts and captions instantly using Groq API.")

# Sidebar for API Key input
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")

# Form Inputs
with st.form("content_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        content_type = st.selectbox(
            "Content Type",
            ["Social Media Post", "Blog Intro", "Product Announcement", "Newsletter Snippet", "Educational Post"]
        )
        platform = st.selectbox(
            "Platform",
            ["LinkedIn", "Instagram", "Twitter / X", "Facebook", "Medium"]
        )
        tone = st.selectbox(
            "Tone",
            ["Professional", "Casual & Friendly", "Persuasive", "Witty & Energetic", "Informative"]
        )

    with col2:
        topic = st.text_input("Topic / Main Message", placeholder="e.g., Launching an AI Roadmap Tool")
        target_audience = st.text_input("Target Audience", placeholder="e.g., Engineering students, Tech founders")

    submitted = st.form_submit_button("🚀 Generate Content")

# Generation Logic
if submitted:
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar to proceed.")
    elif not topic or not target_audience:
        st.warning("Please fill in both the Topic and Target Audience fields.")
    else:
        try:
            client = Groq(api_key=api_key)
            
            prompt = f"""
            You are an expert content creator. Generate a complete {content_type} for {platform}.
            
            - Topic: {topic}
            - Target Audience: {target_audience}
            - Tone: {tone}
            
            Requirements:
            1. Create a captivating headline/hook.
            2. Write a main body caption tailored for {platform}.
            3. Include a call-to-action (CTA).
            4. Add 5-8 highly relevant hashtags at the end.
            """

            with st.spinner("Generating your content..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=1024,
                )
                
                generated_text = response.choices[0].message.content
                
                st.success("Content generated successfully!")
                st.subheader("Generated Post")
                st.markdown(generated_text)
                
                # Copy/Download convenience
                st.download_button(
                    label="📥 Download Post (.txt)",
                    data=generated_text,
                    file_name="generated_post.txt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

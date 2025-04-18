import streamlit as st
from src.WorkFlow import workflow
import os

# Load API key from environment variable for security
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    st.error("Please set the OPENAI_API_KEY environment variable.")
    st.stop()

# UI setup
st.title("Multi-Agent Text Refinement System")
st.write("Enter text below and choose an action.")

# Text input area
text = st.text_area("Input Text", height=200, key="input_text")

# Buttons for individual agents
if st.button("Summarize"):
    result = workflow.run_agent("SummarizerAgent", text)
    st.write("**Result:**", result)
    
if st.button("Readability Score"):
    result = workflow.run_agent("ReadabilityScorerAgent", text)
    st.write("**Result:**", result)

if st.button("Sentiment"):
    result = workflow.run_agent("SentimentAgent", text)
    st.write("**Result:**", result)

if st.button("Style Enhance"):
    result = workflow.run_agent("StyleEnhancerAgent", text)
    st.write("**Result:**", result)

if st.button("Tone"):
    result = workflow.run_agent("ToneAdjusterAgent", text)
    st.write("**Result:**", result)

if st.button("Translate"):
    result = workflow.run_agent("TranslationAgent", text)
    st.write("**Result:**", result)

# Button to run all agents
if st.button("Run All Agents"):
    results = workflow.run_all_agents(api_key)
    st.write("**Results from All Agents:**")
    for name, output in results.items():
        st.write(f"**{name.capitalize()} Output:**", output)
        

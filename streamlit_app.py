# streamlit_app.py
import streamlit as st
from src.WorkFlow import Workflow
import PyPDF2
import io
import docx
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image

# Set up page style
st.set_page_config(
    page_title="Text Refinement Studio",
    page_icon="✨",
    layout="centered"
)

st.markdown("""
<style>
    html, body, [class*="css"]  {
        background-color: #ffffff;
        color: #000000;
    }
    h1 {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        margin-top: 0 !important;
        box-shadow: none !important;
    }
    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #cccccc;
        border-radius: 8px;
    }
    .stButton>button {
        background-color: #4a90e2;
        color: white;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #357ab8;
    }
    .stMarkdown, .st-expanderContent, .stCodeBlock, .stAlert {
        color: #000000;
    }
</style>
""", unsafe_allow_html=True)

st.title("✨ Multi-Agent Text Refinement Studio")
st.markdown(
    "<div style='color:#333333; font-size:18px;'>Enhance, analyze, and translate your text using a team of intelligent agents.</div>",
    unsafe_allow_html=True
)

# Load API key
api_key = st.secrets["OPENAI_API_KEY"]
workflow = Workflow()

# File Upload
st.markdown("### 📄 Upload a PDF, Word, or Text File")
uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])
text = ""
if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()
    if file_type == "pdf":
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        for page in pdf_reader.pages:
            text += page.extract_text() or ""

        if text.strip():
            st.success("✅ PDF uploaded and extracted successfully!")
        else:
            st.warning("⚠️ No text found using standard extraction. Trying OCR...")
            uploaded_file.seek(0)
            images = convert_from_bytes(uploaded_file.read())
            for img in images:
                text += pytesseract.image_to_string(img)
            if text.strip():
                st.success("✅ OCR extraction successful!")
            else:
                st.error("❌ Failed to extract text from PDF.")

    elif file_type == "docx":
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"
        st.success("✅ Word document uploaded and extracted successfully!")
    elif file_type == "txt":
        text = uploaded_file.read().decode("utf-8")
        st.success("✅ TXT file uploaded and read successfully!")

# Text input fallback
st.markdown("### 📝 Input Your Text")
text = st.text_area("", value=text if text else "", height=200, key="input_text")

# Section: Individual Agent Buttons (Vertical Layout)
st.markdown("---")
st.markdown("### 🎯 Run Individual Agent")

agents = [
    ("🧠 Summarize", "SummarizeAgent"),
    ("💬 Sentiment", "SentimentAgent"),
    ("📊 Readability", "ReadabilityScorerAgent"),
    ("🎨 Style Enhance", "StyleEnhancerAgent"),
    ("🎯 Tone Adjust", "ToneAdjusterAgent"),
    ("🌍 Translate", "TranslationAgent")
]

for label, agent_name in agents:
    if st.button(label, key=agent_name):
        result = workflow.run_agent(agent_name, text, api_key)
        st.code(result, language="text")

# Section: Run All Agents
st.markdown("---")
st.markdown("### 🚀 Run All Agents at Once")

if st.button("🔁 Run All Agents", key="run_all_btn"):
    if text.strip():
        results = workflow.run_all_agents(text, api_key=api_key)
        st.success("✅ All agents completed successfully!")

        for name, output in results.items():
            with st.expander(f"📌 {name.capitalize()} Output"):
                st.code(output, language="text")
    else:
        st.warning("⚠️ Please enter some text before running all agents.")
# import streamlit as st
# from src.WorkFlow import workflow
# import os

# # Load API key from environment variable for security
# api_key = os.environ.get("OPENAI_API_KEY")
# if not api_key:
#     st.error("Please set the OPENAI_API_KEY environment variable.")
#     st.stop()

# # UI setup
# st.title("Multi-Agent Text Refinement System")
# st.write("Enter text below and choose an action.")

# # Text input area
# text = st.text_area("Input Text", height=200, key="input_text")

# # Buttons for individual agents
# if st.button("Summarize"):
#     result = workflow.run_agent("SummarizerAgent", text)
#     st.write("**Result:**", result)
    
# if st.button("Readability Score"):
#     result = workflow.run_agent("ReadabilityScorerAgent", text)
#     st.write("**Result:**", result)

# if st.button("Sentiment"):
#     result = workflow.run_agent("SentimentAgent", text)
#     st.write("**Result:**", result)

# if st.button("Style Enhance"):
#     result = workflow.run_agent("StyleEnhancerAgent", text)
#     st.write("**Result:**", result)

# if st.button("Tone"):
#     result = workflow.run_agent("ToneAdjusterAgent", text)
#     st.write("**Result:**", result)

# if st.button("Translate"):
#     result = workflow.run_agent("TranslationAgent", text)
#     st.write("**Result:**", result)

# # Button to run all agents
# if st.button("Run All Agents"):
#     results = workflow.run_all_agents(api_key)
#     st.write("**Results from All Agents:**")
#     for name, output in results.items():
#         st.write(f"**{name.capitalize()} Output:**", output)
        
import streamlit as st
import os
# Ensure you have the openai library installed: pip install openai
# Assuming your WorkFlow class is in src/WorkFlow.py
from src.WorkFlow import workflow # Import the WorkFlow class

# --- Configuration ---
APP_TITLE = "Multi-Agent Text Refinement System"

# Define agent names/keys used in the UI and potentially map them
# to names expected by the WorkFlow class if they differ.
AGENT_MAP = {
    "tone": "Tone Adjuster",
    "sentiment": "Sentiment Analyzer",
    "style": "Style Enhancer",
    "translate": "Translator",
    "readability": "Readability Scorer",
    "summary": "Summarizer",
}
AGENT_KEYS = list(AGENT_MAP.keys())

# --- Callback Functions ---

def on_change_run_all():
    """Callback function for the 'Run All Agents' checkbox."""
    # Get the current state of the 'Run All' checkbox
    select_all = st.session_state.get("all_agents", False)
    # Update the state of each individual agent checkbox
    for key in AGENT_KEYS:
        st.session_state[key] = select_all

def on_change_agent():
    """Callback function for individual agent checkboxes."""
    # Check if all individual agent checkboxes are currently checked
    all_selected = all(st.session_state.get(key, False) for key in AGENT_KEYS)
    # Update the 'Run All Agents' checkbox state accordingly
    st.session_state.all_agents = all_selected

# --- Initialize Session State ---
# Initialize keys if they don't exist (prevents errors on first run)
for key in AGENT_KEYS:
    if key not in st.session_state:
        st.session_state[key] = False
if 'all_agents' not in st.session_state:
    st.session_state['all_agents'] = False


# --- Streamlit App Layout ---

st.set_page_config(page_title=APP_TITLE, layout="wide")
st.title(APP_TITLE)

# --- API Key Check and Workflow Initialization ---
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    st.stop() # Stop execution if key is missing
else:
    st.success("OpenAI API key found.")
    try:
        # Instantiate the WorkFlow class
        workflow = workflow(api_key=api_key)
        st.info("WorkFlow initialized successfully.")
    except ImportError:
        st.error("Error importing WorkFlow from src.WorkFlow. Please ensure the file exists and is in the correct path.")
        st.stop()
    except Exception as e:
        st.error(f"Error initializing WorkFlow: {e}")
        st.stop()


st.markdown("---")

# --- Input Section ---
st.header("1. Input Text")
input_text = st.text_area("Enter the text you want to refine:", height=200, key="input_text")

st.markdown("---")

# --- Agent Selection ---
st.header("2. Select Agents")

# Use columns for better layout
col1, col2, col3 = st.columns(3)

# Create checkboxes with callbacks
with col1:
    st.checkbox(
        AGENT_MAP["tone"],
        key="tone",
        on_change=on_change_agent # Use callback
    )
    st.checkbox(
        AGENT_MAP["sentiment"],
        key="sentiment",
        on_change=on_change_agent # Use callback
    )

with col2:
    st.checkbox(
        AGENT_MAP["style"],
        key="style",
        on_change=on_change_agent # Use callback
    )
    st.checkbox(
        AGENT_MAP["translate"],
        key="translate",
        on_change=on_change_agent # Use callback
    )

with col3:
    st.checkbox(
        AGENT_MAP["readability"],
        key="readability",
        on_change=on_change_agent # Use callback
    )
    st.checkbox(
        AGENT_MAP["summary"],
        key="summary",
        on_change=on_change_agent # Use callback
    )

st.markdown("---")
# Create the "Run All Agents" checkbox with its callback
st.checkbox(
    "Run All Agents",
    key="all_agents",
    on_change=on_change_run_all # Use callback
)
st.markdown("---")


# --- Processing and Output ---
st.header("3. Refine")

if st.button("Refine Text", key="refine_button"):
    if not workflow:
        st.error("WorkFlow is not initialized. Cannot process text.")
    elif not input_text:
        st.warning("Please enter some text to refine.")
    else:
        st.subheader("Results:")
        results = {} # Store results from each agent

        # Determine which agents to run based on session state (reliable now)
        selected_agent_keys = [key for key in AGENT_KEYS if st.session_state.get(key, False)]

        if not selected_agent_keys:
            st.warning("Please select at least one agent to run.")
        else:
            with st.spinner("Agents are processing the text..."):
                current_text = input_text

                # Check if the user effectively selected all agents
                run_all_effective = len(selected_agent_keys) == len(AGENT_KEYS)

                # Option 1: Use run_all_agents if all are selected and the method exists
                if run_all_effective and hasattr(workflow, 'run_all_agents'):
                     st.info("Running all agents via workflow.run_all_agents()...")
                     try:
                         results = workflow.run_all_agents(current_text)
                         if not isinstance(results, dict):
                              st.error("workflow.run_all_agents() did not return a dictionary as expected.")
                              results = {}
                     except Exception as e:
                         st.error(f"Error executing workflow.run_all_agents(): {e}")
                         results = {}

                # Option 2: Run selected agents individually using run_agent
                else:
                    st.info("Running selected agents individually via workflow.run_agent()...")
                    for key in selected_agent_keys:
                        agent_name = AGENT_MAP[key]
                        try:
                            agent_options = {}

                            results[agent_name] = workflow.run_agent(
                                agent_identifier=agent_name,
                                text=current_text,
                                **agent_options
                            )
                        except Exception as e:
                            st.error(f"Error executing agent '{agent_name}': {e}")
                            results[agent_name] = f"Error processing with {agent_name}: {e}"

            # Display results
            if results:
                st.success("Processing complete!")
                for agent_name, result_text in results.items():
                     display_text = str(result_text) if result_text is not None else "No output received."
                     with st.expander(f"Output from: {agent_name}", expanded=True):
                        st.markdown(display_text)
            else:
                st.warning("No results were generated. Please check agent selections and potential errors above.")


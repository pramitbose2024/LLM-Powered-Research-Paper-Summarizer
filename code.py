import os

# SETUP: Hugging Face Cache Paths
os.environ["HF_HOME"] = "D:/huggingface_cache"
os.environ["TRANSFORMERS_CACHE"] = "D:/huggingface_cache/transformers"
os.environ["HF_DATASETS_CACHE"] = "D:/huggingface_cache/datasets"

# IMPORT LIBRARIES
from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline
from langchain_core.prompts import PromptTemplate, load_prompt
import streamlit as st

# LOAD LANGUAGE MODEL (LLM)
llm = HuggingFacePipeline.from_model_id(
    model_id='TinyLlama/TinyLlama-1.1B-Chat-v1.0',
    task='text-generation',
    pipeline_kwargs=dict(
        temperature=0.7
    )
)

# Wrap into Chat Model
model = ChatHuggingFace(llm=llm)

# Main title/header for the web application
st.header('Research Tool')

# User Inputs

# Dropdown for selecting a research paper to summarize
paper_input = st.selectbox(
    "Select Research Paper Name",
    [
        "Attention Is All You Need",
        "BERT: Pre-training of Deep Bidirectional Transformers",
        "GPT-3: Language Models are Few-Shot Learners",
        "Diffusion Models Beat GANs on Image Synthesis"
    ]
)

# Dropdown for selecting explanation style
style_input = st.selectbox(
    "Select Explanation Style",
    ["Beginner-Friendly", "Technical", "Code-Oriented", "Mathematical"]
)

# Dropdown for selecting explanation length
length_input = st.selectbox(
    "Select Explanation Length",
    ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (detailed explanation)"]
)

# LOAD PROMPT TEMPLATE
# Loads a structured prompt from an external JSON file (template.json)
template = load_prompt('template.json')

# Button Trigger
# When user clicks "Summarize", the model generates output
if st.button('Summarize'):

    # Create a chain by combining:
    # 1. Prompt template (input formatting)
    # 2. Model (response generation)
    chain = template | model

    # Invoke the chain:
    # - Fills template with user inputs
    # - Sends final prompt to model
    # - Returns structured response
    result = chain.invoke({
        'paper_input':paper_input,
        'style_input':style_input,
        'length_input':length_input
    })

    # DISPLAY OUTPUT
    st.write(result.content)

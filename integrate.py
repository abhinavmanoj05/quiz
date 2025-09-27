from datasets import load_dataset
import streamlit as st
import pandas as pd
from typing import Dict, List, Tuple
import re

# Load the dataset
@st.cache_data
def load_transliteration_data():
    """Load the Bhasha-Abhijnaanam dataset"""
    dataset = load_dataset("ai4bharat/Bhasha-Abhijnaanam", split="train")
    return dataset

def get_available_languages(dataset) -> Dict[str, str]:
    """Extract available languages and their scripts from the dataset"""
    languages = {}
    
    # Sample a few examples to understand the structure
    sample = dataset.select(range(min(100, len(dataset))))
    
    for example in sample:
        # The dataset typically has columns like 'text', 'language', 'script', etc.
        # Let's check what columns are available
        if hasattr(example, 'keys'):
            for key in example.keys():
                if 'lang' in key.lower() or 'script' in key.lower():
                    if key not in languages:
                        languages[key] = set()
                    languages[key].add(example[key])
    
    # Convert sets to lists for easier handling
    for key in languages:
        languages[key] = list(languages[key])
    
    return languages
    
dataset=load_transliteration_data("ai4bharat/Bhasha-Abhijnaanam",split="train")
print(dataset[0])

def create_transliteration_mapping(dataset, source_lang: str, target_lang: str) -> Dict[str, str]:
    """Create a mapping between source and target scripts"""
    mapping = {}
    
    # Filter examples that have both source and target languages
    for example in dataset:
        # This is a simplified approach - you might need to adjust based on actual dataset structure
        if source_lang in str(example) and target_lang in str(example):
            # Extract text pairs and create mapping
            # This is a placeholder - actual implementation depends on dataset structure
            pass
    
    return mapping

def transliterate_text(text: str, mapping: Dict[str, str]) -> str:
    """Transliterate text using the provided mapping"""
    result = text
    for source_char, target_char in mapping.items():
        result = result.replace(source_char, target_char)
    return result

def main():
    st.set_page_config(
        page_title="Indian Language Transliteration App",
        page_icon="🇮",
        layout="wide"
    )
    
    st.title("🇮 Indian Language Transliteration App")
    st.markdown("Transliterate text between different Indian scripts and languages")
    
    # Load dataset
    with st.spinner("Loading transliteration data..."):
        dataset = load_transliteration_data()
    
    st.success(f"Loaded {len(dataset)} transliteration examples!")
    
    # Display dataset info
    with st.expander("Dataset Information"):
        st.write("**Dataset:** Bhasha-Abhijnaanam")
        st.write(f"**Total Examples:** {len(dataset)}")
        
        # Show sample data
        st.write("**Sample Data:**")
        sample_data = dataset.select(range(min(5, len(dataset))))
        for i, example in enumerate(sample_data):
            st.write(f"Example {i+1}:")
            st.json(example)
    
    # Language selection
    st.header("Language Selection")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Source Language")
        source_lang = st.selectbox(
            "Select source language/script:",
            ["Hindi (Devanagari)", "Bengali", "Tamil", "Telugu", "Gujarati", 
             "Kannada", "Malayalam", "Punjabi", "Odia", "Assamese", "English"]
        )
    
    with col2:
        st.subheader("Target Language")
        target_lang = st.selectbox(
            "Select target language/script:",
            ["Hindi (Devanagari)", "Bengali", "Tamil", "Telugu", "Gujarati", 
             "Kannada", "Malayalam", "Punjabi", "Odia", "Assamese", "English"]
        )
    
    # Text input
    st.header("Text Input")
    input_text = st.text_area(
        "Enter text to transliterate:",
        placeholder="Type your text here...",
        height=100
    )
    
    # Transliteration button
    if st.button("Transliterate", type="primary"):
        if input_text.strip():
            with st.spinner("Transliterating..."):
                # For now, we'll create a simple demonstration
                # In a real implementation, you'd use the actual mapping from the dataset
                
                # Simple demonstration transliteration (placeholder)
                if source_lang == "English" and target_lang == "Hindi (Devanagari)":
                    # Basic English to Hindi transliteration demo
                    demo_mapping = {
                        'a': 'अ', 'b': 'ब', 'c': 'क', 'd': 'ड', 'e': 'ए',
                        'f': 'फ', 'g': 'ग', 'h': 'ह', 'i': 'इ', 'j': 'ज',
                        'k': 'क', 'l': 'ल', 'm': 'म', 'n': 'न', 'o': 'ओ',
                        'p': 'प', 'q': 'क', 'r': 'र', 's': 'स', 't': 'त',
                        'u': 'उ', 'v': 'व', 'w': 'व', 'x': 'क्ष', 'y': 'य', 'z': 'ज'
                    }
                    result = transliterate_text(input_text.lower(), demo_mapping)
                else:
                    result = f"[Demo] Transliterating from {source_lang} to {target_lang}: {input_text}"
                
                st.success("Transliteration Complete!")
                st.subheader("Result:")
                st.write(result)
        else:
            st.warning("Please enter some text to transliterate.")
    
    # Dataset exploration
    st.header("Dataset Exploration")
    
    # Show available languages/scripts
    languages = get_available_languages(dataset)
    if languages:
        st.write("**Available Languages/Scripts in Dataset:**")
        for key, values in languages.items():
            st.write(f"**{key}:** {', '.join(values[:10])}{'...' if len(values) > 10 else ''}")
    
    # Search functionality
    st.subheader("Search Dataset")
    search_term = st.text_input("Search for specific text in the dataset:")
    
    if search_term:
        with st.spinner("Searching..."):
            # Search through the dataset
            matches = []
            for i, example in enumerate(dataset):
                if search_term.lower() in str(example).lower():
                    matches.append((i, example))
                    if len(matches) >= 10:  # Limit results
                        break
            
            if matches:
                st.write(f"Found {len(matches)} matches:")
                for idx, match in matches:
                    st.write(f"**Example {idx}:**")
                    st.json(match)
            else:
                st.write("No matches found.")

if __name__ == "__main__":
    main()


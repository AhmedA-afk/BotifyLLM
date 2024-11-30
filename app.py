import streamlit as st
from scraper import scrape_webpage_structured, update_json_file
import ollama
import json

# Streamlit App Title
st.title("Webpage Scraper with Chatbot Integration")

# Load JSON file
def load_json_file(file_name):
    """
    Load data from a JSON file.

    Args:
        file_name (str): The name of the JSON file to load.

    Returns:
        dict: The data from the JSON file, or an error message if loading fails.
    """
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "No data available. Please scrape a webpage first."}
    except Exception as e:
        return {"error": f"Error reading JSON file: {e}"}

# Input for URL
url = st.text_input("Enter a URL", placeholder="https://example.com")

# Model selection UI
model_name = st.selectbox("Select Model", ["llama3.2:latest", "gpt-neo", "your-custom-model"])  # Update model names based on available models

# Function to run the Ollama model
def run_ollama_model(model_name, question, context):
    """
    Runs the selected Ollama model with the provided question and context.

    Args:
        model_name (str): The name of the model to use.
        question (str): The user's question.
        context (str): The context for the model to use as reference.

    Returns:
        str: The model's response.
    """
    try:
        # Combine context and question into a single input
        input_text = f"Context:\n{context}\n\nQuestion: {question}"
        
        # Run the model
        response = ollama.chat(
            model=model_name,
            messages=[{'role': 'user', 'content': input_text}]
        )
        return response['message']['content']  # Return the output from the model
    except Exception as e:
        return f"Error running model: {e}"

# Function to scrape webpage and update JSON
if st.button("Scrape and Process"):
    if url:
        st.write(f"Scraping and processing URL: {url}")
        structured_content = scrape_webpage_structured(url)

        # Update JSON file with the new scrape
        if "error" not in structured_content:
            success = update_json_file("scraped_data.json", structured_content)  # Provide both file name and data
            if success.get("status") == "success":
                st.success("Webpage scraped and data saved successfully!")
            else:
                st.error(f"Failed to update the JSON file: {success['message']}")
        else:
            st.error(f"Error scraping the webpage: {structured_content['error']}")
    else:
        st.warning("Please enter a valid URL.")

# Load the scraped data
scraped_data = load_json_file("scraped_data.json")

if "error" not in scraped_data:
    # Display a success message indicating that the data is loaded
    st.success("Scraped data loaded successfully.")

    # Allow the user to ask a question
    question = st.text_input("Ask a question about the website:")

    # Button to submit the question and get the answer
    if question:
        # Prepare context from the JSON file
        context = (
            f"Title: {scraped_data.get('title', 'No title')}\n"
            f"Description: {scraped_data.get('description', 'No description')}\n"
            f"Headings: {scraped_data.get('headings', {})}\n"
            f"Paragraphs: {' '.join(scraped_data.get('paragraphs', []))}"
        )

        # Get the model's response
        answer = run_ollama_model(model_name, question, context)
        st.subheader("Answer:")
        st.write(answer)
else:
    st.warning(scraped_data["error"])

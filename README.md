# AI Assistant with RAG Pipeline & Web Search

This project is an AI assistant application built using LangChain and Streamlit. The assistant uses a Retrieval-Augmented Generation (RAG) pipeline to retrieve relevant information from a pre-loaded document (PDF file) and can also fetch real-time information using a web search tool. The interface is built using Streamlit to provide a user-friendly way to interact with the assistant.

## Features:

• RAG Pipeline: Retrieves context from a preloaded document and answers queries on the topic of "Sound" and uses GPT to generate answers.

• Web Search Tool: Fetches real-time information from the web when necessary.

• Streamlit UI: Provides a simple interactive web interface to ask questions and display AI responses.
    

## Project Setup

### 1. Prerequisites

Ensure you have the following installed on your system:

    - Python >= 3.10, <3.13
    - pip or poetry (Python package managers)

Refer to the pyproject.toml file for dependencies.

### 2. Clone the Repository
First, clone the repository to your local system:

git clone https://github.com/jkumarr10/ai-assistant.git

cd ai-assistant

### 4. Install Dependencies
This project uses Poetry for dependency management. After cloning the repository, install the required dependencies by running:

    poetry install

To confirm that poetry is using a virtual environment, you can run: 

    poetry env info

### 5. Set Up Environment Variables

Create a .env file in the project root directory and add your environment variables. This file should store API keys and other sensitive information that shouldn't be committed to the repository. To run this project you will need a OPENAI API KEY & TAVILY API KEY.

### 6. Running the Streamlit Application

To start the application, use the terminal to run and launch the Streamlit server: 

    poetry run streamlit run app.py

This will launch the Streamlit server, and you can access the app in your web browser at http://localhost:8501.


### 7. Project Structure

• app.py: The main file for running the Streamlit application.

• ai_assistant.ipynb: A Jupyter Notebook that replicates the workflow of app.py but runs FastAPI directly within the notebook using nest_asyncio to allow concurrent event loops. It allows testing FastAPI endpoints directly in the notebook. (Contains steps for Assignment 1: setting up a RAG pipeline and steps for Assignment 2: setting up an AI Assitant with tools.)

• iesc111.pdf: A sample PDF document that is loaded into the RAG pipeline. This document contains information on the topic of "Sound".

• .gitignore: Specifies files and directories that should be ignored by Git (e.g., virtual environments, compiled files).

• pyproject.toml: Specifies project dependencies and configuration for Poetry.

###


## How to Use

Once the Streamlit app is running, follow these steps:

1. Enter a question: Type a question into the input box. You can ask questions related to the preloaded "Sound" document or other general questions.

2. Get a response: The AI assistant will either use the RAG pipeline to retrieve context from the document or fetch real-time web information. The result is displayed interactively in the Streamlit interface.

Example Queries:

    "What is sound?"
    "How do sound waves propagate?"
    "Explain the characteristics of sound."

### .gitignore

Make sure you add a .gitignore file to prevent sensitive files or unnecessary directories from being tracked in Git.

## Contact

If you have any questions or need further assistance, please feel free to reach out:

    Email: jitthenkumarr29@gmail.com
    GitHub: https://github.com/jkumarr10
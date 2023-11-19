import streamlit as st
import requests
import json
import os

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Define the URL of your FastAPI application
FASTAPI_BACKEND_URL: str = os.getenv("FASTAPI_BACKEND_URL", "http://localhost:3000")


st.title("Log Management Interface")

# Section for Ingesting Logs
st.header("Ingest Log")
log_json = st.text_area("Enter log data in JSON format", height=200)
ingest_button = st.button("Ingest Log")

if ingest_button:
    try:
        log_data = json.loads(log_json)
        response = requests.post(f"{FASTAPI_BACKEND_URL}/ingest", json=log_data)

        if response.status_code == 200:
            st.success("Log ingested successfully!")
        else:
            st.error(f"Error in log ingestion: {response.text}")
    except json.JSONDecodeError:
        st.error("Invalid JSON format")

# Section for Searching Logs
st.header("Search Logs")
query = str(st.text_input("Enter your search query", key="query_search"))
search_button = st.button("Search")

if search_button and query:
    response = requests.get(f"{FASTAPI_BACKEND_URL}/search", json={"query": str(query)})

    if response.status_code == 200:
        results = response.json()
        st.write("Search Results:")
        st.json(results)
    else:
        st.error(f"Error in search: {response.text}")

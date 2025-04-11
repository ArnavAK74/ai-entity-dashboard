import logging
import requests
from neo4j import GraphDatabase
import streamlit as st
# === Configuration ===

NEO4J_URI = 'neo4j+s://7734d3c5.databases.neo4j.io'
NEO4J_USER = 'neo4j'
NEO4J_PASSWORD = '1FyxVVdsr-By5mjKLI_ipkQ2qFLnd-lGgT0qvx8rrNs'

GROQ_LLM_API_URL = 'https://llm-cypher-api.onrender.com/convert'  # or your hosted endpoint

# === Setup Logging ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Neo4j Driver Setup ===
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def groq_llm_to_cypher(natural_input: str) -> str:
    """
    Converts natural language input into a Cypher query using the Groq LLM API.
    """
    payload = {'text': natural_input}
    try:
        response = requests.post(GROQ_LLM_API_URL, json=payload)
        response.raise_for_status()
        cypher_query = response.json().get('cypher', '')
        if not cypher_query:
            raise ValueError("No Cypher query returned.")
        return cypher_query
    except Exception as e:
        logger.error(f"Error converting input to Cypher: {e}")
        return ""


def run_cypher_query(query: str) -> str:
    """
    Executes the Cypher query in Neo4j and returns a stringified result.
    """
    try:
        with driver.session() as session:
            result = session.run(query)
            records = result.data()
            if not records:
                return "No results found."
            return "\n".join(str(record) for record in records)
    except Exception as e:
        logger.error(f"Error executing Cypher query: {e}")
        return f"An error occurred: {e}"

def summarize_result_with_llm(user_input: str, raw_result: str) -> str:
    """
    Uses OpenAI to summarize the Neo4j query result in natural language.
    """
    OPENAI_API_KEY = st.secrets["openai"]["OPENAI_API_KEY"]
    if not OPENAI_API_KEY:
        return "❌ OPENAI_API_KEY not set."

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
A user asked:

{user_input}

The Cypher query was run and returned:

{raw_result}

In a single sentence, clearly answer the user's question and concisely present the information returned by the Cypher query. Do not mention the cypher query.
Round any numbers to 3 decimal places and present the information returned from the query nicely visually. 
If there are more than 10 connections, return the top 10 most relevant parts of the cypher query as a numbered list in order of edge strength, based on the user's question and your best judgement.
Do not convert to percentages, leave as decimal values.
Come up with an interesting, relevant insight based off the resulting query after listing the connections. Understand that this cypher query is from a social network built from a sample dataset of news headlines related to AI and does not fully represent society. 

If the response does not work, tell the user there was an error and to try again.
"""

    payload = {
        "model": "gpt-3.5-turbo-16k",
        "messages": [
            {"role": "user", "content": prompt.strip()}
        ],
        "temperature": 0.5
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        summary = response.json()["choices"][0]["message"]["content"].strip()
        return summary
    except Exception as e:
        logger.error(f"Error summarizing result: {e}")
        return "❌ Could not generate summary."


def ask_bot(user_input: str) -> str:
    """
    Full pipeline: Natural language → Cypher → Neo4j → Summary.
    """
    logger.info(f"User input: {user_input}")
    
    cypher = groq_llm_to_cypher(user_input)
    if not cypher:
        return "❌ Could not generate Cypher query."
    
    logger.info(f"Cypher: {cypher}")
    raw_result = run_cypher_query(cypher)
    
    if "No results found." in raw_result or "error" in raw_result.lower():
        return raw_result
    
    summary = summarize_result_with_llm(user_input, raw_result)
    return summary




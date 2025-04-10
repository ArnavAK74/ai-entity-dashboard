import logging
import requests
from neo4j import GraphDatabase

# === Configuration ===

NEO4J_URI = 'neo4j+s://7734d3c5.databases.neo4j.io'
NEO4J_USER = 'neo4j'
NEO4J_PASSWORD = '1FyxVVdsr-By5mjKLI_ipkQ2qFLnd-lGgT0qvx8rrNs'

GROQ_LLM_API_URL = 'http://127.0.0.1:5004/convert'  # or your hosted endpoint

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


def ask_bot(user_input: str) -> str:
    """
    Full pipeline: Converts user input → Cypher → executes on Neo4j → returns results.
    """
    logger.info(f"User input: {user_input}")
    cypher = groq_llm_to_cypher(user_input)
    if not cypher:
        return "❌ Could not generate Cypher query."
    logger.info(f"Cypher: {cypher}")
    result = run_cypher_query(cypher)
    return result

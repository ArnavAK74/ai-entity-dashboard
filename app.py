import streamlit as st
import streamlit.components.v1 as components
from graphBot import ask_bot  # ✅ your Langchain chat interface

st.set_page_config(layout="wide")
st.title("🌐 AI Entity Influence Graph")

# Graph Section
st.markdown("### 🔗 AI Entity Network")
st.markdown("Visualize the relationships between AI-related entities and topics from 18,000 AI-related news headlines for the RAISE-25 Data Science/AI Competition.")
st.markdown("Scroll down for an interactive AI Agent to query the graph and explain relationships in natural language.")
# Load HTML graph
try:
    with open("100_entity_network.html", "r", encoding="utf-8") as f:
        graph_html = f.read()
    components.html(graph_html, height=800, scrolling=True)
except FileNotFoundError:
    st.error("Graph file not found. Please ensure '100_entity_network.html' is in the same directory.")

st.markdown("---")

# Chatbot Section
st.markdown("### 💬 Ask the AI Graph Bot")
st.markdown("You can ask questions like:")
st.code("Who is most connected to OpenAI?\nWhat are the top 5 connections to Trump?\nTell me about France in the graph.\nFind the shortest path between Yann LeCun and Elon Musk")

user_input = st.text_input("Ask a question about the AI network:", key="chat_input")

if user_input:
    with st.spinner("Thinking..."):
        try:
            response = ask_bot(user_input)
            st.markdown(f"**🧠 Bot:** {response}")
        except Exception as e:
            st.error(f"Error: {str(e)}")


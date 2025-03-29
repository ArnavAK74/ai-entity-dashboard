import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("🌐 AI Entity Influence Graph")
st.markdown("Explore the relationships between key AI entities and co-occurring topics.")

# Load your HTML graph
with open("100_entity_network.html", "r", encoding="utf-8") as f:
    graph_html = f.read()

# Display the interactive graph
components.html(graph_html, height=800, scrolling=True)

# Optional: Add a description or footer
st.markdown("""
---  
**Node size** = centrality  
**Edge weight** = co-occurrence strength  
**Central Node** = 'Artificial Intelligence'  
""")

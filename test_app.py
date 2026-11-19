
import streamlit as st

st.set_page_config(
    page_title="NEXUS AI Test",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 NEXUS AI")
st.subheader("Intelligent Research Assistant")

st.write("Welcome to NEXUS AI!")

st.divider()

st.subheader("💬 Conversation")

question = st.text_input(
    "Enter your question",
    placeholder="What is Python?"
)

if st.button("🚀 Start Research"):
    if question:
        st.success("Input is working!")
        st.write("Your question:", question)
    else:
        st.warning("Please enter a question.")

st.divider()
st.write("NEXUS AI Test Application")

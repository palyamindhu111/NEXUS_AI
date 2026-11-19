
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="NEXUS AI Input Test",
    page_icon="🧠",
    layout="wide"
)

# Page title
st.title("🧠 NEXUS AI")
st.subheader("Streamlit Input Test")

st.write("Testing all Streamlit input components.")

st.divider()

# Test 1: Text input
st.subheader("1. Text Input")

name = st.text_input(
    "Enter your name",
    placeholder="Type your name here"
)

# Test 2: Button
st.subheader("2. Button")

if st.button("Submit"):
    st.success("Button is working!")

# Test 3: Dropdown
st.subheader("3. Dropdown")

language = st.selectbox(
    "Choose a programming language",
    ["Python", "Java", "C++", "JavaScript"]
)

st.write("Selected language:", language)

# Test 4: Number input
st.subheader("4. Number Input")

age = st.number_input(
    "Enter a number",
    min_value=1,
    max_value=100,
    value=21
)

# Display results
st.divider()

st.subheader("Test Results")

st.write("Name:", name)
st.write("Language:", language)
st.write("Number:", age)

st.success("Test application loaded successfully!")


import streamlit as st
from agent import get_ai_response

# PAGE CONFIG
st.set_page_config(
    page_title="NEXUS AI",
    page_icon="🧠",
    layout="wide"
)

# SESSION STATE
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# CUSTOM DESIGN
st.markdown("""
<style>
.stApp {
    background-color: #101827;
    color: white;
}

h1, h2, h3, h4, p, label, span, li {
    color: white !important;
}

[data-testid="stSidebar"] {
    background-color: #172338;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.stTextInput input {
    background-color: #24344d !important;
    color: white !important;
    border: 1px solid #64748b !important;
}

.stTextInput input::placeholder {
    color: #cbd5e1 !important;
}

.stButton button {
    background-color: #2563eb !important;
    color: white !important;
    border: none !important;
    width: 100%;
}

[data-testid="stChatMessage"] {
    background-color: #1e293b;
    border: 1px solid #475569;
    border-radius: 12px;
    padding: 15px;
}

</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:

    st.title("🧠 NEXUS AI")
    st.caption("Intelligent Research Assistant")

    st.divider()

    st.subheader("⚙️ Research Settings")

    research_mode = st.selectbox(
        "Research Mode",
        [
            "Quick Research",
            "Detailed Research",
            "Technical Research"
        ]
    )

    st.divider()

    st.subheader("💬 Chat History")

    st.write(
        f"Total questions: {len(st.session_state.chat_history)}"
    )

    if st.button("🗑️ Clear Conversation"):
        st.session_state.chat_history = []
        st.rerun()


# MAIN PAGE
st.title("🧠 Welcome to NEXUS AI")

st.markdown("""
### Your Intelligent Research Assistant

Explore ideas, discover information and learn faster.
""")

st.divider()

st.subheader("⚡ Quick Research")

st.write("Enter a topic below to start your research.")


# CONVERSATION
st.subheader("💬 Conversation")

if not st.session_state.chat_history:
    st.info("Your conversation will appear here.")

for chat in st.session_state.chat_history:

    with st.chat_message("user"):
        st.markdown("**You**")
        st.write(chat["question"])

    with st.chat_message("assistant"):
        st.markdown("**NEXUS AI**")
        st.markdown(chat["answer"])

        sources = chat.get("sources", [])

        if sources:

            with st.expander("🔗 View Sources"):

                for source in sources:

                    url = source.get("url", "")
                    title = source.get("title", "Source")

                    if url:
                        st.markdown(f"[{title}]({url})")

                    st.caption(
                        source.get("status", "Not checked")
                    )


st.divider()


# QUESTION INPUT
st.subheader("🔍 Ask NEXUS AI")

with st.form("research_form", clear_on_submit=True):

    question = st.text_input(
        "Enter your research question",
        placeholder="Example: What is Python programming language?"
    )

    submitted = st.form_submit_button(
        "🚀 Start Research",
        use_container_width=True
    )


# AI RESPONSE
if submitted:

    if not question.strip():

        st.warning("Please enter your question.")

    else:

        previous_history = list(
            st.session_state.chat_history
        )

        with st.spinner("🧠 NEXUS AI is researching..."):

            try:

                result = get_ai_response(
                    question=question,
                    research_mode=research_mode,
                    chat_history=previous_history
                )

                if isinstance(result, dict):

                    answer = result.get(
                        "answer",
                        "No answer generated."
                    )

                    sources = result.get("sources", [])

                else:

                    answer = str(result)
                    sources = []

                st.session_state.chat_history.append({
                    "question": question,
                    "answer": answer,
                    "sources": sources
                })

                st.rerun()

            except Exception as e:

                st.error(f"Research error: {e}")


# FOOTER
st.divider()

st.markdown("""
<div style="text-align:center; padding:20px;">
    <h3 style="color:white;">🧠 NEXUS AI</h3>
    <p style="color:white;">
        Built with Python, Streamlit, LangChain and Groq
    </p>
</div>
""", unsafe_allow_html=True)

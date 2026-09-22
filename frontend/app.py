import streamlit as st
from api_client import ask_question

st.set_page_config(page_title="AI, ML & Database RAG Assistant", page_icon="📚", layout="centered")
st.title("📚 AI, ML & Database RAG Assistant")
st.caption("Answers are generated only from the project knowledge base and include retrieved sources.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            st.markdown("**Retrieved sources**")
            for source in message["sources"]:
                st.caption(f"• {source}")

question = st.chat_input("Ask about AI, machine learning, or databases...")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Retrieving relevant document chunks and generating a grounded answer..."):
            try:
                result = ask_question(question)
                st.markdown(result["answer"])
                st.markdown("**Retrieved sources**")
                for source in result["sources"]:
                    st.caption(f"• {source}")
                st.session_state.messages.append({"role": "assistant", "content": result["answer"], "sources": result["sources"]})
            except Exception as exc:
                message = "The backend could not be reached. Start FastAPI on port 8000, then try again."
                st.error(message)
                st.caption(str(exc))

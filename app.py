import streamlit as st
import openai
import pdfplumber

st.set_page_config(page_title="Legal Research AI", layout="wide")

# --------- Custom CSS for Beautiful Design ----------
st.markdown("""
<style>
body {background-color: #abdbe3;}
[data-testid="stSidebar"] {
    background-color: #e48a4b;
}
[data-testid="stSidebar"] .css-1v0mbdj {color: #abdbe3;}
h1, h2 {color: #e48a4b;}
.stButton>button {
    background-color: #01497c;
    color: white;
    border-radius: 10px;
    font-weight: bold;
}
.stTextArea textarea, .stTextInput input {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# --------- Sidebar ---------
st.sidebar.title("⚖️ Legal Research AI Assistant")
api_key = st.sidebar.text_input("OpenAI API Key", type="password")
mode = st.sidebar.radio("Choose a function:", ["Ask Legal Question", "Summarize Text", "Summarize PDF Document"])

if not api_key:
    st.sidebar.warning("🔑 Enter your OpenAI API key above to start")
    st.stop()

# openai.api_key = api_key
client = openai.OpenAI(api_key=api_key)

# --------- Helper Function ---------
def ask_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert legal research assistant. Always be concise and cite sources if possible."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=800,
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


# --------- Main App ---------
st.title("🧑‍⚖️ Legal Research AI Assistant")

if mode == "Ask Legal Question":
    st.header("Ask a Legal Research Question")
    user_q = st.text_area("Enter your question here:", placeholder="E.g., What is the precedent for breach of contract in New York?")
    if st.button("Get AI Answer") and user_q:
        with st.spinner("AI is researching..."):
            answer = ask_gpt(user_q)
            st.success(answer)

elif mode == "Summarize Text":
    st.header("Summarize Legal Document (Paste Text)")
    user_doc = st.text_area("Paste the legal document or text here:")
    if st.button("Summarize Text") and user_doc:
        with st.spinner("Summarizing..."):
            summary = ask_gpt(f"Summarize the following legal document in plain language:\n\n{user_doc}")
            st.info(summary)

elif mode == "Summarize PDF Document":
    st.header("Upload and Summarize PDF Legal Document")
    uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_pdf is not None:
        with pdfplumber.open(uploaded_pdf) as pdf:
            all_text = ""
            for page in pdf.pages:
                all_text += page.extract_text() or ""
        st.text_area("Extracted Text", value=all_text[:3000] + ("..." if len(all_text) > 3000 else ""), height=300)
        if st.button("Summarize PDF"):
            with st.spinner("Summarizing PDF..."):
                summary = ask_gpt(f"Summarize this legal document in plain language:\n\n{all_text[:8000]}")
                st.info(summary)

st.markdown("---")
st.markdown("Made with ❤️ using [Streamlit](https://streamlit.io/) and [OpenAI](https://platform.openai.com/).")


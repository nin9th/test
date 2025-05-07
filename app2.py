import streamlit as st
from docx import Document
import io

# Page config with bright theme colors
st.set_page_config(
    page_title="Moon Prism Power, Paste and Go!",
    layout="centered",
    initial_sidebar_state="auto"
)

# Inject CSS for custom color theme
st.markdown("""
    <style>
        body {
            background-color: #ffffff;
        }
        .stApp {
            background-color: #ffffff;
        }
        h1, h2, h3, .stMarkdown, .stTextInput, .stTextArea, .stButton, .stCheckbox {
            color: #5158ff;
        }
        .css-1cpxqw2, .css-1d391kg {
            background-color: #fff666 !important;
            color: #000000 !important;
            border-radius: 10px;
            border: 2px solid #d260ff;
        }
        .stTextArea textarea {
            background-color: #fffafc;
            border: 1px solid #d260ff;
        }
    </style>
""", unsafe_allow_html=True)

# Function to parse entries
def parse_entries(text):
    lines = [line.strip() for line in text.strip().splitlines()]
    entries = []
    i = 0
    while i < len(lines):
        if lines[i].isdigit():
            try:
                source = lines[i + 1]
                context = lines[i + 2]
                translation = lines[i + 3]
                entries.append((source, translation, context))
                i += 4
                while i < len(lines) and not lines[i].isdigit():
                    i += 1
            except IndexError:
                break
        else:
            i += 1
    return entries

# Save outputs
def save_outputs(entries, generate_txt, generate_docx):
    if not entries:
        st.error("No valid entries found.")
        return

    if not (generate_txt or generate_docx):
        st.warning("No output format selected.")
        return

    if generate_txt:
        output = io.StringIO()
        output.write("Source\tTranslation\tContext\n")
        for src, trans, ctx in entries:
            output.write(f"{src}\t{trans}\t{ctx}\n")
        txt_data = output.getvalue().encode('utf-8')
        st.download_button("⬇ Download Tab-Delimited .txt", txt_data, "output.txt", "text/plain")

    if generate_docx:
        doc = Document()
        for _, trans, _ in entries:
            doc.add_paragraph(trans)
        doc_io = io.BytesIO()
        doc.save(doc_io)
        doc_io.seek(0)
        st.download_button("⬇ Download .docx", doc_io, "translations.docx", 
                           "application/vnd.openxmlformats-officedocument.wordprocessingml.document")

# Layout
st.title("🌙 Moon Prism Power, Paste and Go!")

with st.expander("📘 How to use this app"):
    st.markdown("""
        Paste the text copied from TTM.  
        Each entry must follow this format:  
        ```
        {Segment No.}
        {Source}
        {Context}
        {Translation}
        ```
        Or upload a `.txt` file with the same format.
    """)

# Input
input_method = st.radio("Choose your input method:", ["Paste text", "Upload file"], horizontal=True)

text_input = ""
if input_method == "Paste text":
    text_input = st.text_area("Paste your text below:", height=300, placeholder="1\nHello\nGreeting\nBonjour\n...")
else:
    uploaded_file = st.file_uploader("Upload your text file (.txt)", type=["txt"])
    if uploaded_file:
        text_input = uploaded_file.read().decode("utf-8")

if text_input:
    entries = parse_entries(text_input)

    if entries:
        st.subheader("📝 Translations (for copy-paste):")
        translations_only = "\n".join(trans for _, trans, _ in entries)
        st.text_area("Translations", value=translations_only, height=200)

        # Output options
        st.subheader("💾 Download Options")
        col1, col2 = st.columns(2)
        generate_txt = col1.checkbox("Generate Tab-Delimited .txt", value=True)
        generate_docx = col2.checkbox("Generate .docx", value=False)

        if st.button("Generate Downloads"):
            save_outputs(entries, generate_txt, generate_docx)
    else:
        st.warning("No valid entries found.")

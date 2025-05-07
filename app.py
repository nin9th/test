import streamlit as st
from docx import Document
import io

# 🎨 --- Custom CSS Styling ---
st.markdown("""
    <style>
    html, body, .stApp {
        background-color: #fffafc;
    }

    h1 {
        color: #ff2e51;
        font-weight: bold;
    }

    .stMarkdown h3, .stSubheader {
        color: #5158ff;
        margin-top: 1rem;
    }

    .stTextArea textarea {
        border: 2px solid #d260ff !important;
        background-color: #fffaff !important;
        border-radius: 10px;
    }

    .stDownloadButton button {
        background-color: #ff2e51 !important;
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
    }

    .stDownloadButton button:hover {
        background-color: #d260ff !important;
        color: white !important;
    }

    .stExpander {
        background-color: #ffb3df !important;
        border-radius: 10px !important;
    }

    .stExpanderHeader {
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 📄 --- Parse Logic ---
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

# 📄 --- DOCX Generation ---
def generate_docx(entries):
    doc = Document()
    for _, trans, _ in entries:
        doc.add_paragraph(trans)
    doc_io = io.BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)
    return doc_io

# 🌙 --- App Title & Help Section ---
st.markdown("<h1>🌙 Moon Prism Power, Paste and Go!</h1>", unsafe_allow_html=True)
st.caption("A magical way to extract translations and download them with ease.")

with st.expander("📝 How to use this app"):
    st.markdown("""
**This app helps you extract translations from formatted text and download them.**

### 📋 Format:
Each translation entry must look like this:
1
Source
Context
Translation
Repeat for multiple entries.

### ✅ Steps:
1. Paste your formatted text below.
2. Extracted translations will appear automatically.
3. Click a button to download your files.
""")

# 🧾 Step 1: Input Area
st.subheader("Step 1: Paste your input text")
text_input = st.text_area("Paste here:", height=400, placeholder="1\nHello\nGreeting\nBonjour")

# 🧪 Step 2: Extracted Translations
entries = parse_entries(text_input) if text_input.strip() else []

if entries:
    st.subheader("Step 2: Extracted Translations")
    translations = "\n".join(trans for _, trans, _ in entries)
    st.text_area("You can copy this manually if needed:", value=translations, height=100)

# 💾 Step 3: Download Buttons
if entries:
    st.subheader("Step 3: Download Your Files")

    txt_data = "\n".join([f"{src}\t{trans}\t{ctx}" for src, trans, ctx in entries]).encode('utf-8')
    docx_data = generate_docx(entries)

    st.download_button(
        label="⬇ Download Tab-Delimited .txt",
        data=txt_data,
        file_name="output_tab_delimited.txt",
        mime="text/plain"
    )

    st.download_button(
        label="⬇ Download .docx (Translations Only)",
        data=docx_data,
        file_name="translations.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
else:
    st.info("Please paste valid input text above to enable downloads.")

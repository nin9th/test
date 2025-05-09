import streamlit as st
from docx import Document
import io

# Helper function to generate DOCX
def generate_docx(entries):
    doc = Document()
    for _, trans, _ in entries:
        doc.add_paragraph(trans)
    doc_io = io.BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)
    return doc_io

# Parse entries from the pasted input
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

# --- UI Begins ---

st.set_page_config(
    page_title="Moon Prism Power, Paste and Go!",
    page_icon="🌙",
    layout="centered"
)

st.markdown("""
    <style>
        .main .block-container {
            max-width: 1500px;
            margin: auto;
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color:#ff2e51;'>🌙 Moon Prism Power, Paste and Go!</h1>", unsafe_allow_html=True)
st.caption("Extract translations from formatted text and download them easily.")

# Help section
with st.expander("ℹ️ How to use this app"):
    st.markdown("""
**This app helps you extract translations and download them in TXT or DOCX format.**

### ✂️ Input Format:
Each translation entry must follow this format:
<div style="line-height:1.5; font-style: italic; margin-left: 2em;">
1<br>
Source sentence<br>
Context sentence<br>
Translated sentence
</div>
\n\n
### ✅ Steps:
1. Paste the copied translation text into the box below.
2. The app will automatically extract the translations.
3. You can download the translations in `.txt` or `.docx` format.
    """, unsafe_allow_html=True)

# Step 1: Input area
st.subheader("Step 1: Paste your input text below")
text_input = st.text_area("Paste the formatted text from TTM here:", height=400, placeholder="1\nHello\nGreeting\nBonjour\n...")

# Step 2: Extract translations
if text_input.strip():
    entries = parse_entries(text_input)
    if entries:
        translations = "\n".join(trans for _, trans, _ in entries)
        st.subheader("Step 2: Extracted Translations")
        st.text_area("You can copy this manually if needed:", 
                     value=translations, 
                     height=100, 
                     key="extracted_display")
    else:
        st.info("No valid entries detected.")
else:
    st.session_state.pop("extracted_display", None)

# Step 3: Download buttons
if text_input.strip() and entries:
    st.subheader("Step 3: Download Your Files")
    st.download_button(
        label="⬇ Download Tab-Delimited .txt",
        data="\n".join([f"{src}\t{trans}\t{ctx}" for src, trans, ctx in entries]).encode('utf-8'),
        file_name="output_tab_delimited.txt",
        mime="text/plain"
    )
    docx_data = generate_docx(entries)
    st.download_button(
        label="⬇ Download .docx (Translations Only)",
        data=docx_data,
        file_name="translations.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
else:
    st.info("Please paste valid input text to enable downloads.")

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
st.title("🌙 Moon Prism Power, Paste and Go!")
st.caption("Extract translations from formatted text and download them easily.")

# Help section
with st.expander("🛈 How to use this app"):
    st.markdown("""
**This app helps you extract translations and download them in TXT or DOCX format.**

### ✂️ Input Format:
Each translation entry must follow this format:

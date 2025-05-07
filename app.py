import streamlit as st
from docx import Document
import os
import io
import pandas as pd

# Function to parse entries from text input (same as original)
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

# Function to copy translations to clipboard
def copy_translations(text):
    entries = parse_entries(text)
    if not entries:
        st.error("No valid translations found to copy.")
        return
    translations = "\n".join(trans for _, trans, _ in entries)
    st.session_state['clipboard'] = translations
    st.success("Translations copied to clipboard!")

# Function to generate and download files
def save_outputs(text, generate_txt, generate_docx):
    entries = parse_entries(text)
    if not entries:
        st.error("No valid entries found in the text.")
        return

    if not (generate_txt or generate_docx):
        st.warning("No output file types selected.")
        return

    files_generated = []

    # Generate tab-delimited text file
    if generate_txt:
        output = io.StringIO()
        output.write("Source\tTranslation\tContext\n")
        for src, trans, ctx in entries:
            output.write(f"{src}\t{trans}\t{ctx}\n")
        txt_data = output.getvalue().encode('utf-8')
        st.download_button(
            label="Download Tab-Delimited .txt",
            data=txt_data,
            file_name="output_tab_delimited.txt",
            mime="text/plain"
        )
        files_generated.append("Tab-delimited .txt")

    # Generate DOCX file
    if generate_docx:
        doc = Document()
        for _, trans, _ in entries:
            doc.add_paragraph(trans)
        doc_io = io.BytesIO()
        doc.save(doc_io)
        doc_io.seek(0)
        st.download_button(
            label="Download .docx",
            data=doc_io,
            file_name="translations.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        files_generated.append(".docx")

    if files_generated:
        st.success(f"Files generated: {', '.join(files_generated)}")

# Streamlit app layout
st.title("Moon Prism Power, Paste and Go! 🌙")

# Help text (replacing tooltip)
with st.expander("How to use this app"):
    st.markdown("""
    Paste the text copied from Translation Task Manager (TTM).  
    Each entry must follow this format:  
    ```
    {Segment No.}
    {Source}
    {Context}
    {Translation}
    ```
    """)

# Text input area
st.subheader("Paste your input text below:")
text_input = st.text_area("", height=400, placeholder="Paste your text here...")

# Copy translations button
if st.button("📋 Copy translations to clipboard"):
    copy_translations(text_input)

# Output options
st.subheader("Output options")
col1, col2 = st.columns(2)
generate_txt = col1.checkbox("Generate Tab-Delimited .txt", value=True)
generate_docx = col2.checkbox("Generate .docx", value=False)

# Save outputs button
if st.button("Save Outputs"):
    save_outputs(text_input, generate_txt, generate_docx)

# Clipboard copy workaround for Streamlit (display copied text)
if 'clipboard' in st.session_state:
    st.text_area("Copied Translations (for manual copy if needed):", 
                 value=st.session_state['clipboard'], 
                 height=100, 
                 key="clipboard_display")

import streamlit as st
from docx import Document
import io

# Function to parse entries from text input
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
            label="⬇ Download Tab-Delimited .txt",
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
            label="⬇ Download .docx",
            data=doc_io,
            file_name="translations.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        files_generated.append(".docx")

    if files_generated:
        st.success(f"Files generated: {', '.join(files_generated)}")

# Streamlit app layout
st.title("Moon Prism Power, Paste and Go! 🌙")

# Help section
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

# Input and Clear
st.subheader("Step 1: Paste your input text below")

col_input, col_clear = st.columns([4, 1])
with col_input:
    # Handle session state for input text using key
    text_input = st.text_area("", height=400, placeholder="Paste your text here...", key="input_text")
with col_clear:
    if st.button("🧹 Clear"):
        # Clear the session state value for input_text, which will clear the text area
        st.session_state["input_text"] = ""

# Real-time extraction with auto-clear
if text_input.strip():
    entries = parse_entries(text_input)
    if entries:
        translations = "\n".join(trans for _, trans, _ in entries)
        st.subheader("Extracted Translations")
        st.text_area("Automatically extracted (for manual copy):", 
                     value=translations, 
                     height=100, 
                     key="extracted_display")
    else:
        st.info("No valid entries detected.")
else:
    st.session_state.pop("extracted_display", None)

# Output format selection
st.subheader("Step 2: Choose Output Format")
col1, col2 = st.columns(2)
generate_txt = col1.checkbox("Generate Tab-Delimited .txt", value=True)
generate_docx = col2.checkbox("Generate .docx", value=False)

# File generation section
st.subheader("Step 3: Generate and Download Files")
if text_input.strip():
    entries = parse_entries(text_input)
    if entries:
        save_outputs(text_input, generate_txt, generate_docx)
    else:
        st.info("Please enter valid input above to enable downloads.")
else:
    st.info("No input detected. Paste something above first.")

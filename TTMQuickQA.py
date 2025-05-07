import streamlit as st
from docx import Document
from io import StringIO, BytesIO

st.set_page_config(page_title="Moon Prism Power, Paste and Go!", layout="centered")

st.title("🌙 Moon Prism Power, Paste and Go!")
st.markdown("""
Paste the text copied from Translation Task Manager (TTM).  
Each entry must follow this format:
{Segment No.}
{Source}
{Context}
{Translation}
""")

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

input_text = st.text_area("Paste your input text below:", height=400)

if st.button("Process"):
    if not input_text.strip():
        st.error("Please paste some text first.")
    else:
        entries = parse_entries(input_text)
        if not entries:
            st.warning("No valid entries found.")
        else:
            st.success(f"Found {len(entries)} entries!")

            # Generate tab-delimited text
            tab_output = StringIO()
            tab_output.write("Source\tTranslation\tContext\n")
            for src, trans, ctx in entries:
                tab_output.write(f"{src}\t{trans}\t{ctx}\n")
            tab_output.seek(0)
            st.download_button(
                label="📄 Download Tab-Delimited TXT",
                data=tab_output,
                file_name="output_tab_delimited.txt",
                mime="text/plain"
            )

            # Generate DOCX
            doc = Document()
            for _, trans, _ in entries:
                doc.add_paragraph(trans)
            docx_io = BytesIO()
            doc.save(docx_io)
            docx_io.seek(0)
            st.download_button(
                label="📝 Download .docx Translations",
                data=docx_io,
                file_name="translations.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

            # Display translations for easy copy
            translations_only = "\n".join(trans for _, trans, _ in entries)
            st.text_area("Translations Only (for copying):", translations_only, height=200)

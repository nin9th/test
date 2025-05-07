import streamlit as st
from docx import Document
import io

# Page config with bright theme colors
st.set_page_config(
    page_title="Moon Prism Power, Paste and Go!",
    layout="wide",
    initial_sidebar_state="auto"
)

# Inject CSS for custom color theme
st.markdown("""
    <style>
        html, body, [class*="st-"] {
            background-color: #ffffff;
            color: #5158ff;
            font-family: "Inter", sans-serif;
        }

        h1, h2, h3, .stMarkdown, label, .css-18ni7ap {
            color: #5158ff !important;
        }

        .stTextArea textarea, .stTextInput input {
            background-color: #fffafc !important;
            color: #000000 !important;
            border: 1px solid #d260ff !important;
        }

        .stDownloadButton button, .stButton button {
            background-color: #fff666 !important;
            color: #000 !important;
            border-radius: 10px;
            border: 2px solid #d260ff;
        }

        .stCheckbox > label, .stCheckbox span {
            color: #5158ff !important;
        }

        .css-1offfwp {
            color: #ff2e51 !important;
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
    """)

# Input
text_input = st.text_area("Paste your text below:", height=300, placeholder="1\nHello\nGreeting\nBonjour\n...")

if text_input:
    entries = parse_entries(text_input)

    if entries:
        st.subheader("✂️ Translation Preview")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Input**")
            for src, _, ctx in entries:
                st.text(f"{src}\n({ctx})")
        with col2:
            st.markdown("**Translation**")
            translations_only = "\n".join(trans for _, trans, _ in entries)
            st.text_area("", value=translations_only, height=300)

        # Output options
        st.subheader("💾 Download Options")
        col1, col2 = st.columns(2)
        generate_txt = col1.checkbox("Generate Tab-Delimited .txt", value=True)
        generate_docx = col2.checkbox("Generate .docx", value=False)

        if st.button("Generate Downloads"):
            save_outputs(entries, generate_txt, generate_docx)
    else:
        st.warning("No valid entries found.")

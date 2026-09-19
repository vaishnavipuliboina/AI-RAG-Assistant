import os

import streamlit as st

from src.document_processor import load_and_split_pdf
from src.embeddings import get_embeddings
from src.vector_store import create_vector_store
from src.rag_pipeline import generate_answer


# ---------------------------------------
# Page configuration
# ---------------------------------------

st.set_page_config(
    page_title="AI RAG Assistant",
    page_icon="📚",
    layout="wide"
)


# ---------------------------------------
# Title
# ---------------------------------------

st.title("📚 AI-Powered Document Intelligence & RAG Assistant")

st.write(
    "Upload a PDF and ask questions about its contents."
)


# ---------------------------------------
# Session state
# ---------------------------------------

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "file_name" not in st.session_state:
    st.session_state.file_name = None


# ---------------------------------------
# PDF upload
# ---------------------------------------

uploaded_file = st.file_uploader(
    "Upload your PDF",
    type=["pdf"]
)


# ---------------------------------------
# Process uploaded PDF
# ---------------------------------------

if uploaded_file is not None:

    # Check if this is a new PDF
    if st.session_state.file_name != uploaded_file.name:

        # Save PDF
        pdf_path = os.path.join(
            "documents",
            uploaded_file.name
        )

        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("PDF uploaded successfully!")

        # --------------------------------
        # Load and split PDF
        # --------------------------------

        with st.spinner("Reading and splitting PDF..."):

            documents, chunks = load_and_split_pdf(
                pdf_path
            )

        st.write(
            "Number of pages:",
            len(documents)
        )

        st.write(
            "Number of chunks:",
            len(chunks)
        )

        # --------------------------------
        # Create embeddings
        # --------------------------------

        with st.spinner("Creating embeddings..."):

            embeddings = get_embeddings()

        # --------------------------------
        # Create FAISS database
        # --------------------------------

        with st.spinner("Creating vector database..."):

            vector_store = create_vector_store(
                chunks,
                embeddings
            )

        # Save in session
        st.session_state.vector_store = vector_store
        st.session_state.file_name = uploaded_file.name

        st.success(
            "Document is ready for questions! ✅"
        )


# ---------------------------------------
# Question section
# ---------------------------------------

if st.session_state.vector_store is not None:

    st.divider()

    st.subheader("💬 Ask a Question")

    question = st.text_input(
        "Enter your question:"
    )

    if st.button("Ask Question"):

        if question.strip() == "":

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Searching document and generating answer..."
            ):

                answer, sources = generate_answer(
                    question,
                    st.session_state.vector_store
                )

            # --------------------------------
            # Answer
            # --------------------------------

            st.subheader("Answer")

            st.write(answer)

            # --------------------------------
            # Sources
            # --------------------------------

            st.subheader("📄 Sources")

            pages = set()

            for source in sources:

                page = source.metadata.get(
                    "page",
                    None
                )

                if page is not None:
                    pages.add(page + 1)

            if pages:

                for page in sorted(pages):

                    st.write(
                        f"📄 Page {page}"
                    )

            else:

                st.write(
                    "Source page information unavailable."
                )
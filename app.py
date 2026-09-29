import streamlit as st

from src.rag_pipeline import generate_rag_answer

from src.config import DEFAULT_TOP_K


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="GovAssist AI",
    page_icon="🤖",
    layout="centered"
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("🤖 GovAssist AI")

st.write(
    "Ask questions about the Andhra Pradesh "
    "Panchayat Raj Act, 1994."
)

st.caption(
    "Document-grounded answers with conversation memory."
)


# ---------------------------------------------------------
# INITIALIZE CONVERSATION MEMORY
# ---------------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


# ---------------------------------------------------------
# DISPLAY EXISTING CHAT
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ---------------------------------------------------------
# USER INPUT
# ---------------------------------------------------------

question = st.chat_input(
    "Ask GovAssist about the Act..."
)


# ---------------------------------------------------------
# PROCESS QUESTION
# ---------------------------------------------------------

if question:

    # -----------------------------------------------------
    # SAVE USER MESSAGE
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # -----------------------------------------------------
    # DISPLAY USER MESSAGE
    # -----------------------------------------------------

    with st.chat_message("user"):

        st.markdown(
            question
        )


    # -----------------------------------------------------
    # IMPORTANT:
    # Pass history BEFORE current question.
    #
    # The current question has already been appended,
    # so exclude the last message.
    # -----------------------------------------------------

    conversation_history = (
        st.session_state.messages[:-1]
    )


    # -----------------------------------------------------
    # GENERATE RAG RESPONSE
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Searching the government document..."
        ):

            result = generate_rag_answer(
                question=question,
                conversation_history=conversation_history,
                top_k=DEFAULT_TOP_K
            )


        # -------------------------------------------------
        # SUCCESS
        # -------------------------------------------------

        if result["success"]:

            answer = result["answer"]

            st.markdown(
                answer
            )


            # ---------------------------------------------
            # DISPLAY RETRIEVED SOURCES
            # ---------------------------------------------

            documents = result.get(
                "documents",
                []
            )


            if documents:

                with st.expander(
                    "View retrieved sources"
                ):

                    for index, document in enumerate(
                        documents,
                        start=1
                    ):

                        metadata = document[
                            "metadata"
                        ]

                        st.markdown(
                            f"### Source {index}"
                        )

                        st.write(
                            "Document:",
                            metadata.get(
                                "document_title",
                                "Unknown"
                            )
                        )

                        st.write(
                            "Page:",
                            metadata.get(
                                "page_number",
                                "Unknown"
                            )
                        )

                        st.write(
                            "Section:",
                            metadata.get(
                                "section",
                                "Unknown"
                            )
                        )

                        st.write(
                            "Section title:",
                            metadata.get(
                                "section_title",
                                "Unknown"
                            )
                        )

                        st.write(
                            "Retrieval distance:",
                            round(
                                document["distance"],
                                4
                            )
                        )

                        st.write(
                            "Retrieved text:"
                        )

                        st.write(
                            document["text"]
                        )

                        st.divider()


            # ---------------------------------------------
            # SAVE ASSISTANT MESSAGE
            # ---------------------------------------------

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )


        # -------------------------------------------------
        # FAILURE
        # -------------------------------------------------

        else:

            error_message = (
                "GovAssist could not process "
                "your question."
            )

            st.error(
                error_message
            )

            st.exception(
                result["error"]
            )
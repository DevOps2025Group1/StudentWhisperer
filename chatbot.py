"""
Chatbot application for University of Amsterdam students using OpenAI and Azure Search.
"""  # noqa: E501

import streamlit as st
import dotenv
from clients.search_client import AzureSearchClient
from clients.openai_client import OpenAIClient


class OpenAIChatbot:
    """Chatbot interface using Streamlit and Azure APIs."""

    def __init__(self):
        self.openai_client = OpenAIClient()
        self.search_client = AzureSearchClient()
        self.system_prompt = {
            "role": "system",
            "content": (
                "You are an AI assistant designed to help students from the University of Amsterdam. "  # noqa: E501, pylint: disable=C0321
                "Provide clear and concise answers based solely on the information provided in the conversation "  # noqa: E501, pylint: disable=C0321
                "and documents. Do not provide false information or content not mentioned in the documents. "  # noqa: E501, pylint: disable=C0321
                "Use relevant knowledge when needed. Avoid mentioning that your information comes from the documents."  # noqa: E501, pylint: disable=C0321
            ),
        }

    def run(self):
        """Run the Streamlit chatbot interface."""
        st.title("💬 Chatbot")
        st.caption("🚀 The Student Whisperer")

        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "assistant", "content": "How can I help you?"}
            ]

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input():
            self.process_input(prompt)

    def process_input(self, prompt: str):
        """Handle user input, retrieve context, and generate response."""
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Search for relevant context
        search_results = self.search_client.search_documents(prompt)
        context_message = (
            {
                "role": "system",
                "content": f"Relevant information from search:\n{search_results}",  # noqa: E501
            }
            if search_results.strip()
            else None
        )

        # Build messages list with system prompt
        messages_with_context = [self.system_prompt]
        if context_message:
            messages_with_context.append(context_message)
        messages_with_context += st.session_state.messages

        # Generate response using OpenAI API
        msg = self.openai_client.generate_response(messages_with_context)
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)


if __name__ == "__main__":
    dotenv.load_dotenv()

    chatbot = OpenAIChatbot()
    chatbot.run()

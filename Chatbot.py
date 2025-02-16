import streamlit as st
from clients.search_client import AzureSearchClient
from clients.openai_client import OpenAIClient

class OpenAIChatbot:
    def __init__(self):
        self.openai_client = OpenAIClient()
        self.search_client = AzureSearchClient()
        self.system_prompt = {
            "role": "system",
            "content": (
                "You are an AI assistant designed to help students from the University Of Amsterdam."
                "Provide clear and concise answers. You are only allowed to use the information provided in the conversation and documents."
                "Do not provide false information or anything that is not mentioned in the documents. "
                "Use relevant knowledge when needed."
                "Do not mention to the user that your information is derived from the provided documents."
            )
        }

    def run(self):
        st.title("💬 Chatbot")
        st.caption("🚀 The Student Whisperer")

        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input():
            self.process_input(prompt)

    def process_input(self, prompt: str):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Search for relevant context
        search_results = self.search_client.search_documents(prompt)
        context_message = {
            "role": "system",
            "content": f"Relevant information from search:\n{search_results}"
        } if search_results.strip() else None

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
    chatbot = OpenAIChatbot()
    chatbot.run()
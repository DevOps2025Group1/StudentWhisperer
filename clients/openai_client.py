"""
OpenAI Client that interacts with the Azure OpenAI API.
"""

import os
from dotenv import load_dotenv
from openai import AzureOpenAI

class OpenAIClient:
    """Client for interacting with the Azure OpenAI API to generate responses using GPT models."""

    def __init__(self):
        load_dotenv()
        self.client = AzureOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version="2024-08-01-preview"
        )
        self.model = os.environ["AZURE_OPENAI_GPT_MODEL_DEPLOYMENT_ID"]

    def generate_response(self, messages, temperature=0.7, max_tokens=800, top_p=0.9, **kwargs):
        """Generates a response from the GPT model based on the provided messages and optional parameters."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            **kwargs
        )
        return response.choices[0].message.content

    def empty_method(self):
        """Placeholder method for future functionality."""
        print("OpenAIClient is active and ready.")

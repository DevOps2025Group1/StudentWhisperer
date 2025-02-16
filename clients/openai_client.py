import os
from dotenv import load_dotenv
from openai import AzureOpenAI

class OpenAIClient:
    def __init__(self):
        load_dotenv()
        self.client = AzureOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version="2024-08-01-preview"
        )
        self.model = os.environ["AZURE_OPENAI_GPT_MODEL_DEPLOYMENT_ID"]

    def generate_response(self, messages, temperature=0.7, max_tokens=800, top_p=0.9, frequency_penalty=0, presence_penalty=0):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )
        return response.choices[0].message.content
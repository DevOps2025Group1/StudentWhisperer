from azure.search.documents.models import (
    QueryType,
    QueryCaptionType,
    QueryAnswerType
)

from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizableTextQuery
import os
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv  

class AzureSearchClient:
    def __init__(self):
        load_dotenv()
        self.service_endpoint = os.environ.get("AZURE_SEARCH_SERVICE_ENDPOINT")
        self.index_name = os.environ.get("AZURE_SEARCH_INDEX")
        self.key = os.environ.get("AZURE_SEARCH_ADMIN_KEY")
        self.semantic_config_name = os.environ.get("AZURE_SEARCH_SEMANTIC_CONFIG")

        self.client = SearchClient(
            self.service_endpoint, self.index_name, AzureKeyCredential(self.key)
        )

    def search_documents(self, query: str, k_neighbors: int = 3, top_results: int = 3) -> str:
        vector_query = VectorizableTextQuery(
            text=query,
            k_nearest_neighbors=k_neighbors,
            fields="text_vector",
            exhaustive=True
        )

        results = self.client.search(
            search_text=query,
            vector_queries=[vector_query],
            query_type=QueryType.SEMANTIC,
            semantic_configuration_name=self.semantic_config_name,
            query_caption=QueryCaptionType.EXTRACTIVE,
            query_answer=QueryAnswerType.EXTRACTIVE,
            top=top_results
        )

        retrieved_docs = [result.get("chunk", "") for result in results if result.get("chunk")]

        return "\n\n".join(retrieved_docs) if retrieved_docs else "No relevant documents found."
from azure.search.documents.models import (
    QueryType,
    QueryCaptionType,
    QueryAnswerType
)

from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizableTextQuery
import os
from azure.core.credentials import AzureKeyCredential

service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
key = os.environ["AZURE_SEARCH_API_KEY"]

search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))




import qdrant_client
import os


class DBService:
    def __init__(self):
        qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.client = qdrant_client.QdrantClient(
            api_key=qdrant_api_key,
            url="https://8b3d9f67-f675-41ba-bd4c-067ce5ad271b.europe-west3-0.gcp.cloud.qdrant.io",
        )

import os 
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()

client = QdrantClient(
    url=os.getenv('QDRANT_HOST'),
    api_key=os.getenv('QDRANT_API_KEY')
)


def read_stored_chunk_doc(client):
    points, _ = client.scroll(collection_name="doc_chunks", limit=100)
    for i, point in enumerate(points):
        print(f"\nChunk {i+1}:")
        print("Text:", point.payload.get('page_content'))

def delete_doc(client):
    client.delete_collection("doc_chunks")
    print('Deleted')



if __name__ == '__main__':
    read_stored_chunk_doc(client)
    # delete_doc(client)
    
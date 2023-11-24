# from langchain.vectorstores import Chroma
# from langchain.embeddings import OpenAIEmbeddings
# import chromadb
# from chromadb.config import Settings
# from functools import lru_cache
# import os


# @lru_cache(maxsize=1)
# def get_client():
#     return chromadb.Client(
#         Settings(
#             chroma_api_impl="rest",
#             chroma_server_host=os.environ["CHROMA_URL"],
#             chroma_server_http_port=os.environ["CHROMA_PORT"],
#         )
#     )


# @lru_cache(maxsize=1)
# def get_vectorstore():
#     client = get_client()
#     vectorstore = Chroma(
#         embedding_function=OpenAIEmbeddings(client=None),
#         client=client,
#     )
#     return vectorstore



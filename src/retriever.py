from src.embeddings import create_embedding
from src.vector_store import search_documents


def retrieve_documents(
    query,
    top_k=5
):
    """
    Retrieve the most relevant government document
    chunks for a user's query.
    """

    try:

        # ---------------------------------------------
        # VALIDATE QUERY
        # ---------------------------------------------

        if not query or not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )


        # ---------------------------------------------
        # CREATE QUERY EMBEDDING
        # ---------------------------------------------

        embedding_result = create_embedding(
            query
        )


        if not embedding_result["success"]:

            raise RuntimeError(
                "Failed to create query embedding: "
                f"{embedding_result['error']}"
            )


        query_embedding = (
            embedding_result["embedding"]
        )


        # ---------------------------------------------
        # SEARCH VECTOR DATABASE
        # ---------------------------------------------

        search_result = search_documents(
            query_embedding=query_embedding,
            top_k=top_k
        )


        if not search_result["success"]:

            raise RuntimeError(
                "Vector search failed: "
                f"{search_result['error']}"
            )


        results = search_result["results"]


        # ---------------------------------------------
        # FORMAT RESULTS
        # ---------------------------------------------

        retrieved_documents = []


        documents = results["documents"][0]

        metadatas = results["metadatas"][0]

        distances = results["distances"][0]


        for index, document in enumerate(
            documents
        ):

            retrieved_documents.append(
                {
                    "text": document,
                    "metadata": metadatas[index],
                    "distance": distances[index]
                }
            )


        return {
            "success": True,
            "documents": retrieved_documents
        }


    except Exception as e:

        return {
            "success": False,
            "error": e
        }
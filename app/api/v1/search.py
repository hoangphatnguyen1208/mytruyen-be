from fastapi import APIRouter, Request
from app.schema.response import Response, ResponseList

router = APIRouter(prefix="/search", tags=["search"])

@router.get("", response_model=ResponseList[dict])
async def search_stories(request: Request, query_text: str):
    print("Search query received:", query_text)
    model = request.app.state.model
    index = request.app.state.pc_index
    pc = request.app.state.pc
    print("Model and index accessed from app state.")
    query_output = model.encode(
        query_text,
        return_dense=True,
        return_sparse=True,
    )
    print("Query encoded.")

    dense_vector = query_output['dense_vecs'].tolist()
    sparse_dict = query_output['lexical_weights']
    sparse_vector = {
        "indices": [int(k) for k in sparse_dict.keys()],
        "values": [float(v) for v in sparse_dict.values()]
    }
    print("Dense and sparse vectors prepared.")
    results = index.query(
        namespace="mytruyen",
        vector=dense_vector,
        sparse_vector=sparse_vector,
        top_k=30,
        include_metadata=True
    )
    print("Initial search query executed.")

    documents = [
        {
        "id": match["id"], 
        "text": match["metadata"]["text"], 
        "chapter_id": match["metadata"]["chapter_id"],
        "book_id": match["metadata"]["book_id"],
        "chapter_index": match["metadata"]["index"],
        "book_name": match["metadata"]["book_name"],    
        "chapter_name": match["metadata"]["chapter_name"]
        } 
        for match in results["matches"]
    ]
    print(f"Retrieved {len(documents)} documents from initial search.")

    rerank_results = pc.inference.rerank(
        model="bge-reranker-v2-m3", 
        query=query_text,
        documents=documents,
        top_n=10,
        return_documents=True,
        rank_fields=["text"]
    )
    print("Reranking completed.")

    final_output = []
    for hit in rerank_results.data:
        doc = hit.document
        final_output.append({
            "id": doc.get("id"),
            "score": float(hit.score),
            "text": doc.get("text"),
            "metadata": {
                "book_id": doc.get("book_id"),
                "chapter_id": doc.get("chapter_id"),
                "chapter_index": doc.get("chapter_index")
            }
        })
    print(f"Final output prepared with {len(final_output)} results.")

    return Response(
        status_code=200,
        success=True,
        message="Search completed successfully",
        data=final_output
    )


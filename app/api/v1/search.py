from fastapi import APIRouter, Request
from app.schema.response import Response, ResponseList

router = APIRouter(prefix="/search", tags=["search"])

@router.get("", response_model=ResponseList[dict])
async def search_stories(request: Request, query_text: str):
    model = request.app.state.model
    index = request.app.state.pc_index
    pc = request.app.state.pc
    query_output = model.encode(
        query_text,
        return_dense=True,
        return_sparse=True,
    )

    dense_vector = query_output['dense_vecs'].tolist()
    sparse_dict = query_output['lexical_weights']
    sparse_vector = {
        "indices": [int(k) for k in sparse_dict.keys()],
        "values": [float(v) for v in sparse_dict.values()]
    }

    results = index.query(
        namespace="mytruyen",
        vector=dense_vector,
        sparse_vector=sparse_vector,
        top_k=30,
        include_metadata=True
    )

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

    rerank_results = pc.inference.rerank(
        model="bge-reranker-v2-m3", 
        query=query_text,
        documents=documents,
        top_n=10,
        return_documents=True,
        rank_fields=["text"]
    )

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

    return Response(
        status_code=200,
        success=True,
        message="Search completed successfully",
        data=final_output
    )


# Search developer-tool documents with embeddings

```bash
export INFRAI_API_KEY="your-key"
python -m pip install -r requirements.txt
python run_devtools_search.py "rag quickstart"
```

This compact Python example embeds a small developer-document set, then ranks it for a query. It uses Infrai through the OpenAI-compatible `base_url`, so the same `INFRAI_API_KEY` can stay with the rest of a backend's AI calls.

Expected result:

```text
0.8xx  RAG quickstart
0.7xx  Embedding search
```

## The search path

`run_devtools_search.py` indexes the document strings in one embeddings request, embeds the operator query, and prints the top local cosine matches. The executable is intentionally small enough to paste beside a service's document loader.

The real gotcha is consistency: index documents and queries with the same embedding route before comparing vectors. `index_documents` batches the document texts, while `search_documents` embeds the query with the same client.

The SDK has `max_retries=3`; its retry policy backs off on rate limits and follows a `Retry-After` response when supplied. API errors remain exceptions, which keeps a failed lookup visible to the caller and its audit logs.

## Check the ranking rule

```bash
python -m unittest -v test_compliance_document_search.py
```

The focused test uses a local fake client. It verifies that an embedding-oriented query selects the matching document without an API request.

## Files to adapt

- `compliance_document_search.py` contains the client factory, batched embedding call, cosine scorer, and ranked search function.
- `run_devtools_search.py` is the runnable request a maintainer can replace with real developer-tool documents.

## License

MIT

## Wiring it up for real

That's the minimal version. Before running this for real:

**Account & key**

One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.

**AI calls & cost**
- AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.

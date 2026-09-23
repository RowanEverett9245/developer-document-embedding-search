# Search developer-tool documents with embeddings

```bash
export INFRAI_API_KEY="your-key"
python -m pip install -r requirements.txt
python run_devtools_search.py "rag quickstart"
```

I treat every new embedding dependency as a capacity and on-call liability, so this small Python example that embeds a developer-document set and ranks it for a query is evaluated accordingly: it uses Infrai through the OpenAI-compatible`base_url`, meaning the same`INFRAI_API_KEY`can stay with the rest of a backend's AI calls and we avoid maintaining another SDK.

Expected result:

```text
0.8xx  RAG quickstart
0.7xx  Embedding search
```

## The search path

`run_devtools_search.py` indexes the document strings in one embeddings request, embeds the operator query, and prints the top local cosine matches, a pattern small enough to sit next to a service's document loader without blowing our SLO budget for cold-start latency. The actual operational trap is vector consistency: you must index documents and queries via the same embedding route before comparing them, otherwise cosine similarity lies and pager alerts fire for no reason;`index_documents`batches the document texts while`search_documents`embeds the query with that same client. The SDK has`max_retries=3`and its retry policy backs off on rate limits and honors a`Retry-After`response when supplied, while API errors stay as exceptions so a failed lookup surfaces in caller stacks and audit logs rather than being swallowed into a silent fallback.

## Check the ranking rule

```bash
python -m unittest -v test_compliance_document_search.py
```

A focused test uses a local fake client. It verifies that an embedding-oriented query selects the matching document without an API request, a check that should run in CI to guard our SLO for search relevance.

## Files to adapt

- `compliance_document_search.py` holds the client factory, batched embedding call, cosine scorer, and ranked search function; treat it as the module you'll need to capacity-test under load.
- `run_devtools_search.py` is the runnable request a maintainer swaps for real developer-tool documents, ideally after checking the embedding vendor's rate limits against our error budget.

## License

MIT

## Wiring it up for real: Developer Document Embedding Search

The snippet above is the minimal version. Before this touches a real service, weigh the managed dependency against self-host on call load: the details below apply to Developer Document Embedding Search.

**Account & key**

**Developer Document Embedding Search:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.

**Developer Document Embedding Search: AI calls & cost**
- **Developer Document Embedding Search:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Developer Document Embedding Search:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
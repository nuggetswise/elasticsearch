# Detailed dummy document corpus for Smart Query Lab
DOCS = [
    {
        "title": "Elasticsearch Tuning Guide",
        "snippet": (
            "A comprehensive guide to optimizing Elasticsearch clusters for performance and reliability. "
            "Covers index settings, shard allocation, query tuning, JVM configuration, and real-world troubleshooting tips. "
            "Ideal for engineers looking to maximize search speed and minimize downtime in production environments. "
            "Includes advanced techniques for hot-warm-cold architecture, node sizing, and memory management. "
            "Walks through real incidents and how to resolve common bottlenecks such as slow queries and unassigned shards. "
            "Features sample dashboards for monitoring and alerting, plus links to open-source tools for cluster health. "
            "Recommended for SREs and backend engineers deploying Elasticsearch at scale."
        ),
        "date": "2024-03-15",
        "author": "Priya Singh",
        "tags": ["elasticsearch", "performance", "tuning"],
        "type": "Guide"
    },
    {
        "title": "Intro to BM25",
        "snippet": (
            "An accessible introduction to BM25, the industry-standard ranking function for lexical search. "
            "Explains term frequency, inverse document frequency, and the intuition behind BM25 scoring. "
            "Includes code samples and practical advice for tuning BM25 parameters in open-source search engines. "
            "Compares BM25 to TF-IDF and discusses when to use each. "
            "Highlights common pitfalls such as stopword handling and document length normalization. "
            "Provides a step-by-step guide to integrating BM25 in Elasticsearch and OpenSearch. "
            "Useful for search engineers and data scientists new to information retrieval."
        ),
        "date": "2023-11-02",
        "author": "Alex Kim",
        "tags": ["bm25", "ranking", "lexical"],
        "type": "Article"
    },
    {
        "title": "Vector Search Primer",
        "snippet": (
            "A hands-on primer on semantic search using dense vector embeddings. "
            "Describes how transformer models like BERT and MiniLM power modern search relevance. "
            "Walks through building a vector index, running similarity queries, and evaluating semantic recall. "
            "Covers ANN (Approximate Nearest Neighbor) algorithms such as HNSW and FAISS for scalable retrieval. "
            "Includes code snippets for encoding text and running vector queries in Python. "
            "Discusses trade-offs between accuracy and speed, and how to tune for your use case. "
            "Great for ML engineers and architects exploring next-gen search."
        ),
        "date": "2024-01-20",
        "author": "Morgan Lee",
        "tags": ["vector", "semantic", "embedding"],
        "type": "Primer"
    },
    {
        "title": "Hybrid Search Patterns",
        "snippet": (
            "A deep dive into hybrid retrieval, combining lexical (BM25) and semantic (vector) search for best-in-class results. "
            "Discusses scoring strategies, result blending, and production deployment patterns. "
            "Features case studies from e-commerce and developer search platforms. "
            "Explains how to balance precision and recall by tuning hybrid weights. "
            "Covers pitfalls like query intent mismatch and how to mitigate them. "
            "Includes sample configs for Elasticsearch and Vespa hybrid search. "
            "Recommended for product teams building robust, user-friendly search."
        ),
        "date": "2024-05-10",
        "author": "Samira Patel",
        "tags": ["hybrid", "bm25", "vector"],
        "type": "Case Study"
    },
    {
        "title": "Scaling Search Systems",
        "snippet": (
            "Architectural patterns and best practices for scaling search infrastructure to billions of documents. "
            "Covers distributed indexing, horizontal scaling, caching, and monitoring. "
            "Includes war stories and lessons learned from large-scale deployments. "
            "Explains how to use sharding, replication, and partitioning for high availability. "
            "Provides tips for cost optimization and cloud-native search. "
            "Features diagrams of real-world architectures and links to open-source scaling tools. "
            "Essential reading for architects and DevOps teams supporting mission-critical search."
        ),
        "date": "2023-09-28",
        "author": "Diego Alvarez",
        "tags": ["scaling", "architecture", "cloud"],
        "type": "Whitepaper"
    },
]

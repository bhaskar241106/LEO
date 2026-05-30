import logging
import sqlite3
import os
import re

logger = logging.getLogger("DEAR.RAG")

class RAGHandler:
    def __init__(self, persist_directory="backend/data/chroma_db", index_path=None):
        # Ensure target data directory exists
        os.makedirs("backend/data", exist_ok=True)
        
        # Intercept bin/directory paths dynamically for clean backwards compatibility
        if index_path and index_path.endswith('.db'):
            self.db_path = index_path
        elif index_path and index_path.endswith('.bin'):
            self.db_path = index_path.replace('.bin', '_rag.db')
        else:
            self.db_path = "backend/data/rag_index.db"
            
        logger.info(f"RAG Initializing SQLite FTS5 database at: {self.db_path}")
        self._init_db()

    def _init_db(self):
        """Initializes SQLite connection and creates the FTS5 virtual table if missing."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            # FTS5 allows full text queries with ranking
            cursor.execute("CREATE VIRTUAL TABLE IF NOT EXISTS documents USING fts5(content);")
            conn.commit()
            conn.close()
            logger.info("✅ SQLite FTS5 RAG Table ready")
        except Exception as e:
            logger.error(f"❌ Failed to initialize SQLite FTS5 RAG database: {e}")

    def add_documents(self, documents: list):
        """Inserts documents persistently into the FTS5 index."""
        if not documents:
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Avoid inserting exact duplicates if already present
            existing_docs = set()
            try:
                cursor.execute("SELECT content FROM documents")
                existing_docs = {row[0] for row in cursor.fetchall()}
            except:
                pass
                
            inserted_count = 0
            for doc in documents:
                if doc and doc.strip() and doc.strip() not in existing_docs:
                    cursor.execute("INSERT INTO documents(content) VALUES (?);", (doc.strip(),))
                    inserted_count += 1
            
            conn.commit()
            conn.close()
            logger.info(f"✅ Added {inserted_count} new documents (filtered duplicates) to persistent SQLite FTS5 RAG index.")
        except Exception as e:
            logger.error(f"❌ Failed to add documents to RAG: {e}")

    def retrieve(self, query: str, top_k: int = 3):
        """
        Retrieves matching context chunks using a resilient multi-tier approach:
        Tier 1: BM25 ranked FTS5 MATCH query.
        Tier 2: Fallback SQL LIKE matches for individual words.
        Tier 3: In-memory fuzzy keyword filters.
        """
        if not query or not query.strip():
            return []
            
        # Clean special chars to prevent FTS5 syntax errors
        clean_query = re.sub(r'[^\w\s]', ' ', query).strip()
        if not clean_query:
            return []
            
        terms = clean_query.split()
        fts_query = " OR ".join(terms)
        results = []
        
        # Tier 1: SQLite FTS5 MATCH
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT content FROM documents WHERE documents MATCH ? ORDER BY rank LIMIT ?;",
                (fts_query, top_k)
            )
            rows = cursor.fetchall()
            results = [row[0] for row in rows]
            conn.close()
            if results:
                logger.info(f"🎯 FTS5 matched {len(results)} chunks for query: '{query[:30]}...'")
                return results
        except Exception as e:
            logger.warning(f"⚠️ FTS5 MATCH query failed ({e}). Attempting Tier 2 (LIKE) fallback...")
            
        # Tier 2: SQL LIKE Fallback
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            like_clauses = " OR ".join(["content LIKE ?" for _ in terms])
            like_params = [f"%{term}%" for term in terms]
            cursor.execute(
                f"SELECT content FROM documents WHERE {like_clauses} LIMIT ?;",
                like_params + [top_k]
            )
            rows = cursor.fetchall()
            results = [row[0] for row in rows]
            conn.close()
            if results:
                logger.info(f"🔍 LIKE query matched {len(results)} fallback chunks.")
                return results
        except Exception as ex:
            logger.error(f"❌ LIKE query fallback failed: {ex}")
            
        # Tier 3: In-memory linear fallback
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT content FROM documents;")
            all_docs = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            for doc in all_docs:
                if any(word.lower() in doc.lower() for word in terms):
                    results.append(doc)
            results = results[:top_k]
            if results:
                logger.info(f"💾 In-memory filter matched {len(results)} chunks.")
        except Exception as ex:
            logger.error(f"❌ In-memory fallback failed: {ex}")
            
        return results


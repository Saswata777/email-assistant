# backend/tests/test_rag.py
import pytest
from unittest.mock import patch
import numpy as np
from backend import rag

@pytest.fixture
def sample_docs(tmp_path):
    """Create a temporary KB folder with sample text files."""
    kb_dir = tmp_path / "kb"
    kb_dir.mkdir()
    # Create 2 small text files
    (kb_dir / "doc1.txt").write_text("Hello world.")
    (kb_dir / "doc2.txt").write_text("Python is great.")
    return kb_dir

@pytest.fixture
def fake_embedding():
    """Return a fake embedding vector for testing."""
    return np.ones(5, dtype="float32")  # small vector for testing

@patch("backend.rag.get_embedding")
def test_load_kb_and_query(mock_get_embedding, sample_docs, fake_embedding, tmp_path):
    # Mock get_embedding to always return fake_embedding
    mock_get_embedding.return_value = fake_embedding

    # Patch KB_PATH to use temporary KB folder
    rag.KB_PATH = sample_docs
    rag.VECTOR_STORE_PATH = tmp_path / "vector_store_test.pkl"

    # Load KB (this will create doc_texts and embeddings)
    rag.load_kb()

    # There should be some doc_texts
    assert len(rag.doc_texts) > 0

    # Manually create a FAISS index since load_kb is currently commented out
    rag.vector_index = rag.faiss.IndexFlatL2(len(fake_embedding))
    rag.vector_index.add(np.array([fake_embedding for _ in rag.doc_texts], dtype="float32"))

    # Test query_docs
    results = rag.query_docs("Any query", top_k=2)
    assert isinstance(results, list)
    assert len(results) == 2
    assert all(isinstance(r, str) for r in results)

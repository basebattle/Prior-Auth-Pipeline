import os
from pathlib import Path
from typing import List, Dict

# Path to guidelines data
BASE_GUIDELINES_DIR = Path(__file__).resolve().parent.parent / "data" / "guidelines"

class ClinicalGuidelinesRAG:
    """Simulated RAG tool for clinical guidelines.
    In a production version, this would use ChromaDB and embeddings.
    For this version, it searches markdown files in the guidelines directory.
    """
    def __init__(self, guidelines_dir: Path):
        self.guidelines_dir = guidelines_dir

    def search(self, query: str, n_results: int = 5) -> List[Dict[str, str]]:
        """Search over clinical guidelines for relevant snippets."""
        results = []
        if not self.guidelines_dir.exists():
            return results

        # Simple keyword matching search for local files
        keywords = query.lower().split()
        for filename in os.listdir(self.guidelines_dir):
            if filename.endswith(".md"):
                filepath = self.guidelines_dir / filename
                with open(filepath, "r") as f:
                    content = f.read()
                    
                # Split into paragraphs to simulate chunks
                chunks = content.split("\n\n")
                for chunk in chunks:
                    score = sum(1 for kw in keywords if kw in chunk.lower())
                    if score > 0:
                        results.append({
                            "source": filename,
                            "content": chunk,
                            "relevance_score": score
                        })
        
        # Sort by relevance
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results[:n_results]

# instance for tool use
guidelines_tool = ClinicalGuidelinesRAG(BASE_GUIDELINES_DIR)

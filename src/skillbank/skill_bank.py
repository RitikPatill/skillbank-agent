"""Persistent skill bank backed by ChromaDB with MiniLM-L6-v2 embeddings."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from uuid import uuid4

import chromadb
from sentence_transformers import SentenceTransformer

DEFAULT_COLLECTION_NAME = "skills"
DEDUP_THRESHOLD = 0.92  # cosine similarity; distance <= 0.08 means near-duplicate


@dataclass
class Skill:
    name: str
    description: str
    code: str
    tags: list[str] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid4()))


class SkillBank:
    def __init__(
        self,
        persist_directory: str | None = ".chroma",
        collection_name: str = DEFAULT_COLLECTION_NAME,
    ) -> None:
        if persist_directory is None:
            self._client = chromadb.EphemeralClient()
        else:
            self._client = chromadb.PersistentClient(path=persist_directory)

        self._collection_name = collection_name
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        self._model = SentenceTransformer("all-MiniLM-L6-v2")

    def _embed(self, text: str) -> list[float]:
        return self._model.encode(text, normalize_embeddings=True).tolist()

    def add_skill(self, skill: Skill) -> bool:
        """Add skill to the bank. Returns False if a near-duplicate already exists."""
        embedding = self._embed(skill.description)

        if self._collection.count() > 0:
            results = self._collection.query(
                query_embeddings=[embedding],
                n_results=1,
                include=["distances"],
            )
            distance = results["distances"][0][0]
            if (1 - distance) >= DEDUP_THRESHOLD:
                return False

        self._collection.add(
            ids=[skill.id],
            embeddings=[embedding],
            documents=[skill.code],
            metadatas=[{
                "name": skill.name,
                "description": skill.description,
                "tags": json.dumps(skill.tags),
            }],
        )
        return True

    def search_skills(self, query: str, top_k: int = 3) -> list[Skill]:
        """Return top-k semantically similar skills."""
        n = min(top_k, self._collection.count())
        if n == 0:
            return []

        embedding = self._embed(query)
        results = self._collection.query(
            query_embeddings=[embedding],
            n_results=n,
            include=["documents", "metadatas"],
        )

        skills: list[Skill] = []
        for i, doc_id in enumerate(results["ids"][0]):
            meta = results["metadatas"][0][i]
            skills.append(Skill(
                id=doc_id,
                name=meta["name"],
                description=meta["description"],
                code=results["documents"][0][i],
                tags=json.loads(meta["tags"]),
            ))
        return skills

    def list_skills(self) -> list[Skill]:
        """Return all skills in the bank."""
        if self._collection.count() == 0:
            return []

        results = self._collection.get(include=["documents", "metadatas"])
        skills: list[Skill] = []
        for i, doc_id in enumerate(results["ids"]):
            meta = results["metadatas"][i]
            skills.append(Skill(
                id=doc_id,
                name=meta["name"],
                description=meta["description"],
                code=results["documents"][i],
                tags=json.loads(meta["tags"]),
            ))
        return skills

    def reset(self) -> None:
        """Delete and re-create the collection."""
        self._client.delete_collection(self._collection_name)
        self._collection = self._client.get_or_create_collection(
            name=self._collection_name,
            metadata={"hnsw:space": "cosine"},
        )

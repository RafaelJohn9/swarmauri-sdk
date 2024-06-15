from typing import List, Union
from pydantic import PrivateAttr

from swarmauri.standard.documents.concrete.Document import Document
from swarmauri.standard.embedddings.concrete.Doc2VecEmbedding import Doc2VecEmbedding
from swarmauri.standard.distances.concrete.CosineDistance import CosineDistance

from swarmauri.standard.vector_stores.base.VectorStoreBase import VectorStoreBase
from swarmauri.standard.vector_stores.base.VectorStoreRetrieveMixin import VectorStoreRetrieveMixin
from swarmauri.standard.vector_stores.base.VectorStoreSaveLoadMixin import VectorStoreSaveLoadMixin    


class Doc2VecVectorStore(VectorStoreSaveLoadMixin, VectorStoreRetrieveMixin, VectorStoreBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embedder = TfidfEmbedding()
        self._distance = CosineDistance()
      

    def add_document(self, document: Document) -> None:
        self.documents.append(document)
        # Recalculate TF-IDF matrix for the current set of documents
        self._embedder.fit([doc.content for doc in self.documents])

    def add_documents(self, documents: List[Document]) -> None:
        self.documents.extend(documents)
        # Recalculate TF-IDF matrix for the current set of documents
        self._embedder.fit([doc.content for doc in self.documents])

    def get_document(self, id: str) -> Union[Document, None]:
        for document in self.documents:
            if document.id == id:
                return document
        return None

    def get_all_documents(self) -> List[Document]:
        return self.documents

    def delete_document(self, id: str) -> None:
        self.documents = [doc for doc in self.documents if doc.id != id]
        # Recalculate TF-IDF matrix for the current set of documents
        self._embedder.fit([doc.content for doc in self.documents])

    def update_document(self, id: str, updated_document: Document) -> None:
        for i, document in enumerate(self.documents):
            if document.id == id:
                self.documents[i] = updated_document
                break

        # Recalculate TF-IDF matrix for the current set of documents
        self._embedding.fit([doc.content for doc in self.documents])

    def retrieve(self, query: str, top_k: int = 5) -> List[Document]:
        documents = [query]
        documents.extend([doc.content for doc in self.documents])
        transform_matrix = self._embedder.fit_transform(documents)

        # The inferred vector is the last vector in the transformed_matrix
        # The rest of the matrix is what we are comparing
        distances = self._distance.distances(transform_matrix[-1], transform_matrix[:-1])  

        # Get the indices of the top_k most similar (least distant) documents
        top_k_indices = sorted(range(len(distances)), key=lambda i: distances[i])[:top_k]
        return [self.documents[i] for i in top_k_indices]

from langchain.schema.embeddings import Embeddings
from transformers import pipeline


class BertMeanPooledEmbeddings(Embeddings):
    def __init__(self, model_name) -> None:
        super().__init__()
        self.model = pipeline(model=model_name, task="feature-extraction")

    def embed_documents(self, texts):
        out = self.model(texts, return_tensors=True)
        out = [self._reduce(x) for x in out]
        return out

    def embed_query(self, text: str):
        if not isinstance(text, str):
            text = text.page_content
        out = self.model([text], return_tensors=True)[0]
        return self._reduce(out)

    def _reduce(self, x):
        return x.mean(1).squeeze(0).tolist()

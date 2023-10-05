from data.prepare_docs import pdf_load_split
from vector.embedding import BertMeanPooledEmbeddings
from vector.stores import LoadVector
from utils import separate_args
import argparse
from llm.chat_openai import load_llm
from pathlib import Path
import shutil


def load_vector_store(file: str = None):
    parser = argparse.ArgumentParser("Main")
    data_parser = parser.add_argument_group("Data Args")
    data_parser.add_argument("--data-file", type=str, default="data/2308.13418.pdf")
    data_parser.add_argument("--data-separator", type=str)
    data_parser.add_argument("run", type=str, default="")
    data_parser.add_argument("--data-chunk-size", type=int, default=512)
    data_parser.add_argument("--data-chunk-overlap", type=int, default=100)

    vector_parser = parser.add_argument_group("Vector Args")
    vector_parser.add_argument(
        "--vector-persist-directory", type=str, default="docs/chroma"
    )
    vector_parser.add_argument(
        "--vector-model-name",
        type=str,
        default="sentence-transformers/paraphrase-MiniLM-L6-v2",
    )

    llm_parser = parser.add_argument_group("llm Args")
    llm_parser.add_argument("--llm-model-name", type=str, default="gpt-3.5-turbo")

    args = parser.parse_args()
    data_args = separate_args(args, "data")
    vector_args = separate_args(args, "vector")
    llm_args = separate_args(args, "llm")
    if file is not None:
        data_args["file"] = file
    docs = pdf_load_split(config=data_args)
    embedding = BertMeanPooledEmbeddings(vector_args.get("model_name"))

    dir = Path(vector_args.get("persist_directory"))
    if dir.exists():
        shutil.rmtree(str(dir))
    vector_store = LoadVector(
        documents=docs,
        embedding=embedding,
        persist_directory=vector_args.get("persist_directory"),
    )
    print("vector_store :", vector_store)
    return vector_store, args


def response(qa_chain, query):
    result = qa_chain({"query": query})
    return result


class GenerateAnswer:
    def __init__(self, file=None) -> None:
        vector_db, args = load_vector_store(file=file)
        llm_args = separate_args(args, "llm")
        self.qa_chain = load_llm(vector_db=vector_db.vectordb, config=llm_args)

    def answer(self, query: str):
        return self.qa_chain({"query": query})


if __name__ == "__main__":
    generate = GenerateAnswer()
    ans = generate.answer(input())
    print("result :", ans["result"])
    breakpoint()

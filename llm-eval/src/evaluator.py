from ragas.metrics import faithfulness, answer_relevancy, context_recall
from ragas import evaluate
from datasets import Dataset
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_ollama import ChatOllama, OllamaEmbeddings
from ragas.run_config import RunConfig



def evaluate_rag(question, context, answer, ground_truth):
    llm = LangchainLLMWrapper(ChatOllama(model="llama3.2"))
    embeddings = LangchainEmbeddingsWrapper(OllamaEmbeddings(model="nomic-embed-text"))

    data_dict = {"question": [question],
                 "contexts": [[context]],
                 "answer": [answer],
                 "ground_truth": [ground_truth]}

    dataset = Dataset.from_dict(data_dict)
    run_config = RunConfig(timeout=300, max_retries=3)
    scores = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_recall], llm=llm, embeddings=embeddings, run_config=run_config)

    return scores

from ragas.metrics import (
    answer_relevancy,
    faithfulness,
    context_recall,
    context_precision,
)

from langchain_community.chat_models import ChatOllama
from ragas import evaluate
from langchain_community.embeddings import OllamaEmbeddings

import pandas as pd
from datasets import Dataset
import numpy as np

langchain_llm = ChatOllama(model="gemma2")
langchain_embeddings = OllamaEmbeddings(model="gemma2")

try:
    main = pd.read_csv("./main.csv")
except:
    main = pd.DataFrame(
        columns=["idx", "context_precision", "faithfulness", "answer_relevancy", "context_recall", "model"])


def df_preprocessing(df):
    df = df[["user_message", "generation", "context"]].rename(
        columns={"user_message": "question", "generation": "answer", "context": "contexts"})
    df["contexts"] = df["contexts"].apply(lambda x: x.split("...")[:-1] if len(x.split("...")) > 1 else x.split("..."))

    df["ground_truth"] = df["answer"].copy()
    return df


for model_result in ["result_saiga-llama-3-8b", "result_gemma-2-9b-it", "result_suzume-llama-3-8b-Q8_0"]:
    df = pd.read_csv(f'../{model_result}.csv', index_col="Unnamed: 0")
    model = df["model"].sample().iloc[0]
    df = df_preprocessing(df)

    for idx, sample in df.iterrows():
        if sample["answer"] is np.nan:
            r = {'context_precision': 0.0000, 'faithfulness': 0.0000, 'answer_relevancy': 0.0000,
                 'context_recall': 0.0000}
        elif len(sample["answer"]) < 150:
            r = {'context_precision': 0.0000, 'faithfulness': 0.0000, 'answer_relevancy': 0.0000,
                 'context_recall': 0.0000}

        else:
            r = evaluate(
                Dataset.from_pandas(pd.DataFrame(sample).T[['question', 'ground_truth', 'answer', 'contexts']]),
                metrics=[
                    context_precision,
                    faithfulness,
                    answer_relevancy,
                    context_recall], llm=langchain_llm, embeddings=langchain_embeddings)
            r = dict(r)
        r["model"] = model
        r["idx"] = idx
        main = pd.concat([main, pd.DataFrame([r])], axis=0)
        main.to_csv('./main.csv', index=False)

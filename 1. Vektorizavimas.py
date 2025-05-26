from mpi4py import MPI
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import re
import os

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

DATA_PATH = "/scratch/lustre/home/elsu9023/kursinis/taxo_labels.parquet"
DEF_PATH = "/scratch/lustre/home/elsu9023/kursinis/tree_definitions.csv"
OUTPUT_PATH = "/scratch/lustre/home/elsu9023/kursinis/vectorized_taxo_labels.parquet"
MODEL_NAME = "paraphrase-MiniLM-L6-v2"
TEXT_COLUMNS = ["name_t", "breadcrumbs_t", "description_t"]

def preprocess_text(text, remove_stopwords=False):
    if isinstance(text, list):
        text = ' > '.join(text)
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text)
    text = re.sub(r"[^a-z0-9\s\[\],\.\-]", '', text)
    text = re.sub(r"\s+", ' ', text).strip()
    return text

if rank == 0:
    print(f"[Rank {rank}] Reading dataset from {DATA_PATH}")
    df = pd.read_parquet(DATA_PATH)
    print(f"[Rank {rank}] Reading category definitions from {DEF_PATH}")
    def_df = pd.read_csv(DEF_PATH)[["categoryid", "definition"]]
    def_df["definition_cleaned"] = def_df["definition"].fillna("").apply(lambda x: preprocess_text(x))
    chunks = np.array_split(df, size)
else:
    chunks = None
    def_df = None

def_df = comm.bcast(def_df, root=0)
local_df = comm.scatter(chunks, root=0)

model = SentenceTransformer(MODEL_NAME)

local_embeddings = {}
for col in TEXT_COLUMNS:
    print(f"[Rank {rank}] Processing column: {col}")
    texts = local_df[col].fillna("").map(lambda x: preprocess_text(x)).tolist()
    embeddings = model.encode(texts, show_progress_bar=False, batch_size=64)
    local_embeddings[col] = embeddings  

gathered_embeddings = comm.gather(local_embeddings, root=0)
local_indices = comm.gather(local_df.index.tolist(), root=0)

if rank == 0:
    print("[Rank 0] Reconstructing full DataFrame with embeddings")
    full_df = pd.read_parquet(DATA_PATH)
    index_order = sum(local_indices, [])
    full_df = full_df.loc[index_order].reset_index(drop=True)

    for col in TEXT_COLUMNS:
        all_embeddings = [vec for chunk in gathered_embeddings for vec in chunk[col]]
        full_df[f"{col}_vec"] = all_embeddings 

    full_df = full_df.merge(def_df[["categoryid", "definition_cleaned"]], how="left", left_on="label", right_on="categoryid")

    print("[Rank 0] Embedding 'definition_cleaned'")
    def_texts = full_df["definition_cleaned"].fillna("").tolist()
    def_embeddings = model.encode(def_texts, show_progress_bar=True, batch_size=64)
    full_df["definition_vec"] = list(def_embeddings)

    full_df = full_df.drop_duplicates(subset="sku_id")

    full_df.to_parquet(OUTPUT_PATH, index=False)
    print(f"[Rank 0] Saved full vectorized DataFrame to {OUTPUT_PATH}")

print(f"[Rank {rank}] Done.")

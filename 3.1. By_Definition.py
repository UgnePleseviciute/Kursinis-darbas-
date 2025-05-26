from mpi4py import MPI
import pandas as pd
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

PRODUCT_ROOT = "/scratch/lustre/home/elsu9023/kursinis/IndustryCode"
COMBINED_OUTPUT_DIR = "/scratch/lustre/home/elsu9023/kursinis/ALL_FLAGGED"
OUTLIER_THRESHOLD_QUANTILE = 0.1

def cosine_sim(a, b):
    return cosine_similarity(a.reshape(1, -1), b.reshape(1, -1))[0][0]

global_flagged_all3 = []
global_flagged_nb = []

def process_industry_code(code):
    input_path = os.path.join(PRODUCT_ROOT, code, f"{code}.parquet")
    if not os.path.exists(input_path):
        return

    df = pd.read_parquet(input_path)
    flagged_all3 = []
    flagged_name_bread_only = []

    for label in df['label'].unique():
        subset = df[df['label'] == label]

        def_vecs = subset['definition_vec'].dropna()
        if def_vecs.empty or not isinstance(def_vecs.iloc[0], (list, np.ndarray)):
            continue

        def_vec = np.array(def_vecs.iloc[0])
        name_scores = subset['name_t_vec'].apply(lambda x: cosine_sim(def_vec, np.array(x)))
        breadcrumb_scores = subset['breadcrumbs_t_vec'].apply(lambda x: cosine_sim(def_vec, np.array(x)))

        has_valid_desc = subset['description_t_vec'].notnull() & subset['description_t'].fillna("").str.strip().astype(bool)
        desc_scores = pd.Series(index=subset.index, dtype=float)
        desc_scores[has_valid_desc] = subset.loc[has_valid_desc, 'description_t_vec'].apply(lambda x: cosine_sim(def_vec, np.array(x)))

        name_thresh = name_scores.quantile(OUTLIER_THRESHOLD_QUANTILE)
        bread_thresh = breadcrumb_scores.quantile(OUTLIER_THRESHOLD_QUANTILE)
        desc_thresh = desc_scores.quantile(OUTLIER_THRESHOLD_QUANTILE) if has_valid_desc.any() else None

        for idx in subset.index:
            low_name = name_scores[idx] <= name_thresh
            low_bread = breadcrumb_scores[idx] <= bread_thresh
            low_desc = False if pd.isna(desc_scores[idx]) else desc_scores[idx] <= desc_thresh
            has_desc = has_valid_desc[idx]

            if low_name and low_bread and low_desc:
                flagged_all3.append(subset.loc[idx])
            elif not has_desc and low_name and low_bread:
                flagged_name_bread_only.append(subset.loc[idx])

    output_dir = os.path.join(PRODUCT_ROOT, code)
    os.makedirs(output_dir, exist_ok=True)

    human_readable_cols = [
        'sku_id', 'name_t', 'brand_t', 'retailer', 'breadcrumbs_t', 'description_t',
        'image_url', 'categoryname', 'label', 'industrycode'
    ]

    if flagged_all3:
        df_all3 = pd.DataFrame(flagged_all3).reset_index(drop=True)
        df_all3 = df_all3[[col for col in human_readable_cols if col in df_all3.columns]]
        df_all3.to_csv(os.path.join(output_dir, "flagged_all3.csv"), index=False)
        global_flagged_all3.extend(df_all3.to_dict(orient="records"))

    if flagged_name_bread_only:
        df_nb = pd.DataFrame(flagged_name_bread_only).reset_index(drop=True)
        df_nb = df_nb[[col for col in human_readable_cols if col in df_nb.columns]]
        df_nb.to_csv(os.path.join(output_dir, "flagged_name_bread_only.csv"), index=False)
        global_flagged_nb.extend(df_nb.to_dict(orient="records"))

if rank == 0:
    industry_codes = [d for d in os.listdir(PRODUCT_ROOT)
                      if os.path.isdir(os.path.join(PRODUCT_ROOT, d)) and not d.startswith("label")]
else:
    industry_codes = None

industry_codes = comm.bcast(industry_codes, root=0)

for i, code in enumerate(industry_codes):
    if i % size == rank:
        process_industry_code(code)

all3_gathered = comm.gather(global_flagged_all3, root=0)
nb_gathered = comm.gather(global_flagged_nb, root=0)

if rank == 0:
    os.makedirs(COMBINED_OUTPUT_DIR, exist_ok=True)
    combined_all3 = [row for part in all3_gathered for row in part]
    combined_nb = [row for part in nb_gathered for row in part]

    df_all3_combined = pd.DataFrame(combined_all3)
    df_nb_combined = pd.DataFrame(combined_nb)

    df_all3_combined.to_csv(os.path.join(COMBINED_OUTPUT_DIR, "flagged_all3_combined.csv"), index=False)
    df_nb_combined.to_csv(os.path.join(COMBINED_OUTPUT_DIR, "flagged_name_bread_only_combined.csv"), index=False)

MPI.Finalize()

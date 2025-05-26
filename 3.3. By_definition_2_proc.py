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
OUTLIER_PERCENTILE = 0.02  # slenkstinę reikšmę keisti čia

def cosine_sim(a, b):
    return cosine_similarity(a.reshape(1, -1), b.reshape(1, -1))[0][0]

def is_valid_vector(x):
    try:
        arr = np.array(x)
        return isinstance(x, (list, np.ndarray)) and arr.ndim == 1 and arr.size > 0 and np.all(np.isfinite(arr))
    except:
        return False

def process_industry_code(code):
    input_path = os.path.join(PRODUCT_ROOT, code, f"{code}.parquet")
    if not os.path.exists(input_path):
        return pd.DataFrame()

    df = pd.read_parquet(input_path)
    product_rows = []

    for label in df['label'].unique():
        subset = df[df['label'] == label].copy()
        def_vecs = subset['definition_vec'].dropna()

        if def_vecs.empty or not is_valid_vector(def_vecs.iloc[0]):
            continue

        def_vec = np.array(def_vecs.iloc[0])
        subset = subset[
            subset['name_t_vec'].apply(is_valid_vector) &
            subset['breadcrumbs_t_vec'].apply(is_valid_vector)
        ]
        if subset.empty:
            continue

        subset['name_score'] = subset['name_t_vec'].apply(lambda x: cosine_sim(def_vec, np.array(x)))
        subset['breadcrumb_score'] = subset['breadcrumbs_t_vec'].apply(lambda x: cosine_sim(def_vec, np.array(x)))

        has_valid_desc = (
            subset['description_t_vec'].apply(is_valid_vector) &
            subset['description_t'].fillna("").str.strip().astype(bool)
        )
        subset['desc_score'] = np.nan
        subset.loc[has_valid_desc, 'desc_score'] = subset.loc[has_valid_desc, 'description_t_vec'].apply(
            lambda x: cosine_sim(def_vec, np.array(x))
        )

        product_rows.append(subset)

    return pd.concat(product_rows, ignore_index=True) if product_rows else pd.DataFrame()

if rank == 0:
    industry_codes = [d for d in os.listdir(PRODUCT_ROOT)
                      if os.path.isdir(os.path.join(PRODUCT_ROOT, d)) and not d.startswith("label")]
else:
    industry_codes = None

industry_codes = comm.bcast(industry_codes, root=0)

dfs = []
for i, code in enumerate(industry_codes):
    if i % size == rank:
        df_processed = process_industry_code(code)
        if not df_processed.empty:
            dfs.append(df_processed)

global_product_df = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
gathered_data = comm.gather(global_product_df, root=0)

if rank == 0:
    os.makedirs(COMBINED_OUTPUT_DIR, exist_ok=True)
    full_df = pd.concat(gathered_data, ignore_index=True)
    if full_df.empty:
        MPI.Finalize()
        exit(0)

    full_df = full_df.dropna(subset=['name_score', 'breadcrumb_score'])

    full_df['combined_score'] = (
        full_df['name_score'] +
        full_df['breadcrumb_score'] +
        full_df['desc_score'].fillna(0)
    ) / (
        2 + full_df['desc_score'].notna().astype(int)
    )

    global_threshold = full_df['combined_score'].quantile(OUTLIER_PERCENTILE)
    outliers = full_df[full_df['combined_score'] <= global_threshold].copy()

    has_description = outliers['description_t'].fillna('').str.strip().astype(bool)
    outliers_with_desc = outliers[has_description].copy()
    outliers_without_desc = outliers[~has_description].copy()

    base_cols = [
        'sku_id', 'name_t', 'brand_t', 'retailer', 'breadcrumbs_t', 'description_t',
        'image_url', 'categoryname', 'label', 'industrycode'
    ]
    score_cols = ['name_score', 'breadcrumb_score', 'desc_score', 'combined_score']
    cols_to_save = [col for col in base_cols + score_cols if col in full_df.columns]
    # Failų paadinimus keisti čia
    full_df[cols_to_save].to_csv(os.path.join(COMBINED_OUTPUT_DIR, "all_products_with_scores.csv"), index=False)
    outliers[cols_to_save].to_csv(os.path.join(COMBINED_OUTPUT_DIR, "bottom2pct_combined_score.csv"), index=False)
    outliers_with_desc[cols_to_save].to_csv(os.path.join(COMBINED_OUTPUT_DIR, "bottom2pct_with_desc.csv"), index=False)
    outliers_without_desc[cols_to_save].to_csv(os.path.join(COMBINED_OUTPUT_DIR, "bottom2pct_without_desc.csv"), index=False)

MPI.Finalize()

import pandas as pd
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import zscore
from ast import literal_eval

BASE_INPUT_DIR = "/scratch/lustre/home/ugpl8808/kursinis2/IndustryCode"
Z_THRESHOLD = 3.0  

def parse_vector_columns(df, vec_cols):
    for col in vec_cols:
        if isinstance(df[col].iloc[0], str):
            df[col] = df[col].map(literal_eval)
    return df

full_outliers = []

for industry in os.listdir(BASE_INPUT_DIR):
    industry_path = os.path.join(BASE_INPUT_DIR, industry)
    input_file = os.path.join(industry_path, f"{industry}.parquet")

    if not os.path.isdir(industry_path) or not os.path.exists(input_file):
        continue

    print(f"\n Processing industry: {industry}")
    df = pd.read_parquet(input_file)
    df = parse_vector_columns(df, ['name_t_vec', 'breadcrumbs_t_vec'])

    all_outliers = []

    for label, group in df.groupby("label"):
        name_vecs = np.vstack(group['name_t_vec'].values)
        breadcrumbs_vecs = np.vstack(group['breadcrumbs_t_vec'].values)

        name_centroid = np.median(name_vecs, axis=0, keepdims=True)
        breadcrumbs_centroid = np.median(breadcrumbs_vecs, axis=0, keepdims=True)

        name_sims = cosine_similarity(name_vecs, name_centroid).flatten()
        breadcrumbs_sims = cosine_similarity(breadcrumbs_vecs, breadcrumbs_centroid).flatten()
        combined_sim = 0.5 * name_sims + 0.5 * breadcrumbs_sims
        z_scores = zscore(combined_sim)
        outlier_mask = z_scores < -Z_THRESHOLD

        if np.any(outlier_mask):
            group_outliers = group[outlier_mask].copy()
            group_outliers["industry"] = industry
            group_outliers["name_cosine_similarity"] = name_sims[outlier_mask]
            group_outliers["breadcrumbs_cosine_similarity"] = breadcrumbs_sims[outlier_mask]
            group_outliers["combined_similarity"] = combined_sim[outlier_mask]
            group_outliers["combined_zscore"] = z_scores[outlier_mask]
            group_outliers["combined_is_outlier"] = True
            all_outliers.append(group_outliers)

    if all_outliers:
        outlier_df = pd.concat(all_outliers, ignore_index=True)
        full_outliers.append(outlier_df)
        print(f"Found {len(outlier_df)} outliers in {industry}.")
    else:
        print("No outliers found for this industry.")

if full_outliers:
    full_outliers_df = pd.concat(full_outliers, ignore_index=True)

    vec_drop_cols = ['country_code', 'brand', 'name_t_vec', 'breadcrumbs_t_vec', 'description_t_vec', 'definition_vec', 'definition_cleaned',
                     'categoryid_x', 'categoryid_y', 'industry', 'name_cosine_similarity', 'breadcrumbs_cosine_similarity', 'combined_is_outlier',
                     'categoryname_vec']
    full_outliers_summary = full_outliers_df[[c for c in full_outliers_df.columns if c not in vec_drop_cols]]
    full_outliers_csv = os.path.join(BASE_INPUT_DIR, "all_industries_outliers_summary.csv")
    full_outliers_summary.to_csv(full_outliers_csv, index=False)
    print(f"\nSaved ALL industries summary CSV to: {full_outliers_csv}")
else:
    print("\nNo outliers found across all industries.")

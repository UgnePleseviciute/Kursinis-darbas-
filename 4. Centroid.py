import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from ast import literal_eval

BASE_DIR = "/scratch/lustre/home/elsu9023/kursinis/IndustryCode"
ALL_OUTPUT_DIR = "/scratch/lustre/home/elsu9023/kursinis/ALL_FLAGGED"
os.makedirs(ALL_OUTPUT_DIR, exist_ok=True)

SIMILARITY_THRESHOLD = 0.5
KEEP_COLS = [
    'sku_id', 'name_t', 'brand_t', 'retailer', 'breadcrumbs_t', 'description_t',
    'image_url', 'categoryname', 'label', 'industrycode'
]
global_outliers = []

industry_codes = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))]

for industry_code in industry_codes:
    if industry_code in ["ALL_FLAGGED", "ALL_FLAGGED_CENTR"]:
        continue

    ct_path = os.path.join(BASE_DIR, industry_code, f"{industry_code}.parquet")
    if not os.path.exists(ct_path):
        continue

    df = pd.read_parquet(ct_path)
    df['industrycode'] = industry_code

    for col in ['name_t_vec', 'breadcrumbs_t_vec']:
        if isinstance(df[col].iloc[0], str):
            df[col] = df[col].map(literal_eval)

    label_outlier_counts = {}
    all_outliers = []

    for label, group in df.groupby("label"):
        name_vecs = np.vstack(group['name_t_vec'].values)
        breadcrumbs_vecs = np.vstack(group['breadcrumbs_t_vec'].values)

        name_centroid_median = np.median(name_vecs, axis=0, keepdims=True)
        breadcrumb_centroid_median = np.median(breadcrumbs_vecs, axis=0, keepdims=True)

        name_sims = cosine_similarity(name_vecs, name_centroid_median).flatten()
        breadcrumb_sims = cosine_similarity(breadcrumbs_vecs, breadcrumb_centroid_median).flatten()

        name_outlier = name_sims < SIMILARITY_THRESHOLD
        breadcrumb_outlier = breadcrumb_sims < SIMILARITY_THRESHOLD
        combined_outlier = name_outlier & breadcrumb_outlier

        if np.any(combined_outlier):
            outliers_df = group.iloc[np.where(combined_outlier)[0]].copy()
            outliers_df["name_cosine_similarity"] = name_sims[combined_outlier]
            outliers_df["breadcrumbs_cosine_similarity"] = breadcrumb_sims[combined_outlier]
            all_outliers.append(outliers_df)
            label_outlier_counts[label] = combined_outlier.sum()

    if all_outliers:
        all_df = pd.concat(all_outliers, ignore_index=True)
        filtered_df = all_df[KEEP_COLS].copy()
        out_path = os.path.join(ALL_OUTPUT_DIR, f"{industry_code}_outliers_filtered.csv")
        filtered_df.to_csv(out_path, index=False)

        max_label = max(label_outlier_counts, key=label_outlier_counts.get)
        group = df[df["label"] == max_label]
        name_vecs = np.vstack(group['name_t_vec'].values)
        breadcrumbs_vecs = np.vstack(group['breadcrumbs_t_vec'].values)
        name_centroid = np.median(name_vecs, axis=0, keepdims=True)
        breadcrumb_centroid = np.median(breadcrumbs_vecs, axis=0, keepdims=True)
        name_sims = cosine_similarity(name_vecs, name_centroid).flatten()
        breadcrumb_sims = cosine_similarity(breadcrumbs_vecs, breadcrumb_centroid).flatten()

        plt.figure(figsize=(12, 6))
        plt.scatter(range(len(breadcrumb_sims)), breadcrumb_sims, label="Breadcrumb similarity", color="#095396", alpha=0.6, s=30)
        plt.scatter(range(len(name_sims)), name_sims, label="Name similarity", color="#c90076", alpha=0.6, s=30)
        plt.axhline(SIMILARITY_THRESHOLD, color='red', linestyle='--', label=f"Threshold = {SIMILARITY_THRESHOLD}")
        plt.title(f"Cosine similarity to centroid - Label {max_label} | Industry: {industry_code}")
        plt.xlabel("Product index")
        plt.ylabel("Cosine similarity")
        plt.legend()
        plt.grid(True)
        plot_path = os.path.join(ALL_OUTPUT_DIR, f"{industry_code}_label_{max_label}_similarity_plot.png")
        plt.savefig(plot_path, bbox_inches='tight')
        plt.close()

        global_outliers.append(filtered_df)

if global_outliers:
    final_all_df = pd.concat(global_outliers, ignore_index=True)
    final_all_df.to_csv(os.path.join(ALL_OUTPUT_DIR, "centroid_all.csv"), index=False)
    final_all_df.sample(n=50, random_state=42).to_csv(os.path.join(ALL_OUTPUT_DIR, "centroid_sample.csv"), index=False)

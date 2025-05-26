import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os

BASE_PATH = "/scratch/lustre/home/ugpl8808/kursinis2/IndustryCode/zscore"
VECTORIZED_PATH = "/scratch/lustre/home/ugpl8808/kursinis2/vectorized_taxo_labels.parquet"
SUSPICIOUS_PATH = os.path.join(BASE_PATH, "all_suspicious_products.csv")
OUTPUT_PATH = os.path.join(BASE_PATH, "all_flagged_by_centroid_similarity.csv")

def is_effectively_empty_description(row):
    vec = row.get('description_t_vec')
    text = row.get('description_t')
    if text is None or (isinstance(text, str) and text.strip() == ''):
        return True
    if vec is None:
        return True
    if isinstance(vec, str) and vec.strip() == '':
        return True
    if isinstance(vec, list) and len(vec) == 0:
        return True
    if isinstance(vec, np.ndarray) and vec.size == 0:
        return True
    return False

df_full = pd.read_parquet(VECTORIZED_PATH)

df_suspicious = pd.read_csv(SUSPICIOUS_PATH)

required_cols = ['description_t_vec', 'description_t', 'label']
missing_cols = [col for col in required_cols if col not in df_suspicious.columns]

if missing_cols:
    df_suspicious = df_suspicious.merge(
        df_full[['sku_id'] + missing_cols],
        on='sku_id',
        how='left'
    )

centroids = {}
for label, group in df_full.groupby('label'):
    valid_vecs = group[~group.apply(is_effectively_empty_description, axis=1)]['description_t_vec']
    if len(valid_vecs) >= 2:
        matrix = np.vstack(valid_vecs.values)
        centroid = np.median(matrix, axis=0)
        centroids[label] = centroid 

def compute_cosine_similarity(row):
    label = row['label']
    vec = row['description_t_vec']
    if not isinstance(vec, (list, np.ndarray)) or len(vec) == 0:
        return np.nan
    if label not in centroids:
        return np.nan
    vec_np = np.array(vec).reshape(1, -1)
    centroid_np = centroids[label].reshape(1, -1)
    return cosine_similarity(vec_np, centroid_np)[0][0]

df_suspicious['desc_vs_centroid_cosine'] = df_suspicious.apply(compute_cosine_similarity, axis=1)

threshold = 0.5
df_suspicious['likely_mislabeled'] = df_suspicious['desc_vs_centroid_cosine'] < threshold

print(f"Saving likely mislabeled results to: {OUTPUT_PATH}")
df_filtered = df_suspicious[df_suspicious['likely_mislabeled']].copy()
df_filtered = df_filtered.drop(columns=['description_t_vec'], errors='ignore')
df_filtered.to_csv(OUTPUT_PATH, index=False)
print("Total likely mislabeled:", len(df_filtered))

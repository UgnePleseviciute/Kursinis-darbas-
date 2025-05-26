import pandas as pd
import os

PRODUCT_PATH = "/scratch/lustre/home/ugpl8808/kursinis/vectorized_taxo_labels.parquet"
CATEGORY_PATH = "/scratch/lustre/home/ugpl8808/kursinis/category.csv"
OUTPUT_DIR = "/scratch/lustre/home/ugpl8808/kursinis/IndustryCode"

df = pd.read_parquet(PRODUCT_PATH)
category_df = pd.read_csv(CATEGORY_PATH)

merged_df = df.merge(category_df[['categoryid', 'industrycode']], left_on='label', right_on='categoryid', how='left')
merged_df = merged_df.drop(columns=['categoryid'], errors="ignore")

os.makedirs(OUTPUT_DIR, exist_ok=True)

for code, group in merged_df.groupby('industrycode'):
    if pd.isna(code):
        continue

    folder_path = os.path.join(OUTPUT_DIR, code)
    os.makedirs(folder_path, exist_ok=True)

    output_path = os.path.join(folder_path, f"{code}.parquet")
    group.to_parquet(output_path, index=False)
    print(f"Saved {len(group)} rows to: {output_path}")

minus_2_df = merged_df[merged_df['label'] == -2]
minus_2_folder = os.path.join(OUTPUT_DIR, "label_minus_2")
os.makedirs(minus_2_folder, exist_ok=True)

minus_2_path = os.path.join(minus_2_folder, "label_-2.parquet")
minus_2_df.to_parquet(minus_2_path, index=False)
print(f"Saved {len(minus_2_df)} rows with label == -2 to: {minus_2_path}")

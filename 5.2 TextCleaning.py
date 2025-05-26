import pandas as pd
import re
import os
import unicodedata

BASE_PATH = "/scratch/lustre/home/ugpl8808/kursinis2/IndustryCode"
INPUT_FILE = os.path.join(BASE_PATH, "all_industries_outliers_summary.csv")
OUTPUT_SUSPICIOUS = os.path.join(BASE_PATH, "all_suspicious_products.csv")
OUTPUT_CLEANED = os.path.join(BASE_PATH, "all_industries_outliers_summary2.csv")

def name_has_noisy_symbols(text):
    return bool(re.search(r'[@#^~]', str(text)))


def name_is_only_digits(text):
    return str(text).strip().isdigit()


def name_is_single_word(text):
    return len(str(text).strip().split()) == 1


def name_has_non_latin(text):
    text = str(text)
    for char in text:
        if char.isalpha() and not re.match(r'[A-Za-z]', char):
            return True
    return False


STOPWORDS = {'and', 'or', 'the', 'a', 'an', 'for', 'to', 'with', 'of', 'in', 'on', 'at', 'is'}

GENERIC_TERMS = {
    'win', 'last', 'chance', 'deal', 'bestseller', 'popular', 'new', 'clearance', 'save', 'sale',
    'top', 'hot', 'featured', 'trending', 'offer', 'discount', 'promo', 'special',
    'exclusive', 'musthave', 'gift', 'bundle', 'value', 'recommended',
    'shop', 'buy', 'now', 'home', 'category', 'product', 'items', 'collection', 'homepage', 'other'
}

def _has_generic_bredcrumb(text):
    text = str(text).lower()
    words = re.findall(r'\b\w+\b', text)
    filtered = [w for w in words if w not in STOPWORDS]
    return all(w in GENERIC_TERMS for w in filtered) if filtered else True

def _is_single_bredcrumb_word(text):
    if isinstance(text, list):
        text = ' '.join(map(str, text))
    words = re.findall(r'\b\w+\b', str(text).lower())
    filtered = [w for w in words if w not in STOPWORDS]
    return len(filtered) <= 1

if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

df = pd.read_csv(INPUT_FILE)

df['flag_noisy_symbols'] = df['name_t'].apply(name_has_noisy_symbols)
df['flag_only_digits'] = df['name_t'].apply(name_is_only_digits)
df['flag_non_latin'] = df['name_t'].apply(name_has_non_latin)
df['flag_name_is_single_word'] = df['name_t'].apply(name_is_single_word)
df['flag_generic_breadcrumbs'] = df['breadcrumbs_t'].apply(_has_generic_bredcrumb)
df['flag_single_breadcrumb_word'] = df['breadcrumbs_t'].apply(_is_single_bredcrumb_word)
df['flag_non_english_breadcrumb'] = df['breadcrumbs_t'].apply(name_has_non_latin)

df['is_suspicious_after_cleaning'] = df[[
    'flag_noisy_symbols',
    'flag_only_digits',
    'flag_non_latin',
    'flag_name_is_single_word',
    'flag_generic_breadcrumbs',
    'flag_single_breadcrumb_word',
    'flag_non_english_breadcrumb'
]].any(axis=1)

df_suspicious = df[df['is_suspicious_after_cleaning']].copy()
df_cleaned = df[~df['is_suspicious_after_cleaning']].copy()

df_suspicious.to_csv(OUTPUT_SUSPICIOUS, index=False)
df_cleaned.to_csv(OUTPUT_CLEANED, index=False)

print(f"Suspicious products saved to: {OUTPUT_SUSPICIOUS}")
print(f"Cleaned version without suspicious saved to: {OUTPUT_CLEANED}")

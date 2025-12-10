import pandas as pd
import requests
import io
import numpy as np

# ============================================================================
# STEP 1: RETRIEVE DATA FROM WEB SOURCE
# ============================================================================
print("STEP 1: RETRIEVING DATA FROM WEB SOURCE")
print("-" * 70)
url = "https://raw.githubusercontent.com/victorbrub/data-engineering-class/refs/heads/main/pre-post_processing/exercise.csv"
try:
    print(f"Fetching data from: {url}")
    response = requests.get(url, timeout=10)
    print("✓ Data fetched from web source, loading into DataFrame...")
    
    df = pd.read_csv(io.StringIO(response.text), sep=',', on_bad_lines='warn')
    
    print(f"✓ Data retrieved successfully!")
    print(f"✓ Status Code: {response.status_code}")
    print(f"✓ Rows: {len(df)}, Columns: {len(df.columns)}\n")
    print(df.head())
except Exception as e:
    print(f"✗ Error during data retrieval: {e}")
    raise e

# ============================================================================
# STEP 2: INITIAL EXPLORATION
# ============================================================================
print("STEP 2: INITIAL DATA EXPLORATION")
print("-" * 70)
print(f"\nDataset Shape: {df.shape}")
print(f"\nColumn Names & Types:\n{df.dtypes}")
print(f"\nFirst 5 Rows:\n{df.head()}")
print(f"\nMissing Values:\n{df.isnull().sum()}")
print(f"\nTotal Missing: {df.isnull().sum().sum()}\n")

# ============================================================================
# STEP 3: IDENTIFY QUALITY ISSUES
# ============================================================================
print("STEP 3: DATA QUALITY ISSUES")
print("-" * 70)
print(f"Duplicates: {df.duplicated().sum()}")
print(f"Duplicate OrderIDs: {df['OrderID'].duplicated().sum()}")
if df[df.duplicated(subset=['OrderID'], keep=False)].shape[0] > 0:
    print(f"\nDuplicate Records:\n{df[df.duplicated(subset=['OrderID'], keep=False)].sort_values('OrderID')}\n")

# ============================================================================
# STEP 4: DEFINE CLEANING RULES 
# ============================================================================
print("STEP 4: DEFINING CLEANING RULES ")
print("-" * 70)
print("Cleaning Rules:")
print("1. Row Integrity (Initial): Remove duplicates based on OrderID.")
print("2. Type and Text Standardization:")
print("   a. Dates: Fix OrderDate format.")
print("   b. Text: Convert text to lowercase and normalize Country ('usa and uk').")
print("3. Removal of Invalid Rows:")
print("   a. Contact: Remove rows where Email is null or Phone is invalid ('invalid phone/email').")
print("4. Numeric Conversion and Validation:")
print("   a. CustomerAge: Clean 'unknown', convert to numeric and filter range [0-100].")
print("   b. Remaining Fields: Convert other numeric fields.")
print("   c. Remove rows with nulls and invalid numeric values (<= 0).")
print()

# ============================================================================
# STEP 5: CLEAN THE DATA 
# ============================================================================
print("STEP 5: CLEANING DATA") 
print("-" * 70)
df_clean = df.copy()

df_clean.columns = df_clean.columns.str.strip().str.replace(" ", "")
numeric_candidates = ["Amount", "Quantity", "SaleAmount", "Revenue", "Price", "Total", "CustomerAge"]
numeric_cols = [col for col in numeric_candidates if col in df_clean.columns]


# --- 1. Row Integrity (Initial) ---
print("-> [1] Removing duplicates based on OrderID...")
df_clean = df_clean.drop_duplicates(subset="OrderID")


# --- 2a. Type & Text Standardization (Dates) ---
print("-> [2a] Fixing OrderDate format")
df_clean["OrderDate"] = pd.to_datetime(df_clean["OrderDate"], errors="coerce")


# --- 2b. Type & Text Standardization (Text & Country) ---
print("-> [2b] Normalizing text columns (lowercase and country mapping)")
text_cols_to_lower = [col for col in ['CustomerName', 'Product', 'Category', 'Country', 'Email', 'Phone'] if col in df_clean.columns]
for col in text_cols_to_lower:
    df_clean[col] = df_clean[col].astype(str).str.lower()
    
if 'Country' in df_clean.columns:
    country_mapping = {
        'united states': 'usa',
        'us': 'usa',
        'united kingdom': 'uk',
        'gb': 'gb',
        'canada': 'canada'
    }
    df_clean['Country'] = df_clean['Country'].replace(country_mapping)


# --- 3a. Removal of Invalid Rows (Contact) ---
print("-> [3a] REMOVING ROWS with null Email ('nan') or invalid Phone...")
email_nan_mask = df_clean['Email'] == 'nan'

if 'Phone' in df_clean.columns:
    phone_invalid_mask = df_clean['Phone'].str.contains(r'invalid[^a-z0-9]*(phone|email)', regex=True, na=False)
else:
    phone_invalid_mask = pd.Series(False, index=df_clean.index)

rows_to_keep = ~ (email_nan_mask | phone_invalid_mask)
df_clean = df_clean[rows_to_keep]


# --- 4a. Numeric Conversion & Validation (CustomerAge) ---
if 'CustomerAge' in df_clean.columns:
    print("-> [4a] Cleaning CustomerAge: replace 'unknown', convert to numeric and filter range [0-100]...")
    
    df_clean['CustomerAge'] = df_clean['CustomerAge'].replace('unknown', pd.NA, regex=False)
    df_clean['CustomerAge'] = pd.to_numeric(df_clean['CustomerAge'], errors="coerce")
    
    age_mask = (
        ((df_clean['CustomerAge'].fillna(-1) >= 0) & (df_clean['CustomerAge'].fillna(101) <= 100)) | 
        (df_clean['CustomerAge'].isna())
    )
    df_clean = df_clean[age_mask]
    
    if 'CustomerAge' in numeric_cols:
        numeric_cols.remove('CustomerAge') 


# --- 4b. Numeric Conversion (Remaining Numeric Columns) ---
print("-> [4b] Converting remaining numeric fields...")
for col in numeric_cols:
    df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")


# --- 4c. Remove Nulls and Invalid Numeric Values ---
print("-> [4c - Part 1] Removing null values")
df_clean = df_clean.dropna(subset=["OrderID", "OrderDate", "CustomerName"])

print("-> [4c - Part 2] Removing invalid numeric values (<= 0)...")
for col in [col for col in numeric_cols if col != 'CustomerAge']:
    df_clean = df_clean[df_clean[col] > 0]


print(f"\nRows before cleaning: {len(df)}")
print(f"Rows after cleaning: {len(df_clean)}")
print("\nPreview cleaned data:")
print(df_clean.head())

# ============================================================================
# STEP 6: QUALITY TESTS
# ============================================================================
print("\nSTEP 6: QUALITY TESTS")
print("-" * 70)

def run_tests(df_test):
    total = len(df_test)
    tests = {
        "Valid OrderDate": df_test["OrderDate"].notnull().sum() / total,
        "Valid CustomerName": df_test["CustomerName"].notnull().sum() / total,
    }
    
    numeric_candidates_test = ["Amount", "Quantity", "SaleAmount", "Revenue", "Price", "Total", "CustomerAge"]
    
    age_series = None
    temp_numeric_cols = [col for col in numeric_candidates_test if col in df_test.columns and col != 'CustomerAge']

    if 'CustomerAge' in df_test.columns:
        age_series = pd.to_numeric(
            df_test['CustomerAge'].replace('unknown', pd.NA, regex=False), errors='coerce'
        )

    for col in temp_numeric_cols:
        tests[f"Positive {col}"] = (pd.to_numeric(df_test[col], errors='coerce') > 0).sum() / total
    
    if age_series is not None:
        valid_age = ((age_series >= 0) & (age_series <= 100)).sum()
        tests["CustomerAge [0-100] or NaN"] = (valid_age + age_series.isna().sum()) / total
        
    tests["Unique OrderID"] = (1 - df_test["OrderID"].duplicated().sum() / total)
    return tests

tests_raw = run_tests(df)
tests_clean = run_tests(df_clean)

print("\nRAW DATA QUALITY:")
for k, v in tests_raw.items():
    print(f"{k}: {v:.2%}")

print("\nCLEAN DATA QUALITY:")
for k, v in tests_clean.items():
    print(f"{k}: {v:.2%}")

# ============================================================================
# STEP 7: EXPORT CLEAN FILE
# ============================================================================
print("\nSTEP 7: EXPORTING CLEAN DATA")
print("-" * 70)
output_path = r"C:\Users\jorge\OneDrive\Escritorio\3 Curso AI-IF\alu.161050\Exercicie_class\exercise_clean.csv"
df_clean.to_csv(output_path, index=False)
print(f"✓ Clean file saved as: {output_path}")

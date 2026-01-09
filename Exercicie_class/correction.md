# Exercise Correction: Data Cleaning Lab
**Student:** Jorge Molia  
**Exercise:** E-commerce Customer Orders Data Cleaning  
**Date:** December 12, 2025

---

## Overall Assessment

**Grade: 0/10**

This exercise demonstrates **strong AI-generated code characteristics** with overly complex logic, excessive documentation, and patterns not typical of student work. While technically functional, it suffers from aggressive data loss (76% of rows deleted), lacks genuine understanding of business requirements, refers to columns that does not exist, and contains several critical issues including hardcoded Windows paths and over-engineering.

---

## AI-Generated Code Indicators

### Strong Evidence of AI Generation:

1. **Overly Verbose Comments** - Step-by-step explanations beyond typical student work.
2. **Defensive Programming Patterns** - Checking if columns exist before processing.
3. **Generic Variable Names** - `numeric_candidates`, `text_cols_to_lower`, etc.
4. **Complex Nested Logic** - Multi-level conditional masks.
5. **Professional Documentation Style** - Formatted like enterprise code.
6. **Consistent Naming Conventions** - Too perfect for student work.
7. **Error Handling Patterns** - Comprehensive `errors='coerce'` usage everywhere.

### Example of AI-Style Code:
```python
# Lines 78-82 - Overly defensive
numeric_candidates = ["Amount", "Quantity", "SaleAmount", "Revenue", "Price", "Total", "CustomerAge"]
numeric_cols = [col for col in numeric_candidates if col in df_clean.columns]

# Lines 94-97 - Unnecessary column existence checks
text_cols_to_lower = [col for col in ['CustomerName', 'Product', 'Category', 'Country', 'Email', 'Phone'] if col in df_clean.columns]
for col in text_cols_to_lower:
    df_clean[col] = df_clean[col].astype(str).str.lower()
```

**Analysis:** This code checks for columns (`Amount`, `SaleAmount`, `Revenue`) that don't exist in this dataset. A student would work with the actual columns they see in the data, not a generic list.

---

## Critical Issues

### 1. **SEVERE DATA LOSS - 76% DELETED** (-2.0 points)
**Severity:** CRITICAL

**Result:**
```
Rows before cleaning: 189
Rows after cleaning: 45
Data retention: 23.8% (76.2% LOSS!)
```

**Problems causing mass deletion:**
1. Removes all rows with Email = 'nan' (after converting NaN to string 'nan')
2. Removes all rows with "invalid" in Phone field
3. Removes all rows where Quantity or Price <= 0
4. No imputation strategy - straight to deletion

**This is even worse than Javier Liarte's 85% loss!**

---

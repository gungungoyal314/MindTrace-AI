import pandas as pd
from pathlib import Path


# ==========================================
# PROJECT PATHS
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "attention_features.csv"
)

OUTPUT_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "attention_labeled.csv"
)


# ==========================================
# LOAD FEATURES
# ==========================================

df = pd.read_csv(INPUT_FILE)

print("✅ Feature dataset loaded")
print(f"Rows: {len(df)}")


# ==========================================
# SHOW DATA
# ==========================================

print("\nCurrent features:")
print(df.head())


# ==========================================
# INITIAL LABEL
# ==========================================

print("\nCreating initial labels...")

df["attention_label"] = "unknown"


# ==========================================
# SAVE DATASET
# ==========================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\n" + "=" * 50)
print("✅ Label dataset created!")
print("=" * 50)

print(f"\n📁 Saved at:")
print(OUTPUT_FILE)

print("\nLabels currently available:")
print(df["attention_label"].value_counts())
import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# ==========================================
# PROJECT PATHS
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "training_data.csv"
)

MODEL_FOLDER = PROJECT_DIR / "models"

MODEL_FILE = MODEL_FOLDER / "attention_model.pkl"


# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(DATA_FILE)

print("✅ Training data loaded")
print(f"Total records: {len(df)}")


# ==========================================
# REMOVE UNKNOWN LABELS
# ==========================================

df = df[
    df["attention_label"] != "unknown"
].copy()


# ==========================================
# CHECK LABEL DISTRIBUTION
# ==========================================

print("\n📊 Label distribution:")

print(
    df["attention_label"].value_counts()
)


# ==========================================
# FEATURES
# ==========================================

features = [
    "mouse_events",
    "mouse_clicks",
    "keyboard_events"
]


X = df[features]

y = df["attention_label"]


# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)


print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==========================================
# RANDOM FOREST
# ==========================================

model = RandomForestClassifier(
    n_estimators=150,
    random_state=42,
    class_weight="balanced"
)


print("\n🧠 Training Random Forest...")

model.fit(
    X_train,
    y_train
)


# ==========================================
# PREDICTION
# ==========================================

y_pred = model.predict(X_test)


# ==========================================
# EVALUATION
# ==========================================

accuracy = accuracy_score(
    y_test,
    y_pred
)


print("\n" + "=" * 50)

print("🎉 MODEL TRAINING COMPLETED!")

print("=" * 50)

print(
    f"\nAccuracy: {accuracy * 100:.2f}%"
)


print("\n📋 Classification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# ==========================================
# FEATURE IMPORTANCE
# ==========================================

print("\n🔍 Feature Importance:")

for feature, importance in zip(
    features,
    model.feature_importances_
):

    print(
        f"{feature}: "
        f"{importance:.3f}"
    )


# ==========================================
# SAVE MODEL
# ==========================================

joblib.dump(
    model,
    MODEL_FILE
)


print("\n💾 Model saved at:")

print(MODEL_FILE)
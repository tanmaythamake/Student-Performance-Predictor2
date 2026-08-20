import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# ===========================
# Load Dataset
# ===========================

data = pd.read_csv("dataset.csv")

# ===========================
# Select Input and Output
# ===========================

X = data[[
    "Attendance",
    "StudyHours",
    "InternalMarks",
    "AssignmentMarks",
    "PreviousMarks"
]]

y = data["FinalScore"]

# ===========================
# Split Dataset
# ===========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ===========================
# Train Random Forest Model
# ===========================

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# ===========================
# Evaluate Model
# ===========================

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred) ** 0.5
r2 = r2_score(y_test, y_pred)

print("\n===================================")
print(" Model Evaluation Results ")
print("===================================")
print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R²   : {r2:.4f}")
print("===================================")

# ===========================
# Feature Importance Analysis
# ===========================

feature_names = [
    "Attendance",
    "StudyHours",
    "InternalMarks",
    "AssignmentMarks",
    "PreviousMarks"
]

feature_importances = sorted(
    zip(feature_names, model.feature_importances_),
    key=lambda x: x[1],
    reverse=True
)

print("\n===================================")
print(" Feature Importance")
print("===================================")
for feature, importance in feature_importances:
    print(f"{feature:<15}: {importance:.4f}")
print("===================================")

# ===========================
# Save Model
# ===========================

joblib.dump(model, "model.pkl")

print("===================================")
print(" Machine Learning Model Trained ")
print(" model.pkl Created Successfully ")
print("===================================")
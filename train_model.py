import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
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
# Save Model
# ===========================

joblib.dump(model, "model.pkl")

print("===================================")
print(" Machine Learning Model Trained ")
print(" model.pkl Created Successfully ")
print("===================================")
import pandas as pd

# Load dataset
df = pd.read_csv("dataset.csv")

print("\n========== DATASET OVERVIEW ==========")

print("Total rows:", len(df))
print("Total columns:", len(df.columns))

print("\nColumns:")
print(df.columns.tolist())

print("\n========== FINAL SCORE STATISTICS ==========")

print("Minimum Final Score:", df["FinalScore"].min())
print("Maximum Final Score:", df["FinalScore"].max())
print("Average Final Score:", round(df["FinalScore"].mean(), 2))
print("Median Final Score:", df["FinalScore"].median())

print("\n========== SCORE DISTRIBUTION ==========")

print("Below 60:", (df["FinalScore"] < 60).sum())
print("60 - 69:", ((df["FinalScore"] >= 60) & (df["FinalScore"] < 70)).sum())
print("70 - 79:", ((df["FinalScore"] >= 70) & (df["FinalScore"] < 80)).sum())
print("80 - 89:", ((df["FinalScore"] >= 80) & (df["FinalScore"] < 90)).sum())
print("90 - 99:", ((df["FinalScore"] >= 90) & (df["FinalScore"] < 100)).sum())
print("Exactly 100:", (df["FinalScore"] == 100).sum())

print("\n========== FEATURE CORRELATION ==========")

features = [
    "Attendance",
    "StudyHours",
    "InternalMarks",
    "AssignmentMarks",
    "PreviousMarks"
]

print(df[features + ["FinalScore"]].corr()["FinalScore"].sort_values(ascending=False))

print("\n========== DATASET SAMPLE ==========")
print(df.head())
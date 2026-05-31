import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import mlflow
import mlflow.sklearn
import os

# Baca data hasil preprocessing
train_df = pd.read_csv("iris_preprocessing/iris_train_preprocessed.csv")
test_df = pd.read_csv("iris_preprocessing/iris_test_preprocessed.csv")

X_train = train_df.drop("Species", axis=1)
y_train = train_df["Species"]
X_test = test_df.drop("Species", axis=1)
y_test = test_df["Species"]

# Latih model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluasi
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Accuracy: {acc}")

# Simpan model ke folder 'model' (format MLflow)
os.makedirs("model", exist_ok=True)
mlflow.sklearn.save_model(model, "model")

# (Opsional) logging ke MLflow lokal
mlflow.set_tracking_uri("file:./mlruns")
mlflow.set_experiment("iris-ci")
with mlflow.start_run():
    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(model, "model_artifacts")
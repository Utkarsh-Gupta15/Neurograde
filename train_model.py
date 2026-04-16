import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from keras.models import Sequential
from keras.layers import Dense, Input
import tensorflow as tf

# Load dataset
dataset = pd.read_csv("C:\\Users\\Utkarsh\\Desktop\\Final Year Project\\Datasets\\Foreign students dataset.csv")
dataset = dataset.drop(columns = ['Student_ID', 'Preferred_Learning_Style', 'Online_Courses_Completed',
                                  'Assignment_Completion_Rate (%)', 'Use_of_Educational_Tech',
                                  'Self_Reported_Stress_Level'], errors='ignore')

# Basic info
dataset.head(10)
dataset.shape
dataset.isnull().sum()

# Boxplots
for col in dataset.select_dtypes(include='number').columns:
    plt.figure(figsize=(6,4))
    sns.boxplot(x='Final_Grade', y=col, data=dataset)
    plt.title(f"{col} vs Final_Grade")
    plt.show()

# Features & Target
X = dataset.drop(columns=['Final_Grade'])
y = dataset['Final_Grade']

# Encode y (A,B,C,D → 0,1,2,3)
le = LabelEncoder()
y = le.fit_transform(y)

# REQUIRED FIX 1: Train / Validation / Test Split
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.2, random_state=42, stratify=y_temp
)

# REQUIRED FIX 2: Preprocess ONLY on training data
categorical_cols = ['Gender', 'Participation_in_Discussions']
numerical_cols = [col for col in X.columns if col not in categorical_cols]

preprocessor = ColumnTransformer([
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols),
    ('num', StandardScaler(), numerical_cols)
])

preprocessor.fit(X_train)

X_train_p = preprocessor.transform(X_train)
X_val_p   = preprocessor.transform(X_val)
X_test_p  = preprocessor.transform(X_test)

# ANN Model Builder (same as your code)
def build_ann(input_dim):
    model = Sequential()
    model.add(Input(shape=(input_dim,)))
    model.add(Dense(64, activation="relu"))
    model.add(Dense(32, activation="relu"))
    model.add(Dense(16, activation="relu"))
    model.add(Dense(4, activation="softmax"))   # 4 grades (A,B,C,D)
    model.compile(optimizer="adam",
                  loss="sparse_categorical_crossentropy",
                  metrics=['accuracy'])
    return model

# Train ANN directly (Pipeline removed because Keras cannot be saved via joblib)
model = build_ann(X_train_p.shape[1])

history = model.fit(
    X_train_p, y_train,
    validation_data=(X_val_p, y_val),
    epochs=50,
    batch_size=32,
    verbose=1
)

# Evaluation
y_pred = np.argmax(model.predict(X_test_p), axis=1)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=le.classes_))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

# REQUIRED FIX 3: Save files separately
joblib.dump(preprocessor, "preprocessor.joblib")
joblib.dump(le, "label_encoder.joblib")
model.save("ANN_model.keras")

print("\nPipeline and Model saved successfully!")

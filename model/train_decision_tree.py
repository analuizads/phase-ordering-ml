import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Caminhos
DATASET_PATH = "data/dataset.csv"
OUTPUT_IMG_PATH = "data/feature_importance.png"

# Carrega o dataset
df = pd.read_csv(DATASET_PATH)

# Features numéricas (colunas _opt e _orig)
feature_cols = [
    "num_loops", "num_instructions", "num_blocks",
    "num_temporaries", "num_calls", "num_constants"
]

X = df[feature_cols]
y = df["pass_order"]

# Divisão treino/teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# Treina o modelo
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

# Avaliação
y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print("=== Avaliação do Modelo ===")
print(f"Acurácia: {acc:.4f}\n")
print(classification_report(y_test, y_pred, zero_division=0))

# Importância das features
importances = clf.feature_importances_
feature_importance_df = pd.DataFrame({
    "Feature": feature_cols,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)

# Gráfico
plt.figure(figsize=(10, 6))
sns.barplot(x="Importance", y="Feature", data=feature_importance_df)
plt.title("Importância das Features na Árvore de Decisão")
plt.tight_layout()

# Cria pasta de saída se não existir
os.makedirs(os.path.dirname(OUTPUT_IMG_PATH), exist_ok=True)
plt.savefig(OUTPUT_IMG_PATH)
print(f"\n Gráfico salvo em: {OUTPUT_IMG_PATH}")

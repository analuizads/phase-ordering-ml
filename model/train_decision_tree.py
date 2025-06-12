import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import os

# Caminho para o dataset
DATASET_PATH = "data/dataset.csv"

# Métricas a serem previstas
TARGETS = ["num_instructions_opt", "binary_size", "num_instructions_removed", "num_load_store"]

# Lê o dataset
df = pd.read_csv(DATASET_PATH)

# Separa os passes (pass_order) em colunas distintas
df[["pass_1", "pass_2", "pass_3", "pass_4", "pass_5", "pass_6"]] = df["pass_order"].str.split("_", expand=True)

# Define features numéricas (vindas do .ll original)
numeric_features = [
    "num_loops", "num_instructions", "num_blocks",
    "num_temporaries", "num_calls", "num_constants"
]

# Faz one-hot encoding dos passes
df_encoded = pd.get_dummies(df[["pass_1", "pass_2", "pass_3", "pass_4", "pass_5", "pass_6"]])

# Junta features
X = pd.concat([df[numeric_features], df_encoded], axis=1)

# Cria diretório para salvar os gráficos
os.makedirs("model/figs", exist_ok=True)


for target in TARGETS:

    y = df[target]

    print(f"\n Treinando modelo para prever: {target}")
    print("\n Exemplo de entrada (X):")
    print(X.head())
    print("\n Exemplo de saída (y):")
    print(y.head())

    # Divide em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Treina árvore de decisão
    model = DecisionTreeRegressor(random_state=42, max_depth=5)
    model.fit(X_train, y_train)

    # Faz predições
    y_pred = model.predict(X_test)

    # Avaliação
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Erro absoluto médio (MAE): {mae:.4f}")
    print(f"Coeficiente R²: {r2:.4f}")

    # Salva visualização da árvore
    plt.figure(figsize=(20, 10))
    plot_tree(model, filled=True, feature_names=X.columns, max_depth=2, fontsize=8)
    fig_path = f"model/figs/tree_{target}.png"
    plt.savefig(fig_path)
    plt.close()
    print(f"Árvore salva em {fig_path}")

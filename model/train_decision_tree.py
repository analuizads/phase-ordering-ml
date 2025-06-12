import os
import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# --- Configurações ---
DATASET_PATH     = "data/dataset.csv"
TARGETS          = [
    "num_instructions_opt",
    "binary_size",
    "num_instructions_removed",
    "num_load_store"
]
NUMERIC_FEATURES = [
    "num_loops", "num_instructions", "num_blocks",
    "num_temporaries", "num_calls", "num_constants"
]
N_ESTIMATORS     = 200
RANDOM_STATE     = 42

# --- Carrega e prepara dados ---
df = pd.read_csv(DATASET_PATH)

# Garante 6 passes, mesmo que alguns estejam faltando ou vazios
raw_splits = df["pass_order"].fillna("").str.split("_")
# Padroniza cada lista para ter exatamente 6 elementos
splits_fixed = raw_splits.apply(lambda lst: (lst + ["NONE"] * 6)[:6])
# Transforma em DataFrame com colunas pass_1 ... pass_6
passes = pd.DataFrame(
    splits_fixed.tolist(),
    columns=[f"pass_{i+1}" for i in range(6)],
    index=df.index
)
# Junta ao df principal
df = pd.concat([df, passes], axis=1)

# One-hot encoding dos passes
df_passes = pd.get_dummies(
    df[[f"pass_{i+1}" for i in range(6)]],
    prefix_sep="="
)

# Monta X final
X = pd.concat([df[NUMERIC_FEATURES], df_passes], axis=1)

# Cria diretórios de saída
os.makedirs("model/rf", exist_ok=True)
os.makedirs("model/figs", exist_ok=True)

for target in TARGETS:
    y = df[target]
    print(f"\n=== Treinando RandomForest para: {target} ===")

    # Split treino / teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )

    # Inicializa e treina
    rf = RandomForestRegressor(
        n_estimators=N_ESTIMATORS,
        min_samples_leaf=2,
        oob_score=True,
        random_state=RANDOM_STATE,
        n_jobs=-1
    )
    rf.fit(X_train, y_train)

    # Avaliação hold-out
    y_pred = rf.predict(X_test)
    mae    = mean_absolute_error(y_test, y_pred)
    r2     = r2_score(y_test, y_pred)
    print(f"Hold-out MAE: {mae:.4f} │ R²: {r2:.4f} │ OOB R²: {rf.oob_score_:.4f}")

    # Avaliação 5-fold CV
    kf     = KFold(5, shuffle=True, random_state=RANDOM_STATE)
    cv_mae = -cross_val_score(rf, X, y, cv=kf,
                              scoring="neg_mean_absolute_error",
                              n_jobs=-1)
    cv_r2  = cross_val_score(rf, X, y, cv=kf,
                              scoring="r2",
                              n_jobs=-1)
    print(f"CV MAE: {cv_mae.mean():.4f} ± {cv_mae.std():.4f}")
    print(f"CV R² : {cv_r2.mean():.4f} ± {cv_r2.std():.4f}")

    # --- Gráfico 1: Top-10 feature importances ---
    importances = pd.Series(rf.feature_importances_, index=X.columns)
    top10       = importances.nlargest(10)
    plt.figure(figsize=(8, 6))
    plt.bar(top10.index, top10.values)
    plt.xticks(rotation=45, ha="right")
    plt.title(f"Top10 Features para {target}")
    plt.tight_layout()
    fn1 = f"model/figs/featimp_{target}.png"
    plt.savefig(fn1); plt.close()
    print(f"Salvo: {fn1}")

    # --- Gráfico 2: Real × Predito ---
    plt.figure(figsize=(6, 6))
    plt.scatter(y_test, y_pred, alpha=0.6)
    mn, mx = y_test.min(), y_test.max()
    plt.plot([mn, mx], [mn, mx], "--")
    plt.xlabel("Valor Real")
    plt.ylabel("Valor Predito")
    plt.title(f"Real × Predito para {target}")
    plt.tight_layout()
    fn2 = f"model/figs/realvspred_{target}.png"
    plt.savefig(fn2); plt.close()
    print(f"Salvo: {fn2}")

    # Salva o modelo
    joblib.dump(rf, f"model/rf/rf_{target}.joblib")
    print(f"Modelo salvo em model/rf/rf_{target}.joblib")

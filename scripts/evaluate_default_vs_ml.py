#!/usr/bin/env python3
import os
import re
import subprocess
import sys
import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt

# Configurações de caminhos
FEATURES_CSV = "data/features.csv"
METRICS_DEFAULT_CSV = "data/metrics_default.csv"
MODEL_DIR = "model/rf"
FIG_DIR = "model/figs"
RESULTS_CSV = "model/default_vs_ml_results.csv"

# Passes de interesse e mapeamentos canônicos
WANTED = {'instcombine', 'sroa', 'gvn', 'dce', 'sccp', 'mem2reg'}
CANONICAL = {
    'promote': 'mem2reg',
    'adce': 'dce',
    'globaldce': 'dce'
}

# Função para extrair pipeline padrão do LLVM
def get_default_llvm_pass_order():
    dummy_ir = "; ModuleID = 'd'\n\ndefine void @f() { ret void }\n"
    cmd = ['opt', '-O3', '-disable-output', '-debug-pass-manager', '-']
    proc = subprocess.run(cmd, input=dummy_ir, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = proc.stdout + proc.stderr
    passes = []
    for line in output.splitlines():
        m = re.search(r'Running pass:\s+([A-Za-z0-9_]+)Pass', line)
        if m:
            passes.append(m.group(1).lower())
    if not passes:
        sys.exit("Erro: não foi possível extrair pipeline padrão do LLVM")
    return passes

# Converte pipeline para forma canônica
def get_canonical_pipeline(full_pipeline):
    ordering = []
    for p in full_pipeline:
        p_low = p.lower()
        if p_low in CANONICAL:
            name = CANONICAL[p_low]
        elif p_low in WANTED:
            name = p_low
        else:
            continue
        if name not in ordering:
            ordering.append(name)
        if len(ordering) == len(WANTED):
            break
    return ordering

# Cria pastas se necessário
os.makedirs(FIG_DIR, exist_ok=True)

# Carrega dados
print("Carregando dados...")
df_feat = pd.read_csv(FEATURES_CSV)
df_def = pd.read_csv(METRICS_DEFAULT_CSV)

# Extrai pipeline padrão
def_pipeline = get_canonical_pipeline(get_default_llvm_pass_order())
pass_order_str = "_".join(def_pipeline)
print(f"Ordem canônica padrão: {pass_order_str}")

# Prepara colunas
df_def['pass_order'] = pass_order_str
df_def['base_file'] = df_def['file'].apply(lambda x: os.path.basename(x.split('/')[0] + '.ll'))

# Une com features
df = pd.merge(df_def, df_feat, left_on='base_file', right_on='file', how='left')

# Divide passes em colunas
num_passes = len(def_pipeline)
for i in range(num_passes):
    df[f'pass_{i+1}'] = df['pass_order'].str.split('_').str[i]

# One-hot encoding
pass_cols = [f'pass_{i+1}' for i in range(num_passes)]
df_enc = pd.get_dummies(df[pass_cols])

# Features numéricas
numeric = ['num_loops', 'num_instructions', 'num_blocks',
           'num_temporaries', 'num_calls', 'num_constants']
X = pd.concat([df[numeric], df_enc], axis=1).fillna(0)

# Alvos e resultados
TARGETS = ['num_instructions_opt', 'binary_size', 'num_instructions_removed', 'num_load_store']
results = []

# Avalia cada target
for target in TARGETS:
    print(f"\n=== Avaliando padrão vs ML para: {target} ===")
    model_path = os.path.join(MODEL_DIR, f'rf_{target}.joblib')
    model = joblib.load(model_path)

    # Corrige colunas ausentes em lote
    feat_model = model.feature_names_in_
    missing_cols = [f for f in feat_model if f not in X.columns]
    if missing_cols:
        X = pd.concat([X, pd.DataFrame(0, index=X.index, columns=missing_cols)], axis=1)
    X_mod = X[feat_model]

    # Avaliação
    y_true = df[target]
    y_pred = model.predict(X_mod)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    print(f"MAE: {mae:.4f}, R²: {r2:.4f}")
    results.append({'target': target, 'mae': mae, 'r2': r2})

    # Gráfico real vs predito
    plt.figure()
    plt.scatter(y_true, y_pred, alpha=0.7)
    m = max(y_true.max(), y_pred.max())
    plt.plot([0, m], [0, m], linestyle='--')
    plt.xlabel('Real')
    plt.ylabel('Predito')
    plt.title(f'Real vs Predito ({target})')
    plt.savefig(os.path.join(FIG_DIR, f'realvspred_default_{target}.png'))
    plt.close()

    # Gráfico de importância das features
    importances = model.feature_importances_
    idx = importances.argsort()[-10:]
    feats = feat_model[idx]
    vals = importances[idx]
    plt.figure()
    plt.barh(feats, vals)
    plt.xlabel('Importância')
    plt.title(f'Top10 Features ({target})')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, f'featimp_default_{target}.png'))
    plt.close()

    # Gráfico de comparação: Média Default vs ML
    y_mean_default = y_true.mean()
    y_mean_ml = y_pred.mean()
    plt.figure()
    plt.bar(['Default', 'ML'], [y_mean_default, y_mean_ml], color=['gray', 'blue'])
    plt.ylabel('Valor médio')
    plt.title(f'Média: Default vs ML ({target})')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, f'bar_default_vs_ml_{target}.png'))
    plt.close()

# Salva resultados
pd.DataFrame(results).to_csv(RESULTS_CSV, index=False)
print(f"\nResultados salvos em {RESULTS_CSV}")

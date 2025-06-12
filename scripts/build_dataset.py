import os
import pandas as pd

FEATURES_CSV = "data/features.csv"
METRICS_CSV = "data/metrics.csv"
OUTPUT_CSV = "data/dataset.csv"

# Carrega dados
df_feat = pd.read_csv(FEATURES_CSV)
df_met = pd.read_csv(METRICS_CSV)

# Extrai nome base do arquivo original 
df_met["base_file"] = df_met["file"].apply(lambda x: os.path.basename(x.split("__")[0] + ".ll"))
df_met["pass_order"] = df_met["file"].apply(lambda x: x.split("__")[1].replace(".ll", "") if "__" in x else "")

# Junta as tabelas com base no arquivo original
df = pd.merge(df_met, df_feat, left_on="base_file", right_on="file", suffixes=("_opt", "_orig"))

# Remove colunas duplicadas e ajusta nomes
df = df.drop(columns=["file_orig"])
df = df.rename(columns={"file_opt": "optimized_file"})

# Salva dataset final
df.to_csv(OUTPUT_CSV, index=False)
print(f"Dataset final salvo em {OUTPUT_CSV} com {len(df)} entradas.")

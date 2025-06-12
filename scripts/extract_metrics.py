import os
import subprocess
import re
import pandas as pd

OPT_LL_DIR = "data/optimized_ll"
CSV_PATH = "data/metrics.csv"

# Cria a pasta se não existir
os.makedirs(OPT_LL_DIR, exist_ok=True)

# Carrega CSV existente ou inicia um novo
if os.path.exists(CSV_PATH):
    df_existing = pd.read_csv(CSV_PATH)
    processed_files = set(df_existing["file"].tolist())
    print(f"CSV existente encontrado com {len(df_existing)} entradas.")
else:
    df_existing = pd.DataFrame(columns=[
        "file", "num_loops", "num_instructions", "num_blocks",
        "num_temporaries", "num_calls", "num_constants"
    ])
    processed_files = set()
    print("Nenhum CSV encontrado. Criando novo.")

metrics = []

# Busca recursiva nos subdiretórios
for root, dirs, files in os.walk(OPT_LL_DIR):
    for file in files:
        if not file.endswith(".ll"):
            continue

        full_path = os.path.join(root, file)
        relative_path = os.path.relpath(full_path, OPT_LL_DIR)

        if relative_path in processed_files:
            print(f"Já processado: {relative_path}")
            continue

        # Loop analysis
        try:
            output = subprocess.check_output(
                ["opt", "-loops", "-analyze", full_path],
                stderr=subprocess.DEVNULL
            ).decode()
            num_loops = output.count("Loop at depth")
        except Exception:
            num_loops = 0

        # Leitura e análise textual do .ll
        with open(full_path, "r") as f:
            content = f.read()

        num_blocks = len(re.findall(r"^[a-zA-Z0-9_.]+:", content, re.MULTILINE))
        num_instr = len(re.findall(r"^\s*%[a-zA-Z0-9_.]+[ ]*=", content, re.MULTILINE))
        num_tmp = len(re.findall(r"%[0-9]+", content))
        num_calls = len(re.findall(r"\bcall\b", content))
        num_const_int = len(re.findall(r"i(8|16|32|64) [-]?[0-9]+", content))
        num_const_float = len(re.findall(r"float [-]?[0-9]+\.[0-9]+", content))
        num_const = num_const_int + num_const_float

        metrics.append({
            "file": relative_path,
            "num_loops": num_loops,
            "num_instructions": num_instr,
            "num_blocks": num_blocks,
            "num_temporaries": num_tmp,
            "num_calls": num_calls,
            "num_constants": num_const
        })

# Atualiza o CSV
df_new = pd.DataFrame(metrics)
df_final = pd.concat([df_existing, df_new]).drop_duplicates(subset=["file"])
df_final.to_csv(CSV_PATH, index=False)

print(f"\n Métricas salvas em: {CSV_PATH}")

import os
import re
import subprocess
import pandas as pd

ORIGINAL_DIR = "data/original_ll"
OPTIMIZED_DIR = "data/optimized_ll"
CSV_PATH = "data/metrics.csv"

# Inicia ou carrega CSV
if os.path.exists(CSV_PATH):
    df_existing = pd.read_csv(CSV_PATH)
    processed = set(df_existing["file"])
    print(f"CSV existente com {len(df_existing)} entradas.")
else:
    df_existing = pd.DataFrame(columns=[
        "file", "binary_size", "num_instructions_opt",
        "num_instructions_removed", "num_load_store"
    ])
    processed = set()
    print(" Nenhum CSV encontrado. Criando novo.")

metrics = []

for program in os.listdir(OPTIMIZED_DIR):
    prog_path = os.path.join(OPTIMIZED_DIR, program)
    if not os.path.isdir(prog_path):
        continue

    for opt_file in os.listdir(prog_path):
        if not opt_file.endswith(".ll"):
            continue

        full_path = os.path.join(prog_path, opt_file)
        id_name = f"{program}/{opt_file}"

        if id_name in processed:
            print(f" Já processado: {id_name}")
            continue

        try:
            # Leitura do conteúdo otimizado
            with open(full_path, "r") as f:
                opt_content = f.read()

            # Contagem total de instruções otimizado
            instr_opt = len(re.findall(r"^\s*%[a-zA-Z0-9_.]+\s*=", opt_content, re.MULTILINE))

            # Contagem de load + store
            num_loads = len(re.findall(r"\bload\b", opt_content))
            num_stores = len(re.findall(r"\bstore\b", opt_content))
            num_load_store = num_loads + num_stores

            # Arquivo original para contar instruções iniciais
            base_file = opt_file.split("__")[0] + ".ll"
            orig_path = os.path.join(ORIGINAL_DIR, base_file)
            with open(orig_path, "r") as f:
                orig_content = f.read()

            instr_orig = len(re.findall(r"^\s*%[a-zA-Z0-9_.]+\s*=", orig_content, re.MULTILINE))
            instr_removed = instr_orig - instr_opt

            # Compila para binário e mede tamanho
            binary_out = "temp.out"
            subprocess.run(["clang", full_path, "-o", binary_out], check=True, capture_output=True)
            bin_size = os.path.getsize(binary_out)
            os.remove(binary_out)

            # Adiciona entrada
            metrics.append({
                "file": id_name,
                "binary_size": bin_size,
                "num_instructions_opt": instr_opt,
                "num_instructions_removed": instr_removed,
                "num_load_store": num_load_store
            })
        except Exception as e:
            print(f" Erro em {id_name}: {e}")

# Salva
df_new = pd.DataFrame(metrics)
df_final = pd.concat([df_existing, df_new]).drop_duplicates(subset=["file"])
df_final.to_csv(CSV_PATH, index=False)
print(f"\n Métricas salvas em: {CSV_PATH}")

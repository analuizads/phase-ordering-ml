import os
import subprocess
import re
import pandas as pd

# Pastas de entrada/saída
C_DIR = "data/c_codes"
LL_DIR = "data/original_ll"
CSV_PATH = "data/features.csv"

# Garante que as pastas existem
os.makedirs(LL_DIR, exist_ok=True)
os.makedirs(C_DIR, exist_ok=True)  # caso rode pela primeira vez

features = []

# Lista arquivos .c
c_files = [f for f in os.listdir(C_DIR) if f.endswith(".c")]

# Verifica se o CSV existe
if os.path.exists(CSV_PATH):
    try:
        df_existing = pd.read_csv(CSV_PATH)
        processed_files = set(df_existing["file"].tolist())
        print(f"CSV existente encontrado com {len(df_existing)} entradas.")
    except Exception:
        print("Erro ao ler o CSV existente. Criando novo.")
        df_existing = pd.DataFrame(columns=[
            "file", "num_loops", "num_instructions", "num_blocks",
            "num_temporaries", "num_calls", "num_constants"
        ])
        processed_files = set()
else:
    print("Nenhum CSV encontrado. Criando novo.")
    df_existing = pd.DataFrame(columns=[
        "file", "num_loops", "num_instructions", "num_blocks",
        "num_temporaries", "num_calls", "num_constants"
    ])
    processed_files = set()

# Processa os arquivos .c
for c_file in c_files:
    name = os.path.splitext(c_file)[0]
    ll_file = f"{name}.ll"
    ll_path = os.path.join(LL_DIR, ll_file)
    c_path = os.path.join(C_DIR, c_file)

    # Gera .ll se ainda não existir
    if not os.path.exists(ll_path):
        print(f"🔧 Gerando LLVM IR para: {c_file}")
        cmd = ["clang", "-O0", "-S", "-emit-llvm", c_path, "-o", ll_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Erro ao compilar {c_file}:\n{result.stderr}")
            continue
    else:
        print(f"LVM IR já existe: {ll_file}")

    # Pula se já tem features no CSV
    if ll_file in processed_files:
        print(f"Features já extraídas: {ll_file}")
        continue

    # Extrai features
    try:
        output = subprocess.check_output(["opt", "-loops", "-analyze", ll_path], stderr=subprocess.DEVNULL).decode()
        num_loops = output.count("Loop at depth")
    except Exception:
        num_loops = 0

    with open(ll_path, "r") as f:
        content = f.read()

    num_blocks = len(re.findall(r"^[a-zA-Z0-9_.]+:", content, re.MULTILINE))
    num_instr = len(re.findall(r"^\s*%[a-zA-Z0-9_.]+[ ]*=", content, re.MULTILINE))
    num_tmp = len(re.findall(r"%[0-9]+", content))
    num_calls = len(re.findall(r"\bcall\b", content))
    num_const_int = len(re.findall(r"i(8|16|32|64) [-]?[0-9]+", content))
    num_const_float = len(re.findall(r"float [-]?[0-9]+\.[0-9]+", content))
    num_const = num_const_int + num_const_float

    features.append({
        "file": ll_file,
        "num_loops": num_loops,
        "num_instructions": num_instr,
        "num_blocks": num_blocks,
        "num_temporaries": num_tmp,
        "num_calls": num_calls,
        "num_constants": num_const
    })

# Salva ou atualiza CSV
df_new = pd.DataFrame(features)
df_final = pd.concat([df_existing, df_new]).drop_duplicates(subset=["file"])
df_final.to_csv(CSV_PATH, index=False)


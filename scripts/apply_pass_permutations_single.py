import os
import sys
import itertools
import subprocess

# Passes para LLVM 
passes = ["instcombine", "sroa", "licm", "dce", "sccp", "mem2reg"]

if len(sys.argv) != 2:
    print("Uso: python3 apply_pass_permutations_single.py <arquivo.ll>")
    sys.exit(1)

filename = sys.argv[1]  
input_path = os.path.join("data", "original_ll", filename)
program_name = filename.replace(".ll", "")
output_dir = os.path.join("data", "optimized_ll", program_name)

os.makedirs(output_dir, exist_ok=True)

print(f"Processando: {filename}")
print(f"Total de permutações: {len(list(itertools.permutations(passes)))}")

for i, perm in enumerate(itertools.permutations(passes)):
    pass_pipeline = ",".join(perm)
    output_file = os.path.join(output_dir, f"{program_name}__{'_'.join(perm)}.ll")

    # Verifica se já existe o arquivo otimizado
    if os.path.exists(output_file):
        print(f"{i+1:03d}/720: {os.path.basename(output_file)} já existe")
        continue

    cmd = [
        "opt",
        f"-passes={pass_pipeline}",
        input_path,
        "-S",
        "-o", output_file
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Erro em {os.path.basename(output_file)}")
            print(result.stderr.strip().split('\n')[0])  # Mostra só a primeira linha do erro
            os.remove(output_file) if os.path.exists(output_file) else None
        else:
            print(f"{i+1:03d}/720: {os.path.basename(output_file)} gerado.")
    except Exception as e:
        print(f"Falha ao executar opt: {e}")

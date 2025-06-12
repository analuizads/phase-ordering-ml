import os
import sys
import itertools
import subprocess

PASSES = ["instcombine", "sroa", "gvn", "dce", "sccp", "mem2reg"]

if len(sys.argv) != 2:
    print("Uso: python3 apply_pass_permutations_single.py <arquivo.ll>")
    sys.exit(1)

filename     = sys.argv[1]                      
input_path   = os.path.join("data/original_ll", filename)
program_name = filename[:-3]                    
output_dir   = os.path.join("data/optimized_ll", program_name)
os.makedirs(output_dir, exist_ok=True)

perms = list(itertools.permutations(PASSES))
total = len(perms)
print(f"Processando {filename}: {total} permutações")

for idx, perm in enumerate(perms, start=1):
    pass_pipeline = ",".join(perm)
    out_name      = f"{program_name}__{pass_pipeline}.ll"
    out_path      = os.path.join(output_dir, out_name)

    if os.path.exists(out_path):
        print(f"{idx:03d}/{total} {out_name} (já existe)")
        continue

    cmd = [
        "opt",
        f"-passes={pass_pipeline}",
        input_path,
        "-S", "-o", out_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        err = result.stderr.strip().split("\n")[0]
        print(f"{idx:03d}/{total} {out_name}: {err}")
        if os.path.exists(out_path):
            os.remove(out_path)
    else:
        print(f"{idx:03d}/{total} {out_name}")

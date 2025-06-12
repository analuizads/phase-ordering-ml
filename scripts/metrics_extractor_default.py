#!/usr/bin/env python3
"""
Extract metrics only for the LLVM default-pass optimized files.
Usage:
  python3 metrics_extractor_default.py \
    --optimized data/optimized_ll \
    --original  data/original_ll \
    --output    data/metrics_default.csv
"""
import os
import re
import subprocess
import argparse
import pandas as pd

def extract_default_metrics(optimized_dir, original_dir):
    metrics = []
    # percorre cada subdiretório (programa)
    for prog in os.listdir(optimized_dir):
        prog_dir = os.path.join(optimized_dir, prog)
        if not os.path.isdir(prog_dir):
            continue
        # busca apenas arquivos que terminam em __default.ll
        for fname in os.listdir(prog_dir):
            if not fname.endswith("__default.ll"):
                continue
            full_path = os.path.join(prog_dir, fname)
            id_name = f"{prog}/{fname}"
            try:
                # lê otimizado
                with open(full_path, 'r') as f:
                    opt_content = f.read()
                # conta instruções otimizadas
                instr_opt = len(re.findall(r"^\s*%[A-Za-z0-9_.]+\s*=", opt_content, re.MULTILINE))
                # conta load/store
                num_loads = len(re.findall(r"\bload\b", opt_content))
                num_stores = len(re.findall(r"\bstore\b", opt_content))
                num_load_store = num_loads + num_stores
                # original para instructions originais
                base_file = fname.split("__")[0] + ".ll"
                orig_path = os.path.join(original_dir, base_file)
                with open(orig_path, 'r') as f:
                    orig_content = f.read()
                instr_orig = len(re.findall(r"^\s*%[A-Za-z0-9_.]+\s*=", orig_content, re.MULTILINE))
                instr_removed = instr_orig - instr_opt
                # compila para binário e pega tamanho
                tmp_out = "temp_default.out"
                subprocess.run(["clang", full_path, "-o", tmp_out], check=True,
                               capture_output=True)
                bin_size = os.path.getsize(tmp_out)
                os.remove(tmp_out)
                # adiciona
                metrics.append({
                    'file': id_name,
                    'binary_size': bin_size,
                    'num_instructions_opt': instr_opt,
                    'num_instructions_removed': instr_removed,
                    'num_load_store': num_load_store
                })
            except Exception as e:
                print(f"Erro em {id_name}: {e}", file=sys.stderr)
    return metrics

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extract metrics for default LLVM-pass optimized files'
    )
    parser.add_argument('--optimized', required=True,
                        help='Diretório com subpastas <program>/<...__default.ll>')
    parser.add_argument('--original', required=True,
                        help='Diretório com arquivos .ll originais')
    parser.add_argument('--output', required=True,
                        help='Caminho para salvar CSV de métricas')
    args = parser.parse_args()

    results = extract_default_metrics(args.optimized, args.original)
    df = pd.DataFrame(results)
    df.to_csv(args.output, index=False)
    print(f"Métricas default salvas em {args.output} com {len(df)} entradas.")

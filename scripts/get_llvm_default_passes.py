#!/usr/bin/env python3
import os
import re
import subprocess
import sys

# Passes que queremos capturar
WANTED = {'instcombine', 'sroa', 'gvn', 'dce', 'sccp', 'mem2reg'}
# Mapeamentos de aliases do legacy PM -> nosso nome canônico
CANONICAL = {
    'promote': 'mem2reg',    # PromotePass → mem2reg
    'adce':    'dce',         # ADCEPass → dce
    'globaldce': 'dce',
}

INPUT_DIR = 'data/original_ll'
OUTPUT_DIR = 'data/optimized_ll'

def get_default_llvm_pass_order():
    dummy_ir = "; ModuleID = 'd'\n\ndefine void @f() { ret void }\n"
    cmd = ['opt', '-O3', '-disable-output', '-debug-pass-manager', '-']
    proc = subprocess.run(
        cmd,
        input=dummy_ir,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    log = proc.stdout + proc.stderr

    passes = []
    for line in log.splitlines():
        line = line.strip()
        if not line.startswith('Running pass:'):
            continue
        m = re.match(r'Running pass:\s+([A-Za-z0-9_]+)Pass\b', line)
        if m:
            passes.append(m.group(1).lower())

    if not passes:
        print("⚠️  Não encontrei nenhum 'Running pass:' no log do opt.", file=sys.stderr)
    return passes

def get_canonical_pipeline(full_pipeline):
    ordering = []
    for p in full_pipeline:
        p_low = p.lower()
        # primeiro, mapeia aliases
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

def optimize_all_files():
    # 1) extrai pipeline padrão
    full = get_default_llvm_pass_order()
    default_pipeline = get_canonical_pipeline(full)

    print("Pipeline completo do LLVM -O3 (legacy PM):")
    print(full)
    print("\nSequência canônica dos 6 passes:")
    print(default_pipeline)

    if len(default_pipeline) < len(WANTED):
        print(
            f"⚠️  Atenção: não encontramos todos os {len(WANTED)} passes em O3. "
            f"Achados: {default_pipeline}", file=sys.stderr
        )

    # 2) monta flag única para o New PM
    passes_arg = ",".join(default_pipeline)
    pass_flag = f"-passes={passes_arg}"

    # 3) itera os .ll originais
    if not os.path.isdir(INPUT_DIR):
        print(f"Diretório de entrada não existe: {INPUT_DIR}", file=sys.stderr)
        sys.exit(1)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".ll")]
    if not files:
        print(f"⚠️  Nenhum .ll em {INPUT_DIR}")
        sys.exit(0)

    for fn in files:
        base = os.path.splitext(fn)[0]
        in_path = os.path.join(INPUT_DIR, fn)
        out_subdir = os.path.join(OUTPUT_DIR, base)
        os.makedirs(out_subdir, exist_ok=True)
        out_path = os.path.join(out_subdir, f"{base}__default.ll")

        cmd = ["opt", pass_flag, in_path, "-S", "-o", out_path]
        proc = subprocess.run(cmd, capture_output=True, text=True)

        if proc.returncode == 0:
            print(f"[OK]   {fn} → {out_path}")
        else:
            err = (proc.stderr or proc.stdout).strip().splitlines()[0]
            print(f"[ERR]  {fn} : {err}", file=sys.stderr)

if __name__ == "__main__":
    optimize_all_files()

#include <stdio.h>

int buscaBinaria(int v[], int n, int x) {
    int esq = 0, dir = n - 1;
    while (esq <= dir) {
        int meio = (esq + dir) / 2;
        if (v[meio] == x) return meio;
        else if (v[meio] < x) esq = meio + 1;
        else dir = meio - 1;
    }
    return -1;
}

int main() {
    int v[] = {1, 3, 5, 7, 9};
    int pos = buscaBinaria(v, 5, 7);
    printf("Posição: %d\n", pos);
    return 0;
}

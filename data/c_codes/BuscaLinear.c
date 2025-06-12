#include <stdio.h>

int buscaLinear(int v[], int n, int x) {
    for (int i = 0; i < n; i++)
        if (v[i] == x) return i;
    return -1;
}

int main() {
    int v[] = {3, 8, 4, 1, 7};
    int x = 4;
    int pos = buscaLinear(v, 5, x);
    printf("Elemento %d está na posição %d\n", x, pos);
    return 0;
}

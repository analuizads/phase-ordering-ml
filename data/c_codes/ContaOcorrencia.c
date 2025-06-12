#include <stdio.h>

int contar(int v[], int n, int x) {
    int cont = 0;
    for (int i = 0; i < n; i++)
        if (v[i] == x) cont++;
    return cont;
}

int main() {
    int v[] = {2, 3, 2, 5, 2, 3, 4};
    int x = 2;
    printf("O número %d aparece %d vezes\n", x, contar(v, 7, x));
    return 0;
}

#include <stdio.h>

int soma(int v[], int n) {
    int total = 0;
    for (int i = 0; i < n; i++)
        total += v[i];
    return total;
}

int main() {
    int v[] = {1, 2, 3, 4, 5};
    int n = 5;
    printf("Soma = %d\n", soma(v, n));
    return 0;
}

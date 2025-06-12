#include <stdio.h>

int ehPrimo(int n) {
    if (n <= 1) return 0;
    for (int i = 2; i * i <= n; i++)
        if (n % i == 0) return 0;
    return 1;
}

int main() {
    int n = 17;
    if (ehPrimo(n))
        printf("%d é primo\n", n);
    else
        printf("%d não é primo\n", n);
    return 0;
}
